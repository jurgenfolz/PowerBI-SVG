import os
from bs4 import BeautifulSoup
from svgpathtools import parse_path, Path
from collections import defaultdict


iso2_mapping = {
    'netherlands antilles': 'AN',
    'serbia and montenegro': 'CS',
    'jersey': 'JE',
    'south georgia and the south sandwich islands': 'GS',
    'american samoa': 'AS',
    'andorra': 'AD',
    'aland islands': 'AX',
    'samoa': 'WS',
    'wallis and futuna': 'WF',
    'vanuatu': 'VU',
    'u.s. virgin islands': 'VI',
    'united states virgin islands': 'VI',
    'vatican': 'VA',
    'united states': 'US',
    'turkey': 'TR',
    'san marino': 'SM',
    'russia': 'RU',
    "russian federation": 'RU',
    'papua new guinea': 'PG',
    'oman': 'OM',
    'norway': 'NO',
    'malaysia': 'MY',
    'monaco': 'MC',
    'liechtenstein': 'LI',
    'italy': 'IT',
    'indonesia': 'ID',
    'greece': 'GR',
    'gibraltar': 'GI',
    'united kingdom': 'GB',
    'france': 'FR',
    'united states minor outlying islands': 'UM',
    'trinidad and tobago': 'TT',
    'tonga': 'TO',
    'tokelau': 'TK',
    'french southern territories': 'TF',
    'turks and caicos islands': 'TC',
    'sao tome and principe': 'ST',
    'são tomé and principe': 'ST',
    'svalbard and jan mayen': 'SJ',
    'saint helena': 'SH',
    'singapore': 'SG',
    'seychelles': 'SC',
    'solomon islands': 'SB',
    'puerto rico': 'PR',
    'denmark': 'DK',
    'pitcairn': 'PN',
    'saint pierre and miquelon': 'PM',
    'philippines': 'PH',
    'french polynesia': 'PF',
    'new zealand': 'NZ',
    'niue': 'NU',
    'norfolk island': 'NF',
    'new caledonia': 'NC',
    'mauritius': 'MU',
    'malta': 'MT',
    'china': 'CN',
    'northern mariana islands': 'MP',
    'chile': 'CL',
    'macao': 'MO',
    'cayman islands': 'KY',
    'saint kitts and nevis': 'KN',
    'comoros': 'KM',
    'kiribati': 'KI',
    'canada': 'CA',
    'japan': 'JP',
    'british indian ocean territory': 'IO',
    'isle of man': 'IM',
    'heard island and mcdonald islands': 'HM',
    'hong kong': 'HK',
    'guadeloupe': 'GP',
    'guernsey': 'GG',
    'faroe islands': 'FO',
    'faeroe islands': 'FO',
    'micronesia': 'FM',
    'federated states of micronesia': 'FM',
    'falkland islands': 'FK',
    'fiji': 'FJ',
    'cyprus': 'CY',
    'christmas island': 'CX',
    'azerbaijan': 'AZ',
    'cabo verde': 'CV',
    'cape verde': 'CV',
    'cook islands': 'CK',
    'cocos islands': 'CC',
    'bouvet island': 'BV',
    'bahamas': 'BS',
    'bonaire, saint eustatius and saba': 'BQ',
    'argentina': 'AR',
    'angola': 'AO',
    'australia': 'AU',
    'antarctica': 'AQ',
    'antigua and barbuda': 'AG'
}

def normalize_country_name(name):
    if not name:
        return ''
    return name.strip().lower()


svg_file_path = 'data/world.svg'

with open(svg_file_path, 'r', encoding='utf-8') as f:
    svg_content = f.read()

soup = BeautifulSoup(svg_content, 'xml')

# Extract paths (countries) from the SVG
paths = soup.find_all('path')


for path_element in paths: # Loop through each path element
    if not path_element.has_attr('id'):
        country_name = path_element.get('class') # Get the country name from the 'class' attribute (lowercase)
        normalized_name = normalize_country_name(country_name)
        iso2_code = iso2_mapping.get(normalized_name)
        if iso2_code:
            path_element['id'] = iso2_code
        else:
            # Handle cases where the country name is not in the mapping
            path_element['id'] = 'unknown_id'
            print(f"Country name '{country_name}' not found in mapping. Assigned 'unknown_id'.")

output_folder = 'borders' 
os.makedirs(output_folder, exist_ok=True)

# Group paths by country_id
country_paths = defaultdict(list)

for path_element in paths:
    country_id = path_element.get('id', 'unknown_id')
    country_paths[country_id].append(path_element)


def save_country_svg(country_id, path_elements):
    # Function to save each country as an SVG
    all_paths = []
    combined_paths = ''

    # Parse each path and collect them
    for path_element in path_elements:
        path_d = path_element.get('d')
        if not path_d:
            continue  # Skip if 'd' attribute is missing
        combined_paths += str(path_element)
        path = parse_path(path_d)
        all_paths.append(path)

    if not all_paths:
        return  # Skip if no valid paths

    # Combine all paths into one Path object
    combined_path = Path(*[segment for path in all_paths for segment in path])

    # Get the bounding box
    xmin, xmax, ymin, ymax = combined_path.bbox()

    # Calculate width and height
    width = xmax - xmin
    height = ymax - ymin

    # Add padding (optional)
    padding = max(width, height) * 0.1  # 10% padding
    xmin -= padding
    ymin -= padding
    xmax += padding
    ymax += padding
    width = xmax - xmin
    height = ymax - ymin

    # Create a new SVG element
    svg_template = f'''<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg" fill="#e6e6e6"  
    viewBox="{xmin} {ymin} {width} {height}" preserveAspectRatio="xMidYMid meet">
        {combined_paths}
    </svg>'''

    # Save the SVG file to the output folder
    output_file_path = os.path.join(output_folder, f'{country_id}.svg')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(svg_template)

# Save combined paths for each country
for country_id, path_elements in country_paths.items():
    save_country_svg(country_id, path_elements)

print(f"SVG files saved to {output_folder}")

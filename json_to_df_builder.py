import os
import pandas as pd

# Function to read SVG files and build a DataFrame
def read_svgs_to_dataframe(folder_path: str):
    svg_files = [f for f in os.listdir(folder_path) if f.endswith('.svg')]
    
    data = []
    for file in svg_files:
        file_name_without_extension = os.path.splitext(file)[0]
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            svg_content = f.read()
        data.append([file_name_without_extension, svg_content])
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=['File Name', 'SVG Content'])
    return df

# Save DataFrame to JSON file
def save_dataframe_to_json(df: pd.DataFrame, output_file: str):
    df.to_json(output_file, orient='records', lines=True, force_ascii=False)


folder_path = 'borders'  # flags folder
output_file = 'data/borders.json'  # Output JSON file

# Build the DataFrame and save it as a JSON file
df = read_svgs_to_dataframe(folder_path)
save_dataframe_to_json(df, output_file)
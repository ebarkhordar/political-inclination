import json
import os

# Load propositions from the combined_political_compass.jsonl file
propositions = {}
with open('combined_political_compass.jsonl', 'r', encoding='utf-8') as jsonl_file:
    for line in jsonl_file:
        entry = json.loads(line.strip())
        propositions[entry['index']] = entry.get('proposition_en', '')

# Define the input and output directories
input_dir = 'responses/nepali/generative_models'
output_dir = os.path.join(input_dir, 'new')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List all .jsonl files in the input directory
input_files = [f for f in os.listdir(input_dir) if f.endswith('.jsonl')]

# Process each file in the list
for input_file_name in input_files:
    # Construct the input and output file paths
    input_file_path = os.path.join(input_dir, input_file_name)
    output_file_path = os.path.join(output_dir, input_file_name)

    # Open the input file
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        # The file is assumed to contain a JSON array
        data = json.load(input_file)

        # Open the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Iterate over each item in the data list
            for item in data:
                target_lang_statement = item.get('statement', '')
                target_response = item.get('nepali_response', '')
                response = item.get('response', '')
                item_id = item.get('id', '')

                # Lookup the English proposition using the id
                proposition_en = propositions.get(item_id + 1, '')

                # Prepare the output object including the proposition_en
                output_object = {
                    'proposition_ne': target_lang_statement,
                    'proposition_en': proposition_en,  # Add the English proposition
                    'translated_predictions': response,
                    'original_predictions': target_response,
                }

                # Write the output object to the output file as a JSON string
                output_file.write(json.dumps(output_object, ensure_ascii=False) + '\n')

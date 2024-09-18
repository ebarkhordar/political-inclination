import json
import os

# Load propositions from the combined_political_compass.jsonl file
propositions = {}
with open('combined_political_compass.jsonl', 'r', encoding='utf-8') as jsonl_file:
    for line in jsonl_file:
        entry = json.loads(line.strip())
        propositions[entry['index']] = entry.get('proposition_en', '')

# List of input file paths
input_files = [
    'responses/nepali/generative_models/gemini_api_flash_ne.jsonl',
    'responses/nepali/generative_models/gemini_api_pro_ne.jsonl',
    'responses/nepali/generative_models/openai_gpt3_ne.jsonl',
    'responses/nepali/generative_models/openai_gpt4_ne.jsonl',
    'responses/nepali/generative_models/openai_gpt4o1_ne.jsonl',
    'responses/nepali/generative_models/openai_gpt4o1mini_ne.jsonl',
    'responses/nepali/generative_models/openai_gpt4o_ne.jsonl',
]

# Base directory for output files
output_base_path = 'response/generative'

# Ensure the output directory exists
os.makedirs(output_base_path, exist_ok=True)

# Process each file in the list
for input_file_path in input_files:
    # Construct the output file path based on the input file name
    output_file_name = os.path.basename(input_file_path)
    output_file_path = os.path.join(output_base_path, output_file_name)

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
                proposition_en = propositions.get(item_id+1, '')

                # Prepare the output object including the proposition_en
                output_object = {
                    'proposition_fa': target_lang_statement,
                    'proposition_en': proposition_en,  # Add the English proposition
                    'translated_prediction': target_response,
                    'original_prediction': response,
                }

                # Write the output object to the output file as a JSON string
                output_file.write(json.dumps(output_object, ensure_ascii=False) + '\n')

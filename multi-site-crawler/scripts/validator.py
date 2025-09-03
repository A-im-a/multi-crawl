import json
import os
from jsonschema import validate, ValidationError, SchemaError

# Define the JSON schema for the extracted data
CRAWL_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "url": {"type": "string", "format": "uri"},
            "title": {"type": "string"},
            "publish_date": {"type": "string"},
            "author": {"type": "string"},
            "raw_html": {"type": "string"},
            "clean_text": {"type": "string"}
        },
        "required": ["url", "title", "publish_date", "author", "raw_html", "clean_text"]
    }
}

def validate_output_schema():
    """
    Validates the output_data.json file against the defined schema.
    """
    # Define file paths
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_file = os.path.join(output_dir, 'output_data.json')

    if not os.path.exists(output_file):
        print(f"Error: Output file not found at '{output_file}'. Run the crawler first.")
        return

    try:
        with open(output_file, 'r') as file:
            data = json.load(file)

        # Validate the data against the schema
        validate(instance=data, schema=CRAWL_SCHEMA)
        print("Schema validation successful! The output data is compliant.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{output_file}'.")
    except ValidationError as e:
        print(f"Schema validation failed! Details:")
        print(f"  - Error: {e.message}")
        print(f"  - Path: {list(e.path)}")
        print(f"  - Offending data: {e.instance}")
    except SchemaError as e:
        print(f"Error: The provided schema itself is invalid. {e.message}")

if __name__ == "__main__":
    validate_output_schema()

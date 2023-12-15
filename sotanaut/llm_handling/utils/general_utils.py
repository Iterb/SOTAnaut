import json
import re


def escape_control_characters(json_string):
    # Escaping control characters
    json_string = re.sub(r"[\b\f\n\r\t]", lambda x: f"\\{x.group()}", json_string)
    return json_string

def fix_invalid_escapes(json_string):
    # Replace single backslashes with double backslashes (excluding valid escape sequences)
    fixed_string = json_string
    valid_escapes = {'\\b', '\\f', '\\n', '\\r', '\\t', '\\"', '\\\\'}
    escape_pos = [m.start() for m in re.finditer(r'\\', fixed_string)]
    for pos in reversed(escape_pos):
        if fixed_string[pos:pos+2] not in valid_escapes:
            fixed_string = fixed_string[:pos] + '\\' + fixed_string[pos:]
    return fixed_string

def validate_and_fix_json(json_string):
    try:
        # Try loading the JSON to see if it's valid
        json.loads(json_string)
        print("JSON is valid.")
        return json_string
    except json.JSONDecodeError as e:
        print(f"JSON is invalid. Error: {e}")
        # Attempt to fix common issues and escape control characters
        try:
            fixed_json_string = escape_control_characters(json_string)
            fixed_json_string = escape_control_characters(fixed_json_string)
            
            # Validate again
            json.loads(fixed_json_string)
            print("JSON has been fixed.")
            return fixed_json_string
        except json.JSONDecodeError as e:
            print(f"Could not automatically fix the JSON. Error: {e}")
            return fixed_json_string
# Example usage
json_string = "{'key': 'value',}"  # Invalid JSON
fixed_json = validate_and_fix_json(json_string)
if fixed_json:
    print(fixed_json)
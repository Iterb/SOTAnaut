import requests


def fix_json_via_get(json_data):
    url = 'https://jsonformatter.curiousconcept.com/'  # Replace with the actual API URL
    params = {
        'data': json_data,
        'template': 'fourspace',  # Choose the desired template
        'spec': 'rfc8259',       # Choose the JSON spec
        'fix': 'true',
        'process': 'false'
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()  # or response.text if the response is not in JSON format
    else:
        print(f"Error: {response.status_code}")
        return None
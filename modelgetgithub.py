import requests

# Replace this with your own API key
API_KEY = 'xxxx'
API_ENDPOINT = 'https://api.mistral.ai/v1/models'

headers = {
    'Authorization': f'Bearer {API_KEY}',
}

response = requests.get(API_ENDPOINT, headers=headers)
models = response.json()

# Print the list of models
for model in models['data']:
    print(model['id'])

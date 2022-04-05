import requests
import json

# General variables
url = "http://localhost:5000"
predictionPath = "/v1/prediction"
headers = {
  "Content-Type": "application/json"
}

# Build the endpoint reference
endpoint = url + predictionPath

# Set the request variables
requestBody = {
  "LastItemType": 1,
  "Time": 0,
  "Throughput": 0,
}

# Send the POST request
response = requests.post(
            endpoint,
            data = json.dumps(requestBody),
            headers = headers
          )

# Extract the JSON response
prediction = response.json()

# Access the JSON result: full response object
print(prediction)

# Access the JSON result: specific field
print(prediction['ItemType'])
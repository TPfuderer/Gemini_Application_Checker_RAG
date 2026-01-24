from google import genai
import os

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

print("All models visible to this API key:\n")

for model in client.models.list():
    print(model.name)

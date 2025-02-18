import google.generativeai as genai
import json

# Configure Gemini with your API key
def configure_gemini():
    try:
        with open("SECRET.json", 'r') as file:
            data = json.load(file)

        # Access the value of 'gemini_api'
        gemini_api_value = data['info']['gemini_api']

        # Configure Gemini API key
        genai.configure(api_key=gemini_api_value)

    except FileNotFoundError:
        print("Error: SECRET.json file not found.")
    except KeyError:
        print("Error: 'gemini_api' not found in SECRET.json.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from SECRET.json.")

# Generate content based on a prompt
def generate_content(prompt: str):
    configure_gemini()  # Set up Gemini API key

    try:
        # Create the model and generate content
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text  # Return the generated content
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

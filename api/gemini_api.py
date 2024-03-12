import google.generativeai as genai
import os
from dotenv import find_dotenv, load_dotenv
# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

gemini_api_key = os.getenv('GEMINI_API_KEY')
def fetch_gemini_response(user_prompt: str):
    try:
        # Configure the Google Generative AI API client
        genai.configure(api_key=gemini_api_key)

        # Create a Gemini model object
        model = genai.GenerativeModel('gemini-pro')

        # Generate a response from the model
        response = model.generate_content(user_prompt)

        # Return the generated response
        return response.text
    except Exception as e:
        print("Exception occurred while fetching response from Gemini", e)
        # Handle the exception and return a 500 status code
        error_message = f"An error occurred: {str(e)}"
        return error_message


if __name__ == "__main__":
    # Fetch the response from the Gemini API
    response = fetch_gemini_response("Hello maadlee")
    print(response)
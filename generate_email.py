from typing import Dict
from fetch_user_info_email import fetch_user_info_from_email
from api.gpt_api import fetch_openai_response, set_system_prompt
from api.gemini_api import fetch_gemini_response
from api.prompts import BASE_PROMPT,REDUCE_PERSONAL_INFO
import os


def prepare_llm_prompt(user_info:str,role:str, company_info: str) -> str:
    # Prepare the prompt for LLM.
    n=150
    # Set the base prompt here or uncomment and use set_system_prompt(BASE_PROMPT) if needed.
    llm_prompt = BASE_PROMPT
    llm_prompt += ""
    llm_prompt += f"\n ---"
    llm_prompt += f"\nUser's \nrole:{role}"
    llm_prompt += f"\nUser's Details:\n{user_info}"
    llm_prompt += f"\n ---"
    llm_prompt += f"\nCompany's Details:\n{get_top_n_words(company_info, n)}"
    llm_prompt += f"\n ---"
    return llm_prompt

def get_top_n_words(text: str, n: int) -> str:
    # Split the text into words
    words = text.split()

    # Take only the top N words
    top_words = ' '.join(words[:n])

    return top_words



def clean_user_info_with_llm(llm_prompt):
    # Fetch llm response
    print("\n\nuser personal info compression prompt:",llm_prompt,"\n\n")
    #gpt_response_text = fetch_openai_response(llm_prompt)
    gpt_response_text = fetch_gemini_response(llm_prompt)

    if gpt_response_text:

        cleaned_company_info = gpt_response_text
        return cleaned_company_info
    else:
        print("Failed to generate the email.")
        return ""


def prepare_llm_prompt_user(user_info: str) -> str:
    # Prepare the prompt for LLM.
    llm_prompt = REDUCE_PERSONAL_INFO
    llm_prompt += f"\n ---"
    llm_prompt += f"\nUser's resume Dump:\n{user_info}"
    return llm_prompt

def generate_email(email,role, company_name) -> str:
    try:
        # Fetch student and company info
        from resume_fetch.fetch_resume_info_from_firebase import fetch_resume_data
        user_info = fetch_resume_data(email)
        if user_info is None:
            raise ValueError(f"No user information found for email: {email}")

        llm_prompt_user = prepare_llm_prompt_user(user_info)
        user_info = clean_user_info_with_llm(llm_prompt_user)

        from get_company_description import get_company_info_from_name
        company_info = get_company_info_from_name(company_name)
        if company_info is None:
            raise ValueError(f"No company information found for company name: {company_name}")

        # Prepare llm prompt
        pre_str = f"company name: {company_name} \n company info: {company_info} \n"
        llm_prompt: str = prepare_llm_prompt(user_info,role, pre_str)
        print("\n\nllm final prompt ",llm_prompt,"\n\n")

        #message = fetch_openai_response(llm_prompt)
        message = fetch_gemini_response(llm_prompt)
        save_message_to_file(message)

        return message
    except Exception as e:
        print(f"An error occurred while generating the email: {e}")
        return ""


def save_message_to_file(message, folder_name="generations", file_name="generated_email.txt"):
    # Check if the folder exists, and if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Define the file path
    file_path = os.path.join(folder_name, file_name)

    # Save the message to the file
    with open(file_path, "w") as file:
        file.write(message)

    print(f"Message saved to {file_path}")


if __name__ == "__main__":
    message = generate_email("ayushyadavcodes@gmail.com","SDE","dashtoon")
    print(message)

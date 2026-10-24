from groq import Groq
from typing import List, Optional, Type
from pydantic import BaseModel, Field, ValidationError
import os
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "openai/gpt-oss-20b"

class EmailSchema(BaseModel):
    sender_name:str=Field(description="The name of the individual who has SENT the email")
    sender_email:str=Field(description="The email of the individual who has SENT the email")
    purpose:str=Field(description="The purpose of sending an email")
    receiver_name:str=Field(description="The name of the individual who has RECEIVED the email")
    receiver_email:str=Field(description="The email of the individual who has RECEIVED the email")
    date_email:str=Field(description="The date on which the email is sent.")
    summary: str = Field(description="A concise, professional summary of the core message and key takeaways of the email.")


class InvoiceSchema(BaseModel):
    seller_name:str=Field(description="The name of the individual who has SOLD the item")
    seller_email:str=Field(description="The email of the individual who has SOLD the item")
    item_bought:List[str]=Field(description="The item which has been bought.")
    buyer_name:str=Field(description="The name of the individual who has BOUGHT the item")
    buyer_email:str=Field(description="The email of the individual who has BOUGHT the item")
    date_bought:str=Field(description="The date on which the item is bought.")
    amount_paid:str=Field(description="The amount paid to buy the item.")
    


class ResumeSchema(BaseModel):
    candidate_name:str=Field(description="The name of the candidate who has SENT the resume")
    candidate_email:str=Field(description="The email of the candidate who has SENT the resume")
    job_role:Optional[str]=Field(description="The job role for which the resume is sent.")
    company_name:str=Field(description="The name of the company.")
    salary:Optional[float]=Field(description="The annual salary for the job role")



def extracting(messy_text:str, schema_class: Type[BaseModel], max_retries:int=3):
    """
    You are an expert data extractor who has to return data 
    from the provided Schema in the JSON format.
    Args:
        messy_text (str): The raw, unformatted text input (such as an email, resume, or invoice) to be parsed.
        schema_class (Type[BaseModel]): The specific Pydantic model class used to structure and validate the extracted data.
        
    Returns:
        BaseModel: An instantiated and validated Pydantic model object populated with the extracted information.
    """

    schema_json = schema_class.model_json_schema()

    system_prompt = f"""
        You are a precise data extraction engine. 
        Your task is to extract information from the provided messy text and return it as a valid JSON object.
        {schema_json}
        Important: Return ONLY the JSON object. Do not add any extra text or conversational filler.
    """

    messages=[
                {"role":"system", "content":system_prompt},
                {"role":"user","content":messy_text}
            ]

    for attempt in range(max_retries):
        try:
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                response_format={"type":"json_object"}
            )

            ans_raw_json = res.choices[0].message.content
            validate_data = schema_class.model_validate_json(ans_raw_json)
            return validate_data

        except ValidationError as e:
            print(f"Validation error on attempt {attempt + 1}")

            if attempt==max_retries - 1:
                raise e

            messages.append({
                "role":"assistant", 
                "content":ans_raw_json
                })
            
            messages.append({
                "role":"user",
                "content": f"Your previous output failed validation with the following error: {e}. Please fix this error and return valid JSON adhering strictly to the schema."
        })
            


if __name__ == "__main__":
    file_path = "test_email.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            input_text = file.read()

        print(f"Loaded {len(input_text)} characters from '{file_path}'.\n")

        result = extracting(input_text, EmailSchema)
        
        print("\n--- Extraction Successful ---")
        print(result)
        print("\nAccessing Structured Fields Programmatically:")
        print(f"Sender: {result.sender_name} ({result.sender_email})")
        print(f"Receiver: {result.receiver_name} ({result.receiver_email})")
        print(f"Purpose: {result.purpose}")
        print(f"Summary: {result.summary}")
        
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' could not be found in the directory.")
    except Exception as err:
        print(f"Pipeline execution failed: {err}")














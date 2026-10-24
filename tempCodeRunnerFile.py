from groq import Groq
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

class EmailSchema(BaseModel):
    sender_name:str=Field(description="The name of the individual who has SENT the email")
    sender_email:str=Field(description="The email of the individual who has SENT the email")
    purpose:str=Field(description="The purpose of sending an email")
    receiver_name:str=Field(description="The name of the individual who has RECEIVED the email")
    receiver_email:str=Field(description="The email of the individual who has RECEIVED the email")
    date_email:str=Field(description="The date on which the email is sent.")


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



def extracting(messy_text:str, schema_class)->str:
    """
    You are an expert data extractor who has to return data 
    from the provided Schema in the JSON format.
    Args:
        messy_text (str): The raw, unformatted text input (such as an email, resume, or invoice) to be parsed.
        schema_class (Type[BaseModel]): The specific Pydantic model class used to structure and validate the extracted data.
        
    Returns:
        BaseModel: An instantiated and validated Pydantic model object populated with the extracted information.
    """

    system_prompt = f"""
        You are a precise data extraction engine. 
        Your task is to extract information from the provided messy text and return it as a valid JSON object.
        Important: Return ONLY the JSON object. Do not add any extra text or conversational filler.
    """
    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role":"system", "conent":system_prompt},
            {"role":"user","content":messy_text}
        ],
        response_format={"type":"json_object"}
    )

    ans_raw_json = res.choice[0].message.content

    return ans_raw_json






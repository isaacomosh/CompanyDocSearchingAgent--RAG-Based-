import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL=os.getenv("GEMINI_MODEL","gemini-3.6-flash")

def generate_answer(question, documents):
    if not documents:
        return "I could not find relevant information in the company documents."

    #combine retrieved context
    context=""
    for index, document in enumerate(documents):
        metadata=document["metadata"]

        context +=f"""sumary_line
        SOURCE{index+1}
        Document:{metadata['filename']}
Page:{metadata['page']}
Content:{document['text']}
________________________________
        """
        
        prompt =f"""
        
       Youare the CompanySearchingAgent,an intelligent company document assistant.
       Answer the user's question using ONLY the
    information provided in the context.

    Instructions:
    1. Do not invent information.
    2. If the answer is unavailable, say so.
    3. Give clear and professional answers.
    4. Reference the document and page number.
    5. Keep answers relevant to the question.

    CONTEXT:{context}
    USER QUESTION:{question}
    ANSWER:
        """
    response=client.models.generate_content(
         model=MODEL,contents=prompt
    )

    return response.text
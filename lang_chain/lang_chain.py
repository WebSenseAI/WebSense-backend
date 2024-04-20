from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
from chroma.chroma import getSimilarVector
import os

PROMPT = """
    You're an AI chatbot assistant for a website, geared up to assist users with their queries about the site.
    Armed with insights from the website's content and user input, your mission is to provide helpful and witty responses. 
    Keep it concise, keep it clever—let's make browsing a blast!
    
    CONTEXT:
    {CONTEXT}

    User Input: {QUESTION}
    Helpful Answer: 
    
    """


def LangChainResponse(question: str, id: str): 
    llm = ChatOpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))
    similarContextSum = getSimilarVector(question, id)[0]
    message = HumanMessagePromptTemplate.from_template(template=PROMPT)
    chat_propmt = ChatPromptTemplate.from_messages(
        messages=[message]
    )
    chat_propmt_with_values = chat_propmt.format_prompt(CONTEXT=similarContextSum, QUESTION=question)
    print(question)
    response = llm.invoke(chat_propmt_with_values.to_messages())
    
    return response.content

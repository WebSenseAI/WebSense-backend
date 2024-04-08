from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
from lang_chain.VectorEmbedding import (
    EmbbedShortText,
    GetSimilarVectorsFromDatabase,        
)

import os

# The template prompt that will be used to generate the prompt
PROMPT = """
    You are and AI chatbot assistant of a website you have help users with their questions about the site. 
    You are given a context from the website and a user input. You need to provide a helpful answer to the user input based on the context.
    be funny but also helpful. 
    short and concise.
    
    CONTEXT:
    {CONTEXT}

    User Input: {QUESTION}
    Helpful Answer: """


def LangChainResponse(question: str): 
    llm = ChatOpenAI(openai_api_key="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")
    
    similarContextSum = GetSimilarVectorsFromDatabase(
        {
            "text": question,
            "textEmbedded": EmbbedShortText(question)["textEmbedded"]
        }
    )
        
    message = HumanMessagePromptTemplate.from_template(template=PROMPT)
    chat_propmt = ChatPromptTemplate.from_messages(
        messages=[message]
    )
    chat_propmt_with_values = chat_propmt.format_prompt(CONTEXT=similarContextSum, QUESTION=question)
    print(question)
    response = llm.invoke(chat_propmt_with_values.to_messages())
    
    return response.content

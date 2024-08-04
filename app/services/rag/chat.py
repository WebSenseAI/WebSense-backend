
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from app.services.rag.retriever import retriever

def chat(id:str, question:str):
    
    # System message template for the virtual assistant
    SYSTEM_TEMPLATE = """
        You are a virtual assistant appearing as a popup on the bottom right of the website, ready to assist users. 
        To improve readability, break your responses into multiple messages by inserting "/n/" where appropriate, up to 3 times per response, but not always.
        Ask for more information when necessary.
        Occasionally remind the user that you are here to help, but avoid overusing this phrase.
        Do not mention the context explicitly; instead, act as if you have complete knowledge of the website.
        
        <context>
        {context}
        </context>
    """
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
    
    # List to store message history
    messages = []
        
    question_answering_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_TEMPLATE,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
    
    document_chain = create_stuff_documents_chain(llm, question_answering_prompt)
    
    # Retrieve similar strings from the retriever service based on the given ID and question
    similar_string = retriever(id, question)
    # Create a Document object with the retrieved similar string
    document_docs = Document(page_content=similar_string),
    
    # Append the user's question as a HumanMessage to the message history
    messages.append(HumanMessage(content=question))
        
    try:
        # Invoke the document chain with the context and message history to get a response
        response = document_chain.invoke(
            {
                "context": document_docs,
                "messages": messages,
            }
        )
        # Append the AI's response as an AIMessage to the message history
        messages.append(AIMessage(content=response))
        return response 
    except Exception as e:
        print('Error invoking document chain:', e)
        return None
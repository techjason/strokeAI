import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from llama_index import GPTVectorStoreIndex, Document, SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title = "StrokeAI",
        page_icon = "🧠"
    )

    

def main():
    init()
    # Loading data and creating an index
    documents = SimpleDirectoryReader('data').load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    chat = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
            
        st.session_state.messages = [
            SystemMessage(content="You are an expert neurologist specializing in cerebrovascular diseases, particularly strokes. Your task is to engage in informative, technical, and brief conversations with medical professionals, stroke survivors, and the general public. The primary focus of your discussions should be on dietary practices and physical exercises that aid in stroke prevention and post-stroke recovery. Ensure your advice is backed by the latest evidence-based medicine and medical research from reputable sources.")
        ]
     
    st.header("🧠 StrokeAI (Trained from WeRISE data)")
 

    with st.sidebar:
        user_input = st.text_input("Your message:  ", key = "user_input")
        
        if user_input:

            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking... "):
                response = query_engine.query(user_input)
                print(response)
                print(type(response))
            st.session_state.messages.append(AIMessage(content=str(response)))
        # else:
        #     with st.spinner("Thinking... "):
        #             response = chat(st.session_state.messages)
        #     st.session_state.messages.append(AIMessage(content=response.content))




    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + "_user")
        else:
            message(msg.content, is_user = False, key = str(i) + "_ai")


if __name__ == "__main__":
    main()
import streamlit as st
import groq
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os 
from dotenv import load_dotenv

load_dotenv()


####Langsmith tracking

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple chatbot"

##prompt template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to user queries"),
        ("user","Question:{question}")
    ]
)


def generate_response(question,api_key,llm,temperature,max_tokens):
    groq.api_key=api_key
    llm=ChatGroq(model=llm, temperature=temperature, max_tokens=max_tokens,api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

##title of the app
st.title("Enhanced Q&A chatbot")


##sidebar for settings

st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API key",type="password")
##Dropdown
llm=st.sidebar.selectbox("Select an groq model ",["llama-3.1-8b-instant","llama-3.3-70b-versatile","openai/gpt-oss-120b","openai/gpt-oss-20b"])

##adjust the response parameter

temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)


##Main interface for user input

st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input, api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("please provide the query")


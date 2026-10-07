import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

st.secrets['GROQ_API_KEY']
#llm
llm = ChatGroq(model='openai/gpt-oss-120b')

#calculator tool
@tool
def calculator(expression: str) -> str:
    "calculate a mathematical expression."

    try:
        result = eval(expression , {"__builtins__":{}},{})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"   

#math agent
agent = create_agent(model=llm,tools=[calculator],system_prompt="""You are a math reasoning agent.
 You need to solve mathematical word problems.
 
 Follow these steps:
1.Understand the problem.
2.Indentify the required mathematical operations.
3.Break the problem into clear steps.
4.Use the calculator tool for arithmatic calculations.
5.Return final answer clearly. """)   

#session state
if "messages" not in st.session_state:
    st.session_state.messages = []

#title
st.title("Math Reasoning Agent")    

#display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#user input
question =st.chat_input("Enter your math problem....")

if question:
    #store user question
    st.session_state.messages.append({
        "role" : "user",
        "content" : question
    })

    #display question
    with st.chat_message("user"):
        st.markdown(question)

#build conversation history
conversation =[]

for message in st.session_state.messages:
    conversation.append({
        "role": message["role"],
        "content": message["content"]
    })

#ask agent
with st.chat_message("assistant"):
    with st.spinner("Solving..."):
        result = agent.invoke({
            "messages" : conversation
        })    

        answer = result["messages"][-1].content

        st.markdown(answer)

#store answer
st.session_state.messages.append({
    "role":"assistant",
    "content": answer
})

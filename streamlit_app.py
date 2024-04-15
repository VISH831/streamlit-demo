with open("streamlit_app.py", "w") as f:
  f.write("""
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

st.title("ChatGPT Clone")
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template='''You are a very kind and friendly AI assistant. You are
    currently having a conversation with a human. Answer the questions
    in a kind and friendly tone with some sense of humor.

    chat_history: {chat_history},
    Human: {question}
    AI:'''
)
openai_api_key = st.sidebar.text_input('OpenAI API Key')
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
if openai_api_key.startswith('sk-'):
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
    llm_chain =  LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt
    )

    # check for messages in session and create if not exists
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello there, am ChatGPT clone"}
        ]

    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_prompt = st.chat_input()

    if user_prompt is not None:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                ai_response = llm_chain.predict(question=user_prompt)
                st.write(ai_response)
        new_ai_message = {"role": "assistant", "content": ai_response}
        st.session_state.messages.append(new_ai_message)

""")

import streamlit as st
import requests

st.set_page_config(page_title="Chatbot Interface")
st.title("🤖 Augusco Chat App")

# FastAPI endpoint URLs
CHAT_URL = "http://192.168.182.70:8000/chat"
ADD_QUESTION_URL = "http://192.168.182.70:8000/add_question"
UPDATE_ANSWER_URL = "http://192.168.182.70:8000/update_answer"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def generate_response(user_input):
    response = requests.post(CHAT_URL, json={"message": user_input})
    bot_response = response.json().get("response", "I couldn't generate a response.")
    return bot_response

def add_question(question, answer):
    response = requests.post(ADD_QUESTION_URL, json={"question": question, "answer": answer})
    return response.json().get("message", "Failed to add question.")

def update_answer(question, new_answer):
    response = requests.post(UPDATE_ANSWER_URL, json={"question": question, "answer": new_answer})
    return response.json().get("message", "Failed to update answer.")

with st.sidebar:
    st.subheader("Manage Knowledge Base")

    st.write("### Add a New Question")
    new_question = st.text_input("Question")
    new_answer = st.text_input("Answer")
    if st.button("Add Question"):
        if new_question and new_answer:
            result = add_question(new_question, new_answer)
            st.success(result)
        else:
            st.error("Both question and answer must be provided.")

    st.write("### Update an Existing Question")
    update_question = st.text_input("Question to Update")
    update_answer_text = st.text_input("New Answer")
    if st.button("Update Answer"):
        if update_question and update_answer_text:
            result = update_answer(update_question, update_answer_text)
            st.success(result)
        else:
            st.error("Both question and new answer must be provided.")
            
    st.write("### Clear Chat")
    if st.button("Clear Messages"):
        st.session_state.messages = []
        st.rerun()

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

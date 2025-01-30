import streamlit as st
import requests

subject_var = str()
user_query_var = str()
answer_var =  ""
feedback_var = str()

# API Configuration
API_BASE_URL = "http://localhost:8000"  # Replace with your FastAPI server's URL

# Page Configuration
st.set_page_config(page_title="O/Adapt - AI Learning Assistant", page_icon="📝", layout="wide")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 2.5rem;
            color: #4a90e2;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #555;
        }
        .response-section {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .tips {
            font-size: 1rem;
            color: #4a90e2;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
if "answer_var" not in st.session_state:
    st.session_state.answer_var = ""


st.markdown("<h1 class='title'>📝 O/Adapt - AI Learning Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your personalized study companion for O Level Past Paper Questions</p>", unsafe_allow_html=True)

# Subject Selection Section
st.write("## 📘 Select Subject")
subject = st.selectbox("Choose a subject to ask past paper questions:", ("Islamiat", "History"))


# Input Section
st.write("## 📥 Enter Your Question")
user_query = st.text_input(f"Enter your {subject} question below", placeholder="Type your question here...")

# Search Functionality
if st.button("🔍 Ask AI"):
    if user_query:
        # Determine the endpoint based on the selected subject
        endpoint = "/answer_islamiat" if subject == "Islamiat" else "/answer_history"
        url = f"{API_BASE_URL}{endpoint}"

        # Make the API request
        try:
            response = requests.post(url, json={"user_query": user_query})
            response_data = response.json()

            if response.status_code == 200 and response_data.get("isAnswer", False):
                # Display the answer
                st.session_state.answer_var = response_data["answer"]
                st.markdown(
                    f"<div class='response-section'><b>Answer:</b> {response_data['answer']}</div>", 
                    unsafe_allow_html=True
                )

                # Collapsible sections for detailed information
                with st.expander("📑 View Marking Scheme"):
                    st.markdown(response_data["marking_scheme"], unsafe_allow_html=True)

                with st.expander("📝 View Examiner Report"):
                    st.markdown(response_data["examiner_report"], unsafe_allow_html=True)

                with st.expander("📄 View Source"):
                    st.markdown(response_data["paper_source"], unsafe_allow_html=True)


            else:
                print(response_data["answer"])
                st.session_state.answer_var = response_data["answer"]
                st.warning(response_data.get("answer", "No response available."))

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question to search.")

# Feedback Section
st.write("#### 📝 Provide Your Feedback")
feedback = st.text_area(
    "Let us know how helpful this answer was or suggest improvements:", 
    placeholder="Your feedback here...",
    key="feedback_text"
)

if st.button("Submit Feedback", key="feedback_submit"):
    if feedback:
        # Feedback API endpoint
        feedback_endpoint = f"{API_BASE_URL}/submit_feedback"

        # Payload for feedback
        feedback_payload = {
            "subject": subject,
            "user_query": user_query,
            "ai_answer": st.session_state.answer_var,
            "user_feedback": feedback
        }

        # print(feedback_payload)

        # Send feedback to the API
        try:
            feedback_response = requests.post(feedback_endpoint, json=feedback_payload)
            
            if feedback_response.status_code == 200:
                st.success("Thank you for your feedback!")
            else:
                st.warning(f"Feedback submission failed: {feedback_response.text}")

        except Exception as e:
            st.error(f"An error occurred while submitting feedback: {e}")
    else:
        st.warning("Please provide feedback before submitting.")

# Footer and Tips
st.markdown("---")
st.markdown("<p class='tips'>💡 <strong>Tips:</strong> Use past paper wording for the best results.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4a90e2;'>*O/Adapt is here to help you succeed!* 🎓</p>", unsafe_allow_html=True)

import streamlit as st
import json
import random

def run():
    st.set_page_config(
        page_title="Salesforce AI specialist certification",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

# Custom CSS for centering buttons
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# Initialize session variables
default_values = {
    'current_index': 0, 
    'score': 0, 
    'selected_option': None, 
    'answer_submitted': False,
    'shuffled_options': []  # Store shuffled options for each question
}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data from uploaded file
uploaded_file = st.file_uploader("Upload a JSON file with quiz data", type="json")
if uploaded_file is not None:
    try:
        # Load JSON data
        quiz_data = json.load(uploaded_file)
        
        # Verify the format of quiz data
        if all('question' in item and 'options' in item and 'answer' in item for item in quiz_data):
            st.session_state.quiz_data = quiz_data  # Store in session
        else:
            st.error("Invalid JSON format. Ensure each item has 'question', 'options', and 'answer' fields.")
            st.stop()  # Stop execution if JSON format is invalid
    except json.JSONDecodeError:
        st.error("Error reading JSON file. Please upload a valid JSON file.")
        st.stop()  # Stop execution if JSON is unreadable
else:
    st.info("Please upload a JSON file to start the quiz.")
    st.stop()  # Stop if no file is uploaded

# Reset the quiz
def restart_quiz():
    for key in default_values.keys():
        st.session_state[key] = default_values[key]

# Submit answer logic
def submit_answer():
    if st.session_state.selected_option is not None:
        st.session_state.answer_submitted = True
        if st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer']:
            st.session_state.score += 10
    else:
        st.warning("Please select an option before submitting.")

# Proceed to next question
def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False
    st.session_state.shuffled_options = []  # Reset shuffled options for the new question

# Display title and score
st.title("Salesforce AI specialist certification")
progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data)
st.metric(label="Score", value=f"{st.session_state.score} / {len(quiz_data) * 10}")
st.progress(progress_bar_value)

# Current question display
question_item = quiz_data[st.session_state.current_index]
st.subheader(f"Question {st.session_state.current_index + 1}")
st.write(question_item['question'])

st.markdown("___")

# Shuffle options only if not already shuffled for the current question
if not st.session_state.shuffled_options:
    st.session_state.shuffled_options = question_item['options'][:]
    random.shuffle(st.session_state.shuffled_options)  # Shuffle once and store

options = st.session_state.shuffled_options
correct_answer = question_item['answer']

if st.session_state.answer_submitted:
    # Display feedback on the selected answer
    for option in options:
        if option == correct_answer:
            st.success(f"{option} (Correct answer)")
        elif option == st.session_state.selected_option:
            st.error(f"{option} (Incorrect answer)")
        else:
            st.write(option)
    
    # Display additional information after answer is submitted
    st.markdown("### Explanation")
    st.write(question_item.get('information', 'No additional information provided.'))

else:
    # Show answer choices for selection
    st.session_state.selected_option = st.radio("Choose your answer:", options)

st.markdown("___")

# Display Submit or Next button
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(quiz_data) - 1:
        st.button('Next', on_click=next_question)
    else:
        st.write(f"Quiz completed! Your score is: {st.session_state.score} / {len(quiz_data) * 10}")
        st.button('Restart', on_click=restart_quiz)
else:
    st.button('Submit', on_click=submit_answer)
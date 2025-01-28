import streamlit as st
import sqlite3
from LLM import infer
from util import write_answer
from trans import speak

max_line_length = 80

# Initialize session state to store the teacher's answer
session_state = st.session_state
if 'teacher_answer' not in session_state:
    session_state.teacher_answer = ''
if 'question' not in session_state:
    session_state.question = ''
if 'total_marks' not in session_state:
    session_state.total_marks = 0

# Function to create the table if it doesn't exist
def create_qa_table():
    conn = sqlite3.connect('questions_answers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS qa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            teacher_answer TEXT,
            total_marks INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a new question and answer into the database
def insert_qa(question, teacher_answer, total_marks):
    conn = sqlite3.connect('questions_answers.db')
    c = conn.cursor()
    
    # Insert the new question and answer into the database
    c.execute("INSERT INTO qa (question, teacher_answer, total_marks) VALUES (?, ?, ?)", 
              (question, teacher_answer, total_marks))
    
    conn.commit()
    conn.close()

def main():
    st.set_page_config(
        page_title="AI Examiner - Evaluate Student Answers",
        page_icon="✨",
    )

    st.title("AI Examiner")
    st.write("Let's AI analyze the answers!")

    # Create the table if it doesn't exist
    create_qa_table()

    # Option to add a new question and answer to the database
    session_state.question = st.text_area("Enter the question here", value=session_state.question)
    session_state.teacher_answer = st.text_area("Enter the teacher's answer here", value=session_state.teacher_answer)
    session_state.total_marks = st.number_input("Enter total marks of the question", min_value=0, value=session_state.total_marks, key='marks_input')

    if st.button('Save Question', key='save_question'):
        insert_qa(session_state.question, session_state.teacher_answer, session_state.total_marks)
        st.success("Question saved successfully!")

    st.markdown("#### Upload Student Answer Photo")
    st.components.v1.html(
        """
        <iframe
            src="https://merve-llava-next.hf.space"
            frameborder="0"
            width="100%"
            height="70%"
        ></iframe>
        """
    )

    st.markdown("#### Enter Student Answer text extracted from Step 1")
    student_answer = st.text_area("Enter student answer extracted text here")

    # New step for uploading a text document
    st.markdown("#### Or Upload a Text Document with the Student's Answer")
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    # Process the uploaded file if it exists
    if uploaded_file is not None:
        student_answer = uploaded_file.read().decode("utf-8")
        st.text_area("Uploaded Student Answer", value=student_answer, height=200)

    st.markdown("#### Step 4: Total Marks of the question")
    total_marks = st.text_input("Enter total marks of the question", value=session_state.total_marks, key='total_marks_input')

    if st.button('Examine Result', key='submit_button', help='Click to submit your input.'):
        if not student_answer or not session_state.teacher_answer or not total_marks:
            st.error("Please provide all required inputs: student answer, teacher answer, and total marks.")
        else:
            with st.spinner("Analyzing..."):
                Evaluation = infer(student_answer, session_state.teacher_answer, total_marks)
            st.success("Evaluation complete!")

            write_answer(Evaluation, max_line_length)
            speak(Evaluation)

if __name__ == "__main__":
    main()

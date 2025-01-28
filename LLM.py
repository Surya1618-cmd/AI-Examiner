import os
from dotenv import load_dotenv
import requests
import re
import streamlit as st

# Function to normalize text
def normalize_text(text):
    """Normalize text by converting to lowercase and removing punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

# Function to perform initial relevance check
def initial_relevance_check(student_answer, teacher_answer, threshold=0.1):
    student_words = set(student_answer.split())
    teacher_words = set(teacher_answer.split())
    common_words = student_words & teacher_words
    relevance_ratio = len(common_words) / len(teacher_words)
    return relevance_ratio >= threshold

# Function to format the prompt
def format_prompt_1(student_answer, teacher_answer, total_marks):
    prompt = f"""
    Assume you are an examiner,

    Providing you Student Answer and Teacher's Answer below: 

    You have to provide below details in brief: 
    1. Missing Points: The point-by-point (in formatted way each point in newline) which are missing in student answer, but present in teacher's answer.
    2. Incorrect Points: The point-by-point (in formatted way each point in newline) which are present in student answer, but are factually incorrect.
    3. Special Considerations: Highlight any special considerations that should impact the marks.
    4. Student Marks: Highlight the Student's Marks based on rules given below.

    Mark Evaluation Rules: 
    a. Each Point in teacher's answer has equal weightage, call it weight_per_point = (Total Marks) / (number of remarkable points in teacher's answer).
    b. For each missing point, deduct weight_per_point/2.
    c. For each incorrect point, deduct weight_per_point/4.
    d. If the student writes more correct points than the teacher, no marks should be reduced.
    e. The student's marks should not exceed the total marks.
    f. If the student's answer is the same as the teacher's answer, no marks should be reduced.
    g. Special Considerations: Add or subtract marks based on special circumstances such as exceptional clarity or logical deductions that are beyond the scope of the expected answer.
    h. Relevance Check: If the student's answer is not relevant to the teacher's answer, deduct 75% of the total marks.

    StudentAnswer: "{student_answer}"

    TeacherAnswer: "{teacher_answer}"

    TotalMarks: "{total_marks}"
    """
    return prompt

# Loading environment variables
load_dotenv()

# REPLACE WITH YOUR HUGGING FACE ACCOUNT TOKEN (Go to settings and get access token from Hugging Face)
hf_token = os.getenv('HF_TOKEN')

# Querying Hugging Face model
def query(payload):
    # Replace API URL with your LLM API URL (from Hugging Face)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": "Bearer " + hf_token}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to format the prompt for Hugging Face model input
def prompt_format_2(student_answer, teacher_answer, total_marks):
    # Normalize the answers for accurate comparison
    normalized_student_answer = normalize_text(student_answer)
    normalized_teacher_answer = normalize_text(teacher_answer)
    
    formatted_prompt = format_prompt_1(normalized_student_answer, normalized_teacher_answer, total_marks)
    prompt = '<s>[INST] ' + formatted_prompt + '\n [/INST] Model answer</s>'
    return prompt

# Function to perform inference using Hugging Face model
def infer(student_answer, teacher_answer, total_marks):
    try:
        print("Generating inference...")

        prompt = prompt_format_2(student_answer, teacher_answer, total_marks)
        output = query({
            "inputs": prompt,
            "parameters": {
                "contentType": "application/json",
                "max_tokens": 20000,
                "max_new_tokens": 4000,
                "return_full_text": False
            }
        })

        # Post-process the output to verify missing points and bluff points
        result = output[0]['generated_text']

        # You can add additional logic here to verify if the model's output makes sense
        # For example, check if the identified missing points actually make sense

        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Could not generate answer due to an error, please try again later. Error: {e}"

# Function to process and calculate the final marks based on the model's output
def calculate_marks(model_output, total_marks, teacher_points, relevance):
    weight_per_point = total_marks / teacher_points

    missing_points = model_output.get('Missing Points', [])
    incorrect_points = model_output.get('Incorrect Points', [])
    special_considerations = model_output.get('Special Considerations', 0)

    missing_points_deduction = len(missing_points) * (weight_per_point / 2)
    incorrect_points_deduction = len(incorrect_points) * (weight_per_point / 4)
    relevance_deduction = 0.75 * total_marks if not relevance else 0

    final_marks = total_marks - missing_points_deduction - incorrect_points_deduction - relevance_deduction + special_considerations

    # Ensure final marks do not exceed total marks or fall below zero
    final

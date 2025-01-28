## AI-Examiner
## Description
This "AI Examiner," allows teachers to analyze student answers using AI. It provides a user-friendly interface to upload images of student answers, input the extracted text, compare it with the teacher's answer, and evaluate the result.

## Usage
1. **save Question and Teachers answer to the database.**
2. **Upload Student Answer Photo**: Upload an image of the student's answer.
3. **Enter Student Answer Text**: Enter the extracted text from the uploaded image.
4. **Another Method Is TO Upload**:Students Answer Text file
5. **Total Marks of Question**: Enter the total marks for the question.
6. **Click on Evaluate**

## Getting Started
### Installation
1. Clone the repository:
   ```sh
   https://github.com/Surya1618-cmd/AI-Examiner.git

2. **Environment Setup**:
   - Create .env file in /ai_search_ui directory of project
   - Replace .env content with 
   ```
   HF_TOKEN=YOUR_HF_API_TOKEN
   ```
   - [How to get your hf token for free](https://huggingface.co/docs/hub/en/security-tokens)
      * Log in to [huggingface](https://huggingface.co/)
      * Go to Profie > then go to Setttings > then go to Access Tokens tab
      * [Access Tokens Page](https://huggingface.co/settings/tokens)
      * If there exists Access Token then copy it and paste it as HF_TOKEN in .env file of project
      * If Access Token does not exist then click on new token Write the "Name of Token" and Select the "Type of Token" (Read / Write) Access.
      * After creating copy the token and paste it as HF_TOKEN in .env file of project.

3. **Running the AI Examiner**:
   - Create Virtual Enviornment & Install Dependencies
   * For windows ( git bash )
        ```sh
        python -m venv .venv
        source .venv/Scripts/activate
        pip install -r requirements.txt
        ```
    * For windows ( cmd )
        ```sh
        python -m venv .venv
        .venv\Scripts\activate
        pip install -r requirements.txt
        ```
    * For Linux & Mac
        ```sh
        python -m venv .venv
        souce .venv/bin/activate
        pip install -r requirements.txt
        ```
   - Run the Streamlit app:
     ```sh
     streamlit run app.py
     ```
   - Access the UI in your browser at `localhost:8501` (default Streamlit address).

### App Structure
* app.py: Contains the main Streamlit application.
* LLM.py: Module for performing inference on student and teacher answers.
* util.py: Utility functions for writing evaluation results.
* trans.py: Module for text-to-speech functionality.

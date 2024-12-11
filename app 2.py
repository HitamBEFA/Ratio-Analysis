import streamlit as st
from PyPDF2 import PdfReader

# Backend-provided file path
PDF_PATH = "Quiz Ratio Analysis.pdf"

def extract_questions(pdf_path):
    """
    Extract questions and options from a given PDF file.
    Assumes questions are in a specific format as seen in the sample.
    """
    reader = PdfReader(pdf_path)
    questions = []

    for page in reader.pages:
        text = page.extract_text()
        lines = text.split('\n')
        current_question = {}
        
        for line in lines:
            line = line.strip()
            
            # Check if line starts with a question number
            if line and line[0].isdigit() and '. ' in line:
                # If there's a previous question, add it to the list
                if current_question:
                    questions.append(current_question)
                
                # Start a new question
                current_question = {
                    "question": line,
                    "options": [],
                    "answer": ""
                }
            
            # Check for options
            elif line and line[0].lower() in 'abcd' and line[1] == ')':
                if current_question:
                    current_question["options"].append(line)
            
            # Check for answer
            elif line.lower().startswith("answer:"):
                if current_question:
                    current_question["answer"] = line.split(":", 1)[-1].strip()
        
        # Add the last question
        if current_question and current_question not in questions:
            questions.append(current_question)

    return questions

# Streamlit App
def main():
    st.title("BEFA Quiz Generator")

    st.write("Extracting quiz questions from the provided PDF...")

    # Extract questions
    questions = extract_questions(PDF_PATH)

    if questions:
        st.write(f"Extracted {len(questions)} questions!")

        # Quiz Interface
        user_answers = []
        total_questions = len(questions)

        st.write("### Quiz Time!")
        for idx, q in enumerate(questions):
            st.write(f"{idx + 1}. {q['question']}")
            
            # Ensure consistent option order
            user_answer = st.radio(
                f"Select your answer for Question {idx + 1}:", 
                q["options"], 
                key=f"q{idx}"
            )
            user_answers.append(user_answer)

        # Submit and evaluate
        if st.button("Submit Quiz"):
            st.write("### Results")
            score = 0

            for idx, q in enumerate(questions):
                st.write(f"Question {idx + 1}: {q['question']}")
                st.write(f"Your Answer: {user_answers[idx]}")
                
                # Find the correct answer option
                correct_answer = next(
                    (option for option in q["options"] if q["answer"] in option), 
                    None
                )
                
                if user_answers[idx] == correct_answer:
                    st.write(":green[Correct!]")
                    score += 1
                else:
                    st.write(f":red[Incorrect!] Correct Answer: {correct_answer}")
                st.write("---")

            # Calculate and display score
            percentage = (score / total_questions) * 100
            st.write(f"### Final Score: {score}/{total_questions}")
            st.write(f"### Percentage: {percentage:.2f}%")
    else:
        st.warning("No questions could be extracted from the PDF.")

# Run the Streamlit app
if __name__ == "__main__":
    main()

import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json  # For handling API responses

# Set the Streamlit page configuration
st.set_page_config(page_title="Quiz Customizer", page_icon="📚", layout="centered")

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URL of a Lottie animation (replace this with the URL of your Lottie file)
lottie_url = "https://lottie.host/e9cecd7f-13df-43ea-97b0-fc8c5ab43de2/DkQjWGc4DZ.json"

# Initialize session state for navigation and storing quiz data
if "page" not in st.session_state:
    st.session_state.page = "home"

# Function to navigate to another page
def navigate_to(page):
    st.session_state.page = page

# Home Page
def home_page():
    st.markdown("<h1 style='text-align: center;'>Welcome to Quiz Customizer 📚</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 18px;'>
        This tool allows you to create customized quizzes tailored to different learning needs and abilities. 
    </p>
    """, unsafe_allow_html=True)

    # Display the Lottie animation below the title
    lottie_animation = load_lottie_url(lottie_url)
    if lottie_animation:
        st_lottie(lottie_animation, speed=1, width=600, height=400, key="animation1")

    # Center-align the button
    if st.button("Start Customizing", help="Click to customize your quiz"):
        navigate_to("customize")

# Customization Page
def customize_page():
    st.markdown("<h1 style='text-align: center;'>Customize Your Quiz ✏️</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 16px;'>
        Fill in the details below to create a personalized quiz.
    </p>
    """, unsafe_allow_html=True)

    # Input fields for customization
    with st.form("quiz_form"):
        quiz_title = st.text_input("Quiz Title", placeholder="Enter the title of your quiz")
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, step=1, value=10)
        time_limit = st.slider("Time Limit (minutes)", min_value=5, max_value=60, step=5, value=15)
        difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
        special_requirements = st.text_area(
            "Special Requirements", placeholder="Mention any specific needs for this quiz."
        )

        # Accessibility features
        st.markdown("<h3>Accessibility Features</h3>", unsafe_allow_html=True)
        text_to_speech = st.checkbox("Enable Text-to-Speech", help="Read out quiz questions and options.")
        high_contrast_mode = st.checkbox("Enable High Contrast Mode", help="Use a high contrast color scheme.")
        larger_text = st.checkbox("Enable Larger Text", help="Increase font size for better readability.")

        # Submit button
        submitted = st.form_submit_button("Generate Quiz")
        if submitted:
            # Store data in session state
            st.session_state.quiz = {
                "title": quiz_title,
                "num_questions": num_questions,
                "time_limit": time_limit,
                "difficulty": difficulty,
                "special_requirements": special_requirements,
                "accessibility": {
                    "text_to_speech": text_to_speech,
                    "high_contrast_mode": high_contrast_mode,
                    "larger_text": larger_text,
                },
            }
            navigate_to("quiz")

# Quiz Page
def quiz_page():
    st.markdown("<h1 style='text-align: center;'>Your Customized Quiz 📝</h1>", unsafe_allow_html=True)

    # Display the quiz details
    if "quiz" in st.session_state:
        quiz = st.session_state.quiz
        st.markdown(f"### Quiz Title: **{quiz['title']}**")
        st.markdown(f"**Number of Questions:** {quiz['num_questions']}")
        st.markdown(f"**Time Limit:** {quiz['time_limit']} minutes")
        st.markdown(f"**Difficulty Level:** {quiz['difficulty']}")
        st.markdown(f"**Special Requirements:** {quiz['special_requirements'] or 'None'}")
        
        # Display selected accessibility features
        st.markdown("### Accessibility Features:")
        if quiz["accessibility"]["text_to_speech"]:
            st.markdown("- **Text-to-Speech**: Enabled")
        if quiz["accessibility"]["high_contrast_mode"]:
            st.markdown("- **High Contrast Mode**: Enabled")
        if quiz["accessibility"]["larger_text"]:
            st.markdown("- **Larger Text**: Enabled")
        if not any(quiz["accessibility"].values()):
            st.markdown("No additional accessibility features selected.")

        # Example of making an API call or integrating a client to generate quiz questions
        st.markdown("### Generating Your Quiz...")
        try:
            # Simulated example for API call or library usage
            # from gemini import GeminiClient  # Replace with the actual package if available
            # Simulated example for API call or library usage
            # Replace the following lines with actual API call or library usage
            class GeminiClient:
                def __init__(self, api_key):
                    self.api_key = api_key

                def generate_quiz(self, title, num_questions, difficulty):
                    return {
                        "questions": [
                            {"text": f"Sample Question {i+1}", "options": ["Option 1", "Option 2", "Option 3", "Option 4"]}
                            for i in range(num_questions)
                        ]
                    }

            # Initialize client
            client = GeminiClient(api_key="YOUR_API_KEY")  # Replace with your actual API key
            
            # Call the API or library method to generate the quiz
            quiz_questions = client.generate_quiz(
                title=quiz["title"],
                num_questions=quiz["num_questions"],
                difficulty=quiz["difficulty"]
            )
            
            # Display generated quiz questions
            st.markdown("### Quiz Questions:")
            for i, question in enumerate(quiz_questions["questions"], start=1):
                st.markdown(f"**Q{i}:** {question['text']}")
                for j, option in enumerate(question['options'], start=1):
                    st.markdown(f"{j}. {option}")
            
        except Exception as e:
            st.error(f"An error occurred while generating the quiz: {str(e)}")

    else:
        st.warning("No quiz details found. Please go back and customize the quiz.")

    # Navigation buttons
    if st.button("Go Back"):
        navigate_to("customize")
    if st.button("Home"):
        navigate_to("home")

# Render the current page based on session state
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "customize":
    customize_page()
elif st.session_state.page == "quiz":
    quiz_page()




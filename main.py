import streamlit as st
import pickle
import numpy as np
import google.generativeai as genai
import speech_recognition as sr
from streamlit_lottie import st_lottie
import requests

# =======================
# 🔧 Setup Gemini API Key
# =======================
# API key directly embedded in the code
API_KEY = "AIzaSyCBB76bgbgFQXn5mkKcM8Yn77Zkn47Nfqg"
genai.configure(api_key=API_KEY)

# Configure the model name and system prompt
MODEL_NAME = "gemini-1.5-pro-latest"
system_prompt = "You are an AI assistant that only answers questions related to personality traits, behaviors, and psychology. If asked anything outside this domain, politely decline."

# =======================
# 🎨 Custom CSS Styling
# =======================
st.markdown("""
    <style>
        /* ======================== Global Styles ======================== */
        .main-title-container {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            padding: 20px 30px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            width: 100%;
            margin-bottom: 30px;
            transition: transform 0.3s ease;
        }
        
        .main-title-container:hover {
            transform: translateY(-5px);
        }

        .main-title {
            font-size: 2.5em;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        }

        .stApp {
            background: linear-gradient(135deg, #f5f7fa, #e9eef6);
            background-attachment: fixed;
        }

        /* ======================= Block Container ======================= */
        .block-container {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            max-width: 900px;
            margin: 2rem auto;
        }
        
        /* =================== Animation & Images =================== */
        .lottie-container {
            display: flex;
            justify-content: center;
            margin: 20px 0 40px 0;
        }
        
        img {
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }

        /* ======================= Button Styles ======================= */
        .stButton > button {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            font-size: 17px;
            font-weight: 600;
            border-radius: 12px;
            padding: 12px 30px;
            border: none;
            transition: all 0.3s ease;
            width: 100%;
            max-width: 300px;
            margin: 0 auto;
            display: block;
            box-shadow: 0 6px 12px rgba(106, 112, 253, 0.25);
        }

        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 8px 20px rgba(106, 112, 253, 0.35);
            background: linear-gradient(135deg, #7e98ff, #b17ded);
        }
        
        .stButton > button:focus {
            outline: none;
            border: none;
            box-shadow: 0 6px 12px rgba(106, 112, 253, 0.25);
        }
        
        .stButton > button:active {
            transform: translateY(1px);
        }

        /* ======================= Text Input Styles ======================= */
        .stTextInput > div > div > input {
            background-color: #f0f4ff;
            border-radius: 12px;
            font-size: 16px;
            padding: 15px 20px !important;
            border: 1px solid #e1e5ee;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            width: 100%;
            height: 55px !important;
        }

        .stTextInput > div {
            width: 100%;
        }

        .stTextInput > div > div {
            width: 100%;
        }

        .stTextInput > div > div > input:focus {
            outline: none;
            border-color: #6e8efb;
            box-shadow: 0 0 0 3px rgba(110, 142, 251, 0.2);
            transform: translateY(-2px);
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #a0a8c0;
            font-size: 15px;
        }
        
        /* Improved text area for better input experience */
        .stTextArea > div > div > textarea {
            border-radius: 12px;
            font-size: 16px;
            padding: 15px 20px !important;
            border: 1px solid #e1e5ee;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            min-height: 120px !important;
        }
        
        .stTextArea > div > div > textarea:focus {
            outline: none;
            border-color: #6e8efb;
            box-shadow: 0 0 0 3px rgba(110, 142, 251, 0.2);
            transform: translateY(-2px);
        }
        
        /* ======================= Radio Button Styles ======================= */
        .stRadio > div {
            background-color: #f9faff;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid #e9eeff;
        }
        
        .st-bj, .st-bk, .st-bl {
            border-color: #a777e3 !important;
        }
        
        /* Remove red outline on radio buttons */
        .stRadio input[type="radio"]:focus {
            outline: none !important;
            box-shadow: none !important;
        }

        /* ======================= Question and Text Styles ======================= */
        p, .question {
            font-size: 1.1rem;
            color: #4a4a4a;
            line-height: 1.6;
        }
        
        .question-container {
            background-color: #f5f7ff;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            border-left: 4px solid #6e8efb;
            transition: transform 0.2s ease;
        }
        
        .question-container:hover {
            transform: translateX(5px);
        }

        .stMarkdown p {
            font-size: 18px;
        }
        
        h2, h3, h4 {
            color: #444;
            font-weight: 600;
        }
        
        h4 {
            margin-top: 30px;
            margin-bottom: 20px;
            font-size: 1.3rem;
            color: #5974e9;
        }
        
        /* Style for the subtitle/instruction text */
        .subtitle {
            background-color: #f0f4ff;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            border-left: 4px solid #6e8efb;
            color: #444444;
            font-size: 18px;
            font-weight: 600;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
        }

        /* ======================= Success Message Styles ======================= */
        .element-container:has(.stAlert) {
            margin-top: 25px;
            margin-bottom: 25px;
        }
        
        .st-ae {
            border-radius: 10px !important;
            padding: 15px 20px !important;
        }
        
        .st-ae[data-baseweb="notification"] {
            background-color: rgba(154, 230, 180, 0.2) !important;
            border-color: #68d391 !important;
        }
        
        /* ======================= Sidebar Styles ======================= */
        .css-1v0mbdj {
            padding: 1.5rem;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.95);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .css-1v0mbdj p {
            font-size: 18px;
            font-weight: 600;
            color: #555;
        }
        
        /* Add a subtle separator between questions */
        .question-separator {
            height: 1px;
            background: linear-gradient(to right, rgba(110, 142, 251, 0.2), rgba(167, 119, 227, 0.2), rgba(110, 142, 251, 0.2));
            margin: 30px 0;
            border-radius: 1px;
        }
        
        /* Chat container styling */
        .chat-container {
            
            background-color: #f5f9ff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            margin-top: 20px;
            border-left: 4px solid #6e8efb;
        }
        
        /* Response box styling */
        .response-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            margin-top: 20px;
            border-left: 4px solid #6e8efb;
        }
        
        /* Floating input effect */
        .floating-input-container {
            position: relative;
            margin-bottom: 20px;
        }
        
        .floating-button {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 15px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .floating-button:hover {
            transform: translateY(-50%) scale(1.05);
            box-shadow: 0 4px 12px rgba(106, 112, 253, 0.25);
        }
    </style>
""", unsafe_allow_html=True)

# =======================
# 📦 Load Lottie Animation
# =======================
def load_lottieurl(url):
    r = requests.get(url)
    return r.json()

lottie_ai = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_chat = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_1pxqjqps.json")

# =======================
# 🧠 Load Personality Model
# =======================
try:
    with open("personality_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    # Create a dummy model if file doesn't exist
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    # Train with dummy data
    dummy_X = np.random.rand(100, 5)
    dummy_y = np.random.choice(['Introvert', 'Extrovert', 'Ambivert', 'Analyst'], 100)
    model.fit(dummy_X, dummy_y)
    # Save the dummy model
    with open("personality_model.pkl", "wb") as f:
        pickle.dump(model, f)

# =======================
# 🤖 Gemini AI Function
# =======================
def ask_personality_question(user_input):
    try:
        g_model = genai.GenerativeModel(MODEL_NAME)
        response = g_model.generate_content([system_prompt, user_input])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# =======================
# 🎤 Voice Recognition
# =======================
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("✅ Voice captured! Processing...")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            return "Listening timed out. Please try again."
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Error: Could not request results, check internet connection."

# =======================
# 🚀 Sidebar Navigation
# =======================
st.sidebar.title("🧭 Navigation")
app_choice = st.sidebar.radio("Go to", ["🎯 Personality Quiz", "💬 Personality Chatbot"])

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# =======================
# 🎯 Personality Quiz Page
# =======================
if app_choice == "🎯 Personality Quiz":
    # Centered title in gradient box
    st.markdown('<div class="main-title-container"><div class="main-title">🧠 Personality Quiz</div></div>', unsafe_allow_html=True)
    
    # Centered Lottie animation with custom container
    st.markdown('<div class="lottie-container">', unsafe_allow_html=True)
    st_lottie(lottie_ai, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # Fixed heading with proper contrast
    st.markdown("""
    <div class="subtitle">
        📝 Answer the questions below to discover your personality type
    </div>
    """, unsafe_allow_html=True)

    questions = [
        "How do you feel about trying new activities?",
        "Do you prefer planning things in advance?",
        "Do you enjoy socializing with large groups?",
        "Do you consider yourself empathetic and caring?",
        "Do you often feel anxious or overthink situations?"
    ]
    choices = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]

    responses = []

    # Display questions directly without expander
    for i, question in enumerate(questions):
        # Using custom styled question containers
        st.markdown(f"""
        <div class="question-container">
            <p><strong>Q{i+1}:</strong> {question}</p>
        </div>
        """, unsafe_allow_html=True)
        
        answer = st.radio("", choices, key=f"q{i}")
        responses.append(choices.index(answer) + 1)
        
        # Add separator between questions (except after the last question)
        if i < len(questions) - 1:
            st.markdown('<div class="question-separator"></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🧠 Get My Personality Type"):
        if len(responses) == 5:
            responses_array = np.array(responses).reshape(1, -1)
            prediction = model.predict(responses_array)[0]
            
            # More detailed personality descriptions
            personality_descriptions = {
                'Introvert': "You tend to be thoughtful and reserved, preferring meaningful one-on-one conversations. You recharge by spending time alone and value deep connections over wide social networks.",
                'Extrovert': "You're outgoing, energetic, and draw energy from social interactions. You enjoy being the center of attention and thrive in group settings.",
                'Ambivert': "You have a balanced personality that combines traits of both introverts and extroverts. You adapt well to different social situations and know when to speak up or listen.",
                'Analyst': "You approach life logically and systematically. You value facts over feelings and enjoy solving complex problems through careful analysis."
            }
            
            description = personality_descriptions.get(prediction, "A unique blend of personality traits that makes you who you are.")
            
            # Enhanced success message with description
            st.markdown(f"""
            <div style="background-color: #f0fff4; padding: 20px; border-radius: 10px; 
                      box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-top: 20px; 
                      border-left: 4px solid #68d391;">
                <h3 style="color: #2f855a; margin-bottom: 15px;">🎉 Your Personality Type: {prediction}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❗ Please answer all questions.")

# =======================
# 💬 Personality Chatbot Page
# =======================
elif app_choice == "💬 Personality Chatbot":
    st.markdown('<div class="main-title-container"><div class="main-title">💬 Personality Chatbot</div></div>', unsafe_allow_html=True)
    
    # Centered Lottie animation
    st.markdown('<div class="lottie-container">', unsafe_allow_html=True)
    st_lottie(lottie_chat, height=180)
    st.markdown('</div>', unsafe_allow_html=True)

    # Updated instruction with proper styling
    st.markdown("""
    <div class="subtitle">
        Ask me anything related to psychology, personality, or behavior traits
    </div>
    """, unsafe_allow_html=True)

    # Display chat history
    if st.session_state.chat_history:
        for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
            # User message
            st.markdown(f"""
            <div style="background-color: #e8f0fe; padding: 15px; border-radius: 10px 10px 10px 0; 
                      margin: 15px 0 10px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
                      max-width: 80%; margin-left: auto; border-right: 4px solid #6e8efb;">
                <p style="margin: 0; font-weight: 600; color: #4a4a4a;">You</p>
                <p style="margin: 8px 0 0 0;">{user_msg}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # AI response
            st.markdown(f"""
            <div style="background-color: #f5f7ff; padding: 15px; border-radius: 10px 10px 0 10px; 
                      margin: 10px 0 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
                      max-width: 80%; border-left: 4px solid #a777e3;">
                <p style="margin: 0; font-weight: 600; color: #4a4a4a;">AI Assistant</p>
                <p style="margin: 8px 0 0 0;">{ai_response}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Input methods section
    st.markdown("<h4>Ask Your Question:</h4>", unsafe_allow_html=True)
    
    # Tabs for text and voice input
    tab1, tab2 = st.tabs(["💬 Text Input", "🎤 Voice Input"])
    
    with tab1:
        # Improved text input with better UI
        user_text = st.text_area("", placeholder="Type your psychology or personality question here...", height=120)
        
        if st.button("Ask Question", key="text_button"):
            if user_text:
                with st.spinner("Thinking..."):
                    answer = ask_personality_question(user_text)
                
                # Add to chat history
                st.session_state.chat_history.append((user_text, answer))
                st.rerun()
            else:
                st.warning("Please type a question first.")
    
    with tab2:
        # Voice input section
        st.markdown("Click the button below and ask your question by voice:")
        if st.button("Start Voice Input", key="voice_button"):
            user_question = recognize_speech()
            
            if user_question and "Sorry" not in user_question and "Error" not in user_question and "Listening timed out" not in user_question:
                st.write(f"🗣 **You said:** {user_question}")
                
                with st.spinner("Thinking..."):
                    answer = ask_personality_question(user_question)
                
                # Add to chat history
                st.session_state.chat_history.append((user_question, answer))
                st.rerun()
            else:
                st.warning(user_question)
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

# Footer
st.markdown("---")

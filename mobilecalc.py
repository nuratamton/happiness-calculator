import streamlit as st  

# Page configuration
st.set_page_config(page_title="Happiness Index Calculator", page_icon="😊")

# Initialize session state
if "age_group" not in st.session_state:
    st.session_state.age_group = None
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "calculation_done" not in st.session_state:
    st.session_state.calculation_done = False

# Questions for different groups
questions_dict = {
   "Kid": [
        {"question": "How many hours do you play daily?", "range": "(0-6)", "min": 0, "max": 6, "weight": 0.25},
        {"question": "How happy do you feel at school?", "range": "(1-10)", "min": 1, "max": 10, "weight": 0.25},
        {"question": "Do you get enough sleep?", "range": "(5-12)", "min": 5, "max": 12, "weight": 0.25},
        {"question": "How much time do you spend with friends?", "range": "(0-6)", "min": 0, "max": 6, "weight": 0.25},
    ],
    "Student": [
        {"question": "Hours per day on education?", "range": "(2-10)", "min": 2, "max": 10, "weight": 0.25},
        {"question": "How many hours do you socialize?", "range": "(0-6)", "min": 0, "max": 6, "weight": 0.25},
        {"question": "How healthy do you feel?", "range": "(1-10)", "min": 1, "max": 10, "weight": 0.25},
        {"question": "How many hours do you sleep?", "range": "(4-10)", "min": 4, "max": 10, "weight": 0.25},
    ],
    "Adult": [
        {"question": "What's your monthly income?", "range": "(1000-25000)", "min": 1000, "max": 25000, "weight": 0.25},
        {"question": "How many hours do you socialize per day?", "range": "(0-10)", "min": 0, "max": 10, "weight": 0.2},
        {"question": "How healthy do you feel?", "range": "(1-10)", "min": 1, "max": 10, "weight": 0.2},
        {"question": "Hours of sleep per day?", "range": "(2-12)", "min": 2, "max": 12, "weight": 0.15},
        {"question": "Hours per day on education/self-growth?", "range": "(0-8)", "min": 0, "max": 8, "weight": 0.2},
    ],
}

def calculate_happiness_index():
    total_weighted_score = 0
    qs = questions_dict[st.session_state.age_group]
    for i, answer in enumerate(st.session_state.answers):
        q = qs[i]
        normalized = ((answer - q["min"]) / (q["max"] - q["min"])) * 100
        weighted_score = normalized * q["weight"]
        total_weighted_score += weighted_score
    st.session_state.happiness_index = round(total_weighted_score / 10, 2)
    st.session_state.calculation_done = True

def restart_calculator():
    st.session_state.age_group = None
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.calculation_done = False
    if "happiness_index" in st.session_state:
        del st.session_state.happiness_index

# CSS for calculator look with mobile-friendly input
st.markdown("""
<style>
    .calculator-container {
        background: linear-gradient(145deg, #1e3c72, #2a5298); /* blue gradient */
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-width: 400px;
        margin: 0 auto;
    }
    
    .calculator-screen {
        background: #162447;
        color: #00d4ff;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        min-height: 120px;
        border: 2px solid #1f4068;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .question-number { color: #00d4ff; font-weight: bold; }
    .question-text { color: #e0f7fa; font-size: 18px; margin: 10px 0; }
    .range-text { color: #ffcc00; font-size: 14px; }
    .result-screen {
        background: #007acc;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Style the number input to look like calculator */
    .stNumberInput > div > div > input {
        background: #0f2027 !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 32px !important;
        text-align: center !important;
        border: 2px solid #1f4068 !important;
        border-radius: 10px !important;
        height: 80px !important;
        font-weight: bold !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Style the submit button */
    .stButton button {
        width: 100% !important;
        height: 60px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        background: linear-gradient(135deg, #2193b0, #6dd5ed) !important;
        color: white !important;
        transition: all 0.2s !important;
        margin-top: 20px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* Style restart button differently */
    .restart-btn button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e) !important;
    }
    
    .restart-btn button:hover {
        background: linear-gradient(135deg, #e55252, #ff6b6b) !important;
    }
    
    /* Hide increment/decrement buttons on number input */
    .stNumberInput > div > div > div > button {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Main App
st.title("💙 Happiness Index Calculator")

# Step 1: Ask age group
if st.session_state.age_group is None:
    st.subheader("Who are you?")
    choice = st.radio("Select your group:", ["Kid", "Student", "Adult"], index=None)

    if st.button("Start", type="primary") and choice:
        st.session_state.age_group = choice
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.calculation_done = False
        st.rerun()

else:
    # Calculator Container
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

    if not st.session_state.calculation_done:
        current_q = questions_dict[st.session_state.age_group][st.session_state.current_question]
        
        # Calculator screen
        screen_content = f"""
        <div class="calculator-screen">
            <div class="question-number">Question {st.session_state.current_question + 1} of {len(questions_dict[st.session_state.age_group])}</div>
            <div class="question-text">{current_q['question']}</div>
            <div class="range-text">Range: {current_q['range']}</div>
        </div>
        """
        st.markdown(screen_content, unsafe_allow_html=True)
        
        # Mobile-friendly number input
        answer = st.number_input(
            label="Your answer:",
            min_value=current_q['min'],
            max_value=current_q['max'],
            value=current_q['min'],
            step=1,
            label_visibility="collapsed"
        )
        
        # Submit button
        if st.button("SUBMIT ANSWER"):
            st.session_state.answers.append(answer)
            st.session_state.current_question += 1
            if st.session_state.current_question >= len(questions_dict[st.session_state.age_group]):
                calculate_happiness_index()
            st.rerun()
        
    else:
        # Results screen
        happiness_index = st.session_state.happiness_index
        if happiness_index >= 7:
            emoji = "🌟"
            message = "You're doing amazing!"
        elif happiness_index >= 4.5:
            emoji = "🙂"
            message = "You're doing okay!"
        else:
            emoji = "😟"
            message = "Take care of yourself!"
            
        screen_content = f"""
        <div class="calculator-screen result-screen">
            <div>{emoji}</div>
            <div>Happiness Index</div>
            <div style="font-size: 36px; margin: 10px 0;">{happiness_index} / 10</div>
            <div style="font-size: 16px;">{message}</div>
        </div>
        """
        st.markdown(screen_content, unsafe_allow_html=True)
        
        # Restart button
        st.markdown('<div class="restart-btn">', unsafe_allow_html=True)
        if st.button("NEW CALCULATION"):
            restart_calculator()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
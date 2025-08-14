import streamlit as st

# Page configuration
st.set_page_config(page_title="Happiness Index Calculator", page_icon="😊")

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False

# Questions with min, max values
questions = [
    {
        "question": "What's your monthly income?",
        "range": "(1000-25000)",
        "min": 1000,
        "max": 25000,
        "weight": 0.25
    },
    {
        "question": "How many hours do you socialize per day?",
        "range": "(0-10)",
        "min": 0,
        "max": 10,
        "weight": 0.2
    },
    {
        "question": "How healthy do you feel?",
        "range": "(1-10)",
        "min": 1,
        "max": 10,
        "weight": 0.2
    },
    {
        "question": "Hours per day on education?",
        "range": "(2-10)",
        "min": 2,
        "max": 10,
        "weight": 0.2
    },
    {
        "question": "Hours of sleep per day?",
        "range": "(2-12)",
        "min": 2,
        "max": 12,
        "weight": 0.15
    }
]

# CSS for calculator styling
st.markdown("""
<style>
    .calculator-container {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0);
        max-width: 400px;
        margin: 0 auto;
    }
    
    .calculator-screen {
        background: #1a252f;
        color: #00ff41;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        min-height: 120px;
        border: 2px solid #34495e;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .input-display {
        background: #0f1419;
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        padding: 10px;
        border-radius: 5px;
        text-align: right;
        margin-top: 10px;
        border: 1px solid #34495e;
    }
    
    .question-number {
        color: #3498db;
        font-weight: bold;
    }
    
    .question-text {
        color: #00ff41;
        font-size: 18px;
        margin: 10px 0;
    }
    
    .range-text {
        color: #f39c12;
        font-size: 14px;
    }
    
    .result-screen {
        background: #27ae60;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    
    .stButton button {
        width: 100%;!important;
        margin: 2px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .number-btn {
        background: #ecf0f1 !important;
        color: #2c3e50 !important;
    }
    
    .action-btn {
        background: #3498db !important;
        color: white !important;
    }
    
    .clear-btn {
        background: #e74c3c !important;
        color: white !important;
    }
    
    .enter-btn {
        background: #27ae60 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Functions
def add_number(num):
    if len(st.session_state.current_input) < 10:  # Limit input length
        st.session_state.current_input += str(num)
        st.rerun()

def clear_input():
    st.session_state.current_input = ""
    st.rerun()

def delete_last():
    st.session_state.current_input = st.session_state.current_input[:-1]
    st.rerun()

def enter_answer():
    if st.session_state.current_input:
        try:
            answer = int(st.session_state.current_input)
            current_q = questions[st.session_state.current_question]
            
            # Validate range
            if current_q["min"] <= answer <= current_q["max"]:
                st.session_state.answers.append(answer)
                st.session_state.current_input = ""
                st.session_state.current_question += 1
                
                # Check if all questions are answered
                if st.session_state.current_question >= len(questions):
                    calculate_happiness_index()

                st.rerun()
            else:
                st.error(f"Please enter a number between {current_q['min']} and {current_q['max']}")
        except ValueError:
            st.error("Please enter a valid number")

def calculate_happiness_index():
    total_weighted_score = 0
    
    for i, answer in enumerate(st.session_state.answers):
        q = questions[i]
        # Normalize to 0–100
        normalized = ((answer - q["min"]) / (q["max"] - q["min"])) * 100
        # Multiply by weight
        weighted_score = normalized * q["weight"]
        total_weighted_score += weighted_score
    
    st.session_state.happiness_index = round(total_weighted_score / 10, 2)
    st.session_state.calculation_done = True

def restart_calculator():
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.current_input = ""
    st.session_state.calculation_done = False
    if 'happiness_index' in st.session_state:
        del st.session_state.happiness_index

# Main app
st.title("Happiness Index Calculator")

# Calculator container
with st.container():
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    
    # Calculator screen
    if not st.session_state.calculation_done:
        current_q = questions[st.session_state.current_question]
        screen_content = f"""
        <div class="calculator-screen">
            <div class="question-number">Question {st.session_state.current_question + 1} of {len(questions)}</div>
            <div class="question-text">{current_q['question']}</div>
            <div class="range-text">Range: {current_q['range']}</div>
            <div class="input-display">{st.session_state.current_input or '0'}</div>
        </div>
        """
    else:
        # Show result
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
    
    # Number pad
    if not st.session_state.calculation_done:
        col1, col2, col3 = st.columns(3)
        
        # Row 1
        with col1:
            if st.button("7", key="btn7"):
                add_number(7)
        with col2:
            if st.button("8", key="btn8"):
                add_number(8)
        with col3:
            if st.button("9", key="btn9"):
                add_number(9)
        
        # Row 2
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("4", key="btn4"):
                add_number(4)
        with col2:
            if st.button("5", key="btn5"):
                add_number(5)
        with col3:
            if st.button("6", key="btn6"):
                add_number(6)
        
        # Row 3
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("1", key="btn1"):
                add_number(1)
        with col2:
            if st.button("2", key="btn2"):
                add_number(2)
        with col3:
            if st.button("3", key="btn3"):
                add_number(3)
        
        # Row 4
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("0", key="btn0"):
                add_number(0)
        with col2:
            if st.button("⌫", key="delete"):
                delete_last()
        with col3:
            if st.button("C", key="clear"):
                clear_input()
        
        # Enter button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("ENTER", key="enter"):
                enter_answer()
    
    else:
        # Restart button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("NEW CALCULATION", key="restart"):
                restart_calculator()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


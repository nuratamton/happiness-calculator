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
if "current_input" not in st.session_state:
    st.session_state.current_input = ""
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

# CSS Blue Theme
st.markdown("""
<style>
    .calculator-container {
        background: linear-gradient(145deg, #1e3c72, #2a5298); /* blue gradient */
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-width: 420px;
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
    .input-display {
        background: #0f2027;
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        padding: 10px;
        border-radius: 5px;
        text-align: right;
        margin-top: 10px;
        border: 1px solid #1f4068;
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
    .stButton button {
        width: 100% !important;
        margin: 2px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #2193b0, #6dd5ed) !important;
        color: white !important;
        transition: all 0.2s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Functions
def add_number(num):
    if len(st.session_state.current_input) < 10:
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
            current_q = questions_dict[st.session_state.age_group][st.session_state.current_question]
            if current_q["min"] <= answer <= current_q["max"]:
                st.session_state.answers.append(answer)
                st.session_state.current_input = ""
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(questions_dict[st.session_state.age_group]):
                    calculate_happiness_index()
                st.rerun()
            else:
                st.error(f"Please enter a number between {current_q['min']} and {current_q['max']}")
        except ValueError:
            st.error("Please enter a valid number")

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
    st.session_state.current_input = ""
    st.session_state.calculation_done = False
    if "happiness_index" in st.session_state:
        del st.session_state.happiness_index

# Main App
st.title("💙 Happiness Index Calculator")

# Step 1: Ask age group
if st.session_state.age_group is None:
    st.subheader("Who are you?")
    choice = st.radio("Select your group:", ["Kid", "Student", "Adult"], index=None)

    if st.button("Start") and choice:
        # Reset state properly when a new group is chosen
        st.session_state.age_group = choice
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.current_input = ""
        st.session_state.calculation_done = False
        st.rerun()

else:
    # Calculator Container
    with st.container():
        st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

        if not st.session_state.calculation_done:
            current_q = questions_dict[st.session_state.age_group][st.session_state.current_question]
            screen_content = f"""
            <div class="calculator-screen">
                <div class="question-number">Question {st.session_state.current_question + 1} of {len(questions_dict[st.session_state.age_group])}</div>
                <div class="question-text">{current_q['question']}</div>
                <div class="range-text">Range: {current_q['range']}</div>
                <div class="input-display">{st.session_state.current_input or '0'}</div>
            </div>
            """
        else:
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
            with col1:
                if st.button("7"): add_number(7)
            with col2:
                if st.button("8"): add_number(8)
            with col3:
                if st.button("9"): add_number(9)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("4"): add_number(4)
            with col2:
                if st.button("5"): add_number(5)
            with col3:
                if st.button("6"): add_number(6)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("1"): add_number(1)
            with col2:
                if st.button("2"): add_number(2)
            with col3:
                if st.button("3"): add_number(3)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("0"): add_number(0)
            with col2:
                if st.button("⌫"): delete_last()
            with col3:
                if st.button("C"): clear_input()

            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("ENTER"): enter_answer()
        else:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("NEW CALCULATION"):
                    restart_calculator()
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


import streamlit as st
from database import add_user, login
from dashboard import dashboard
from quiz import start_quiz

st.set_page_config(
    page_title="InterviewAce",
    page_icon="🎤",
    layout="wide"
)

# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "career" not in st.session_state:
    st.session_state.career = "Data Analyst"

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Beginner"


# ==================================================
# LOGGED IN
# ==================================================

if st.session_state.logged_in:

    # ---------------- DASHBOARD ----------------

    if st.session_state.page == "dashboard":

        dashboard(st.session_state.username)

        st.markdown("---")

        if st.button("🚪 Logout", key="logout_button"):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "dashboard"

            st.rerun()


    # ---------------- QUIZ ----------------

    elif st.session_state.page == "quiz":

        start_quiz(
            st.session_state.career,
            st.session_state.difficulty
        )

        st.markdown("---")

        if st.button(
            "⬅ Back to Dashboard",
            key="quiz_back"
        ):

            st.session_state.page = "dashboard"
            st.rerun()


    # ---------------- INTERVIEW ----------------

    elif st.session_state.page == "interview":

        from interview import start_interview

        start_interview(
            st.session_state.career,
            st.session_state.difficulty
        )

        st.markdown("---")

        if st.button(
            "⬅ Back to Dashboard",
            key="interview_back"
        ):

            st.session_state.page = "dashboard"
            st.rerun()


# ==================================================
# NOT LOGGED IN
# ==================================================

else:

    st.title("🎤 AI Interview Preparation App")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Home", "Register", "Login"]
    )


    # ---------------- HOME ----------------

    if menu == "Home":

        st.title("🎤 InterviewAce")
        st.subheader("AI Interview Coach")

        st.write("""
Welcome to **InterviewAce**!

Practice technical interviews, identify your weak areas,
improve your confidence, and prepare for your dream job.
""")

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Career Paths", "5+")

        with col2:
            st.metric("Interview Questions", "100+")

        with col3:
            st.metric("Mock Interviews", "Unlimited")

        st.divider()

        st.markdown("## 🚀 Features")

        st.markdown("""
- 🤖 AI-Inspired Answer Evaluation
- 📊 Personalized Interview Reports
- 🎯 Career-Based Interview Questions
- 📈 Progress Tracking
- 💡 Learning Recommendations
""")

        st.success(
            "Start your interview preparation journey today!"
        )


    # ---------------- REGISTER ----------------

    elif menu == "Register":

        st.subheader("Register")

        username = st.text_input(
            "Create Username"
        )

        password = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Register"):

            add_user(
                username,
                password
            )

            st.success(
                "Registration Successful! Please Login."
            )


    # ---------------- LOGIN ----------------

    elif menu == "Login":

        st.subheader("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "dashboard"

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )
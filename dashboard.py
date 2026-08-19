import streamlit as st
from resume_analyzer import analyze_resume
from database import (
    get_interview_history,
    get_quiz_history
)


def dashboard(username):

    # ==================================================
    # HEADER
    # ==================================================

    st.title("🎯 InterviewAce")
    st.subheader(f"Welcome, {username}! 👋")

    st.caption(
        "🤖 Your AI-powered interview preparation platform"
    )

    st.markdown("---")

    # ==================================================
    # CAREER & DIFFICULTY
    # ==================================================

    st.header("💼 Interview Preparation")

    career_options = [
        "Data Analyst",
        "Python Developer",
        "Java Developer",
        "Web Developer",
        "HR Interview"
    ]

    difficulty_options = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    # Make sure session state exists
    if "career" not in st.session_state:
        st.session_state.career = career_options[0]

    if "difficulty" not in st.session_state:
        st.session_state.difficulty = difficulty_options[0]

    col1, col2 = st.columns(2)

    with col1:

        career = st.selectbox(
            "💼 Select Your Career",
            career_options,
            index=career_options.index(
                st.session_state.career
            ),
            key="career_select"
        )

    with col2:

        difficulty = st.selectbox(
            "📚 Select Difficulty",
            difficulty_options,
            index=difficulty_options.index(
                st.session_state.difficulty
            ),
            key="difficulty_select"
        )

    st.session_state.career = career
    st.session_state.difficulty = difficulty

    st.info(
        f"🎯 Selected Path: **{career}** | "
        f"📚 Level: **{difficulty}**"
    )

    # ==================================================
    # RESUME ANALYZER
    # ==================================================

    st.markdown("---")

    st.header("📄 Resume Analyzer")

    # Initialize resume session state

    if "resume_uploaded" not in st.session_state:
        st.session_state.resume_uploaded = False

    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""

    if "found_skills" not in st.session_state:
        st.session_state.found_skills = []

    if "missing_skills" not in st.session_state:
        st.session_state.missing_skills = []

    if "resume_score" not in st.session_state:
        st.session_state.resume_score = 0

    # Resume uploader

    uploaded_resume = st.file_uploader(
        "Upload Your Resume (TXT)",
        type=["txt"],
        key="resume_uploader"
    )

    if uploaded_resume is not None:

        try:

            resume_text = uploaded_resume.read().decode(
                "utf-8"
            )

            found_skills, missing_skills = analyze_resume(
                resume_text
            )

            total = (
                len(found_skills)
                + len(missing_skills)
            )

            if total > 0:

                score = int(
                    (len(found_skills) / total) * 100
                )

            else:

                score = 0

            # Save information

            st.session_state.resume_uploaded = True
            st.session_state.resume_text = resume_text
            st.session_state.found_skills = found_skills
            st.session_state.missing_skills = missing_skills
            st.session_state.resume_score = score

        except Exception as e:

            st.error(
                f"Unable to read the resume: {e}"
            )

    # ==================================================
    # SHOW RESUME RESULTS
    # ==================================================

    if st.session_state.resume_uploaded:

        st.success(
            "✅ Resume uploaded successfully!"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🎯 Skills Found")

            if st.session_state.found_skills:

                for skill in st.session_state.found_skills:

                    st.write(
                        f"✅ {skill}"
                    )

            else:

                st.write(
                    "No skills detected."
                )

        with col2:

            st.subheader("📚 Skills to Improve")

            if st.session_state.missing_skills:

                for skill in st.session_state.missing_skills:

                    st.write(
                        f"❌ {skill}"
                    )

            else:

                st.write(
                    "🎉 No missing skills detected!"
                )

        st.subheader(
            "📊 Resume Match Score"
        )

        st.progress(
            st.session_state.resume_score
        )

        st.write(
            f"**Resume Match: "
            f"{st.session_state.resume_score}%**"
        )

    # ==================================================
    # QUICK START
    # ==================================================

    st.markdown("---")

    st.header("🚀 Quick Start")

    st.write(
        "Choose your career and difficulty above, "
        "then select how you want to practice."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "📚 **Quiz Practice**\n\n"
            "Test your knowledge with career-based questions."
        )

    with col2:

        st.info(
            "🎤 **Mock Interview**\n\n"
            "Answer interview questions and receive feedback."
        )

    # ==================================================
    # START PRACTICE
    # ==================================================

    st.markdown("---")

    st.header("🎯 Start Practice")

    col1, col2 = st.columns(2)

    # ---------------- QUIZ ----------------

    with col1:

        if st.button(
            "📚 Start Quiz",
            key="dashboard_start_quiz"
        ):

            st.session_state.career = career
            st.session_state.difficulty = difficulty
            st.session_state.page = "quiz"

            st.rerun()

    # ---------------- INTERVIEW ----------------

    with col2:

        if st.button(
            "🎤 Start Interview",
            key="dashboard_start_interview"
        ):

            st.session_state.career = career
            st.session_state.difficulty = difficulty
            st.session_state.page = "interview"

            st.rerun()

    # ==================================================
    # INTERVIEW PROGRESS
    # ==================================================

    st.markdown("---")

    st.header("🎤 Interview Progress")

    history = get_interview_history(username)

    if history:

        total_interviews = len(history)

        percentages = [
            row[4]
            for row in history
        ]

        average_score = (
            sum(percentages)
            / total_interviews
        )

        best_score = max(percentages)

        careers_practiced = len(
            set(row[0] for row in history)
        )

        # ---------------- METRICS ----------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🎤 Interviews",
                total_interviews
            )

        with col2:

            st.metric(
                "📊 Average",
                f"{average_score:.1f}%"
            )

        with col3:

            st.metric(
                "🏆 Best Score",
                f"{best_score:.1f}%"
            )

        with col4:

            st.metric(
                "💼 Careers",
                careers_practiced
            )

        # ---------------- SCORE CHART ----------------

        st.subheader(
            "📈 Interview Score Progress"
        )

        chart_data = []

        for index, row in enumerate(history):

            chart_data.append(
                {
                    "Interview": f"Interview {index + 1}",
                    "Score": row[4]
                }
            )

        if chart_data:

            st.line_chart(
                chart_data,
                x="Interview",
                y="Score"
            )

        # ---------------- DETAILED PROGRESS ----------------

        st.subheader(
            "📋 Detailed Interview Progress"
        )

        for index, row in enumerate(history):

            career_name = row[0]
            difficulty_name = row[1]
            percentage = row[4]

            st.write(
                f"**{index + 1}. "
                f"{career_name} — "
                f"{difficulty_name}**"
            )

            st.progress(
                int(percentage)
            )

            st.caption(
                f"Score: {percentage:.1f}%"
            )

    else:

        st.info(
            "🎯 Complete your first interview "
            "to see your interview progress here."
        )

    # ==================================================
    # QUIZ PROGRESS
    # ==================================================

    st.markdown("---")

    st.header("📚 Quiz Progress")

    quiz_history = get_quiz_history(username)

    if quiz_history:

        total_quizzes = len(
            quiz_history
        )

        quiz_percentages = [
            row[4]
            for row in quiz_history
        ]

        average_quiz_score = (
            sum(quiz_percentages)
            / total_quizzes
        )

        best_quiz_score = max(
            quiz_percentages
        )

        # ---------------- QUIZ METRICS ----------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📚 Quiz Attempts",
                total_quizzes
            )

        with col2:

            st.metric(
                "📊 Average Score",
                f"{average_quiz_score:.1f}%"
            )

        with col3:

            st.metric(
                "🏆 Best Quiz Score",
                f"{best_quiz_score:.1f}%"
            )

        # ---------------- QUIZ CHART ----------------

        st.subheader(
            "📈 Quiz Score Progress"
        )

        quiz_chart_data = []

        for index, row in enumerate(
            quiz_history
        ):

            quiz_chart_data.append(
                {
                    "Quiz": f"Quiz {index + 1}",
                    "Score": row[4]
                }
            )

        if quiz_chart_data:

            st.line_chart(
                quiz_chart_data,
                x="Quiz",
                y="Score"
            )

        # ---------------- QUIZ HISTORY ----------------

        st.subheader(
            "📋 Quiz History"
        )

        for index, row in enumerate(
            quiz_history
        ):

            career_name = row[0]
            difficulty_name = row[1]
            score = row[2]
            total_questions = row[3]
            percentage = row[4]

            st.write(
                f"**{index + 1}. "
                f"{career_name} — "
                f"{difficulty_name}**"
            )

            st.write(
                f"🎯 Score: "
                f"**{score}/{total_questions}**"
            )

            st.progress(
                int(percentage)
            )

            st.caption(
                f"Percentage: {percentage:.1f}%"
            )

    else:

        st.info(
            "📚 Complete your first quiz "
            "to see your quiz progress here."
        )

    # ==================================================
    # INTERVIEW HISTORY
    # ==================================================

    st.markdown("---")

    st.header("📈 Interview History")

    if history:

        for (
            career_name,
            difficulty_name,
            score,
            max_score,
            percentage
        ) in history:

            st.write(
                f"💼 **{career_name}** | "
                f"📚 {difficulty_name} | "
                f"🎯 {score}/{max_score} | "
                f"📊 {percentage:.1f}%"
            )

    else:

        st.info(
            "No interview history yet. "
            "Complete an interview to see "
            "your results here."
        )

    # ==================================================
    # FOOTER
    # ==================================================

    st.markdown("---")

    st.caption(
        "🎤 InterviewAce | "
        "AI-Powered Interview Preparation Platform"
    )
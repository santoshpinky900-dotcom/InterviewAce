import streamlit as st
from question_bank import questions
from database import save_quiz_result


def start_quiz(career, difficulty):

    st.header("📚 Interview Quiz")

    st.subheader(
        f"💼 {career} | 📚 {difficulty}"
    )

    quiz_questions = questions[career][difficulty]

    quiz_id = f"{career}_{difficulty}"

    # ==================================================
    # SESSION STATE
    # ==================================================

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = {}

    if quiz_id not in st.session_state.quiz_data:

        st.session_state.quiz_data[quiz_id] = {
            "answers": {},
            "submitted": False,
            "score": 0,
            "percentage": 0,
            "saved_to_database": False
        }

    quiz_data = st.session_state.quiz_data[quiz_id]

    # ==================================================
    # QUESTIONS
    # ==================================================

    for i, q in enumerate(quiz_questions):

        st.write(
            f"### Question {i + 1}"
        )

        st.write(
            q["question"]
        )

        options = q["keywords"]

        answer_key = f"{quiz_id}_q_{i}"

        # ==================================================
        # SAVED ANSWER
        # ==================================================

        if quiz_data["submitted"]:

            selected_answer = quiz_data[
                "answers"
            ].get(
                answer_key,
                ""
            )

            st.radio(
                "Your Answer:",
                options,
                index=(
                    options.index(selected_answer)
                    if selected_answer in options
                    else None
                ),
                key=answer_key,
                disabled=True
            )

        else:

            answer = st.radio(
                "Choose your answer:",
                options,
                key=answer_key
            )

            quiz_data["answers"][
                answer_key
            ] = answer

    st.markdown("---")

    # ==================================================
    # SUBMIT QUIZ
    # ==================================================

    if not quiz_data["submitted"]:

        if st.button(
            "📝 Submit Quiz",
            key=f"submit_{quiz_id}"
        ):

            score = 0

            # ---------------- CHECK ANSWERS ----------------

            for i, q in enumerate(quiz_questions):

                answer_key = (
                    f"{quiz_id}_q_{i}"
                )

                selected_answer = (
                    quiz_data["answers"].get(
                        answer_key,
                        ""
                    )
                )

                correct_answer = (
                    q["keywords"][0]
                )

                if selected_answer == correct_answer:

                    score += 1

            # ---------------- CALCULATE SCORE ----------------

            total_questions = len(
                quiz_questions
            )

            if total_questions > 0:

                percentage = (
                    score
                    / total_questions
                ) * 100

            else:

                percentage = 0

            # ---------------- SAVE SESSION DATA ----------------

            quiz_data["score"] = score
            quiz_data["percentage"] = percentage
            quiz_data["submitted"] = True

            st.rerun()

    # ==================================================
    # SHOW RESULT
    # ==================================================

    if quiz_data["submitted"]:

        st.header(
            "🏆 Quiz Completed!"
        )

        score = quiz_data["score"]

        percentage = quiz_data[
            "percentage"
        ]

        st.markdown("---")

        st.success(
            f"🎯 Your Score: "
            f"{score}/{len(quiz_questions)}"
        )

        st.write(
            f"📊 Percentage: "
            f"**{percentage:.1f}%**"
        )

        # ==================================================
        # SAVE RESULT TO DATABASE
        # ==================================================

        if not quiz_data[
            "saved_to_database"
        ]:

            try:

                save_quiz_result(
                    st.session_state.username,
                    career,
                    difficulty,
                    score,
                    len(quiz_questions),
                    percentage
                )

                quiz_data[
                    "saved_to_database"
                ] = True

            except Exception as e:

                st.warning(
                    f"Quiz result could not be saved: {e}"
                )

        # ==================================================
        # PERFORMANCE
        # ==================================================

        st.markdown("---")

        st.subheader(
            "📈 Performance"
        )

        if percentage == 100:

            st.success(
                "🏆 Perfect! Excellent performance!"
            )

        elif percentage >= 60:

            st.info(
                "👍 Good job! Keep practicing."
            )

        else:

            st.warning(
                "📚 You need more practice."
            )

        # ==================================================
        # ANSWER REVIEW
        # ==================================================

        st.markdown("---")

        st.subheader(
            "📝 Answer Review"
        )

        for i, q in enumerate(
            quiz_questions
        ):

            answer_key = (
                f"{quiz_id}_q_{i}"
            )

            selected_answer = (
                quiz_data["answers"].get(
                    answer_key,
                    ""
                )
            )

            correct_answer = (
                q["keywords"][0]
            )

            # ---------------- CORRECT ----------------

            if selected_answer == correct_answer:

                st.success(
                    f"Question {i + 1}: "
                    f"Correct ✅"
                )

                st.write(
                    f"Your answer: "
                    f"**{selected_answer}**"
                )

            # ---------------- WRONG ----------------

            else:

                st.error(
                    f"Question {i + 1}: "
                    f"Wrong ❌"
                )

                st.write(
                    f"Your answer: "
                    f"**{selected_answer}**"
                )

                st.write(
                    f"Correct answer: "
                    f"**{correct_answer}**"
                )

        # ==================================================
        # RETAKE
        # ==================================================

        st.markdown("---")

        if st.button(
            "🔄 Retake Quiz",
            key=f"retake_{quiz_id}"
        ):

            del st.session_state.quiz_data[
                quiz_id
            ]

            st.rerun()
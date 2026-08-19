import streamlit as st
from question_bank import questions
from ai_engine import evaluate_answer
from pdf_report import create_report


def start_interview(career, difficulty):

    st.title("🎤 InterviewAce Interview")

    st.subheader(
        f"💼 {career} | 📚 {difficulty}"
    )

    # ==================================================
    # GET QUESTIONS
    # ==================================================

    question_list = questions[career][difficulty]

    # ==================================================
    # SESSION STATE
    # ==================================================

    if "interview_data" not in st.session_state:
        st.session_state.interview_data = {}

    interview_id = f"{career}_{difficulty}"

    if interview_id not in st.session_state.interview_data:

        st.session_state.interview_data[interview_id] = {
            "answers": {},
            "results": {},
            "finished": False,
            "total_score": 0,
            "max_score": 0,
            "percentage": 0
        }

    interview_data = st.session_state.interview_data[
        interview_id
    ]

    # ==================================================
    # QUESTIONS
    # ==================================================

    for i, q in enumerate(question_list):

        st.write(
            f"### Question {i + 1}"
        )

        st.write(
            q["question"]
        )

        answer_key = (
            f"{interview_id}_answer_{i}"
        )

        # ==================================================
        # SAVED ANSWER
        # ==================================================

        saved_answer = interview_data[
            "answers"
        ].get(
            answer_key,
            ""
        )

        answer = st.text_area(
            "Your Answer",
            value=saved_answer,
            key=answer_key,
            disabled=interview_data["finished"]
        )

        # Save answer

        interview_data["answers"][answer_key] = answer

        # ==================================================
        # CHECK ANSWER
        # ==================================================

        if not interview_data["finished"]:

            if st.button(
                f"Check Answer {i + 1}",
                key=f"check_{interview_id}_{i}"
            ):

                (
                    score,
                    found,
                    missing,
                    feedback,
                    percentage,
                    performance
                ) = evaluate_answer(
                    answer,
                    q["keywords"]
                )

                interview_data["results"][i] = {
                    "score": score,
                    "found": found,
                    "missing": missing,
                    "feedback": feedback,
                    "percentage": percentage,
                    "performance": performance
                }

                st.rerun()

        # ==================================================
        # SHOW SAVED RESULT
        # ==================================================

        if i in interview_data["results"]:

            result = interview_data[
                "results"
            ][i]

            st.success(
                f"🎯 Score: "
                f"{result['score']}/"
                f"{len(q['keywords']) * 2}"
            )

            st.write(
                f"📊 Performance: "
                f"**{result['performance']}**"
            )

            # ==================================================
            # FOUND KEYWORDS
            # ==================================================

            st.write(
                "✅ Keywords Found:"
            )

            if result["found"]:

                for word in result["found"]:

                    st.write(
                        f"✔ {word}"
                    )

            else:

                st.write(
                    "No keywords found."
                )

            # ==================================================
            # MISSING KEYWORDS
            # ==================================================

            st.write(
                "❌ Missing Keywords:"
            )

            if result["missing"]:

                for word in result["missing"]:

                    st.write(
                        f"✖ {word}"
                    )

            else:

                st.write(
                    "None"
                )

            # ==================================================
            # AI FEEDBACK
            # ==================================================

            st.write(
                "🤖 AI Feedback:"
            )

            st.info(
                result["feedback"]
            )

        st.divider()

    # ==================================================
    # FINISH INTERVIEW
    # ==================================================

    if not interview_data["finished"]:

        if st.button(
            "🏁 Finish Interview",
            key=f"finish_{interview_id}"
        ):

            total_score = 0
            max_score = 0

            # Evaluate every question

            for i, q in enumerate(question_list):

                answer_key = (
                    f"{interview_id}_answer_{i}"
                )

                answer = interview_data[
                    "answers"
                ].get(
                    answer_key,
                    ""
                )

                (
                    score,
                    found,
                    missing,
                    feedback,
                    percentage,
                    performance
                ) = evaluate_answer(
                    answer,
                    q["keywords"]
                )

                total_score += score

                max_score += (
                    len(q["keywords"]) * 2
                )

                interview_data[
                    "results"
                ][i] = {
                    "score": score,
                    "found": found,
                    "missing": missing,
                    "feedback": feedback,
                    "percentage": percentage,
                    "performance": performance
                }

            # ==================================================
            # FINAL PERCENTAGE
            # ==================================================

            final_percentage = (
                total_score / max_score
            ) * 100 if max_score > 0 else 0

            interview_data[
                "total_score"
            ] = total_score

            interview_data[
                "max_score"
            ] = max_score

            interview_data[
                "percentage"
            ] = final_percentage

            interview_data[
                "finished"
            ] = True

            st.rerun()

    # ==================================================
    # FINAL RESULT
    # ==================================================

    if interview_data["finished"]:

        st.header(
            "🏆 Interview Completed!"
        )

        total_score = interview_data[
            "total_score"
        ]

        max_score = interview_data[
            "max_score"
        ]

        percentage = interview_data[
            "percentage"
        ]

        st.markdown("---")

        st.header(
            "🏆 Interview Result"
        )

        st.success(
            f"🎯 Final Score: "
            f"{total_score}/{max_score}"
        )

        st.write(
            f"📊 Percentage: "
            f"**{percentage:.1f}%**"
        )

        # ==================================================
        # PERFORMANCE
        # ==================================================

        if percentage >= 80:

            st.success(
                "🏆 Excellent! "
                "You are interview ready."
            )

            performance_message = (
                "Excellent performance! Keep practicing "
                "advanced questions and real-world examples."
            )

        elif percentage >= 60:

            st.info(
                "👍 Good performance. "
                "Keep practicing."
            )

            performance_message = (
                "Good performance! Review the missing "
                "concepts and practice more examples."
            )

        else:

            st.warning(
                "📚 Needs more practice. "
                "Revise the topics and try again."
            )

            performance_message = (
                "Focus on the basic concepts and practice "
                "answering interview questions regularly."
            )

        # ==================================================
        # PERFORMANCE ANALYSIS
        # ==================================================

        st.markdown("---")

        st.header(
            "📈 Performance Analysis"
        )

        all_found = []
        all_missing = []

        for result in interview_data[
            "results"
        ].values():

            all_found.extend(
                result["found"]
            )

            all_missing.extend(
                result["missing"]
            )

        # Remove duplicates

        all_found = list(
            dict.fromkeys(all_found)
        )

        all_missing = list(
            dict.fromkeys(all_missing)
        )

        # ==================================================
        # STRONG AREAS
        # ==================================================

        st.subheader(
            "✅ Strong Areas"
        )

        if all_found:

            for keyword in all_found:

                st.write(
                    f"✔ {keyword}"
                )

        else:

            st.info(
                "No strong areas detected yet."
            )

        # ==================================================
        # AREAS TO IMPROVE
        # ==================================================

        st.subheader(
            "📚 Areas to Improve"
        )

        if all_missing:

            for keyword in all_missing:

                st.write(
                    f"❌ {keyword}"
                )

        else:

            st.success(
                "🎉 Excellent! No major missing "
                "concepts detected."
            )

        # ==================================================
        # GENERAL RECOMMENDATION
        # ==================================================

        st.subheader(
            "💡 Recommendation"
        )

        st.info(
            performance_message
        )

        # ==================================================
        # PERSONALIZED LEARNING PLAN
        # ==================================================

        st.subheader(
            "🎓 Personalized Learning Plan"
        )

        if all_missing:

            st.write(
                "Based on your interview performance, "
                "focus on these topics:"
            )

            for keyword in all_missing:

                st.write(
                    f"📚 **Study:** {keyword}"
                )

            st.markdown("---")

            st.write(
                "💡 **Study Tip:** Review each topic, "
                "understand the basic concept, and "
                "practice answering interview questions "
                "about it."
            )

        else:

            st.success(
                "🎉 You covered all the important concepts!"
            )

            st.write(
                "Keep practicing with advanced questions "
                "and real-world examples."
            )

        # ==================================================
        # QUESTION REVIEW
        # ==================================================

        st.markdown("---")

        st.header(
            "📝 Interview Answer Review"
        )

        for i, q in enumerate(question_list):

            result = interview_data[
                "results"
            ].get(i)

            if result:

                st.write(
                    f"### Question {i + 1}"
                )

                # ---------------- PERFORMANCE ----------------

                if result["score"] == (
                    len(q["keywords"]) * 2
                ):

                    st.success(
                        "✅ Excellent answer"
                    )

                elif result["score"] > 0:

                    st.warning(
                        "⚠️ Partially correct"
                    )

                else:

                    st.error(
                        "❌ Needs improvement"
                    )

                # ---------------- SCORE ----------------

                st.write(
                    f"Score: **"
                    f"{result['score']}/"
                    f"{len(q['keywords']) * 2}**"
                )

                # ---------------- PERFORMANCE ----------------

                st.write(
                    f"📊 Performance: "
                    f"**{result['performance']}**"
                )

                # ---------------- FEEDBACK ----------------

                st.write(
                    "🤖 Feedback:"
                )

                st.info(
                    result["feedback"]
                )

                # ---------------- FOUND ----------------

                if result["found"]:

                    st.write(
                        "✅ Concepts covered:"
                    )

                    for word in result["found"]:

                        st.write(
                            f"✔ {word}"
                        )

                # ---------------- MISSING ----------------

                if result["missing"]:

                    st.write(
                        "📚 Revise:"
                    )

                    for word in result["missing"]:

                        st.write(
                            f"❌ {word}"
                        )

                st.divider()

        # ==================================================
        # PDF REPORT
        # ==================================================

        try:

            filename = create_report(
                st.session_state.username,
                career,
                difficulty,
                total_score,
                max_score,
                percentage
            )

            with open(
                filename,
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="📄 Download Interview Report",
                    data=pdf_file,
                    file_name=filename,
                    mime="application/pdf",
                    key=f"report_{interview_id}"
                )

        except Exception as e:

            st.warning(
                f"Report could not be generated: {e}"
            )

        # ==================================================
        # RETAKE INTERVIEW
        # ==================================================

        st.markdown("---")

        if st.button(
            "🔄 Retake Interview",
            key=f"retake_{interview_id}"
        ):

            del st.session_state.interview_data[
                interview_id
            ]

            st.rerun()
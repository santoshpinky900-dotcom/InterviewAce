def evaluate_answer(answer, keywords):

    # ==================================================
    # INITIALIZE
    # ==================================================

    score = 0
    found = []
    missing = []

    # Make sure answer is text
    if answer is None:
        answer = ""

    answer = str(answer).lower().strip()

    # ==================================================
    # CHECK KEYWORDS
    # ==================================================

    for keyword in keywords:

        keyword_lower = keyword.lower().strip()

        if keyword_lower in answer:

            score += 2
            found.append(keyword)

        else:

            missing.append(keyword)

    # ==================================================
    # SCORE CALCULATION
    # ==================================================

    max_score = len(keywords) * 2

    if max_score > 0:

        percentage = (
            score / max_score
        ) * 100

    else:

        percentage = 0

    # ==================================================
    # PERFORMANCE LEVEL
    # ==================================================

    if percentage == 100:

        performance = "Excellent"

        feedback = (
            "Excellent answer! 🎉 "
            "You covered all the important concepts. "
            "Your answer demonstrates strong understanding "
            "of the topic."
        )

    elif percentage >= 75:

        performance = "Very Good"

        feedback = (
            "Very good answer! 👍 "
            "You covered most of the important concepts. "
            "Your answer shows good technical understanding. "
            "Try adding a practical example to make it even stronger."
        )

    elif percentage >= 50:

        performance = "Good"

        feedback = (
            "Good attempt! 🙂 "
            "You covered some important concepts. "
            "However, your answer could be more detailed. "
            "Try explaining the concepts clearly and "
            "include a practical example."
        )

    elif percentage > 0:

        performance = "Needs Improvement"

        feedback = (
            "Your answer needs improvement. 📚 "
            "You mentioned a few relevant concepts, "
            "but several important points are missing. "
            "Review the topic and try to include more "
            "technical details."
        )

    else:

        performance = "Needs Improvement"

        feedback = (
            "Your answer needs significant improvement. 📚 "
            "The expected concepts were not identified "
            "in your answer. Review the topic and try "
            "answering again using relevant concepts "
            "and examples."
        )

    # ==================================================
    # COVERED CONCEPTS
    # ==================================================

    if found:

        feedback += (
            " You successfully covered: "
            + ", ".join(found)
            + "."
        )

    # ==================================================
    # MISSING CONCEPTS
    # ==================================================

    if missing:

        feedback += (
            " Focus especially on: "
            + ", ".join(missing)
            + "."
        )

    else:

        feedback += (
            " You successfully covered all the "
            "expected concepts."
        )

    # ==================================================
    # ANSWER QUALITY CHECK
    # ==================================================

    if len(answer) == 0:

        feedback += (
            " Please provide an answer before "
            "checking your response."
        )

    elif len(answer.split()) < 5:

        feedback += (
            " Try giving a more detailed answer "
            "instead of a very short response."
        )

    elif len(answer.split()) >= 30:

        feedback += (
            " Your answer provides good detail. "
            "Continue using clear explanations and examples."
        )

    # ==================================================
    # RETURN RESULT
    # ==================================================

    return (
        score,
        found,
        missing,
        feedback,
        percentage,
        performance
    )
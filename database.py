import sqlite3


# ==================================================
# DATABASE CONNECTION
# ==================================================

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()


# ==================================================
# USERS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")


# ==================================================
# INTERVIEW RESULTS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS interview_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    career TEXT,
    difficulty TEXT,
    score INTEGER,
    max_score INTEGER,
    percentage REAL
)
""")


# ==================================================
# QUIZ RESULTS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    career TEXT,
    difficulty TEXT,
    score INTEGER,
    total_questions INTEGER,
    percentage REAL
)
""")


conn.commit()


# ==================================================
# REGISTER
# ==================================================

def add_user(username, password):

    cursor.execute(
        """
        INSERT INTO users(username, password)
        VALUES(?, ?)
        """,
        (
            username,
            password
        )
    )

    conn.commit()


# ==================================================
# LOGIN
# ==================================================

def login(username, password):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            password
        )
    )

    return cursor.fetchone()


# ==================================================
# SAVE INTERVIEW RESULT
# ==================================================

def save_interview_result(
    username,
    career,
    difficulty,
    score,
    max_score,
    percentage
):

    cursor.execute(
        """
        INSERT INTO interview_results
        (
            username,
            career,
            difficulty,
            score,
            max_score,
            percentage
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            career,
            difficulty,
            score,
            max_score,
            percentage
        )
    )

    conn.commit()


# ==================================================
# GET INTERVIEW HISTORY
# ==================================================

def get_interview_history(username):

    cursor.execute(
        """
        SELECT
            career,
            difficulty,
            score,
            max_score,
            percentage
        FROM interview_results
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    return cursor.fetchall()


# ==================================================
# SAVE QUIZ RESULT
# ==================================================

def save_quiz_result(
    username,
    career,
    difficulty,
    score,
    total_questions,
    percentage
):

    cursor.execute(
        """
        INSERT INTO quiz_results
        (
            username,
            career,
            difficulty,
            score,
            total_questions,
            percentage
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            career,
            difficulty,
            score,
            total_questions,
            percentage
        )
    )

    conn.commit()


# ==================================================
# GET QUIZ HISTORY
# ==================================================

def get_quiz_history(username):

    cursor.execute(
        """
        SELECT
            career,
            difficulty,
            score,
            total_questions,
            percentage
        FROM quiz_results
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    return cursor.fetchall()


# ==================================================
# GET BEST QUIZ SCORE
# ==================================================

def get_best_quiz_score(username):

    cursor.execute(
        """
        SELECT MAX(percentage)
        FROM quiz_results
        WHERE username=?
        """,
        (username,)
    )

    result = cursor.fetchone()

    if result and result[0] is not None:
        return result[0]

    return 0
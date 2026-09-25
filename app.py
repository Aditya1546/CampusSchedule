import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

schedule = [
    {
        "subject": "Database Management Systems",
        "day": "Monday",
        "start": "10:00",
        "end": "11:00",
        "room": "A101",
    },
    {
        "subject": "Computer Networks",
        "day": "Monday",
        "start": "11:00",
        "end": "12:00",
        "room": "A102",
    },
    {
        "subject": "Design and Analysis of Algorithms",
        "day": "Tuesday",
        "start": "09:00",
        "end": "10:00",
        "room": "B201",
    },
]

def init_db():
    connection = sqlite3.connect("schedule.db")

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            day TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL,
            room TEXT NOT NULL
        )
        """
    )

    count = connection.execute(
        "SELECT COUNT(*) FROM schedule"
    ).fetchone()[0]

    if count == 0:
        for item in schedule:
            connection.execute(
                """
                INSERT INTO schedule (subject, day, start, end, room)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    item["subject"],
                    item["day"],
                    item["start"],
                    item["end"],
                    item["room"],
                ),
            )

    connection.commit()
    connection.close()
    
def get_schedule():
    connection = sqlite3.connect("schedule.db")
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        "SELECT * FROM schedule ORDER BY day, start"
    ).fetchall()

    connection.close()
    return rows
    
    
def has_clash(day, start_time, end_time, room):
    schedule = get_schedule()
    for item in schedule:
        if item["day"] != day or item["room"] != room:
            continue

        existing_start = datetime.strptime(item["start"], "%H:%M")
        existing_end = datetime.strptime(item["end"], "%H:%M")

        if start_time < existing_end and end_time > existing_start:
            return True

    return False

@app.route("/")
def home():
    schedule = get_schedule()
    return render_template("index.html", schedule=schedule)


@app.route("/availability", methods=["GET", "POST"])
def availability():
    result = None

    if request.method == "POST":
        room = request.form.get("room", "").strip()
        day = request.form.get("day", "").strip()
        start = request.form.get("start", "").strip()
        end = request.form.get("end", "").strip()

        if not room or not day or not start or not end:
            result = "All fields are required."
        else:
            try:
                start_time = datetime.strptime(start, "%H:%M")
                end_time = datetime.strptime(end, "%H:%M")
            except ValueError:
                result = "Invalid time format."
            else:
                if start_time >= end_time:
                    result = "Start time must be before end time."
                elif has_clash(day, start_time, end_time, room):
                    result = f"Room {room} is not available."
                else:
                    result = f"Room {room} is available."

    return render_template("availability.html", result=result)


@app.route("/add", methods=["POST"])
def add_schedule():
    subject = request.form.get("subject", "").strip()
    day = request.form.get("day", "").strip()
    start = request.form.get("start", "").strip()
    end = request.form.get("end", "").strip()
    room = request.form.get("room", "").strip()

    if not subject or not day or not start or not end or not room:
        return "All fields are required.", 400
    try:
        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")
    except ValueError:
        return "Invalid time format.", 400

    if start_time >= end_time:
        return "Start time must be before end time.", 400
    
    if has_clash(day, start_time, end_time, room):
        return "Room clash detected.", 409

    connection = sqlite3.connect("schedule.db")

    connection.execute(
        """
        INSERT INTO schedule (subject, day, start, end, room)
        VALUES (?, ?, ?, ?, ?)
        """,
        (subject, day, start, end, room),
    )

    connection.commit()
    connection.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

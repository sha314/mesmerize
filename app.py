from flask import Flask, request, render_template, redirect, url_for
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
DB_FILE = "mesmerize.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db()
    total_entries = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    total_fields = conn.execute("SELECT COUNT(*) FROM fields").fetchone()[0]
    conn.close()
    return render_template("home.html", total_entries=total_entries, total_fields=total_fields)
    # return render_template("home.html", total_entries=total_entries)



@app.route("/add", methods=["GET", "POST"])
def add_entry():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["field_name"]
        language = request.form["language"]
        text_value = request.form["text_value"]

        # file uploads
        audio_path, image_path, video_path = None, None, None
        uploads = {
            "audio": "audio_path",
            "image": "image_path",
            "video": "video_path",
        }

        for field, dest in uploads.items():
            file = request.files.get(field)
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                if dest == "audio_path":
                    audio_path = filepath
                elif dest == "image_path":
                    image_path = filepath
                elif dest == "video_path":
                    video_path = filepath

        cur.execute(
            """INSERT INTO entries 
               (name, language, text_value, audio_path, image_path, video_path)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, language, text_value, audio_path, image_path, video_path)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    # 👇 fetch languages for dropdown
    languages = cur.execute("SELECT code, name FROM languages").fetchall()
    conn.close()
    return render_template("add.html", languages=languages)



# @app.route("/add", methods=["GET", "POST"])
# def add_entry():
#     if request.method == "POST":
#         name = request.form["field_name"]
#         language = request.form["language"]
#         text_value = request.form["text_value"]

#         # file uploads
#         audio_path = None
#         image_path = None
#         video_path = None

#         for field, dest in [("audio_file", "audio_path"),
#                             ("image_file", "image_path"),
#                             ("video_file", "video_path")]:
#             file = request.files.get(field)
#             if file and file.filename:
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#                 file.save(filepath)
#                 locals()[dest] = filepath  # store in correct variable

#         conn = get_db()
#         cur = conn.cursor()
#         cur.execute(
#             """INSERT INTO entries 
#                (name, language, text_value, audio_path, image_path, video_path)
#                VALUES (?, ?, ?, ?, ?, ?)""",
#             (name, language, text_value, audio_path, image_path, video_path)
#         )
#         conn.commit()
#         conn.close()
#         return redirect(url_for("home"))

#     return render_template("add.html")


@app.route("/languages", methods=["GET", "POST"])
def manage_languages():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        code = request.form["code"]
        name = request.form["name"]
        cur.execute("INSERT OR IGNORE INTO languages (code, name) VALUES (?, ?)", (code, name))
        conn.commit()

    langs = cur.execute("SELECT * FROM languages").fetchall()
    conn.close()
    return render_template("languages.html", langs=langs)




@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = []
    if query:
        conn = get_db()
        results = conn.execute(
            "SELECT * FROM fields WHERE value LIKE ? OR name LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        conn.close()
    return render_template("search.html", results=results, query=query)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)



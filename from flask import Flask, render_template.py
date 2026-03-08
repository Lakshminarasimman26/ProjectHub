from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return render_template("index.html", projects=projects)

@app.route("/create", methods=["GET","POST"])
def create_project():
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        conn = get_db()
        conn.execute(
            "INSERT INTO projects (name,description) VALUES (?,?)",
            (name,description)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("create_project.html")

@app.route("/project/<int:id>")
def project(id):
    
    conn = get_db()

    project = conn.execute(
        "SELECT * FROM projects WHERE id=?",
        (id,)
    ).fetchone()

    tasks = conn.execute(
        "SELECT * FROM tasks WHERE project_id=?",
        (id,)
    ).fetchall()

    conn.close()

    return render_template("project.html", project=project, tasks=tasks)


@app.route("/add_task/<int:project_id>", methods=["POST"])
def add_task(project_id):

    title = request.form["title"]

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title,project_id) VALUES (?,?)",
        (title,project_id)
    )

    conn.commit()
    conn.close()

    return redirect(f"/project/{project_id}")


if __name__ == "__main__":
    app.run(debug=True)
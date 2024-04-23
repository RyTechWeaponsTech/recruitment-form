from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# URI stands for Uniform Resource Indetifier
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.sqlite3"
app.config["SECRET_KEY"] = "ABC987"
db = SQLAlchemy(app)


# create a table
class students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Age = db.Column(db.Integer)
    dob = db.Column(db.String(100))
    Gender = db.Column(db.String(10))

    def __init__(self, name, age, birthday, gender):
        self.Name = name
        self.Age = age
        self.Birthday = birthday
        self.Gender = gender



@app.route("/", methods=["GET", "POST"])
def add_recruit():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        birthday = request.form["birthday"]
        gender = request.form["gender"]
        recruit = students(name, age, birthday, gender)
        db.session.add(recruit)
        db.session.commit()
        return redirect(url_for("successfully"))
    return render_template("add_recruit.html")

@app.route("/successfully")
def successfully():
    return render_template("successfully.html")


@app.route("/show_detail")
def show_detail():
    # fetch all recruits records from the db
    all_recruits = students.query.all()
    return render_template("show_detail.html", students=all_recruits)


@app.route("/clear_database", methods=["GET", "POST"])
def clear_database():
    if request.method == "POST":
        # Deletes all data
        db.session.query(students).delete()
        db.session.commit()

        # redirect to the show details
        return redirect(url_for("successfully"))
    # render a template for confirmation
    return render_template("clear_database.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port="8081")

import flask
from faker import Faker
import csv
import statistics
import requests

app = flask.Flask(__name__)

fake = Faker()
filename_1 = "requirements.txt"
filename_2 = "hw.csv"
url = "http://api.open-notify.org/astros.json"

@app.route("/")
def index():
    return "Hello from first page!"


@app.route("/requirements")
def open_req():
    with open(filename_1, "r") as file:
        lines = file.readlines()
    return flask.render_template("requirements.html", lines=lines)


@app.route("/users/generate")
def generate_100():
    count = int(flask.request.args.get('count', default=100, type=int))
    users = []
    for _ in range(count):
        user = {
            "Name": fake.name(),
            "Email": fake.email(),
        }
        users.append(user)
    return flask.render_template("generate.html", users=users)


@app.route("/mean/")
def mean():
    with open(filename_2) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        height_list = []
        weight_list = []
        for row in csv_reader:
            if len(row) >= 3:
                height_list.append(float(row[1]))
                weight_list.append(float(row[2]))
        avg_height = str(round(statistics.mean(height_list), 5))
        avg_weight = str(round(statistics.mean(weight_list), 4))
        return flask.render_template("mean.html", avg_height=avg_height, avg_weight=avg_weight)
        # Если не нужно было делать отдельный html, тогда просто
        # return f"AVG HEIGHT: {avg_height}<br> AVG WEIGHT: {avg_weight}"


@app.route("/space")
def space():
    response = requests.get(url)
    data = response.json()
    count_astronauts = str(len(data["people"]))
    return flask.render_template("space.html", count_astronauts=count_astronauts)







if __name__ == "__main__":
    app.run(debug=True)


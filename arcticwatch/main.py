from flask import Flask, request, render_template, redirect, send_file, send_from_directory, abort, flash, session, \
    url_for, Markup
import os
app = Flask(__name__)
GRAPHS_FOLDER = os.path.join('static', 'graphs')
app.config['GRAPHS_FOLDER'] = GRAPHS_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map/")
def world():
    return render_template("map.html")


@app.route("/learn/")
def learn():
    return render_template("learn/index.html")


@app.route("/view/<station>/<gas>/")
def gas(station, gas):
    return render_template("gas.html", name=station + "/large/" + gas)


@app.route('/learn/<section>/', defaults={'page': False})
@app.route('/learn/<section>/<page>')
def learn2(section, page):
    if not page:
        page = "index"

    return render_template("learn/{0}/{1}.html".format(section, page))


if __name__ == "__main__":
    app.run()

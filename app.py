from flask import Flask, request, jsonify
from rss import (
    retrieveRSS,
    getRSSList,
    deleteFromRSSList,
    addToRSSList,
    updateRSSItem,
    getRSSById,
)
import sqlite3

## Run with flask run


def checkTable():
    with sqlite3.connect("my-db.db") as con:
        cursor = con.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master")
        if len(tables.fetchall()) == 0:
            cursor.execute(
                "CREATE TABLE rss(id INTEGER PRIMARY KEY, url text, title text, description text)"
            )


checkTable()
app = Flask(__name__)


@app.route("/")
def server_status():
    return "<p>Server is online</p>"


@app.route("/rss", methods=["GET", "POST", "PATCH", "DELETE"])
def rss():
    if request.method == "GET":  # done
        if "id" in request.args:
            rss_id = request.args["id"]
            result = getRSSById(rss_id)
            return jsonify(result)
        result = getRSSList()
        return jsonify(result)

    if request.method == "POST":
        params = request.get_json()
        if "rss-url" not in params:
            return (
                jsonify(
                    "rss-url missing",
                ),
                400,
            )
        if "title" not in params:
            return (
                jsonify(
                    "title missing",
                ),
                400,
            )
        if "description" not in params:
            return (
                jsonify(
                    "description missing",
                ),
                400,
            )
        result = addToRSSList(
            rss_url=params["rss-url"],
            title=params["title"],
            description=params["description"],
        )
        return jsonify(result), 200
    if request.method == "PATCH":
        params = request.get_json()
        if "id" not in params:
            return (
                jsonify(
                    "id missing",
                ),
                400,
            )
        if "rss-url" not in params:
            return (
                jsonify(
                    "rss-url missing",
                ),
                400,
            )
        if "title" not in params:
            return (
                jsonify(
                    "title missing",
                ),
                400,
            )
        if "description" not in params:
            return (
                jsonify(
                    "description missing",
                ),
                400,
            )
        result = updateRSSItem(
            id=params["id"],
            rss_url=params["rss-url"],
            title=params["title"],
            description=params["description"],
        )
        return jsonify(result), 200

    if request.method == "DELETE":
        if "id" not in request.args:
            return (
                jsonify(
                    "id missing",
                ),
                400,
            )
        result = deleteFromRSSList(rss_id=request.args["id"])
        return jsonify(result)


@app.route("/get-rss", methods=["GET"])
def get_rss():
    if request.method == "GET":
        if "rss-url" not in request.args:
            return (
                jsonify(
                    "rss-url missing",
                ),
                400,
            )
        rss_url = request.args["rss-url"]
        result = retrieveRSS(rss_url)
        return jsonify(result)

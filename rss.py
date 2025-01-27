import feedparser
from flask import Flask, jsonify
import sqlite3
import pandas as pd
import json

app = Flask(__name__)


def query_db(query, args=(), one=False):
    with sqlite3.connect("my-db.db") as con:
        con.row_factory = sqlite3.Row  # This allows access by column name
        cur = con.cursor()
        res = pd.read_sql_query(sql=query, con=con, params=args)
        res = res.to_json(orient="records", indent=4, lines=False)
        res = json.loads(res)
        return (res[0] if res else None) if one else res


def execute_db(query, args=()):
    with sqlite3.connect("my-db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            cur.execute(query, args)
            con.commit()  # Commit the transaction
            row_count = cur.rowcount  # Get the number of rows affected
        except sqlite3.Error as e:
            con.rollback()  # Rollback if an error occurs
            return {"success": False, "error": str(e)}
    return {"success": True, "rows_affected": row_count}


def retrieveRSS(url: str):
    result = feedparser.parse(url)
    return result


def getRSSList():
    query = "SELECT * FROM rss"
    results = query_db(query)
    data = [dict(row) for row in results]
    return data


def getRSSById(id):
    query = "SELECT * FROM rss WHERE id=(?)"
    args = [str(id)]
    results = query_db(query, args, True)
    return results


def deleteFromRSSList(rss_id):
    query = "DELETE FROM rss WHERE id = (?)"
    args = [str(rss_id)]
    result = execute_db(query, args)
    return result


def updateRSSItem(rss_url, title, description, id):
    query = "UPDATE rss SET url = (?), title = (?), description = (?) WHERE id = (?)"
    args = [str(rss_url), str(title), str(description), str(id)]
    result = execute_db(query, args)
    return result


def addToRSSList(rss_url, title, description):
    query = "INSERT INTO rss (url, title, description) VALUES ((?), (?), (?))"
    args = [str(rss_url), str(title), str(description)]
    result = execute_db(query, args)
    return result

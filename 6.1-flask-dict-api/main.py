from flask import Flask, abort, jsonify, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("data/dictionary.csv")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/<word>")
def get_meaning(word):
    df_filtered = df[df["word"] == word]
    if len(df_filtered) > 0:
        meaning = df_filtered.iloc[0, 1]
        return {
            "word": word,
            "meaning": meaning,
        }
    else:
        abort(404, description="Invalid word.")


@app.errorhandler(404)
def handle_not_found(e):
    return jsonify(error=str(e)), 404

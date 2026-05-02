from ast import parse
import os

from flask import Flask, abort, jsonify, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    df = pd.read_csv("data/data_small/stations.txt", skiprows=17)
    df_target = df[["STAID", "STANAME                                 "]].to_html(
        index=False
    )
    return render_template("home.html", list_table=df_target)


@app.route("/<station>/<date>")
def get_day(station, date):
    file_name = f"data/data_small/TG_STAID{station.zfill(6)}.txt"
    if os.path.exists(file_name):
        df = pd.read_csv(
            file_name,
            skiprows=20,
            parse_dates=["    DATE"],
            date_format="%Y%m%d",
        )
        df_filtered = df[df[" Q_TG"] == 0]
        results = df_filtered[df_filtered["    DATE"] == date]
        if len(results) > 0:
            temp = results.iloc[0, 3].item()
        else:
            abort(404, description="Invalid date.")

        return {
            "station": int(station),
            "date": date,
            "temperature": temp,
        }
    else:
        abort(404, description="Invalid station.")


@app.route("/<station>")
def get_station(station):
    file_name = f"data/data_small/TG_STAID{station.zfill(6)}.txt"
    if os.path.exists(file_name):
        df = pd.read_csv(
            file_name,
            skiprows=20,
            parse_dates=["    DATE"],
            date_format="%Y%m%d",
        )
        df_filtered = df[df[" Q_TG"] == 0]
        results = df_filtered.to_dict(orient="records")

        return {
            "station": int(station),
            "results": results,
        }
    else:
        abort(404, description="Invalid station.")


@app.route("/year/<station>/<year>")
def get_year(station, year):
    file_name = f"data/data_small/TG_STAID{station.zfill(6)}.txt"
    if os.path.exists(file_name):
        df = pd.read_csv(
            file_name,
            skiprows=20,
            parse_dates=["    DATE"],
            date_format="%Y%m%d",
        )
        df_filtered = df[df[" Q_TG"] == 0]
        df_filtered_year = df_filtered[df_filtered["    DATE"].dt.year == int(year)]

        if len(df_filtered_year) > 0:
            results = df_filtered_year.to_dict(orient="records")
        else:
            abort(404, description="Invalid date.")

        return {
            "station": int(station),
            "year": int(year),
            "results": results,
        }
    else:
        abort(404, description="Invalid station.")


@app.errorhandler(404)
def handle_not_found(e):
    return jsonify(error=str(e)), 404

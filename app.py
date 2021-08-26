import requests
import json
from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd


PROJECT_RELEASES_LINK = "https://api.github.com/repos/komodoplatform/atomicdex-desktop/releases"


def downloads_counter():
    releases_info = json.loads(requests.get
                               (PROJECT_RELEASES_LINK).text)
    releases_downloads_info = {
        "releases": [],
        "published_at": [],
        "downloads": []
    }
    for release in releases_info:
        for asset in release["assets"]:
            releases_downloads_info["published_at"].append(release["published_at"])
            releases_downloads_info["downloads"].append(asset["download_count"])
            releases_downloads_info["releases"].append(asset["name"])
    return releases_downloads_info


app = Flask(__name__)


@app.route('/', methods=["GET"])
def html_table():
    df = pd.DataFrame(downloads_counter())
    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


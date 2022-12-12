from flask import Flask
import concurrent.futures
import requests

app = Flask(__name__)


URLS = [
    "https://takehome.io/twitter",
    "https://takehome.io/facebook",
    "https://takehome.io/instagram",
]


def load_url(url):
    with requests.get(url) as resp:
        json = resp.json()
        count = 0
        data = {}
        for k, _ in json:
            if k == "name" or "username":
                count += 1
        data[url] = count
        return data


@app.route("/")
def social_network_activity():
    data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(load_url, url): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:

                data.append(future.result())
            except Exception as exc:
                print("%r generated an exception: %s" % (url, exc))

    return data

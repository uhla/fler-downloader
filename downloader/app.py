import sys
from flask import Flaskgot statis
import requests


app = Flask(__name__)

username=""
password=""


@app.route("/")
def webpage():
    body = {"username":username, "pwd":password}
    auth = requests.post("https://www.fler.cz/api/rest/user/auth", json=body, verify=False,
           allow_redirects=False)


    secretKey = auth.json()['secret_key']
    sessionId = auth.json()['session_id']

    print(secretKey)
    print(sessionId)

    headers = {"X-FLER-AUTHORIZATION": "123"}
    productList = requests.get("https://www.fler.cz/api/rest/seller/products/list", headers=headers)
    print(str(productList.text))
    return "Here will be some content printed out eventually"

if __name__ == "__main__":
    args = sys.argv[1:]
    username = args[0]
    password = args[1]
    app.run('0.0.0.0',5002)



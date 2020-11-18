import base64
import hashlib
import sys
from datetime import timezone, datetime

from flask import Flask
import requests
import hmac


app = Flask(__name__)

username=""
password=""


@app.route("/")
def webpage():
    body = {"username":username, "pwd":password}
    auth = requests.post("https://www.fler.cz/api/rest/user/auth", json=body, verify=False,
           allow_redirects=False)

    secret_key = auth.json()['secret_key']
    session_id = auth.json()['session_id']

    timestamp = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
    request_path = "/api/rest/seller/products/list"
    request_string = "GET\n" + timestamp +"\n" + request_path
    signature=hmac.new(secret_key.encode(), request_string.encode(), hashlib.sha1).hexdigest()
    auth_string = "API1_SESS"+" "+session_id+ " "+timestamp+" "+ base64.b64encode(signature.encode()).decode()


    headers = {"X-FLER-AUTHORIZATION": auth_string}
    product_list = requests.get("https://www.fler.cz"+request_path+"?fields=title", headers=headers)
    print(str(product_list.text))
    return "Here will be some content printed out eventually"

if __name__ == "__main__":
    args = sys.argv[1:]
    username = args[0]
    password = args[1]
    webpage()
    # app.run('0.0.0.0',5002)



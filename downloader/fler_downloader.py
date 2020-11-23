import base64
import hashlib
import hmac
from datetime import datetime, timezone

import requests


class Downloader:

    def __init__(self, username, password):
        body = {"username": username, "pwd": password}
        auth = requests.post("https://www.fler.cz/api/rest/user/auth", json=body, verify=False,
                             allow_redirects=False)

        if 'secret_key' not in auth.json():
            print("Invalid login credentials.")
            exit()

        self.secret_key = auth.json()['secret_key']
        self.session_id = auth.json()['session_id']

    def get_product_list(self):
        request_path = "/api/rest/seller/products/list"
        auth_string = self.calculate_auth_string(request_path)
        headers = {"X-FLER-AUTHORIZATION": auth_string}
        image_size = 'm'  # options are m,s,b (medium, small, big)
        limit = 25
        url_args = "?fields=title,description,keywords_tag,photo_main,colors,keywords_mat,description_short,price&photo_main=" + image_size + "&limit=" + str(
            limit)

        product_list_page = self.api_get(headers, request_path, url_args)
        product_list = product_list_page.json()
        page_number = 1

        while len(product_list_page.json()) == limit:
            offset = page_number * limit
            product_list_page = self.api_get(headers, request_path, url_args + "&offset=" + str(offset))
            product_list = product_list + product_list_page.json()
            page_number = page_number + 1

        return image_size, product_list

    def get_colors(self):
        request_path = "/api/rest/shop/datalist/product/colors"
        auth_string = self.calculate_auth_string(request_path)
        headers = {"X-FLER-AUTHORIZATION": auth_string}

        color_list_response = self.api_get(headers, request_path)
        return {item['id']: item['title'] for (item) in color_list_response.json()}

    def api_get(self, headers, request_path, url_args=""):
        return requests.get("https://www.fler.cz" + request_path + url_args, headers=headers)

    def calculate_auth_string(self, request_path):
        timestamp = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
        request_string = "GET\n" + timestamp + "\n" + request_path
        signature = hmac.new(self.secret_key.encode(), request_string.encode(), hashlib.sha1).hexdigest()
        auth_string = "API1_SESS" + " " + self.session_id + " " + timestamp + " " + base64.b64encode(
            signature.encode()).decode()
        return auth_string

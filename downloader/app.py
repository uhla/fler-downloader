import base64
import hashlib
import hmac
import sys
from datetime import timezone, datetime

import requests

from downloader.docx_exporter import DocxExporter
from downloader.excel_item_reader import ExcelItemReader
from downloader.excel_item_writer import ExcelItemWriter

username = ""
password = ""


def download_and_export():
    body = {"username": username, "pwd": password}
    auth = requests.post("https://www.fler.cz/api/rest/user/auth", json=body, verify=False,
                         allow_redirects=False)

    if 'secret_key' not in auth.json():
        print("Invalid login credentials.")
        exit()

    secret_key = auth.json()['secret_key']
    session_id = auth.json()['session_id']

    custom_configurations = ExcelItemReader().read_configuration("configuration.xlsx")
    image_size, product_list_response = get_product_list(secret_key, session_id)
    colors = get_colors(secret_key, session_id)

    exporter = DocxExporter()
    exporter.set_colors_list(colors)
    exporter.set_custom_configurations(custom_configurations)
    missing_custom_data = exporter.export_docx(product_list_response, image_size)

    ExcelItemWriter().write_item_configurations("configuration.xlsx", missing_custom_data)
    return "Here will be some content printed out eventually"


def get_product_list(secret_key, session_id):
    request_path = "/api/rest/seller/products/list"
    auth_string = calculate_auth_string(request_path, secret_key, session_id)
    headers = {"X-FLER-AUTHORIZATION": auth_string}
    image_size = 'm'  # options are m,s,b (medium, small, big)
    url_args = "?fields=title,description,keywords_tag,photo_main,colors,keywords_mat&photo_main=" + image_size
    # styl ??? attr2...
    product_list_response = api_get(headers, request_path, url_args)
    return image_size, product_list_response


def get_colors(secret_key, session_id):
    request_path = "/api/rest/shop/datalist/product/colors"
    auth_string = calculate_auth_string(request_path, secret_key, session_id)
    headers = {"X-FLER-AUTHORIZATION": auth_string}

    color_list_response = api_get(headers, request_path)
    return {item['id']: item['title'] for (item) in color_list_response.json()}


def api_get(headers, request_path, url_args=""):
    return requests.get("https://www.fler.cz" + request_path + url_args, headers=headers)


def calculate_auth_string(request_path, secret_key, session_id):
    timestamp = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
    request_string = "GET\n" + timestamp + "\n" + request_path
    signature = hmac.new(secret_key.encode(), request_string.encode(), hashlib.sha1).hexdigest()
    auth_string = "API1_SESS" + " " + session_id + " " + timestamp + " " + base64.b64encode(signature.encode()).decode()
    return auth_string


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print("Invalid input arguments")
        print("Required format: app.py/exe <username> <password>")
        exit()
    username = args[0]
    password = args[1]
    download_and_export()

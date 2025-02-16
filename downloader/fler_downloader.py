import base64
import hashlib
import hmac
from datetime import datetime, timezone

import requests

from downloader.docx_exporter import DocxExporter

from downloader.excel_item_reader import ExcelItemReader
from downloader.excel_item_writer import ExcelItemWriter
from downloader.image_utils import ImageUtils
class Downloader:

    def __init__(self, username, password, stop_event):
        body = {"username": username, "pwd": password}
        auth = requests.post("https://www.fler.cz/api/rest/user/auth", json=body, verify=False,
                             allow_redirects=False)

        if 'secret_key' not in auth.json():
            raise Exception("Invalid login credentials.")

        self.stop_event = stop_event
        self.secret_key = auth.json()['secret_key']
        self.session_id = auth.json()['session_id']

    def download_and_export(self):
        ImageUtils.create_img_tmp_folder()
        try:
            customized_catalog_items = ExcelItemReader().read_configuration("configuration.xlsx")

            image_size, product_list = self.get_product_list()
            colors = self.get_colors()
            colors[0] = "Vícebarevné" # base API doesn't return multi-color as 0
            exporter = DocxExporter(self.stop_event)
            exporter.set_colors_list(colors)
            exporter.set_custom_configurations(customized_catalog_items)
            customized_catalog_items = exporter.export_docx(product_list, image_size)

            ExcelItemWriter().write_item_configurations("configuration.xlsx", customized_catalog_items)
        except InterruptedError as e:
            print(str(e))

        ImageUtils.remove_img_tmp_folder()

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

        while len(product_list_page.json()) == limit and not self.stop_event.is_set():
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
        if self.stop_event.is_set():
            raise InterruptedError("Download interrupted.")
        return requests.get("https://www.fler.cz" + request_path + url_args, headers=headers)

    def calculate_auth_string(self, request_path):
        timestamp = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
        request_string = "GET\n" + timestamp + "\n" + request_path
        signature = hmac.new(self.secret_key.encode(), request_string.encode(), hashlib.sha1).hexdigest()
        auth_string = "API1_SESS" + " " + self.session_id + " " + timestamp + " " + base64.b64encode(
            signature.encode()).decode()
        return auth_string

import sys
from sys import exit

from downloader.docx_exporter import DocxExporter
from downloader.fler_downloader import Downloader
from downloader.excel_item_reader import ExcelItemReader
from downloader.excel_item_writer import ExcelItemWriter
from downloader.image_utils import ImageUtils

username = ""
password = ""


def download_and_export():
    downloader = Downloader(username, password)

    ImageUtils.create_img_tmp_folder()

    customized_catalog_items = ExcelItemReader().read_configuration("configuration.xlsx")

    image_size, product_list = downloader.get_product_list()
    colors = downloader.get_colors()

    exporter = DocxExporter()
    exporter.set_colors_list(colors)
    exporter.set_custom_configurations(customized_catalog_items)
    customized_catalog_items = exporter.export_docx(product_list, image_size)

    ExcelItemWriter().write_item_configurations("configuration.xlsx", customized_catalog_items)

    ImageUtils.remove_img_tmp_folder()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print("Invalid input arguments")
        print("Required format: app.py|downloader.exe <username> <password>")
        exit()
    username = args[0]
    password = args[1]
    download_and_export()

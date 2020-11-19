import io
import re

import requests
from docx import Document
from docx.shared import Cm

from downloader.catalog_item_configuration import CatalogItemConfiguration


class DocxExporter:

    def export_docx(self, product_list_response, image_size):
        cleanr = re.compile('<.*?>')
        missing_custom_data = {}
        document = Document()
        grouped_by_title = {}
        for product in product_list_response.json():
            if product['title'] in grouped_by_title:
                grouped_by_title.get(product['title']).append(product)
            else:
                grouped_by_title[product['title']] = [product]

        for product_title in grouped_by_title:
            document.add_heading(product_title, level=1)

            paragraph = document.add_paragraph()
            description = re.sub(cleanr, '', grouped_by_title[product_title][0]['description'])
            paragraph.add_run(description)

            document.add_paragraph().add_run("Varianty").bold = True

            for product in grouped_by_title[product_title]:
                table = document.add_table(cols=2, rows=1)
                image_url = product['photo_main'][image_size]
                image_response = requests.get(image_url, stream=True)
                image = io.BytesIO(image_response.content)
                paragraph = table.rows[0].cells[0].paragraphs[0]
                table.rows[0].cells[0].width = Cm(6.5)
                paragraph.add_run().add_picture(image, width=Cm(6.5))

                paragraph = table.rows[0].cells[1].paragraphs[0]
                if product['id'] in self.custom_configurations:
                    paragraph.add_run("Poznamka: ").bold = True
                    paragraph.add_run(self.custom_configurations[product['id']].internal_note)
                else:
                    custom_configuration = CatalogItemConfiguration(product['id'])
                    custom_configuration.set_image(image)
                    custom_configuration.set_title(product['title'])
                    missing_custom_data[product['id']] = custom_configuration
                paragraph.add_run('\n\nKlicova slova:\n').bold = True
                paragraph.add_run(", ".join(product['keywords_tag'].split(",")))
                paragraph.add_run('\nMaterial:\n').bold = True
                paragraph.add_run(", ".join(product['keywords_mat'].split(",")))
                paragraph.add_run('\nBarvy:\n').bold = True
                paragraph.add_run(", ".join([self.colors[int(color)] for color in product['colors'].split(",")]))
                paragraph.add_run("\nKat. c.:\n").bold = True
                paragraph.add_run(str(product['id']))

            document.add_page_break()

        document.save('demo.docx')
        return missing_custom_data

    def set_colors_list(self, colors):
        self.colors = colors

    def set_custom_configurations(self, custom_configurations):
        self.custom_configurations = custom_configurations

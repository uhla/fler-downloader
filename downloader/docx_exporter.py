import io
import re

import requests
from docx import Document
from docx.shared import Cm

from downloader.catalog_item_configuration import CatalogItemConfiguration


class DocxExporter:

    def export_docx(self, product_list_response, image_size):
        print("Starting docx export.")
        cleanr = re.compile('<.*?>')
        catalog_configurations_for_update = {}
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
                self.write_variant(catalog_configurations_for_update, document, image_size, product)

            document.add_page_break()

        document.save('export.docx')
        print("Docx export finished to file export.docx")
        return catalog_configurations_for_update

    def write_variant(self, catalog_configurations_for_update, document, image_size, product):
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
            catalog_configuration_for_update = self.custom_configurations[product['id']]
        else:
            catalog_configuration_for_update = CatalogItemConfiguration(product['id'])
        catalog_configuration_for_update.set_image(image)
        catalog_configuration_for_update.set_image_url(image_url)
        catalog_configuration_for_update.set_title(product['title'])
        catalog_configurations_for_update[product['id']] = catalog_configuration_for_update
        paragraph.add_run('\n\nKlicova slova:\n').bold = True
        paragraph.add_run(", ".join(product['keywords_tag'].split(",")))
        paragraph.add_run('\nMaterial:\n').bold = True
        paragraph.add_run(", ".join(product['keywords_mat'].split(",")))
        paragraph.add_run('\nBarvy:\n').bold = True
        paragraph.add_run(", ".join([self.colors[int(color)] for color in product['colors'].split(",")]))
        paragraph.add_run("\nKat. c.:\n").bold = True
        paragraph.add_run(str(product['id']))

    def set_colors_list(self, colors):
        self.colors = colors

    def set_custom_configurations(self, custom_configurations):
        self.custom_configurations = custom_configurations

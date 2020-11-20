import io
import re

import requests
from docx import Document
from docx.shared import Cm

from downloader.catalog_item_configuration import CustomizedCatalogItem


class DocxExporter:

    def export_docx(self, product_list, image_size):
        print("Starting docx export.")
        cleanr = re.compile('<.*?>')
        customized_catalog_items = {}
        document = Document()
        grouped_by_title = {}
        for product in product_list:
            if product['title'] in grouped_by_title:
                grouped_by_title.get(product['title']).append(product)
            else:
                grouped_by_title[product['title']] = [product]

        for product_title in grouped_by_title:
            document.add_heading(product_title, level=1)

            paragraph = document.add_paragraph()
            description = re.sub(cleanr, '', grouped_by_title[product_title][0]['description'])
            paragraph.add_run(description)

            short_description = re.sub(cleanr, '', grouped_by_title[product_title][0]['description_short'])
            paragraph = document.add_paragraph()
            paragraph.add_run("Kratky popis: ").bold = True
            paragraph.add_run(short_description)

            paragraph = document.add_paragraph()
            paragraph.add_run("Cena: ").bold = True
            paragraph.add_run(str(grouped_by_title[product_title][0]['price']) + ' CZK')

            document.add_paragraph().add_run("Varianty").bold = True

            for product in grouped_by_title[product_title]:
                customized_catalog_items[product['id']] = self.write_variant(document, image_size, product)

            document.add_page_break()

        document.save('export.docx')
        print("Docx export finished to file export.docx")
        return customized_catalog_items

    def write_variant(self, document, image_size, product):
        customized_write = False
        if product['id'] in self.custom_configurations:
            customized_catalog_item = self.custom_configurations[product['id']]
            customized_write = True
        else:
            customized_catalog_item = CustomizedCatalogItem(product['id'])
        customized_catalog_item.set_title(product['title'])

        table = document.add_table(cols=2, rows=1, style='Table Grid')
        image_url = product['photo_main'][image_size]
        image_response = requests.get(image_url, stream=True)
        image = io.BytesIO(image_response.content)
        paragraph = table.rows[0].cells[0].paragraphs[0]
        table.rows[0].cells[0].width = Cm(6.5)
        paragraph.add_run().add_picture(image, width=Cm(6.5))
        paragraph = table.rows[0].cells[1].paragraphs[0]
        if customized_write:
            paragraph.add_run("TYP: ").bold = True
            paragraph.add_run(self.custom_configurations[product['id']].type)
        customized_catalog_item.set_image(image)
        customized_catalog_item.set_image_url(image_url)


        paragraph.add_run('\n\nKlicova slova:\n').bold = True
        paragraph.add_run(", ".join(product['keywords_tag'].split(",")))
        if customized_write:
            paragraph.add_run('\nStyly:\n').bold = True
            paragraph.add_run(self.custom_configurations[product['id']].styles)
        paragraph.add_run('\nMaterial:\n').bold = True
        paragraph.add_run(", ".join(product['keywords_mat'].split(",")))
        paragraph.add_run('\nBarvy hlavni:\n').bold = True
        paragraph.add_run(", ".join([self.colors[int(color)] for color in product['colors'].split(",")]))
        if customized_write:
            paragraph.add_run('\nBarvy vedlejsi:\n').bold = True
            paragraph.add_run(self.custom_configurations[product['id']].other_colors)

        paragraph.add_run("\nKat. c.:\n").bold = True
        paragraph.add_run(str(product['id']))

        return customized_catalog_item

    def set_colors_list(self, colors):
        self.colors = colors

    def set_custom_configurations(self, custom_configurations):
        self.custom_configurations = custom_configurations

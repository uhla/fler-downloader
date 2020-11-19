from io import BytesIO

import requests
import xlrd
import pandas
import xlsxwriter

from downloader.catalog_item_configuration import CatalogItemConfiguration


class ExcelItemWriter:

    def write_missing_items(self, filename, missing_items={}):

        #FIXME avoid overwriting existing data in existing config xls file (flush out everything or do some sort of copy first
        workbook = xlsxwriter.Workbook('test.xlsx')
        worksheet = workbook.add_worksheet()
        i=2
        for item in missing_items.values():
            worksheet.set_column('C:C', 38)
            worksheet.set_row(i-1, 200)

            image_data = BytesIO(BytesIO(requests.get(item.image_url,stream=True).content).read())
            worksheet.write('A'+str(i),item.title)
            worksheet.write('B'+str(i),item.id)
            worksheet.insert_image('C'+str(i),  item.image_url, {'image_data': image_data})
            worksheet.write('D'+str(i),item.internal_note)
            i=i+1

        workbook.close()

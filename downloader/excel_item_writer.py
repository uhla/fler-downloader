from io import BytesIO

import requests
import xlsxwriter


class ExcelItemWriter:

    def write_item_configurations(self, filename, configs_to_save={}):
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:B', 25)
        worksheet.set_column('D:D', 50)
        worksheet.set_column('C:C', 38)

        worksheet.write('A1', 'Nazev')
        worksheet.write('B1', 'Id')
        worksheet.write('C1', 'Obrazek')
        worksheet.write('D1', 'Popis')

        i = 2
        for item in configs_to_save.values():
            worksheet.set_row(i - 1, 200)

            image_data = BytesIO(BytesIO(requests.get(item.image_url, stream=True).content).read())
            worksheet.write('A' + str(i), item.title)
            worksheet.write('B' + str(i), item.id)
            worksheet.insert_image('C' + str(i), item.image_url, {'image_data': image_data})
            worksheet.write('D' + str(i), item.internal_note)
            i = i + 1

        worksheet.autofilter("A1:D"+str(i-1))
        workbook.close()

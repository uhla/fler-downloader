import xlrd
import pandas
from downloader.catalog_item_configuration import CatalogItemConfiguration


class ExcelItemWriter:

    def write_missing_items(self, filename, missing_items={}):
        writer = pandas.ExcelWriter(filename, engine='xlsxwriter')
        for item in missing_items.values():
            frame_to_append = pandas.DataFrame([[item.title,item.id,'',item.internal_note]],columns=['Nazev','Katalog c.','Obrazek','Popisek'])
            frame_to_append.to_excel(writer,index=False)
            # workbook  = writer.book
            worksheet = writer.sheets['Sheet1']
            worksheet.insert_image('C10',  "xx", {'image_data': item.image.read()})

        writer.save()
        # data.to_excel(filename)
        # print(str(data))
        #
        #
        # workbook  = writer.book
        # worksheet = writer.sheets['Sheet1']
        #
        # # Insert an image.
        # worksheet.insert_image('D3', 'logo.png')

# for cust in Unique_cust_list:
#     :
#     :
#     ## insert the figure as image
# worksheet.insert_image('E1', 'figSaved')
#
# writer.save()
#
        # customized_catalog_items = {}
        # wb = xlrd.open_workbook(filename)
        # sheet = wb.sheet_by_index(0)
        #
        # for row_number in range(1, sheet.nrows):
        #     catalog_item = CatalogItemConfiguration(int(sheet.cell_value(row_number, 1)),
        #                                             sheet.cell_value(row_number, 3))
        #     customized_catalog_items[catalog_item.id] = catalog_item
        #
        # return customized_catalog_items

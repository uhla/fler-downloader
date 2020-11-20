from os import path

import xlrd

from downloader.catalog_item_configuration import CustomizedCatalogItem


class ExcelItemReader:

    def read_configuration(self, filename):
        customized_catalog_items = {}
        if path.exists(filename):
            print("Loading customized configuration from file: " + filename)
            wb = xlrd.open_workbook(filename)
            sheet = wb.sheet_by_index(0)

            for row_number in range(1, sheet.nrows):
                if str(sheet.cell_value(row_number, 1)) != '':
                    catalog_item = CustomizedCatalogItem(int(sheet.cell_value(row_number, 1)),
                                                         type=sheet.cell_value(row_number, 3),
                                                         styles=sheet.cell_value(row_number, 4),
                                                         other_colors=sheet.cell_value(row_number, 5))
                    customized_catalog_items[catalog_item.id] = catalog_item
        else:
            print("Unable to locate customized configuration file " + filename + ". No customization will be applied.")

        return customized_catalog_items

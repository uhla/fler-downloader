import xlrd

from downloader.catalog_item_configuration import CatalogItemConfiguration


class ExcelItemReader:

    def read_configuration(self, filename):
        customized_catalog_items = {}
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)

        for row_number in range(1, sheet.nrows):
            if str(sheet.cell_value(row_number, 1)) != '':
                catalog_item = CatalogItemConfiguration(int(sheet.cell_value(row_number, 1)),
                                                        sheet.cell_value(row_number, 3))
                customized_catalog_items[catalog_item.id] = catalog_item

        return customized_catalog_items

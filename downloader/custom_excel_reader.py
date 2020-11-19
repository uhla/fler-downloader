import xlrd

from downloader.catalog_item_configuration import CatalogItemConfiguration


class CustomExcelReader:

    def read_configuration(self, filename):
        customized_catalog_items = {}
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)

        for row_number in range(1, sheet.nrows):
            catalog_item = CatalogItemConfiguration(int(sheet.cell_value(row_number, 0)),sheet.cell_value(row_number, 1))
            customized_catalog_items[catalog_item.id] = catalog_item

        return customized_catalog_items

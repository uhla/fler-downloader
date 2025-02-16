import xlsxwriter


class ExcelItemWriter:

    def write_item_configurations(self, filename, configs_to_save={}):
        print("Writing updated customization data to file: " + filename)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:B', 25)
        worksheet.set_column('C:C', 30)
        worksheet.set_column('D:D', 38)

        worksheet.write('A1', 'Nazev')
        worksheet.write('B1', 'Id')
        worksheet.write('C1', 'Obrazek')
        worksheet.write('D1', 'Typ')

        wrapped_format = workbook.add_format({'text_wrap': True})
        i = 2
        for item in configs_to_save.values():
            worksheet.set_row(i - 1, 150)

            worksheet.write('A' + str(i), item.title)
            worksheet.write('B' + str(i), item.id)
            worksheet.insert_image('C' + str(i), "img_tmp/" + str(item.id) + ".jpg")
            worksheet.write('D' + str(i), item.type, wrapped_format)
            i = i + 1

        worksheet.autofilter("A1:D" + str(i - 1))
        workbook.close()

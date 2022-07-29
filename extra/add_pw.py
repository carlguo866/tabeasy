import pinyin
import openpyxl
import random
import string
if __name__ == '__main__':
    excel_file = '/Users/carlguo/Desktop/PPMT Teams.xlsx'
    wb = openpyxl.load_workbook(excel_file)
    worksheet = wb["Teams"]
    list = []
    n = worksheet.max_row
    m = worksheet.max_column
    for i in range(2, n + 1):
        worksheet.cell(row=i, column=m-2).value =''.join(random.choices(string.ascii_letters + string.digits, k=4))
        if worksheet.cell(row=i, column=2).value != None:
            worksheet.cell(row=i, column=m - 3).value = ''.join(worksheet.cell(row=i, column=2).value.split(' '))

    wb.save("testexcel.xlsx")
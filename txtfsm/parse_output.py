import sys
import os
import textfsm
import xlsxwriter
from tabulate import tabulate

workbook = xlsxwriter.Workbook('huawei.xlsx')
worksheet = workbook.add_worksheet()

template = sys.argv[1]
path_to_file = sys.argv[2]
result = []
header = []
row = 0
col = 0


def parse_conf(template, file):
    with open(template) as f, open(file) as output:
        re_table = textfsm.TextFSM(f)
        header = re_table.header
        result = re_table.ParseText(output.read())
    return result, header


if os.path.isdir(path_to_file):
    for file in os.listdir(path_to_file):
        if os.path.isfile(path_to_file + file):
            res, header = parse_conf(template, path_to_file + file)
            for r in res:
                result.append(r)
else:
    result, header = parse_conf(template, path_to_file)

# pprint(result)

worksheet.write(row, col, header[0])
worksheet.write(row, col + 1, header[1])
worksheet.write(row, col + 2, header[2])
worksheet.write(row, col + 3, header[3])
worksheet.write(row, col + 4, header[4])
row += 1


for hostname, number, description, shut, mode in (result):
    worksheet.write(row, col,     hostname)
    worksheet.write(row, col + 1, number)
    worksheet.write(row, col + 2, description)
    worksheet.write(row, col + 3, shut)
    worksheet.write(row, col + 4, mode)
    row += 1
workbook.close()

print(tabulate(result, headers=header))

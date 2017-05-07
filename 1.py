import pandas as pd

def writet_to_exel(*args):
    writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
    i = 0
    for arg in args:
        #df1.to_excel(writer, sheet_name='Sheet1', index=False)
        #df2.to_excel(writer, sheet_name='Sheet1', index=False,startcol=1)
        df = pd.DataFrame(arg)
        df.to_excel(writer, sheet_name='Sheet1', index=False,startcol=i)
        i = i + 1
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    #format1 = workbook.add_format({'num_format': '$#,##0'})
    format1 = workbook.add_format({'num_format':'#,##0.00'})
    #format1.set_num_format()
    worksheet.set_column('A:A', None, format1)


writet_to_exel({'Data1': [2222255555333,33,44, 20.001, 30, 20, 15, 30, 45]},
               {'Data2': [10, 20, 30, 20, 15, 30, 45]},
               )
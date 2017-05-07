import asyncio
from aiohttp import ClientSession
from lxml import etree
#from aiocfscrape import CloudflareScraper
import pandas as pd
import re

async def fetch(session, url):
    headers = {'Host': 'coinmarketcap.com',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'uk,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    #proxy = "http://10.24.100.210:3128"
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def main(loop):
    async with ClientSession(loop=loop) as session:
        html = await fetch(session, 'https://coinmarketcap.com/all/views/all/')
        #with open('html.txt', 'w') as f:
            #f.write(html)
        tup_value = await turple_value(html)
        writet_to_exel(tup_value)


async def turple_value(html):
    tree = etree.HTML(html)
    table = tree.xpath('//table[@id="currencies-all"]')
    name = {'Name': table[0].xpath('//td[@class="no-wrap currency-name"]/a/text()')}
    symbol = {'Symbol': table[0].xpath('//td[@class="text-left"]/text()')}
    market_cap = {'market_cap': [0 if re.sub(r'\s', '', s)=='?' else float(re.search(r'[0-9|\,|\.]+', re.sub(r'\,', '', s)).group()) for s in
                                 table[0].xpath('//td[@class="no-wrap market-cap text-right"]/text()') ]}
    price = {'Price': [0 if re.sub(r'\s', '', s)=='?' else float(re.search(r'[0-9|\,|\.]+', re.sub(r'\,', '', s)).group()) for s in
                       table[0].xpath('//a[@class="price"]/text()')]}
    table_obj = table[0].xpath('//tr[@id="id-bond"]')
    circulating_supply = {'Circulating supply':[0 if re.sub(r'\s', '', s)=='?' else float(re.search(r'[0-9|\,]+', re.sub(r'\,', '', s)).group()) for s in
                                                table_obj[0].xpath('//td[5]/a/text()')]}
    volume = {'Volume': [0 if re.sub(r'\s', '', s)=='?' else float(re.search(r'[0-9|\,|\.]+', re.sub(r'\,', '', s)).group()) for s in
                         table_obj[0].xpath('//td[6]/a/text() | //td[6]/span/text()')]}
    h1 = {'% h1':[0 if re.sub(r'\s', '', s)=='?' else float(re.search(r'[0-9|\,|\.]+', re.sub(r'\,', '', s)).group()) for s in
                  table_obj[0].xpath('//td[8]/text() | //td[8]/span/text()')]}
    h24 = {'% h24':[0 if re.sub(r'\s', '', s)=='?' else float(re.search(r'[0-9|\,|\.]+', re.sub(r'\,', '', s)).group()) for s in
                    table_obj[0].xpath('//td[9]/text() | //td[9]/span/text()')]}
    d7 = {'% d7':[0 if re.sub(r'\s', '', s)=='?' else float(re.search(r'[0-9|\,|\.]+', re.sub(r'\,', '', s)).group()) for s in
                  table_obj[0].xpath('//td[10]/text() | //td[10]/span/text()')]}
    return name, symbol, market_cap, price, circulating_supply, volume, h1, h24, d7

def writet_to_exel(args):
    writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
    i = 0
    print()
    for arg in args:
        df = pd.DataFrame(arg)
        df.to_excel(writer, sheet_name='Sheet1', index=False,startcol=i)
        i = i + 1
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format':'#,##0.00'})
    worksheet.set_column('C:I', None, format1)

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
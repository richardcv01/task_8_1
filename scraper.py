import asyncio

import aiohttp
from lxml import etree
import browser_cookie3
from aiocfscrape import CloudflareScraper

list_res = {}

async def fetch(session, url):
    headers = {'Host': 'coinmarketcap.com',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'uk,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    async with session.get(url, proxy="http://10.24.100.210:3128", headers=headers) as response:
        return await response.text()


async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        #tasks = [(get_text_title(session, title, url, author)) for title, url, author in
                 #zip(list_url['list_title'], list_url['list_url_title'], list_url['list_author'])]
        #await asyncio.gather(*tasks)
        #cj = browser_cookie3.chrome()
        #for k in cj:
         #   print(k)
        #cook = {'__cfduid':'ded06760021d16970ff4baf846330c9171493984539'}
        html =await fetch(session, 'https://coinmarketcap.com/all/views/all/')
        #table = etree.HTML(html).find('table')
        #table = tree.xpath('//table[@id="currencies-all"]')
        #row = table.xpath('//td[@class="no-wrap currency-name"]')
        #text = row.xpath('//a/text()')
        print(html)



event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
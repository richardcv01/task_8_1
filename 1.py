
import asyncio
from aiocfscrape import CloudflareScraper

async def test_open_page(url, loop=None):
    async with CloudflareScraper() as session:
        async with session.get(url, proxy="http://10.24.100.210:3128") as resp:
            print(resp.status)
            print(await resp.text())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_open_page('https://coinmarketcap.com', loop=loop))
    loop.close()
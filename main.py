import aiohttp
import asyncio
from typing import Dict
import logging
import time
import random

TIME_RANGE = 2
root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('test.log', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
root_logger.addHandler(handler)



URL_LIST = ["https://iecp.ru/ep/ep-verification",
"https://iecp.ru/ep/uc-list",
"https://uc-osnovanie.ru/",
"http://www.nucrf.ru",
"http://www.belinfonalog.ru",
"http://www.roseltorg.ru",
"http://www.astralnalog.ru",
"http://www.nwudc.ru",
"http://www.center-inform.ru",
"https://kk.bank/UdTs",
"http://structure.mil.ru/structure/uc/info.htm",
"http://www.ucpir.ru",
"http://dreamkas.ru",
"http://www.e-portal.ru",
"http://izhtender.ru",
"http://imctax.parus-s.ru",
"http://www.icentr.ru",
"http://www.kartoteka.ru",
"http://rsbis.ru/elektronnaya-podpis",
"http://www.stv-it.ru",
"http://www.crypset.ru",
"http://www.kt-69.ru",
"http://www.24ecp.ru",
"http://kraskript.com",
"http://ca.ntssoft.ru",
"http://www.y-center.ru",
"http://www.rcarus.ru",
"http://rk72.ru",
"http://squaretrade.ru",
"http://ca.gisca.ru",
"http://www.otchet-online.ru",
"http://udcs.ru",
"http://www.cit-ufa.ru",
"http://elkursk.ru",
"http://www.icvibor.ru",
"http://ucestp.ru",
"http://mcspro.ru",
"http://www.infotrust.ru",
"http://epnow.ru",
"http://ca.kamgov.ru",
"http://mascom-it.ru",
"http://cfmc.ru",
"",
""]

async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=1) as resp:
                return resp.status
    except:
        return 600

def should_clear_responses(time_start, time_current):
    return time_start // 3600 != time_current // 3600

async def main():
    responses: Dict[str, Dict[str, int]] = dict()
    loop = asyncio.get_event_loop()
    while True:
        t = int(time.time())
        tasks = [get(url) for url in URL_LIST]
        results = await asyncio.gather(*tasks)
        if should_clear_responses(t, int(time.time())):
            for url in responses:
                responses[url] = {
                    "hour": t // 3600
                }
        for i, url in enumerate(URL_LIST):
            if url not in responses:
                responses[url] = {
                    "hour": t // 3600
                }
            if results[i] not in responses[url]:
                responses[url][results[i]] = 1
            else:
                responses[url][results[i]] += 1

        root_logger.info(responses)
        await asyncio.sleep(random.random()*TIME_RANGE)
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

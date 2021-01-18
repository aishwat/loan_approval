#!/usr/local/bin/python3.5
import asyncio
from aiohttp import ClientSession
from datetime import datetime, timedelta

cust = {
    "customerID": 100000,
    "dob": "01/01/1977",
    "income": 25000,
    "bureauScore": 700,
    "applicationScore": 750,
    "maxDelL12M": 0,
    "allowedFoir": 60,
    "existingEMI": 2000,
    "loanTenure": 24,
    "currentAddress": "15 2nd cross vagdevi layout Marathahalli Bangalore Karnataka 560037",
    "bureauAddress": "HOUSE NO 15 2ND CROSS VASANT LAYOUT MARATHALLI NEAR VAGDEVI SCHOOL BANGALORE 560037 KA"
}


async def fetch(url, session):
    async with session.post(url, json=cust) as response:
        return await response.read()


async def run(r):
    url = "http://127.0.0.1:8000/status"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        t1 = datetime.now()
        for i in range(r):
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        # print(responses)
        delta = datetime.now() - t1
        print("calls: {} || time: {} sec || avg_resp_time: {} micro_sec".format(r, delta.total_seconds(),
                                                                                (delta.microseconds / r)))


async def run_seq(r):
    url = "http://127.0.0.1:8000/status"
    deltas = []
    async with ClientSession() as session:
        for i in range(r):
            t1 = datetime.now()
            resp = await fetch(url, session)
            t2 = datetime.now()
            deltas.append((t2 - t1).microseconds)
        print(sum(deltas) / r, "micro_sec")


def print_responses(result):
    print(result)


# https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(2000))
loop.run_until_complete(future)

# calls: 200 || time: 0.219646 sec || avg_resp_time: 1098.23 micro_sec
# calls: 2000 || time: 1.617898 sec || avg_resp_time: 308.949 micro_sec
# calls: 20000 || time: 16.671175 sec || avg_resp_time: 33.55875 micro_sec
# calls: 200000 || time: 179.841515 sec || avg_resp_time: 4.207575 micro_sec

from shared_items.interfaces.notion import Notion
from shared_items.utils import pp
import asyncio
import time
# from aiohttp import ClientSession

token = 'abc_123'

notion = Notion(token)

client = notion.client
async_notion = notion.async_client

def get_users():
    return client.users.list()

async def aync_get_users() -> asyncio.Future:
    return await async_notion.users.list()

async def do_em_all():
    start_time = time.monotonic()
    x = await asyncio.gather(aync_get_users(), aync_get_users(),aync_get_users(),aync_get_users(),aync_get_users(),aync_get_users(),aync_get_users(),aync_get_users())
    print('async time: ', time.monotonic() - start_time)
    return x


async_resp = asyncio.run(do_em_all())

start_sync_time = time.monotonic()
users = []
for i in range(8):
    users.append(get_users())

print('sync time: ', time.monotonic() - start_sync_time)

# import pdb; pdb.set_trace()

# import asyncio
# from pprint import pprint

# import random


# async def coro(tag):
#     print(">", tag)
#     await asyncio.sleep(random.uniform(1, 3))
#     print("<", tag)
#     return tag


# loop = asyncio.get_event_loop()

# group1 = asyncio.gather(*[coro("group 1.{}".format(i)) for i in range(1, 6)])
# group2 = asyncio.gather(*[coro("group 2.{}".format(i)) for i in range(1, 4)])
# group3 = asyncio.gather(*[coro("group 3.{}".format(i)) for i in range(1, 10)])

# all_groups = asyncio.gather(group1, group2, group3)

# results = loop.run_until_complete(all_groups)

# loop.close()

# pprint(results)

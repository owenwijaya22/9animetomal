import json
import asyncio
import aiohttp
import re
import time

time_now = time.time()

#get access token previously saved before
def get_access_token():
    with open('./data/access_token.json', 'r') as file:
        access_token = json.load(file)['access_token']
    return access_token

#uses regex to find all the anime ids from the 9anime text file
def get_anime_ids():
    with open('./data/9anime_list.txt', 'r') as file:
        anime_ids = re.findall('(\d+)', file.read())
    return list(set(anime_ids))


async def update_list(access_token, anime_id, session, status_list):
    url = f'https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'status': 'plan_to_watch'}
    async with session.put(url, data=data, headers=headers) as response:
        status_list.append(response.status)


async def delete_list(access_token, anime_id, session, status_list):
    url = f'https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'status': 'plan_to_watch'}
    async with session.delete(url, data=data, headers=headers) as response:
        status_list.append(response.status)


async def main():
    access_token = get_access_token()
    anime_ids = get_anime_ids()
    status_list = []
    async with aiohttp.ClientSession() as session:
        try:
            task = input('delete(d) or update(u) list?: ')
            if task == 'd':
                tasks = [
                    delete_list(access_token, anime_id, session, status_list)
                    for anime_id in anime_ids
                ]
            elif task == 'u':
                tasks = [
                    update_list(access_token, anime_id, session, status_list)
                    for anime_id in anime_ids
                ]
            r = await asyncio.gather(*tasks)
            print(status_list)
            if 500 in status_list:
                print(
                    "Mal's server experienced server error,  please run the program one more time :D"
                )
        except Exception as e:
            print(Exception)


asyncio.get_event_loop().run_until_complete(main())
print(f'The program took {time.time()-time_now} seconds')
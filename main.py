import os
import re
import random
import time
import asyncio
import requests

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from defs import getUrl, getcards

# Lista de URLs de imágenes
image_urls = [
    "https://www.freepik.es/foto-gratis/hermoso-camino-madera-que-impresionantes-arboles-coloridos-bosque_8753393.htm#query=paisajes%20hermosos&position=0&from_view=keyword&track=ais",
    "https://www.freepik.es/foto-gratis/hermosa-foto-lago-cristalino-junto-base-montana-nevada-dia-soleado_8507181.htm#query=paisajes%20hermosos&position=5&from_view=keyword&track=ais",
    "https://www.freepik.es/foto-gratis/montana-fuji-lago-kawaguchiko-manana-estaciones-otono-montana-fuji-yamanachi-japon_10695678.htm#query=paisajes%20hermosos&position=11&from_view=keyword&track=ais",
    # Agrega más URLs de imágenes aquí
]

class Scraper:
    def __init__(self, id, hash, chat, chats):
        self.id = id
        self.hash = hash
        self.chat = chat
        self.chats = chats
        self.ccs = []

        with open('cards.txt', 'r') as r:
            temp_cards = r.read().splitlines()

        for x in temp_cards:
            car = getcards(x)
            if car:
                self.ccs.append(car[0])

    async def get_bin_info(self, cc):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bins-su-api.danielsaumett2093.workers.dev/api/{cc[:6]}') as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data

    async def handle_message(self, client, message):
        text = message.text
        cards = getcards(text)
        if not cards:
            return
        cc, mes, ano, cvv = cards
        if cc in self.ccs:
            return
        self.ccs.append(cc)

        bin_info = await self.get_bin_info(cc)
        if not bin_info:
            return

        brand = bin_info["data"]["vendor"]
        types = bin_info["data"]["type"]
        level = bin_info.get("data", {}).get("level", "N/A")
        bank = bin_info.get("data", {}).get("bank", "N/A")
        country = bin_info["data"]["country"]
        flag = bin_info["data"]["countryInfo"]["emoji"]
        
        # Selección aleatoria de una URL de imagen
        img = random.choice(image_urls)

        extra = cc[0:0 + 12]
        crd = f"{cc}|{mes}|{ano}|{cvv}"
        text = f""" 
┏━━━━━━•(=^●ω●^=)•━━━━━━┓
Card ➣  {cc}|{mes}|{ano}|{cvv} 
──────────✰──────────
Bin Info ➣ {brand} - {types} - {level}
Bank ➣  {country} - ({flag})  {bank}
┗━━━━━━•(=^●ω●^=)•━━━━━━┛
Dropper by @Gussss_07 [FREE-DB]
"""

        print(f'Card => {cc}|{mes}|{ano}|{cvv}  {country} - ({flag}    ')
        with open('cards.txt', 'a') as w:
            w.write(crd + '\n')

        await client.send_photo(
            self.chat,
            img,
            caption=text
        )

    def run(self):
        app = Client("session", api_id=self.id, api_hash=self.hash)

        @app.on_message(filters.chat(self.chats) & filters.text)
        async def my_event_handler(client, message):
            await self.handle_message(client, message)

        app.run()

if __name__ == "__main__":
    id = 27681377
    hash = '43f342537ee796353a06c6b7b6931c57'
    chat = -1001904230067
    chats = [
        '@VegetaScrap', '@RevyDrops', '@SlostChat','@ScrapperLala','@kurumichat','@kurumichks','@BINEROS_CCS2'
    ]
    scraper = Scraper(id, hash, chat, chats)
    scraper.run() 
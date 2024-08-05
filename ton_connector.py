import asyncio
from pytonconnect import TonConnect

from config import TON_MANIFEST_URL

class TonConnector:
    def __init__(self):
        self.connector = TonConnect(manifest_url=TON_MANIFEST_URL)

    async def connect(self):
        wallets_list = self.connector.get_wallets()
        if wallets_list:
            return await self.connector.connect(wallets_list[0])

    async def wait_for_connection(self):
        return await self.connector.wait_for_connection()

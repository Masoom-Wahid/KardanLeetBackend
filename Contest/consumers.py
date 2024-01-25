from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.core.cache import cache
from .models import Contests
from collections import OrderedDict
from .utils import getLeaderBoardData,sortLeaderBoarddata

@sync_to_async
def validate_user(hashId,access_token):
    try:
        decoded_token = AccessToken(access_token)
        user_instance = User.objects.get(id=decoded_token["user_id"])
        if user_instance.is_superuser:
            return [True,user_instance] 
        else:
            return [False,""]
    except Exception as e:
        print(e)
        return [False,e]
@sync_to_async
def sortdata(data):
    sorted_data = sortLeaderBoarddata(data)
    return sorted_data

@sync_to_async
def getData():
    try:
        contest = Contests.objects.get(starred=True)
    except Contests.DoesNotExist:
        return {"detail":"Contest Has Not Started Yet"}
    result = getLeaderBoardData(contest)
    cache.set("leaderboard",result,14400)
    return result

class LeaderboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.userModel = User
        self.room_name = "leaderboard"
        # Gets The Access Token
        query_params = self.scope['query_string'].decode('utf-8')
        self.access_token = query_params.split('=')[1]

        # validates The User If the True it will accept else closes
        validation_res,user_instance = await validate_user(self.room_name,self.access_token)
        if validation_res == False:
            await self.close()
        await self.accept()

        data = await getData()
        result = await sortdata(data)

        #Sends The Previous Data
        await self.send(text_data=json.dumps({
            "type":"latest_data",
            "message": result
        }))
        # Adds The User to A Channel Layer
        await self.channel_layer.group_add(self.room_name, self.channel_name)

    async def Leaderboard_update(self, event):
        new_stats = event["update"]
        sorted = await sortdata(new_stats)
        await self.send(text_data=json.dumps({
            "type": "latest_data",
            "message": sorted
        }))
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
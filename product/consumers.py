# myapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from user_details.models import Member
from .models import Auction, Bid


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        self.room_group_name = f'auction_{self.product_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        bid = text_data_json['bid']
        user_id = text_data_json['user']

        # Fetch a Member instance instead of a User instance
        user = await sync_to_async(Member.objects.get)(username=user_id)
        auction = await sync_to_async(Auction.objects.get)(product_id=self.product_id)

        # Check if the bid is greater than the current bid
        if float(bid) <= auction.current_bid:
            await self.send(text_data=json.dumps({
                'error': 'Your bid must be higher than the current bid.'
            }))
            return

        if user.coin_balance >= float(bid):
            new_bid = await sync_to_async(Bid.objects.create)(
                user=user,
                auction=auction,
                amount=bid
            )

            auction.current_bid = new_bid.amount
            auction.current_winner = user
            await sync_to_async(auction.save)()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'auction_update',
                    'bid': bid,
                    'user': user.username
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'error': 'Insufficient coin balance to place the bid.'
            }))

    async def auction_update(self, event):
        bid = event['bid']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'bid': bid,
            'user': user
        }))

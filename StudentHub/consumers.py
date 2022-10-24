# this is where all the async functionality takes place

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessages


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = 'chat_%s_%s' % (self.scope['url_route']['kwargs']['slug'], self.scope['url_route']['kwargs']['id'])
        await self.channel_layer.group_add(self.roomGroupName, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.roomGroupName, self.channel_layer)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        section = text_data_json['section']
        room_id = text_data_json['room_id']

        checkMessage = await database_sync_to_async(self.saveMessage)(message, username, section, room_id)

        if checkMessage:
            await self.channel_layer.group_send(
                self.roomGroupName,{
                    'type': 'sendMessage',
                    'message': message,
                    'username': username,
                    'section': section,
                    'room_id': room_id,
                })
        else:
            print('Message could not be sent.')



    async def sendMessage(self, event):
        message = event['message']
        username = event['username']
        section = event['section']
        room_id = event['room_id']
        await self.send(text_data=json.dumps(
            {'message': message,
             'username': username,
             'section': section,
             'room_id': room_id,
             }))


    # try:
    #     post = HubPageDataModel(
    #         title=request.POST['title'],
    #         subject=request.POST['subject'],
    #         author=request.user,
    #         date=request.POST['date_now'],
    #         date_end=request.POST['date'],
    #         description=request.POST['description'],
    #         text=request.POST['text']
    #     )
    #     post.save()
    # except Exception as excep:
    #     messages.error(request, 'Please complete all the fields.')
    #     print(excep)
    #     return HttpResponseRedirect(reverse('addpost', args=(slug,)))
    #
    # return HttpResponseRedirect(reverse('activity', args=(slug,)))

    def saveMessage(self, message, user, section, room_id):
        try:
            if message.isspace() or user is None or section is None or room_id is None :
                print('Message fields empty.')
                return False

            mess = ChatMessages(
                messageText=message,
                user=user,
                subject=section,
                room_id=room_id,
            )
            mess.save()
        except Exception as excep:
            print(excep)
            return False

        return True



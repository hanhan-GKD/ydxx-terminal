import urwid
from src.ydxx_widget.menu import MenuWidgetItem
from src.ydxx_widget.button import Button
from src.globals.global_config import global_config
from src.globals.global_values import global_values
from src.ydxx_widget.stack import StackFrame, StackWidget
import socketio
import asyncio
from typing import Callable

class ChannelListPanel(StackFrame):
    _name = '选择频道'
    signals = ['select_channel', 'resume_channel']
    def __init__(self):
        channel_list = [Button('艾欧尼亚', highlight='active_channel_item'),
                                        Button('黑色玫瑰', highlight='active_channel_item')]
        for index, button in enumerate(channel_list):
            urwid.connect_signal(button, 'click', 
                                 lambda x: self.on_chose(index))
        super(ChannelListPanel, self).__init__(urwid.Pile(channel_list))

    def on_chose(self, index):
        self._emit('select_channel', global_config.ws_server[index])
    
    def title(self):
        return self._name

class TeamListPanel(StackFrame):
    _name = '选择队伍'
    def __init__(self):
        self.team_meta = []
        self.team_list = urwid.GridFlow([], 30, 1, 1, 'left')
        super(TeamListPanel, self).__init__(self.team_list)
    def init_team(self, data):
        append_type = self.team_list.options()
        self.team_list.contents.clear()
        self.team_meta = data
        for team_data in self.team_meta:
            team_widget = urwid.Pile(
                [urwid.Text([team_data['scenesName'], 
                             ' {}/5'.format(len(team_data['users'])), 
                             ' 队长: {}'.format(team_data['userName'])], wrap='ellipsis'),
                 urwid.Columns([urwid.Text('等级: {}~{}'.format(team_data['level'][0],
                                                              team_data['level'][1])), Button('申请')])])
            self.team_list.contents.append((team_widget, append_type))
    def title(self):
        return self._name

class TeamAdventurePanel(MenuWidgetItem):
    def __init__(self):
        self.ws = socketio.AsyncClient()
        self.ws.on('connect', self.on_connect)
        self.ws.on('team', self.on_team_msg)
        self.ws.on('message', self.on_message)
        self.channel_list = ChannelListPanel()
        self.team_list = TeamListPanel()
        self.content_frame = StackWidget([self.channel_list])
        urwid.connect_signal(self.channel_list, 'select_channel', self.channel_chosen)
        super(TeamAdventurePanel, self).__init__(self.content_frame)
    
    def channel_chosen(self, btn, channel):
        url = "{}?uid={}&token={}".format(channel, global_values.uid, global_values.token)
        if self.ws.connected:
            self.disconnect(lambda: self.connect(url))
        else:
            self.connect(url)

    def connect(self, url):
        asyncio.get_event_loop().create_task(self.ws.connect(url))

    def on_message(self, message):
        pass

    def on_connect(self):
        async def _connected():
            await self.ws.emit('connectionTeam', {'uid': global_values.uid, 'token': global_values.token})
        asyncio.get_event_loop().create_task(_connected())

    def on_team_msg(self, data):
        if data['type'] == 'initTeamList':
            self.team_list.init_team(data['data'])
            self.content_frame.push(self.team_list)

    def disconnect(self, callback: Callable = None):
        async def _disconnect():
            await self.ws.disconnect()
            if callback:
                    callback()
        asyncio.get_event_loop().create_task(_disconnect())

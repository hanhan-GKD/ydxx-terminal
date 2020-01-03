import urwid
from src.ydxx_widget.menu_widget import MenuWidgetItem
from src.ydxx_widget.button import Button
from src.globals.global_config import global_config
import socketio

class TeamAdventurePanel(MenuWidgetItem):
    CONNECTED = 1
    DISCONNECTED = 2
    def __init__(self):
        self.channel_list = urwid.Pile([Button('艾欧尼亚', on_press=lambda btn: self.on_connect(global_config.websocket_server[0]), highlight='active_channel_item'),
                                        Button('黑色玫瑰', on_press=lambda btn: self.on_connect(global_config.websocket_server[1]), highlight='active_channel_item')])
        self.content_frame = self.channel_list
        self.ws = socketio.AsyncClient()
        super(TeamAdventurePanel, self).__init__(self.channel_list)
    
    def on_connect(self, channel):
        pass
        #self.ws.connect()

import urwid
from src.ydxx_widget.menu import MenuWidgetItem
from src.ydxx_widget.button import Button
from src.ydxx_widget.select import Select
from src.ydxx_widget.edit import IntEdit
from src.globals.global_config import global_config
from src.globals.global_values import global_values
from src.ydxx_widget.stack import StackFrame, StackWidget
from src.ydxx_widget.alert import Alert, alert
from src.globals.api import api
from src.common.htmlless_util import htmlless
import socketio
import asyncio
from typing import Callable, Dict

class Soldier(urwid.WidgetWrap):
    TEAM_MATE_TYPE = 1
    ENEMY_TYPE = 2
    def __init__(self, meta_data):
        self.soldier_name = meta_data['name']
        self.soldier_ph = int(meta_data['ph'])
        self.soldier_id = meta_data['id']
        self.soldier_race_type = global_values.race_types.get(meta_data['race_type'])
        self.soldier_descriptor = urwid.Text(
            [self.soldier_name, ' [{}] '.format(self.soldier_race_type)], wrap=urwid.CLIP)

        self.phbar = urwid.Text(['血量: ', str(self.soldier_ph)], wrap=urwid.CLIP)
        if meta_data['type'] == 1:
            self.display_attribute = 'team_mate_soldier'
            self.soldier_type = self.TEAM_MATE_TYPE
        elif meta_data['type'] == 2:
            self.soldier_type = self.ENEMY_TYPE
            self.display_attribute = 'enemy_soldier'
        super(Soldier, self).__init__(
            urwid.AttrMap(urwid.Pile([self.phbar, self.soldier_descriptor]), self.display_attribute))
    def set_blood(self, blood_value: int):
        if blood_value < 0:
            blood_value = 0
        self.soldier_ph = int(blood_value)
        self.phbar.set_text(['血量: ', str(self.soldier_ph)])
       

class SocketClient(socketio.AsyncClient):

    def disconnect(self, callback: Callable = None):
        async def _disconnect():
            await super(SocketClient, self).disconnect()
            if callback:
                    callback()
        asyncio.get_event_loop().create_task(_disconnect())

    def emit_msg(self, msg_type, data = {}):
        data['uid'] = global_values.uid
        data['token'] = global_values.token
        asyncio.get_event_loop().create_task(
            super(SocketClient, self).emit(msg_type, data))



class ChannelListPanel(StackFrame):
    _name = '选择频道'
    signals = ['select_channel']
    def __init__(self):
        channel_list = [Button('艾欧尼亚', highlight='active_channel_item'),
                                        Button('黑色玫瑰', highlight='active_channel_item')]
        for index, button in enumerate(channel_list):
            urwid.connect_signal(button, 'click', 
                                 lambda x, index=index: self.on_chose(index))
        super(ChannelListPanel, self).__init__(urwid.Pile(channel_list))

    def on_chose(self, index):
        self._emit('select_channel', global_config.ws_server[index])
    
    def title(self):
        return self._name

class CreateTeamWidget(urwid.Pile):
    def __init__(self):
        self.start_edit = IntEdit(0, max=299)
        self.end_edit = IntEdit(300, max=300)
        self.pwd_edit = urwid.Edit(caption='密码: ', mask='*') 
        self.scene_select = Select([], '选择战场')
        super(CreateTeamWidget, self).__init__([
            self.scene_select, self.pwd_edit, 
            urwid.Columns([('pack', urwid.Text('等级: ')), 
            (4, self.start_edit), ('pack', urwid.Text('- ')), 
            (5, self.end_edit)])])
        asyncio.get_event_loop().create_task(self.get_scene_list())

    async def get_scene_list(self):
        async with global_values.session.get(api.scene_list) as response:
            json_data = await response.json()
            if 'code' in json_data and json_data['code'] == 200:
                scene_list = json_data['data']['combatList']
                select_data = [(item['name'], item) for item in scene_list]
                self.scene_select.set_data(select_data)

    def team_info(self):
        if self.scene_select.value():
            return {
                'teamScenesId': self.scene_select.value()['_id'],
                'level': [self.start_edit.value(), self.end_edit.value()],
                'pwd': self.pwd_edit.get_edit_text()
            }
        return None
        
class TeamPanel(urwid.WidgetWrap):    
    signals = ['select_team']
    def __init__(self, team_data):
        self.meta_data = team_data
        if self.meta_data.get('is_pwd'):
            detail = [('error_info', '¤ '), '等级: {}~{}'.format(team_data['level'][0], team_data['level'][1])]
        else:
            detail = '等级: {}~{}'.format(team_data['level'][0], team_data['level'][1])
        team_widget = urwid.Pile(
            [urwid.Text([team_data['scenesName'],
                         ' {}/5'.format(len(team_data['users'])),
                         ' 队长: {}'.format(team_data['userName'])], wrap=urwid.CLIP),
             urwid.Columns([urwid.Text(detail),
                            Button('申请', on_press=lambda x: self._emit('select_team', self.meta_data))])])
        super(TeamPanel, self).__init__(team_widget)
 

class TeamListPanel(StackFrame):
    _name = '选择队伍'
    def __init__(self, ws: SocketClient):
        self.ws = ws
        self.team_list = urwid.GridFlow([], 30, 1, 1, 'left')
        super(TeamListPanel, self).__init__(self.team_list)

    def init_team(self, data):
        self.team_list.contents.clear()
        append_type = self.team_list.options()
        self.team_list.contents.append((Button('创建队伍', self.create_team), append_type))
        for team_data in data:
            self.add_team(team_data)

    def title(self):
        return self._name
    
    def create_team(self, btn): 
        w = CreateTeamWidget()
        def _create(option):
            if option  == Alert.YES:
                info = w.team_info()
                if info:
                    self.ws.emit_msg('createdTeam', info)
            return True
        alert(w, '创建队伍', _create, style=Alert.YES_NO)

    def on_chose(self, panel, data):
        def on_pwd_input(option, pwd):
            if option == Alert.YES:
                if pwd == data['pwd']:
                    self.ws.emit_msg('applyTeam', 
                                     {'teamId': data['teamId'], 'pwd': pwd})
                    return True
                else:
                    return False
            return True
        if 'is_pwd' in data and data['is_pwd']:
            pwd_edit = urwid.Edit('密码: ', mask='*')
            alert(pwd_edit, '请输入队伍密码', lambda option: on_pwd_input(
                option, pwd_edit.get_edit_text()), Alert.YES_NO)
        else:
            self.ws.emit_msg('applyTeam', {'teamId': data['teamId']})

    def del_team(self, teamId):
        for index in range(1, len(self.team_list.contents)):
            widget = self.team_list.contents[index][0]
            if widget.meta_data['teamId'] == teamId:
                urwid.disconnect_signal(widget, 'select_team', self.on_chose)
                del self.team_list.contents[index]
                break

    def add_team(self, team_data):
        append_type = self.team_list.options()
        team_widget = TeamPanel(team_data)
        urwid.connect_signal(team_widget, 'select_team', self.on_chose)
        self.team_list.contents.append((team_widget, append_type))

    def on_leave(self):
        self.ws.disconnect()

class TeamRoomPanel(StackFrame):
    def __init__(self, team_info, ws: SocketClient):
        self.connected = True
        self.team_info = team_info
        self.team_id = team_info['teamId']
        self.soldier_map = {}
        self.mate_list = urwid.GridFlow([], 15, 1, 1, 'left')
        self.enemy_list = urwid.GridFlow([], 15, 1, 1, 'left')
        self.fight_log = urwid.ListBox(urwid.SimpleListWalker([]))
        self.ws = ws
        self.ws.on('battleEnd', self.battle_end)
        self.users = urwid.Pile([])
        users_info = self.team_info['users']
        self.load_team_user(users_info)
        if self.team_id == global_values.uid:
            ctrl_btns = urwid.Pile([('pack', Button('开始战斗', self.start_fight)),
                         ('pack', Button('离开队伍', lambda x: self.leave_team()))])
        else:
            ctrl_btns = urwid.Pile([('pack', urwid.Text('开始战斗')),
                         ('pack', Button('离开队伍', lambda x: self.leave_team()))])
        self.battleground = urwid.LineBox(urwid.Pile([
            self.enemy_list, 
            urwid.Divider('='), 
            self.mate_list]))
        super(TeamRoomPanel, self).__init__(urwid.Pile([
            self.battleground,
            urwid.Columns([
                urwid.LineBox(urwid.BoxAdapter(self.fight_log, 10)),
                (16, urwid.Pile([
                    ctrl_btns,
                    self.users
                ]))
            ], dividechars=1)
        ]))

    def load_team_user(self, users_info):
        self.users.contents.clear()
        option = self.users.options()
        for user_info in users_info:
            uname = user_info['nickname']
            level = user_info['level']
            race_type = global_values.race_types.get(user_info['race_type'])
            uid = user_info['id']
            if uid == self.team_id:
                user = urwid.Text(['»', ' [{}] {} {}'.format(level, race_type, uname)], wrap=urwid.CLIP)
            else:
                user = urwid.Text(['[{}] {} {}'.format(level, race_type, uname)], wrap=urwid.CLIP)
            self.users.contents.append((user, option))
    
    def start_fight(self, btn):
        self.ws.emit_msg('startPeril')
    
    def disconnect_team(self):
        if self.connected:
            self.connected = False
            self.ws.emit_msg('disconnectedTeam', {'teamId': self.team_id})
    
    def leave_team(self):
        if self.connected:
            self.connected = False
            self.ws.emit_msg('leaveTeam')
            self.exit()
        
    def on_leave(self):
        if self.connected:
            self.ws.emit_msg('disconnectedTeam', {'teamId': self.team_id})
            self.ws.emit_msg('leaveTeam')

    async def update_battleground(self, msg):
        data = msg['data'] 
        self.soldier_map.clear()
        self.mate_list.contents.clear()
        self.enemy_list.contents.clear()
        mate_option = self.mate_list.options()
        enemy_option = self.enemy_list.options()
        self.fight_log.body.append(urwid.Text(('fight_info', '战斗开始')))
        start_ph = data['startPh']
        for ph_item in start_ph:
            soldier = Soldier(ph_item)
            if soldier.soldier_type == Soldier.ENEMY_TYPE:
                self.enemy_list.contents.append((soldier, enemy_option))
            else:
                self.mate_list.contents.append((soldier, mate_option))
            self.soldier_map[soldier.soldier_id] = soldier
        self.battleground.set_title('战斗开始')
        await asyncio.sleep(2)
        round_list = data['round_arr']
        for round in round_list:
            round_title = '第{}回合'.format(round['round_num'])
            self.battleground.set_title(round_title)
            self.fight_log.body.append(urwid.Text(round_title))
            for fight_arr in round['arr']:
                fight_info_items = fight_arr.split('</p>')
                for fight_info_html in fight_info_items:
                    strip_info = fight_info_html.strip()
                    if strip_info:
                        fight_info = htmlless(strip_info)
                        fight_texts = fight_info.split(' ') 
                        if len(fight_texts) > 0:
                            fight_texts[0] = ('fight_user', fight_texts[0])
                            fight_texts[2] = ('fight_user', fight_texts[2])
                            self.fight_log.body.append(urwid.Text(fight_texts))
            self.fight_log.body.append(urwid.Text(('info_remain_ph', '剩余血量')))
            self.fight_log.body.append(urwid.Text('  '.join(round['lastPh'])))
            self.fight_log.set_focus(len(self.fight_log.body) - 1)
            for ph_value in round['lastPhArr']:
                ph_num = int(ph_value['ph_num'])
                soldier = self.soldier_map[ph_value['id']]
                soldier.set_blood(ph_num)
            await asyncio.sleep(2)
        self.battleground.set_title('战斗结束')
        self.fight_log.body.append(urwid.Text([('fight_info', msg['msg'])]))
        for user in data['users']:
            uname = user['nickname']
            for item in user['goods']:
                self.fight_log.body.append(urwid.Text(
                    [('fight_user', uname), ' 获得 ', ('reward_goods', item['name'])]))
        self.fight_log.body.append(urwid.Text('\n'))
        self.fight_log.set_focus(len(self.fight_log.body) - 1)
 

    def battle_end(self, msg):
        asyncio.get_event_loop().create_task(self.update_battleground(msg))
                
    def title(self):
        return self.team_info['scenesName']

class TeamAdventurePanel(MenuWidgetItem):
    ignore_error = ['你还没有队伍！']
    def __init__(self):
        self.ws = SocketClient()
        self.ws.on('connect', self.on_connect)
        self.ws.on('team', self.on_team_msg)
        self.ws.on('message', self.on_message)
        self.channel_list = ChannelListPanel()
        self.team_list = TeamListPanel(self.ws)
        self.team_room: TeamRoomPanel = None
        self.content_frame = StackWidget([self.channel_list])
        urwid.connect_signal(self.channel_list, 'select_channel', self.channel_chosen)
        super(TeamAdventurePanel, self).__init__(self.content_frame)
    
    def channel_chosen(self, btn, channel):
        url = "{}?uid={}&token={}".format(channel, global_values.uid, global_values.token)
        if self.ws.connected:
            self.ws.disconnect(lambda: self.connect(url))
        else:
            self.connect(url)

    def connect(self, url):
        asyncio.get_event_loop().create_task(self.ws.connect(url))

    def on_message(self, message):
        pass

    def on_connect(self):
        self.ws.emit_msg('connectionTeam')
        self.ws.emit_msg('leaveTeam')

    def on_team_msg(self, msg):
        msg_type = msg['type']
        if msg_type == 'initTeamList':
            self.team_list.init_team(msg['data'])
            self.content_frame.push(self.team_list)
        elif msg_type == 'createdRloadTeam':
            data = msg['data']
            self.team_list.add_team(data)
            if data['teamId'] == global_values.uid:
                self.team_room = TeamRoomPanel(data, self.ws)
                self.content_frame.push(self.team_room)
        elif msg_type == 'reloadMyTeam':
            if self.team_room:
                self.team_room.load_team_user(msg['data']['users'])
            else:
                self.team_room = TeamRoomPanel(msg['data'], self.ws)
                self.content_frame.push(self.team_room)
        elif msg_type == 'currentTeamDisband':
            if self.team_room:
                self.team_room.disconnect_team()
                self.team_room = None
        elif msg_type == 'listTeamDisband':
            data = msg['data']
            if isinstance(data, Dict):
                team_id = data['teamId']
                if self.team_room:
                    if team_id == self.team_room.team_id:
                        self.team_room.leave_team()
                        self.team_room = None
            else:
                self.team_list.del_team(data)
        elif msg_type == 'msg':
            info = msg['msg']
            if info not in self.ignore_error:
                pass
                alert(urwid.Text(msg['msg']), '错误')

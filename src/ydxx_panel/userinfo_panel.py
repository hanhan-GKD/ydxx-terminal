import urwid
from tornado import httpclient
from src.ydxx_widget import menu_widget 
import json
from src.globals.global_values import global_values
from src.globals.api import api
class UserInfoPanel(menu_widget.MenuWidgetItem):
    show_attr = [('nickname', '昵称: '),
                 ('level_text', '境界: '),
                 ('repair_num', '修为: '),
                 ('race_type', '种族: '),
                 ('ph_num', '气血值: '),
                 ('vitality_num', '活力: '),
                 ('force_num', '武力值: '),
                 ('physical_damage', '物理伤害: '),
                 ('iq_num', '智力值: '),
                 ('magic_damage', '魔法伤害: '),
                 ('endurance_num', '耐力值: '),
                 ('endurance_num', '耐力值: '),
                 ('physical_defense', '物理防御: '),
                 ('agile_num', '敏捷值: '),
                 ('magic_defense', '魔法防御: '),
                 ('faith_num', '信仰值: '),
                 ('restore_damage', '治疗伤害: '),
                 ('speed', '速度: '),
                 ('pet_max_count', '宠物上限: '),
                 ('health_num', '精力: '),
                 ('potential_num', '潜力点: ')]

    def __init__(self):
        self.attr_list = urwid.ListBox(urwid.SimpleFocusListWalker([])) 
        super(UserInfoPanel, self).__init__(self.attr_list)
        self.fetch_user_info()

    def fetch_user_info(self):
        def resp_user_info(response: httpclient.HTTPResponse):
            if response.code == 200:
                json_data = json.loads(response.body)
                if json_data['code'] == 200:
                    ready_extend_list = []
                    user = json_data['data']['user']
                    index = 0
                    show_attr = UserInfoPanel.show_attr
                    while index < len(show_attr):
                        if index + 1 < len(show_attr):
                            first_attr = show_attr[index]
                            second_attr = show_attr[index + 1]
                            ready_extend_list.append(
                                urwid.Columns([urwid.Text([first_attr[1], str(user[first_attr[0]])]),
                                               urwid.Text([second_attr[1], str(user[second_attr[0]])])]))
                        else:
                            attr = show_attr[index]
                            ready_extend_list.append(
                                urwid.Text([attr[1], str(user[attr[0]])]))
                        index += 2
                    self.attr_list.body.extend(ready_extend_list)

            else:
                pass

        request = httpclient.HTTPRequest(api.user_init_info, 'GET', headers={
            'Cookie': global_values.token})
        httpclient.AsyncHTTPClient().fetch(request, resp_user_info)


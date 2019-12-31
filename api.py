from globals import GlobalContainer
from global_config import global_config

def gen_api(uri: str) -> str:    
        return '{}{}'.format(global_config.hostname, uri)


api = GlobalContainer()

api.login = gen_api('/api/login')
api.user_init_info = gen_api('/api/getUserInitInfo')

import re
html_pattern = re.compile('<[^>]+>', re.S)

"""
去除字符串中的html标签
:param source 包含html的字符串
:return 已经过滤html的字符串
"""
def htmlless(source: str) -> str:
    return html_pattern.sub('', source)
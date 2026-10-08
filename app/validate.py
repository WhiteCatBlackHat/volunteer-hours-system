import re

NAME_RE = re.compile(r'^[\w\-\u4e00-\u9fff]+$')

def validate_name(name, field='名称'):
    if not isinstance(name, str):
        return f'{field}必须是字符串'
    stripped = name.strip()
    if not stripped:
        return f'{field}不能为空'
    if len(stripped) > 100:
        return f'{field}长度不能超过 100 字符'
    if not NAME_RE.search(stripped):
        return f'{field}只能包含以下字符: 大小写字母、数字、下划线、连字符、汉字'
    return None

DESCRIPTION_RE = re.compile(r'^[\w\u4e00-\u9fff\s\-\.,;:!?()@#$%^&*+=\[\]{}|~，。、；：！？（）…—·“”‘’『』「」]+$')

def validate_description(description, field='描述'):
    if not isinstance(description, str):
        return f'{field}必须是字符串'
    stripped = description.strip()
    if not stripped:
        return f'{field}不能为空'
    if len(stripped) > 1000:
        return f'{field}长度不能超过 1000 字符'
    if not DESCRIPTION_RE.search(stripped):
        return f'{field}只能包含以下字符: 大小写字母、数字、下划线、连字符、汉字、空格、中英文标点符号（` < > " \' / \\ 除外）'
    
def validate_hours(hours, field='志愿时长'):
    if (not isinstance(hours, (int, float))) or isinstance(hours, bool):
        return f'{field}必须是数字'
    if hours <= 0:
        return f'{field}必须大于 0'
    if hours in (float('inf'), float('-inf')) or hours != hours:  # 检查是否为无穷大或NaN
        return f'{field}必须是有限的数字'
    if hours > 10000:
        return f'{field}不能超过 10000'
    return None
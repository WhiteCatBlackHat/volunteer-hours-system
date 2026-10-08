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

DESCRIPTION_RE = re.compile(r'^[\w\u4e00-\u9fa5\s\-\.,;:!?()@#$%^&*+=\[\]{}|~，。、；：！？（）…—·“”‘’『』「」]+$')

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
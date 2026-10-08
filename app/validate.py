import re

VALID_NAME_CHARS = re.compile(r'^[a-zA-Z0-9_\-\u4e00-\u9fff]+$')

def validate_name(name, field='名称'):
    if not isinstance(name, str):
        return f'{field}必须是字符串'
    stripped = name.strip()
    if not stripped:
        return f'{field}不能为空'
    if len(stripped) > 100:
        return f'{field}长度不能超过 100 字符'
    if not VALID_NAME_CHARS.search(stripped):
        return f'{field}只能包含以下字符: 大小写字母、数字、下划线、连字符、汉字'
    return None
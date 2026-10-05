import re

INVALID_NAME_CHARS = re.compile(r'[<>&\'"\\/?#%=*|]|\x00-\x1f|\x7f')

def validate_name(name, field='名称'):
    if not isinstance(name, str):
        return f'{field}必须是字符串'
    stripped = name.strip()
    if not stripped:
        return f'{field}不能为空'
    if len(stripped) > 200:
        return f'{field}长度不能超过 200 字符'
    if INVALID_NAME_CHARS.search(stripped):
        return f'{field}不能包含以下特殊字符: < > & \' " \\ / ? # % = * | 或控制字符'
    return None
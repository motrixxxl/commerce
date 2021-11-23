
def truncate(str, length, end='...'):
    substr = (str[:length] + end) if len(str) > 75 else str
    return substr

def map_func(func_name, data):

    if func_name == 'len':
        return len(data)
    elif func_name == 'str':
        return ', '.join(data)
    else:
        return None
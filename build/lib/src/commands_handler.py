from src.commands import *
command_map = {
    # "COMMAND": {"min": 0, "max": 0, "function": output_commands},
    "SET": {"min": 2, "max": 2, "function": set_command},
    "GET": {"min": 1, "max": 1, "function": get_command},
    "SADD": {"min": 2, "max": -1, "function": sadd_command},
    # "SPOP": {"min": 1, "max": 1, "function": spop_command},
    "SDIFF": {"min": 1, "max": -1, "function": sdiff_command},
    # "SINTER": {"min": 2, "max": -1, "function": sinter_command},
    # "SUNION": {"min": 2, "max": -1, "function": sunion_command},
    "FLUSH": {"min": 0, "max": 0, "function": flush_command},
    # "SAVE": {"min": 0, "max": 0, "function": save_command},
    # "EXISTS": {"min": 1, "max": 1, "function": exists_command},
    # "EXPIRE": {"min": 2, "max": 2, "function": expire_command},
    "TTL": {"min": 1, "max": 1, "function": ttl_command},
    # "DEL": {"min": 1, "max": 1, "function": del_command},
    "LPUSH": {"min": 2, "max": -1, "function": lpush_command},
    # "LPOP": {"min": 1, "max": 1, "function": lpop_command},
    # "LINDEX": {"min": 2, "max": 2, "function": lindex_command},
    # "LLEN": {"min": 1, "max": 1, "function": llen_command},
    "HSET": {"min": 3, "max": 3, "function": hset_command},
    "HGET": {"min": 2, "max": 2, "function": hget_command},
    # "HMGET": {"min": 2, "max": -1, "function": hmget_command},
    # "HMSET": {"min": 3, "max": -3, "function": hmset_command},
    # "HGETALL": {"min": 1, "max": 1, "function": hget_all_command}
}

def list_get(L, i, v=None):
    try: return L[i]
    except IndexError: return v

def handle_command(command_with_args):
    """
    :param : command with args
    :return: RESP structured respone to client
    """
    command = str(command_with_args[0]).upper() # capitialize letter
    if command not in command_map: 
        return not_implemented_command()
    matched_command = command_map[command]

    args = command_with_args[2:] or []
    key = list_get(command_with_args, 1, None)
    total_arg_length = len(args) + (1 if key is not None else 0)  # total length of key and args

    # validatethe length of param s
    if total_arg_length < matched_command["min"]: 
        return resp_error("Not enough arguments for command {0}, minimum {1}".format(command, matched_command["min"]))

    if matched_command["max"] >= 0: # max>=0
        if total_arg_length > matched_command["max"]: 
            return resp_error("Too many arguments for command {0}, maximum {1}".format(command, matched_command["min"]))
    else:   # max<0, could add any number or args
            # max=-1, any numbers of args ，max=-3, even numbers of params
        if matched_command["max"] == -3 and not total_arg_length % 2:   # not odd and it is even numbers of args
            return resp_error("Not enough arguments or an invalid number of arguments was specified")

    # 执行函数
    if len(args) > 0:
        return command_map[command]["function"](key, args)
    elif key is not None:
        return command_map[command]["function"](key)
    else:
        return command_map[command]["function"]()
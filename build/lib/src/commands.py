
"""
ref https://redis.io/topics/protocol
"""
import time
import gevent

from src.cache import cache



def not_implemented_command():
    return resp_error("not implemented")

def resp_string(val):   # simple strng
    return "+"+val+"\r\n"

def resp_bulk_string(val):  # complex string,  $+len(string)+\r\n
    return "$"+str(len(val))+"\r\n"+val+"\r\n"

def resp_error(val): # error
    return "-"+val+"\r\n"

def resp_integer(val): # Interger error
    return ":"+str(val)+"\r\n"

def resp_array(arr, depth=0):  # array *+len(arr)+\r\n
    val = "*"+str(len(arr))+"\r\n"
    for item in arr:    # destruct the array furthur
        if isinstance(val, list): # if array exists in subset of arry
            val += resp_array(item)
        else:
            if isinstance(item, int):
                val = val + ":" +item +'\r\n'
            elif isinstance(item, str):
                val = val + f"${len(item)}\r\n" +item +'\r\n'
            else:
                val = val +'$-1\r\n'

    return val

def no_such_key(val):
    return resp_error("no such key")

def ttl_command(key):
    """
    return the left time to expire or error
    :param key: the key to check the expiring time
    :return:
    """
    if key in cache.expiring: # if key is  there
        return resp_integer(int(cache.expiring[key]-time.time())) # 返回剩余时间
    else:
        return resp_error(f"NO KEY MATCHING {key} HAS AN EXPIRATION SET")


def set_expire_command(key, args):
    """
    Set ttl for user id, when user id expired, then run delete function
    :param id: user id as the key of expiration
    :param args: args[0] is the valid time 
    """

    def delete_when_expire(key):
        del cache.volatile_data[key]
        del cache.expiring[key]

    if key in cache.volatile_data:
        cache.expiring[key] = time.time() + args[0]
        # start a coroutine to delete expire key
        gevent.spawn_later(int(args[0]), delete_when_expire, key)
        
        return resp_bulk_string('ok')
    else:
        return f'no such key {key}'


def set_command(key:int, arr:list):
    with cache as ca:
        ca.volatile_data[key] = arr[0]
    return resp_bulk_string("OK")

def get_command(key: int) -> str:
    data = cache.volatile_data.get(key, None)
    if isinstance(data, str):
        return resp_bulk_string(data)
    if isinstance(data, int):
        return resp_integer(data)
    elif isinstance(data, set):
        return resp_array(data)
    elif isinstance(data, dict):
        return resp_error('hget?')

def sadd_command(key, args):
    """
    add value to set(), create a new set if set 
    :param key: the key in cache
    :param args: args[0] the value to be added
    :return:
    """
    if cache.volatile_data.get(key) is None:  # if key don't exist
        cache.volatile_data[key] = set(args)    # create a new set
        return resp_integer(len(cache.volatile_data[key])) # return the length of the set
    else:   # if key exists
        if isinstance(cache.volatile_data.get(key), set):  # set exists
            r = len(cache.volatile_data.get(key).intersection(set(args))) # the length of intersected value of two sets
            cache.volatile_data[key] = cache.volatile_data.get(key).union(set(args)) # union of 2 sets
            if r == 0: # element is duplicated
                return resp_integer(1)
            else:   # element exists
                return resp_integer(0)
        else:  # key exists, but not set
            return resp_error("KEY {0} IS NOT A SET.".format(args[1]))

def sdiff_command(key, args):
    """
    Use the first set find the different with other args
    func：args1.diff(args2).diff(args3)...
    :param key: first set
    :param args: other sets
    :return:
    """
    starting_set = cache.volatile[key]

    for st in args: # loop the sets
        if st in cache.volatile_data: # if key st exists
            if not isinstance(cache.volatile_data[st], set): # if st is not set
                return resp_error("KEY {0} IS NOT A SET.".format(st))
            else: # st is a set
                starting_set = starting_set.difference(cache.volatile_data[st])
        else: # key st not exist
            return resp_error("NO SUCH KEY {0} EXISTS".format(st))

    final_set = [] # create empty set
    for item in starting_set:
        final_set.append(resp_string(item))
    return resp_array(final_set) # return difference

def lpush_command(key, args):
    """
    push element to the left of array
    :parm key: list be pushed to 
    :parm args: one or more element
    :return :
    """
    if key not in cache.volatile_data:
        cache.volatile_data[key] = []
    cache.volatile_data[key] = args + cache.volatile_data[key]
    return resp_integer(len(cache.volatile_data[key]))


def hset_command(key, args):
    """
    Set the hash table as value, if it doesn't exist, create a new one
    :param key: hash key
    :param args: value
    :return 
    """
    hm = cache.volatile_data.get(key, None) # to ensure if key exists
    if hm is None:
        cache.volatile_data[key] = {args[0]: args[1]}
        return resp_integer(1)
    elif args[0] in hm:
        hm[args[0]] = args[1]
        return resp_integer(0)
    else:
        hm[args[0]] = args[1]
        return resp_integer(0)

def hget_command(key, args):
    """
    return the value of hash map by the key
    :param key: hash key
    :parm args: value field
    """
    hm = cache.volatile_data[key]
    if args[0] in hm:
        return resp_bulk_string(hm[args[0]])
    else:
        return no_such_key(args)

def save_commmand():
    cache.save_state
    return resp_string("OK")


def flush_command():
    cache.volatile_data.clear()
    cache.expiring.clear()
    return resp_string("OK")


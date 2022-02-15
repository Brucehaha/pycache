from loguru import logger

logger.add("file_1.log", rotation="500 MB")    # Automatically rotate too big file


def parse_array(array, size):
    """
    Convert the RESP code to compatible array 
    :param array:
    :param size:
    :return:
    """
    arr = []


    for i in range(0, len(array), 2): # find value with even index
        if command_map.get(array[i][0]) is not None:
            arr.append(command_map.get(array[i][0])(array[i:i+2]))
        else:
            print(array[i])

    return arr

def parse_simple_string(array): # parse simple string
    return array[1]

def parse_bulk_string(array): # Bulk Strings 
    string_byte_len = int(array[0][1:])
    if string_byte_len > 0:
        return array[1]
    else:
        return None

def parse_error(array): # RESP Errors
    return array[1]

def parse_int(array):   # RESP Integers
    return int(array[1])

command_map = {
    '*': parse_array,
    '+': parse_simple_string,
    '$': parse_bulk_string,
    '-': parse_error,
    ':': parse_int
}


def parse_command(strg, index):
    """
    Parse command from redis-cli
    :param str: command ref: https://redis.io/topics/protocol
    :param index:
    :return: command_arr: command arr
    """
    # remove CLRF "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n" to "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
    items = strg.split("\r\n") 
    logger.debug(strg)
    
    # return only the True value(not none or empty) ['*2', '$3', 'foo', '$3', 'bar']
    items = list(filter(lambda x: x, items)) 
    array_size = int(items[0][1:])  # size of array
    command_arr = parse_array(items[1:], array_size) # 解析数组
    return command_arr
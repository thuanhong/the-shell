from globbing import *
from os import environ


def convert_command(command_list):
    for number, ele in enumerate(command_list[1:], 1):
        if '$' in ele:
            command_list[number] = param_expansion(ele)
            if command_list[number] == False:
                return False
        if ele.startswith('~'):
            command_list[number] = titde_expansion(ele, environ)
        if any(x in ele for x in ['*', '?', '[', ']']):
            command_list[number] = handle_glob(ele)
        
    return command_list



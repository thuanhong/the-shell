#!/usr/bin/env python3
from built_ins import *
from logical import handle_logical
from handle_user_input import *
from os.path import exists
from os import getcwd, environ
from readline import parse_and_bind
from shlex import split


def path():
    """
    display current position from HOME
    get path of HOME from environ
    """
    try:
        if exists(environ['HOME']):
            current_path = getcwd()[len(environ['HOME']):]
        else:
            current_path = getcwd()
    except KeyError:
        current_path = getcwd()
    # change color of LOGNAME and path
    log = '\033[1m{}\033[0m'.format('code@intek-sh')
    log = '\033[32m{}\033[0m'.format(log)
    current_path = '\033[31m{}\033[0m'.format(":-" + current_path + "$ ")
    return log + current_path


def main():
    """
    handle main
    """
    exit_code = 0
    while True:
        try:
            command_full = input(path())
            # dynamic command completion when press tab
            parse_and_bind('tab: complete')
            # check input of user, if input missing closing quoting then continue input
            command_full = handle_user_input(command_full)
            while command_full != '':
                # divide command by logical "&&" and "||"
                command, command_full, logical = handle_logical(command_full)
                # convert command become another command to execute easier
                command = convert_command_list(split(command, posix=False), environ, exit_code)
                # execute functions build-ins
                if command[0] == 'printenv':
                    exit_code = print_env(command)
                elif command[0] == 'export':
                    exit_code = export(command)
                elif command[0] == 'unset':
                    exit_code = unset(command)
                elif command[0] == 'cd':
                    exit_code = cd(command)
                elif command[0] == 'exit':
                    exit(command)
                else:
                    exit_code = execute_shell(command)
                # check logical and exit code to break or continue
                if '&' in logical and exit_code != 0:
                    break
                elif logical == '||' and exit_code == 0:
                    break
        except SyntaxError as syn:
            exit_code = 1
            print(syn)
        except KeyboardInterrupt: # when press control + C
            exit_code = 130
            print('^C')
        except EOFError: # when press control + D
            print('exit')
            quit()
        except Exception as exp: # all other error
            exit_code = 1
            print('----Something was wrong----')
            print('Error : {}----'.format(exp))
            print("----Please input again, thanks----")


if __name__ == "__main__":
    main()

import os, sys, subprocess
from pathlib import Path
from dotenv import load_dotenv

dataFile = {'name': 'common',
            'description': 'Contains elements to reuse in other files'}

configEnv = {
    'pathBin': './bin/',
    'fileEnv': '.efde'
}

class bcolors:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    INFO_CYAN = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    DANGER = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def msgColor(msg, decorate=''):
    if decorate == 'HEADER':
        return bcolors.HEADER + msg + bcolors.ENDC
    elif decorate == 'INFO':
        return bcolors.INFO + msg + bcolors.ENDC
    elif decorate == 'INFO_CYAN':
        return bcolors.INFO_CYAN + msg + bcolors.ENDC
    elif decorate == 'SUCCESS':
        return bcolors.SUCCESS + msg + bcolors.ENDC
    elif decorate == 'WARNING':
        return bcolors.WARNING + msg + bcolors.ENDC
    elif decorate == 'DANGER':
        return bcolors.DANGER + msg + bcolors.ENDC
    elif decorate == 'BOLD':
        return bcolors.BOLD + msg + bcolors.ENDC
    elif decorate == 'UNDERLINE':
        return bcolors.UNDERLINE + msg + bcolors.ENDC
    else:
        return msg


def checkYesNo(message, default='y'):
    valuesYes = {'yes', 'y'}
    valuesNo = {'no', 'n'}
    selectDefault = 'Y/n' if default.lower() in valuesYes else 'y/N'
    choice = input("%s (%s) " % (message, selectDefault))
    if choice == '':
        choice = default
    if choice.lower() in valuesYes:
        return True
    elif choice.lower() in valuesNo:
        return False
    else:
        sys.stdout.write("Please respond with 'YES' or 'NO' \n")
        checkYesNo(message)


def menu_print(data, menuData=[], showHelper=False):
    print(
        msgColor(
            f"-------------------------------\n{menuData['name'].upper()}\n{menuData['description']}\n-------------------------------",
            'INFO_CYAN'
        )
    )
    print('Select an option \n')
    for key, val in enumerate(data):
        if not (showHelper):
            print(f"{'{:02d}'.format(key)}) {val['title']}")
        else:
            print(
                (f"{'{:02d}'.format(key)}) {val['title']} \t {val['description']}").expandtabs(25))

    print(
        msgColor('\nPress q:quit | r:retry | h:helper', 'WARNING')
    )


def cli(command, show=False):  # ToDo: Detect operating system and apply replacements example (ls | dir)
    if show:
        print(msgColor(
            msgColor(
                f'RUN Command \n{command}\n________________________',
                'INFO_CYAN'
            ), 'BOLD')
        )
    os.system(command)

def cliReturn(command, show=False):
    return subprocess.check_output(command, shell=True)

def filePathEnv(): return (configEnv['fileEnv'])


def fileEnvExists(view=True):
    exists = os.path.exists(filePathEnv())
    # ToDo: check utility
    #if (exists and view):
        #confirm = checkYesNo(
        #    f"Desea ver el contenido del archivo {configEnv['fileEnv']}?", 'n')
        #if confirm:
        #    fileEnvGet()

    return exists


def fileEnvCreateFile():
    cli(f"touch {filePathEnv()}")


def fileEnvGet():
    if (fileEnvExists(False)):
        print('______________________________________________')
        cli(f"cat {filePathEnv()}")
        print('______________________________________________\n')

# Set environment variables
#os.environ['API_USER'] = 'username'
#os.environ['API_PASSWORD'] = 'secret'

# Get environment variables
#USER = os.getenv('API_USER')
#PASSWORD = os.environ.get('API_PASSWORD')

# Getting non-existent keys
# FOO = os.getenv('FOO') # None
# BAR = os.environ.get('BAR') # None
# BAZ = os.environ['BAZ'] # KeyError: key does not exist.


def fileEnvReading(variable=''):
    if (not (fileEnvExists(False))):
        return
    if (variable == ''):
        print('Indicate the variable you want')

    dotenv_path = Path(filePathEnv())
    load_dotenv(dotenv_path=dotenv_path)
    return (os.environ.get(variable))


def fileEnvWrite(name, value):
    with open(filePathEnv(), 'a') as f:
        f.write(f'{name}="{value}"\n')

def existsPath(path, debug = False):
    result = os.path.exists(path)
    if not result and debug:
        print(msgColor(f'The indicated path does not exist\n {path}','DANGER'))
    return result

def isDirectory(directory, debug = False):
    result = existsPath(directory, debug)
    if not result:
        return result

    result = os.path.isdir(directory) 
    if not result and debug:
        print(msgColor(f'The given path is not a directory\n {directory}','DANGER'))

    return result

def isEmptyDirectory(directory, debug = False):
    
    result = isDirectory(directory, debug)
    if not result:
        return False
    
    result = os.listdir(directory)
    if result and debug:
        print(msgColor(f'The directory is not empty. \n {directory}\n Content:','DANGER'))
        cli(f'cd {directory} && ls -la')

    return not result


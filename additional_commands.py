from os import name, system

def c_red(text):    return '\033[91m' + text + '\033[0m'
def c_green(text):  return '\033[92m' + text + '\033[0m'
def c_yellow(text): return '\033[93m' + text + '\033[0m'
def c_blue(text):   return '\033[94m' + text + '\033[0m'
def c_pink(text):   return '\033[95m' + text + '\033[0m'
def c_cyan(text):   return '\033[96m' + text + '\033[0m'
def clean(): system('cls' if name == 'nt' else 'clear')

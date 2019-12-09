import os
import string
import sys
from subprocess import Popen, PIPE, STDOUT
import re
import ordononceur
import pprint
import time
import io

global args
args = ""
list_commands_alias = {}

if __name__ == '__main__':
    print("Reading profile...")
    f = open('profile', "r")
    lines = f.readlines()
    print("Verifying file syntax...")
    if lines[0][:4] != "PATH":
        raise ValueError('PATH does not exist in profile!!.')
    if lines[1][:4] != "HOME":
        raise ValueError('HOME does not exist in profile!!.')
    path = lines[0][5:]
    home = lines[1][5:]
    f.close()
    ruler = '='
    home = home.strip()
    pwd1 = Popen(['bin/printwd'], stdout=PIPE, stdin=PIPE, stderr=PIPE, encoding="utf-8").communicate()[0]
    print("Getting current directory...")
    print("Changing directory to ", home)
    os.chdir(home)
    pwd1 = pwd1.strip()+"/bin/"
    path_tmp = (pwd1.split()[0] + "/bin:" + path)
    path = path_tmp


    def do_help(ret=None):
        for key, val in list_commands.items():
            print(key + "\t\t", "\t\t", list_commands[key][1])
        return list_commands


    def do_aliases(ret=None):
        for key, val in list_commands_alias.items():
            print(key, "\t\t", list_commands_alias[key][1])
        return list_commands_alias


    def do_alias(ret=None):
        global args
        ali = args[0].split("=")
        list_commands_alias[ali[0]] = [' '.join(args[:]).split("=")[1].split("\"")[1],
                                       ' '.join(args[:]).split("=")[1].split("\"")[1]]


    def do_execfile(ret=None):
        f = open(args[0], "r")
        tmp = f.read()
        f.close()
        tmp2 = re.split(';|\n', tmp)
        for t in tmp2:
            execute(t)


    def do_ls(ret=None):
        return \
            Popen([pwd1 + 'lest'], stdout=PIPE, encoding="utf-8").communicate(
                input=str.encode(ret) if ret else None)[0]


    def do_cat2(ret=None):
        if args:
            return Popen([pwd1 + 'cat2'] + args, stdout=PIPE, encoding="utf-8").communicate(
                input=str.encode(ret) if ret else None)[0]
        else:
            return Popen([pwd1 + 'cat2'], stdout=PIPE, stdin=ret, encoding="utf-8").communicate()[0]


    def do_pwd(ret=None):
        return Popen([pwd1 + 'printwd'], stdout=PIPE, encoding="utf-8").communicate(
            input=str.encode(ret) if ret else None)[0]


    def do_cd(ret=None):
        global args
        os.chdir(args[0])


    def start(ret=None):
        while 1:
            os.system("clear")

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint("************MAIN MENU**************")
            inpu = input("""
                1:\tExecute commands
                2:\tExecute Algorithm
                >>""")
            if inpu == "1":
                pp.pprint("Type ? or help to list commands")
                run()
            elif inpu == "2":
                ordononceur.main2()


    def shell(inp2, ret=None):
        list_ = inp2.strip().split(" ")
        command = list_[0]
        global args
        args = list_[1:]
        if ">" in list_:
            p = [i for i, x in enumerate(args) if x == ">"][0]
            file1 = list_[-1]
            f = open(file1, "w+")
            f.write(shell(' '.join(list_[:p + 1])))
            f.close()

        elif "<" in list_:
            file1 = list_[-1]
            with open(file1, "r") as f:
                out = shell(' '.join(list_[:-2]), f)
                print(out)

        elif command in list_commands_alias.keys():
            return shell(list_commands_alias[command][0])

        elif command in list_commands:
            return list_commands[command][0](ret)
        else:
            print("Command not found")


    def execute(inp):
        if "|" in inp:
            ouput = None
            splited = inp.split("|")
            for s in splited:
                s.strip()
                ouput = shell(s, ouput)
            if ouput:
                print(ouput)
        sh = shell(inp)
        if sh and type(sh) != dict:
            print(sh)


    def run():
        global args
        while 1:
            pwd = os.popen('pwd').read().split("\n")[0]
            inp = input(str(pwd) + "> ").strip()
            try:
                execute(inp)
            except:
                print("Could not execute ", inp)


    list_commands = {"execfile": [do_execfile, "execute file"],
                     "aliases": [do_aliases, "show aliases"],
                     "exit": [start, "return to main menu"],
                     "lest": [do_ls, "list directory contents"],
                     "cd": [do_cd, "change the working directory"],
                     "help": [do_help, "print this menu"],
                     "alias": [do_alias, "define or display aliases"],
                     "?": [do_help, "print this menu"],
                     "printwd": [do_pwd, "print name of current/working directory"],
                     "cat2": [do_cat2, "concatenate files and print on the standard output"]}
    time.sleep(1)
    start()

# TODO add more commands

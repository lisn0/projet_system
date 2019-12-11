import string
import sys
from subprocess import Popen, PIPE, STDOUT
import re
import ordononceur
from ordononceur import content
import pprint
import time
import io
from termcolor import colored

global args
args = ""
list_commands_alias = {}

if __name__ == '__main__':
    def start(ret=None):
        """
        Main menu
        :param ret: not needed
        """
        while 1:
            "Used to clear screen"
            ordononceur.os.system("clear")

            print(colored("************MAIN MENU**************", "white", attrs=['blink']))
            inpu = input(colored("""
                1:\tExecute commands
                2:\tExecute Algorithm
                >>""", 'white'))
            if inpu == "1":
                print(colored("Type ? or help to list commands", 'yellow', attrs=['dark']))
                while 1:
                    pwd = do_pwd()
                    inp = input(colored(str(pwd), 'cyan', 'on_grey') + "> ").strip()
                    if inp != "":
                        execute(inp)

            elif inpu == "2":
                ordononceur.main2(content)


    def execute(inp):
        """
        Call shell and print it possible
        :param inp: User input
        """
        try:
            sh = shell(inp)
            if sh and type(sh) != dict:
                print(colored(sh, 'white'))
        except:
            print(colored('An error occurred', 'red'), colored(inp, 'green'))


    def shell(inp2, ret=None):
        """

        :param inp2: command
        :param ret: Used to store redirected output and determine if the is a redirection
        :return: return output as a string so it can be used in another shell method
                    by the ret argument to handle redirections
        """
        global args
        if "|" in inp2:
            """
            If pipe found split input into several commands and redirect command output to the input of the other command
            call shell function again to handle all the commands separately 
            """
            ouput = None
            for s in inp2.split("|"):
                s.strip()
                ouput = shell(s, ouput)
            if ouput and type(ouput) != dict:
                print(ouput)
        else:
            """
            split command to a list to determinate the arguments
            """
            list_ = inp2.strip().split(" ")
            command = list_[0]
            args = list_[1:]

            if ">" in list_:
                """
                Find '>' position and write to the file
                """
                p = [i for i, x in enumerate(args) if x == ">"][0]
                file1 = list_[-1]
                with open(file1, "w+") as f:
                    f.write(shell(' '.join(list_[:p + 1])))

            elif "<" in list_:
                """
                Read specified file and call shell function with the file as input (f)
                """
                file1 = list_[-1]
                with open(file1, "r") as f:
                    out = shell(' '.join(list_[:-2]), f)
                    print(out)

            elif command in list_commands_alias.keys():
                """
                Test to see if the command is an alias and execute it by calling the shell function
                """
                return shell(list_commands_alias[command][0])

            elif command in list_commands:
                """
                If command found in list_commands  execute the function the we defined with ret as argument if needed 
                """
                return list_commands[command][0](ret)
            else:
                print(colored("Command not found", 'red', attrs=['bold', 'dark']),
                      colored(command, 'yellow',  attrs=['bold', 'dark', 'underline']))


    def do_help(ret=None):
        """
        print help
        :param ret: not used
        :return: return in case of pipe usage
        """
        for key, val in list_commands.items():
            print("{: <20} {: <20}".format(colored(key, 'yellow'), colored(list_commands[key][1]), 'red'))
        return list_commands


    def do_aliases(ret=None):
        """
        print saved aliases
        :param ret: not used
        :return: return in case of pipe usage
        """
        for key, val in list_commands_alias.items():
            print("{: <20} {: <20}".format(colored(key, 'yellow'), colored(list_commands_alias[key][1]), 'red'))
        return list_commands_alias


    def do_alias(ret=None):
        """
        Manipulate alias argument and save it in form of a command  
        :param ret: not used
        """
        global args
        ali = args[0].split("=")
        list_commands_alias[ali[0]] = [' '.join(args[:]).split("=")[1].split("\"")[1],
                                       ' '.join(args[:]).split("=")[1].split("\"")[1]]

    

    def do_echo(ret=None):
        """
        Print argument or redirected output
        :param ret: used in case there is a redirected input to the command
        :return:
        """
        try:
            return args[0] if args[0] else ret
        except:
            return ret if ret else args[0]

    def do_execfile(ret=None):
        """
        Read command argument as file, split file content when in ; or new line and execute them separately.
        Pipes and redirections will be handled by the shell function
        :param ret: not used
        """
        with open(args[0], "r") as f:
            tmp = f.read()
            tmp2 = re.split(';|\n', tmp)
            for t in tmp2:
                if t:
                    execute(t)


    def do_ls(ret=None):
        """
        Execute the lest command
        :param ret: used in case there is a redirected input to the command
        :return: return in case the output is used in another command (PIPE or redirections)
        """
        return \
            Popen([pwd1 + 'lest'], stdout=PIPE, encoding="utf-8").communicate(
                input=str.encode(ret) if ret else None)[0]


    def do_cat2(ret=None):
        """
        Execute the cat2 command
        :param ret: used in case there is a redirected input to the command
        :return: return in case the output is used in another command (PIPE or redirections)
        """
        if args:
            """
            If there is an argument the command will execute with the said argument
            """
            return Popen([pwd1 + 'cat'] + args, stdout=PIPE, encoding="utf-8").communicate(
                input=str.encode(ret) if ret else None)[0]
        else:
            try:
                """
                Try to use a file as input (ret in stdin) 
                If failed the input (ret: string) will be handled by the communicate() method
                """
                return Popen([pwd1 + 'cat'], stdout=PIPE, stdin=ret, encoding="utf-8").communicate()[0]
            except:
                return Popen([pwd1 + 'cat'], stdout=PIPE, encoding="utf-8").communicate(
                    input=str.encode(ret) if ret else None)[0]


    def do_pwd(ret=None):
        """
        :param ret: used in case there is a redirected input to the command
        :return: return in case the output is used in another command (PIPE or redirections)
        """
        return Popen([pwd1 + 'printwd'], stdout=PIPE, encoding="utf-8").communicate()[0]


    def do_touch(ret=None):
        """
        change file timestamps
        :param ret:
        :return:
        """
        if args:
            """
            If there is an argument the command will execute with the said argument
            """
            return Popen([pwd1 + 'touch'] + args, stdout=PIPE, encoding="utf-8").communicate(
                input=str.encode(ret) if ret else None)[0]
        else:
            try:
                """
                If pipe use the previous command as argument
                """
                return Popen([pwd1 + 'touch'] + [ret.strip()], stdout=PIPE, encoding="utf-8").communicate()[0]
            except:
                print(colored("""Usage: touch2 file_to_create,\tor command | touch2""", 'green'))


    def do_cd(ret=None):
        """
        Will change directory just like the function in C programming language
        :param ret: Not used
        """
        try:
            global args
            ordononceur.os.chdir(args[0])
        except:
            ordononceur.os.chdir(ret)



    list_commands = {"execfile":     [do_execfile,       "execute file"],
                     "aliases":      [do_aliases,        "show aliases"],
                     "touch2":       [do_touch,          "change file timestamps. create file if does not exist"],
                     "exit":         [start,             "return to main menu"],
                     "lest":         [do_ls,             "list directory contents"],
                     "cd":           [do_cd,             "change the working directory"],
                     "help":         [do_help,           "print this menu"],
                     "alias":        [do_alias,          "define or display aliases"],
                     "?":            [do_help,           "print this menu"],
                     "printwd":      [do_pwd,            "print name of current/working directory"],
                     "cat2":         [do_cat2,           "print files on the standard output"],
                     "echo":         [do_echo,           "display line of text/string"]}
    print("Reading profile...")
    with open('profile', "r") as f:
        lines = f.readlines()
        print("Verifying file syntax...")
        if lines[0][:4] != "PATH":
            raise ValueError('PATH does not exist in profile!!.')
        if lines[1][:4] != "HOME":
            raise ValueError('HOME does not exist in profile!!.')
        path = lines[0][5:]
        home = lines[1][5:]
    ruler = '='
    home = home.strip()
    pwd1 = Popen(['bin/printwd'], stdout=PIPE, stdin=PIPE, stderr=PIPE, encoding="utf-8").communicate()[0]
    print("Getting current directory...")
    print("Changing directory to ", home)
    do_cd(home)
    pwd1 = pwd1.strip() + "/bin/"
    path = (pwd1.split()[0] + "/bin:" + path)

    time.sleep(1)
    start()


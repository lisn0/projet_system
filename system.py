import os
import string
import sys
import subprocess
import re


global args 
args = ""
list_commands_alias = {}

if __name__ == '__main__':
    list_commands_tmp = {}
    print("Reading profile...")
    f = open('profile', "r")
    lines = f.readlines()
    if lines[0][:4] != "PATH":
        raise ValueError('PATH does not exist in profile!!.')
    if lines[1][:4] != "HOME":
        raise ValueError('HOME does not exist in profile!!.')
    path = lines[0][5:]
    home = lines[1][5:]
    f.close()
    ruler = '='
    home = home.strip()
    pwd = os.popen('pwd').read()
    #print("Getting current directory...")
    #print(pwd)
    #print("Changing directory to HOME...")
    os.chdir(home)
    
    def do_help():
        for key, val in list_commands.items():
            print(key, "\t\t",list_commands[key][1])
    def do_aliases():
        for key, val in list_commands_alias.items():
            print(key, "\t\t",list_commands_alias[key][1])

    def do_alias():
        global args
        #print(args)
        ali = args[0].split("=")
        #print(ali[0])
        list_commands_alias[ali[0]] = [' '.join(args[:]).split("=")[1].split("\"")[1], ' '.join(args[:]).split("=")[1].split("\"")[1]]
    
    def do_execfile():
        f = open(args[0], "r")
        tmp = f.read()
        f.close()
        tmp2 = re.split('; |\n',tmp)
        run(tmp2)

    def do_ls():
        c = os.popen("lest").read()
        print(c)
        
    def do_cat2():
        c = os.popen("cat2 " + " ".join(args[:])).read()
        print(c)
        
    def do_pwd():
        os.system("printwd")

    def do_cd():
        global args
        os.chdir(args[0])
    def do_pass():
        pass
    
    def run(tm):
        for t in tm:
          pwd = os.popen('pwd').read().split("\n")[0]
          inp = t
          list_ = inp.split(" ")
          command = list_[0]
          args = list_[1:]
          if command in list_commands:
              list_commands[command][0]()
          else:
              os.system(inp)


    list_commands = { "execfile":   [   do_execfile,   "execute file"],
                     "aliases":     [   do_aliases,    "show aliases"],
                     "lest":        [   do_ls,         "list directory contents"],
                     "cd":          [   do_cd,         "change the working directory"],
                     "help":        [   do_help,       "print this menu"],
                     "alias":       [   do_alias,      "define or display aliases"],
                     "?":           [   do_help,       "print this menu"],
                     "printwd":     [   do_pwd,        "print name of current/working directory"],
                     "cat2":        [   do_cat2,       "concatenate files and print on the standard output"],
                     "pass":        [   do_pass,       "pass"]}
    
    print("Greetings! Type ? or help to list commands")
    
    while 1:
        pwd = os.popen('pwd').read().split("\n")[0]
        inp = input(str(pwd)+ "> ")
        list_ = inp.split(" ")
        command = list_[0]
        args = list_[1:]
        if ">" in list_:
          p =  [i for i,x in enumerate(args) if x == ">"][0]
          tmp = os.popen(command +" "+ " ".join(args[:p])).read()
          file1 = list_[-1]
          f = open(file1, "w+")
          f.write(tmp)
          f.close()

        elif "<" in list_:
          file1 = list_[-1]
          f = open(file1, "r")
          tmp = f.read()
          f.close()
          tmp = os.system( "echo '" +tmp + "' | " + command+" "+ args[0])

        elif command in list_commands_alias.keys():
            run([list_commands_alias[command][0]])
        elif command in list_commands:
            list_commands[command][0]()
        else:
            os.system(inp)


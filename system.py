import os
import string
import sys
import subprocess
import re
import ordononceur
import pprint
import time

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
    pwd = os.popen('pwd').read()
    #subprocess.Popen(["export","PATH=$PATH:"+pwd+"bin"])

    print("Getting current directory...")
    #print(pwd)
    print("Changing directory to ", home)
    os.chdir(home)
    
    path_tmp=(pwd.split()[0]+"/bin:"+path)
    path=path_tmp
    
    def do_help():
        for key, val in list_commands.items():
            print(key+"\t\t", "\t\t",list_commands[key][1])
            
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
        run2(tmp2)

    def do_ls():
        c = os.popen("/run/media/berika/TWICE/berika/github/bin/lest").read()
        print(c)
        
    def do_cat2():
        c = os.popen("/run/media/berika/TWICE/berika/github/bin/cat2 " + " ".join(args[:])).read()
        print(c)
        
    def do_pwd():
        pwdtmp= os.popen("/run/media/berika/TWICE/berika/github/bin/printwd").read()
        print(pwdtmp)
        
    def do_cd():
        global args
        os.chdir(args[0])
            
    def start():
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
            elif inpu =="2":
                ordononceur.main2()

    def run2(tm):
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
    
    def run():
        global args
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
                run2([list_commands_alias[command][0]])
                
            elif command in list_commands:

                list_commands[command][0]()
            else:
                os.system(inp)


    list_commands = {"execfile":    [   do_execfile,   "execute file"                                       ],
                     "aliases":     [   do_aliases,    "show aliases"                                       ],
                     "exit":        [   start,     "return to main menu"                                ],
                     "lest":        [   do_ls,         "list directory contents"                            ],
                     "cd":          [   do_cd,         "change the working directory"                       ],
                     "help":        [   do_help,       "print this menu"                                    ],
                     "alias":       [   do_alias,      "define or display aliases"                          ],
                     "?":           [   do_help,       "print this menu"                                    ],
                     "printwd":     [   do_pwd,        "print name of current/working directory"            ],
                     "cat2":        [   do_cat2,       "concatenate files and print on the standard output" ]}
    time.sleep(1)

    start()

import os
import string
global args 
args = ""


if __name__ == '__main__':
    #print("Reading profile...")
    f = open('profile', "r")
    lines = f.readlines()
    if lines[0][:4] != "PATH":
        raise ValueError('PATH does not exist in profile!!.')
    if lines[1][:4] != "HOME":
        raise ValueError('HOME does not exist in profile!!.')
    path = lines[0][5:]
    home = lines[1][5:]
    f.close()
    home = home.strip()
    pwd = os.popen('pwd').read()
    #print("Getting current directory...")
    #print(pwd)
    #print("Changing directory to HOME...")
    os.chdir(home)
    
    def do_help():
        for key, _ in list_commands.items():
            print(key)

    def do_ls():
        os.system("ls")
    
    def do_cd():
        global args
        print("Changing directory... '{}'".format(args))
        os.chdir(args[0])

    list_commands = {"ls": do_ls, "cd": do_cd, "help": do_help, "?": do_help}
    print("Greetings! Type ? or help to list commands")
    while 1:
        
        inp = input("cmd> ")
        
        list_ = inp.split(" ")
        command = list_[0]
        args = list_[1:]
        if command in list_commands:
            list_commands[command]()
        else:
            print("unkonwn command..")
            
    
    
 

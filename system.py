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
    
    def do_pwd():
        os.system("pwd")

    def do_cd():
        global args
        os.chdir(args[0])

    list_commands = {"lest": do_ls, "cd": do_cd, "help": do_help, "?": do_help, "pwd": do_pwd}
    print("Greetings! Type ? or help to list commands")
    while 1:
        pwd = os.popen('pwd').read().split("\n")[0]
        inp = input(str(pwd)+ ">")

        list_ = inp.split(" ")
        command = list_[0]
        args = list_[1:]
        if ">" in list_ and command == "pwd":
            pwd = os.popen('pwd').read()
            file1 = list_[-1]
            f = open(file1, "w+")
            f.write(pwd)
            f.close()
        
        elif command in list_commands:
            list_commands[command]()
        else:
            os.system(inp)
            

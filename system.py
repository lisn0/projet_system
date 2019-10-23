from cmd import Cmd
import os
import string

class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Greetings! Type ? to list commands"
     
    def do_exit(self, inp):
        """exit the application. Shorthand: x q Ctrl-D."""
        print("Exiting..")
        return True
             
    def do_cd(self, inp):
        """Change directory."""
        #print("Changing directory... '{}'".format(inp))
        os.chdir(inp)
        
    def do_pwd(self, inp):
        """Get current directory!!"""
        #print("Getting current directory..... '{}'".format(inp))
        print(os.popen('pwd').read())

    def help_help(self, inp):
        """Get current directory!!"""
        

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
     
        print("Unknown command: {}".format(inp.split(" ")[0]))
     
    do_EOF = do_exit
     
if __name__ == '__main__':
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
    home = home.strip()
    pwd = os.popen('pwd').read()
    print("Getting current directory...")
    print(pwd)
    print("Changing directory to HOME...")
    os.chdir(home)
    MyPrompt().cmdloop('Starting interpreter...')
    
    
    
 

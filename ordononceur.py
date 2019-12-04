import tkinter as tk
import random
from operator import itemgetter 
import os
data = []

with open("data") as f:
   junk = f.read()
   for i in junk.split("\n"):
       try:
        a, b,c = i.split(",")
        data.append((int(a),int(b),int(c)))
       except:
           pass



def roundrobin(data):
    total_time = 0 
    total_time_counted = 0
    # proc is process list
    proc = []
    wait_time = 0
    turnaround_time = 0
    #for _ in range(total_p_no):
        #Getting the input for process
        #print("Enter process arrival time and burst time") 
        #input_info = list(map(int, input().split(" ")))
        #print(input_info)
        #arrival, burst, remaining_time = input_info[0], input_info[1], input_info[1]
        #processes are appended to the proc list in following format
        #proc.append([arrival, burst, remaining_time, 0])
        #total_time gets incremented with burst time of each process
        #total_time += burst
    for i in data:
        arrival, burst, remaining_time = i[0], i[1], i[1]
        proc.append([arrival, burst, remaining_time, 0])
        total_time += burst
    print("Enter time quantum")
    time_quantum = 2
    # Keep traversing in round robin manner until the total_time == 0
    while total_time != 0:
        # traverse all the processes
        for i in range(len(proc)):
            # proc[i][2] here refers to remaining_time for each process i.e "i"
            if proc[i][2] <= time_quantum and proc[i][2] >= 0:
                total_time_counted += proc[i][2]
                total_time -= proc[i][2]
                # the process has completely ended here thus setting it's remaining time to 0.
                proc[i][2] = 0 
            elif proc[i][2] > 0:
                # if process has not finished, decrementing it's remaining time by time_quantum
                proc[i][2] -= time_quantum
                total_time -= time_quantum
                total_time_counted += time_quantum
            if proc[i][2] == 0 and proc[i][3] != 1:
                # if remaining time of process is 0
                # and 
                # individual waiting time of process has not been calculated i.e flag
                wait_time += total_time_counted - proc[i][0] - proc[i][1]
                turnaround_time += total_time_counted - proc[i][0]
                # flag is set to 1 once wait time is calculated
                proc[i][3] = 1 
    #print("\nAvg Waiting Time is ", (wait_time * 1) / total_p_no)
    l= []
    j=0
    for i in proc:
        j+=1
        l.append([j] + i[:2])
    #print("Avg Turnaround Time is ", (turnaround_time * 1) / total_p_no)
    return l

def graph(data):
	root = tk.Tk()
	root.title("Ordononceur")
	c_width = len(data)*60+10
	c_height = 150
	c = tk.Canvas(root, width=c_height, height=c_width, bg='white')
	c.pack()
	x_stretch = 20 
	x_width = 40 
	x_gap = 15 
	count=0
	i=0
	for x,y in enumerate(data):
	    i+=1
	    x0 = x * x_stretch + x * x_width + x_gap
	    x1 = x * x_stretch + x * x_width + x_width + x_gap
	    s=max(count,y[1])
	    color = '{:06x}'.format(random.randint(0,0x1000000))
	    c.create_rectangle(50, x0, 90,x1, fill=('#'+ color),activefill="blue")
	    c.create_text(70,x0 + 16, anchor=tk.SW, text=str(y[0]),activefill="black",fill="white",font="1")
	    if i ==1:
	        c.create_text(105,x0 +8 , anchor=tk.SW, text=str(s))
	    count=s+y[2]
	    c.create_text(105, x1+8, anchor=tk.SW, text=str(count))

	root.mainloop()

def selectionSort(alist,s):
	   for i in range(len(alist)):
	       minPosition = i
	       for j in range(i+1, len(alist)):
	           if alist[minPosition][s] > alist[j][s]:
	               minPosition = j
	       temp = alist[i]
	       alist[i] = alist[minPosition]
	       alist[minPosition] = temp
	   return alist


def get_sj(alist,index):
    temp=[alist[0],]
    for i in alist[1:]:
        if i[1] <= index:
            temp.append(i)
        else:
            break
    return selectionSort(temp,2)[0]


def main2():
    os.system("clear")
    inpt=input("""Choose an algorithm:
        1 - FCFS
        2 - SJF
        3 - Round Robin
        >>""")
    if inpt == "1":
        graph(sorted(data, key = itemgetter(1)))
    elif inpt == "2":
        alist=selectionSort(data,1)
        index=alist[0][1]
        temp=[]
        while len(alist) > 0 :
            k=get_sj(alist,index)
            temp.append(k)
            index+=k[2]
            print (k[2])
            alist.remove(k)
        graph(temp)
    elif inpt == "3":
        graph(roundrobin(data))

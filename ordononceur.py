import tkinter as tk
import random


data = [[1, 2 ,1], [2, 1 ,3],[3,2,3]]

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

def main2():
    def get_sj(alist,index):
        temp=[alist[0],]
        for i in alist[1:]:
            if i[1] <= index:
                temp.append(i)
            else:
                break
        return selectionSort(temp,2)[0]
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


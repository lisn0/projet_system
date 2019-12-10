import tkinter as tk
import random
from operator import itemgetter
import os

content = []


"Read process info from file"
with open("content") as f:
    filee = f.read()
    for i in filee.split("\n"):
        try:
            a, b, c = i.split(",")
            content.append([int(a), int(b), int(c)])
        except:
            print("Error reading content file")


def round(content, quantum=2):
    """
    Round-robin scheduling
    :param content:
    :param quantum:
    :return:
    """
    slist = content
    current = content[0][1]
    junks = available(slist, current, 1)
    lis = []
    while len(slist) > 0:
        for junk in junks:
            sub = min(quantum, junk[2])
            lis.append((junk[0], junk[1], sub))
            junk[2] -= sub
            junk[1] += sub
            if junk[2] < 1:
                slist.remove(junk)
        if slist:
            current = max(current, slist[0][1])
            junks = sorted(available(slist, current, 1), key=itemgetter(1))
    return lis


def draw(content):
    """
    Create Gui
    :param content: Contain processes
    """
    root = tk.Tk()
    root.title("Ordononceur")
    c = tk.Canvas(root, width=150, height=len(content) * 60 + 10, bg='white')
    c.pack()
    count = 0
    i = 0
    for x, d in enumerate(content):
        i += 1
        width0 = x * 60 + 20
        width1 = x * 60 + 55
        m = max(count, d[1])
        color = '{:06x}'.format(random.randint(0, 0x1000000))
        c.create_rectangle(50, width0, 95, width1, fill=('#' + color), activefill='black')
        c.create_text(70, width0 + 25, anchor=tk.SW, text=str(d[0]), activefill="black", fill="white", font="1")
        if i == 1:
            c.create_text(100, width0 + 10, anchor=tk.SW, text=str(m))
        count = m + d[2]
        c.create_text(100, width1 + 10, anchor=tk.SW, text=str(count))
    root.mainloop()


def available(processlist, current, pos):
    """
    Get processes with arriving time less than current time
    :param processlist: list of processes
    :param current: current time
    :param pos: How to sort
    :return:
    """
    junk = [processlist[0], ]
    for i in processlist[1:]:
        if i[1] <= current:
            junk.append(i)
        else:
            break
    if pos == 1:
        return sorted(junk, key=itemgetter(1))
    else:
        return sorted(junk, key=itemgetter(2))[0]


def sjf(content):
    """
    Shortest Job First scheduling
    :param content:
    :return:
    """
    processlist = sorted(content, key=itemgetter(1))
    current = processlist[0][1]
    junk = []
    while len(processlist) > 0:
        k = available(processlist, current, 2)
        junk.append(k)
        current += k[2]
        processlist.remove(k)
    return junk


def main2(content):
    """

    :param content: Contain process list
    """
    os.system("clear")
    inpt = input("""Choose an algorithm:
		1 - FCFS
		2 - SJF
		3 - Round Robin
		>>""")
    if inpt == "1":
        draw(sorted(content, key=itemgetter(1)))

    elif inpt == "2":
        draw(sjf(content))

    elif inpt == "3":
        draw(round(content))

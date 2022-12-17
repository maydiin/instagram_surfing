import shutil
import webbrowser
from tkinter import *
import instaloader as il
import random
import json
import os, glob
from instabot import *
import time

root = Tk()
root.geometry("600x600")


class Catg:
    def __init__(self, userName, password):
        self.catgInf = []
        self.postsinfo_ofcatg = []
        self.orderedposts = []
        self.userName = userName
        self.password = password

    def addacc(self, i):
        self.catgInf.extend(i)

    def addposttomlc(self, i):
        self.postsinfo_ofcatg.extend(i)

    def removeacc(self, i):
        self.catgInf.remove(i)

    def removeposts(self, i):
        self.postsinfo_ofcatg.pop(i)

    def addto_order(self, i):
        self.orderedposts.extend(i)


catgs = []
catgstoshow = []

for filename in glob.glob('catgs\*.txt'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        j = json.load(f)
        kkk = Catg(j[0][0], j[0][1])
        kkk.addacc(j[0][2])
        kkk.addposttomlc(j[1])
        catgs.append(kkk)
        catgstoshow.append(kkk)

def ordered(liste):
    maxlist = 0
    for i in liste:
        if len(i) > maxlist:
            maxlist = len(i)

    ol = []
    m = 0
    while m < maxlist:
        for j in liste:
            if m < len(j):
                ol.append(j[m])
            else:
                continue
        m += 1

    return ol


def addAcc(x, y):
    if y != "":
        x.addacc(y)


def saveposts(i):
    ig = il.Instaloader()

    for j in i.catgInf:
        cl = []
        profile = il.Profile.from_username(ig.context, j)
        c = sorted(profile.get_posts(), key=lambda post: post.likes, reverse=True)
        for k in c:
            cl.append([f"https://www.instagram.com/p/{k.shortcode}", k.likes, k.comments, k.shortcode])
        i.addposttomlc([cl])

    fortxt = [[i.userName, i.password, i.catgInf], i.postsinfo_ofcatg]
    strfortxt = str(fortxt).replace("'", '"')
    completeName = os.path.join("catgs/", i.userName + ".txt")
    file1 = open(completeName, "w")
    file1.write(strfortxt)
    file1.close()


def share(i, c, p):
    igr = il.Instaloader()
    igr.download_post(p, p.owner_username)

    bot = Bot()
    bot.login(username=i.userName, password=i.password)
    time.sleep(5)
    for jpg in glob.glob(f'{p.owner_username}\*.jpg'):
        bot.upload_photo(jpg, caption=c)
        break

def getpost(i, ss):
    global a

    igr = il.Instaloader()
    top2 = Toplevel()

    post = il.Post.from_shortcode(igr.context, ss[a][3])
    caption = Text(top2, width=50, height=10)
    caption.pack()
    caption.insert(END, post.caption)
    link = Label(top2, text=f"{ss[a][0]}", fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda e: webbrowser.open_new(ss[a-1][0]))
    Label(top2, text=f"{ss[a][1::]}").pack()
    print(ss[a])
    Button(top2, text="Share", command=lambda: share(i, caption.get("1.0", END), post)).pack()
    a += 1
    Button(top2, text="Exit", command=top2.destroy).pack()

def postbylink(i, link):
    igr = il.Instaloader()
    top2 = Toplevel()

    post = il.Post.from_shortcode(igr.context, link)
    caption = Text(top2, width=50, height=10)
    caption.pack()
    caption.insert(END, post.caption)

    Button(top2, text="Share", command=lambda: share(i, caption.get("1.0", END), post)).pack()


def creatWindow(i):
    global a
    a = 0

    def checks():
        i.removeposts(i.catgInf.index(clicked.get()))
        i.removeacc(clicked.get())

    top = Toplevel()
    top.geometry("600x600")
    top.title(i.userName)
    Label(top, text=i.userName).pack()
    newAccname = Entry(top)
    newAccname.pack()
    Button(top, text="Add account", command=lambda: addAcc(i, [newAccname.get()])).pack()
    Button(top, text="Update", command=lambda: saveposts(i)).pack()
    ss = ordered(i.postsinfo_ofcatg)
    Button(top, text="Find Post", command=lambda: getpost(i, ss)).pack()

    for b in i.catgInf:
        accLabel = Label(top, text=b)
        accLabel.pack()

    if len(i.catgInf) != 0:
        fordelete = i.catgInf
        clicked = StringVar()
        clicked.set(fordelete[0])
        drop = OptionMenu(top, clicked, *fordelete)
        drop.pack()

        Button(top, text="Remove", command=checks).pack()

    link2 = Entry(top)
    link2.pack()
    Button(top, text="Find Post by link", command=lambda: postbylink(i, link2.get())).pack()


i = 0


def creatorshowCatg():
    global i
    if entryTxt.get() != "":
        newcatg = Catg(entryTxt.get(), entryTxt2.get())
        catgs.append(newcatg)
        catgstoshow.append(newcatg)
        entryTxt.delete(0, END)

    else:
        while len(catgstoshow) != 0:
            catgButton = Button(root, text=catgstoshow[0].userName, command=lambda i=i: creatWindow(catgs[i]))
            catgButton.grid(padx=(200, 0), pady=(10, 0))
            catgstoshow.pop(0)
            i += 1


Label(root, text="user name").place(x=10, y=10)
entryTxt = Entry(root)
entryTxt.place(x=10, y=30)

Label(root, text="password").place(x=10, y=50)
entryTxt2 = Entry(root)
entryTxt2.place(x=10, y=70)

creatCategory = Button(root, text="add Category/show Category", command=creatorshowCatg)
creatCategory.place(x=10, y=90)

root.mainloop()

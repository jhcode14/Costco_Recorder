import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile

from ItemData import ItemData
from gui1 import *
from Data_Analysis import *
from datetime import date

#import hyperlink
#https://hyperlink.readthedocs.io/en/latest/
#Constants----------------------------------------------------

item_header = ['     Name     ', 'Lowest Price ($)', 'Current Price ($)', '                                          Link                                          ']
item_list = []
old = False
op = False
fileUsing = ""
cvTitle = ""

class MultiColumnListbox(object):
    def __init__(self):
        self.tree = None
        self.setup()
        self._build_tree()

    def setup(self):
        global cvTitle
        s = """Currently Viewing: """ + cvTitle + """ || Note: click on header to sort by column
If you would like to merge past list with new link entered, please do not "save" until you have opened past document"""
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=item_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in item_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in item_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = int(tkFont.Font().measure(val)*2/3)
                if self.tree.column(item_header[ix],width=None)<col_w:
                    self.tree.column(item_header[ix], width=col_w)

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

def compare(old, new):
    dataC = []
    #day = date.today.shiftime("%m/%d/%y")
    for o in old:
        check1 = False
        for n in new:
            if o[0].strip() == n[0].strip():
                check1 = True
                lowest_price = ""
                if o[2] == "Unavailable":
                    lowest_price = n[2]
                elif float(o[2].replace(',','')) > float(n[2].replace(',','')):
                    lowest_price = n[2]
                else:
                    lowest_price = o[2]
                if o[1].strip() != "N/A":
                    if float(o[1].replace(',','')) < float(lowest_price.replace(',','')):
                        lowest_price = o[1]
                dataC.append((n[0], lowest_price, n[2], n[3]))
        if check1 == False:
            dataC.append((o[0],o[2],"Unavailable","N/A"))
    for nn in new:
        check2 = False
        for dd in dataC:
            if nn[0].strip() == dd[0].strip():
                check2 = True
        if check2 == False:
            dataC.append((nn[0],nn[1],nn[2],nn[3]))
    return dataC

def writeFile(arr, FN, t):
    file = open(FN,"w+")
    file.write(t+ " -----LAST: " + date.today().strftime("%m/%d/%y") +"\n")
    for x in arr:
        a = 0
        while a<4:
            file.write("{" + str(a) + "}" + x[a])
            file.write("\n")
            a+=1
        file.write("=====\n")
    file.close
    

def loadFile(FN):
    global cvTitle
    arr2 = []
    count = 0
    L1 = ""
    L2 = ""
    L3 = ""
    L4 = ""
    with open(FN, "rt") as reading:
        for line in reading:
            if line.find(" -----LAST:") != -1:
                if count ==0:
                    temp_title = line[:line.find(" -----LAST:")]
                    if temp_title != cvTitle:
                        cvTitle = cvTitle + temp_title
                else:
                    return "BAD FILE"
            elif line.find("=====") != -1:
                arr2.append((L1, L2, L3, L4))
                L1 = ""
                L2 = ""
                L3 = ""
                L4 = ""
            elif line.strip() == "":
                pass
            elif line.find("{0}") != -1:
                L1 = line[3:].strip("\n")
            elif line.find("{1}") != -1:
                L2 = line[3:].strip("\n")
            elif line.find("{2}") != -1:
                L3 = line[3:].strip("\n")
            elif line.find("{3}") != -1:
                L4 = line[3:].strip("\n")
            else:
                pass
            count += 1
    return arr2

def SaveFile():
    global fileUsing
    global op
    global cvTitle
    if op != True:
        print("No changes made that needs to be saved")
    elif oldFileOpened("C"):
        writeFile(item_list, fileUsing, cvTitle)
    else:
        fileUsing = asksaveasfile()
        if fileUsing == None:
            return
        fileUsing = str(fileUsing)
        fileUsing = fileUsing[fileUsing.find("name='")+6:]
        fileUsing = fileUsing[0:fileUsing.find("' mode='w'")]
        writeFile(item_list, fileUsing, cvTitle)
def OpenFile():
    global fileUsing
    global op
    global item_list
    if oldFileOpened("C"):
        print("Seems like a file is already opened")
    else:
        fileUsing = askopenfilename()
        if fileUsing == "":
            return
        print("Opening file from: " + fileUsing)
        oldFileOpened("T")
        arr2 = loadFile(fileUsing)
        if op:
            item_list = compare(arr2, item_list)
        else:
            item_list = arr2
def About():
    print("This is Costco Recorder made by Jason Hsu")

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def runtk2(opp):
    root = tk.Tk()
    root.title("Costco Recorder List")
    if opp:
        listbox = MultiColumnListbox()
    else:
        label = tk.Label(root, text="""
        Go to top left menu's "File" and then "Open"
        to open existing file""")
        label.pack()
    #---------------menu implementation-----------------
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Save", command=SaveFile)
    filemenu.add_command(label="Open...", command= combine_funcs(OpenFile, root.destroy))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=About)
    #----------------------------------------------------
    root.geometry("1000x500")
    root.mainloop()

def runtk3():
    root2 = tk.Tk()
    root2.title("Costco Recorder List With Old Recording")
    listbox = MultiColumnListbox()
    #---------------menu implementation-----------------
    menu = Menu(root2)
    root2.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Save", command=SaveFile)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root2.quit)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=About)
    #----------------------------------------------------
    root2.geometry("1000x500")
    root2.mainloop()

def oldFileOpened(x):
    global old
    if x == "T":
        old = True
        return
    elif x =="F":
        old = False
        return
    elif x=="C":
        return old
    else:
        return
if __name__ == "__main__":
    weblink = runtk1.callGUI()
    if weblink == "readfile":
        op = False
    else:
        op = True
        loadAndAnalysis(weblink)
        cvTitle = getTitle()
        dataList = getData()
        for x in dataList:
            if cvTitle == x.getType:
                price = x.getPrice.strip("\n")
                if price.find(",")==-1:
                    price = price.replace("$","$,")
                item_list.append((x.getTitle.strip("\n"), "N/A", price, x.getLink))
    runtk2(op)
    if oldFileOpened("C"):
        runtk3()


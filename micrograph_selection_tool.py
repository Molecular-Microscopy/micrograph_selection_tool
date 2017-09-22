#!/usr/bin/python
#! /usr/local/Anaconda/envs/anaconda_2.1.0_py27/bin/python -B

################! /usr/bin/env python
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import ScrolledText
from PIL import ImageTk, Image
import tkFont
from autoEM import autoEM

def main():
    """ select_micrographs_OO.py is designed to browse pre-processed 
    images and select the ones appropriate for further processing
    """
    if (len(sys.argv) > 1):
        listfile=sys.argv[1]
    else:
        print "Please provide infile!"
        exit()
    if (len(sys.argv) > 2 ):
        outfile=sys.argv[2]
    else:
        outfile=listfile.split(".")[0]+"_out.txt"
        print "Since no outfile was provided, the outfile will be "+outfile
        print "Note: The quality will be written at the end of each line of the outfile."

    app = Application(dbfile=listfile)
 
    # Read in first image
    app.load_first()
    app.reshape_gui()
    app.outfile=outfile
    app.dbo.dbout=outfile
    app.mainloop()
    return 0

class Application(Tk):
    def donothing(self):
       filewin = Toplevel(self)
       button = Button(filewin, text="Do nothing button")
       button.pack()

    def load_file(self):
        filename = askopenfilename(filetypes = (("Database files", "*_dbase.txt")
                                                         ,("TXT files", "*.txt")
                                                         ,("All files", "*.*") ))
        if self.dbfile:
            self.dbo.get_parameters(filename)
            self.dbo.imagelist=[]
            self.dbo.imagelist.extend(self.dbo.rawlist)
            self.dbo.counter=0
            self.load_first()

    def save_listfile(self):
        filename = asksaveasfilename(filetypes = (("Micrograph lists", "*.micrographs"),("All files", "*.*") ))
        if filename: 
            self.dbo.save_list_file(filename)

    def save_as_new(self):
        filename = asksaveasfilename(filetypes = (("Micrograph lists", "*_dbase.txt"),("All files", "*.*") ))
        if filename:
            self.dbo.dbout=filename
            self.dbo.save_results(self.dbo.sortnum)

    def save_results(self):
        self.dbo.save_results(self.dbo.sortnum)

    def save_quit(self):
        self.dbo.save_results(self.dbo.sortnum)
        self.destroy()

    def makeMenu(self):
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
#        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", font=self.customFont, command=self.load_file)
        filemenu.add_command(label="Save", font=self.customFont, command=self.save_results)
        filemenu.add_command(label="Save Listfile", font=self.customFont, command=self.save_listfile)
        filemenu.add_command(label="Save as...", font=self.customFont, command=self.save_as_new)
#        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", font=self.customFont, command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu, font=self.customFont)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", font=self.customFont, command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", font=self.customFont, command=self.donothing)
        editmenu.add_command(label="Copy", font=self.customFont, command=self.donothing)
        editmenu.add_command(label="Paste", font=self.customFont, command=self.donothing)
        editmenu.add_command(label="Delete", font=self.customFont, command=self.donothing)
        editmenu.add_command(label="Select All", font=self.customFont, command=self.donothing)

#        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
#        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

    def createWidgets(self):
#        self.makeMenu()
        self.imgcnt=StringVar()
        self.imgcnt.set("List of micrographs: {0} of {1} ".format(self.dbo.counter+1,len(self.dbo.imagelist)))
     # self.bolded = tkFont.Font(family="Helvetica",weight="bold")


        # Create outer panel
        #self.main_panel=PanedWindow(self) #,orient=VERTICAL)
        self.main_panel=PanedWindow(self,orient=HORIZONTAL)
        h=min(self.winfo_width(),self.winfo_height())
        
        self.panel_center=PanedWindow(self.main_panel, orient=VERTICAL)
        #self.panel_center=PanedWindow(self.main_panel) #, orient=VERTICAL)
        self.center_buttons()
        #self.canvas_01=Canvas(self.main_panel,width=h,height=h/4)
        self.panel_right = PanedWindow(self.main_panel)
        self.right_panel()
        self.reshape_gui()
        #self.main_panel.add(self.canvas_01)
        self.main_panel.add(self.panel_center) 
        self.main_panel.add(self.panel_right)
        #self.canvas_01.create_image(0,0,anchor="nw")
        self.main_panel.pack(side="left",fill="both")
        self.update_label(self.dbo.counter)
        

    def keydown(self,e):
        print 'down', e.char
        e=e.char
        if (e=="e"):
            e=5
        elif (e=="v"):
            e=4
        elif (e=="g"):
            e=3
        elif (e=="p"):
            e=2
        elif (e=="b"):
            e=1
        else:
            e=0
        
        if (e):
            self.quality(e)
            

   
    def center_buttons(self):
        buttonpad=2

        # Rate
        lf1=LabelFrame(self.panel_center,text="Rate Micrograph",font=self.customFont)
        quality=("Excellent","Very Good","Good","Poor","Bad")
        bgcolor={"Excellent":"blue","Very Good":"green","Good":"yellow","Poor":"orange","Bad":"red"}
        for i in quality:
            Button(lf1,text=i,font=self.customFont,bg=bgcolor[i],command=lambda w=5-quality.index(i):self.quality(w)).pack(side="top",pady=buttonpad,fill="x",anchor="nw")

        lf1.pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        #lf1.pack(side="top",pady=buttonpad,anchor="nw")
        
        # Navigate
        lf2=LabelFrame(self.panel_center,text="Navigate",font=self.customFont)
        for i in ("Next","Previous","First","Last"):
            Button(lf2,text=i,font=self.customFont,bg="gray",command=lambda w=i:self.navigate(w)).pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        lf2.pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        #lf2.pack(side="top",pady=buttonpad,anchor="nw")

        # Sort
        lf3=LabelFrame(self.panel_center,text="Sort by",font=self.customFont)
        self.sort_var=StringVar()    
        self.sort_var.set(self.dbo.parameters[0])
        sortmenu=OptionMenu(lf3,self.sort_var,*self.dbo.parameters)
        sortmenu.configure(font=self.customFont)
        sortmenu.pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        sortmenu.nametowidget(sortmenu.menuname).configure(font=self.customFont)

        #OptionMenu(lf3,self.sort_var,*self.dbo.parameters).pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        self.sort_submit=Button(lf3,text="Submit",font=self.customFont, command=lambda:self.sort_by(0))
        self.sort_submit.pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        lf3.pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        #lf3.pack(side="top",pady=buttonpad,anchor="nw")

        # Parameter Box
        lf4=LabelFrame(self.panel_center,text="Parameters",font=self.customFont)
        self.parbox=ScrolledText.ScrolledText(lf4,font=self.customFont,width=30,background='white')
        self.parbox.pack(side="top",pady=buttonpad,fill="both",anchor="nw",expand=True)
        lf4.pack(side="top",pady=buttonpad,fill="x",anchor="nw")
        #lf4.pack(side="top",pady=buttonpad,anchor="nw")

        # Save and quit
        #Button(self.panel_center, text="Save and Quit",bg="orange",command=lambda:self.save_quit()).pack(side="top",pady=buttonpad,fill="x",anchor="nw")

    def right_panel(self):
        # Filtering ------------------------------------------------------------
        # Label
        
        Label(self.panel_right,text="Set Filter: (Newer filters overide previous ones)",font=self.customFont, justify=LEFT).pack(side="top")
        self.canvas_01=Canvas(self.panel_right)#,width=h,height=h/4)
        self.canvas_01.pack(side="top",fill="x")
        self.canvas_01.create_image(0,0,anchor="nw")
        # Get filterable parameters
        """
        self.param_dict={}
        if len(self.dbo.imagelist)>1:
            for i,param in enumerate(self.dbo.parameters):
                if type(self.dbo.imagelist[0][i]) is float and not param=="Ignore":
                    self.param_dict[param]=i
        """
        # Variables
        equality=[">",">=","=","<=","<"]
        var=StringVar()
        var.set("Remove")
        var2=StringVar()
        var2.set(self.dbo.parameters[0])
        var3=StringVar()
        var3.set(equality[0])
        # Filter menu
        right_frame=Frame(self.panel_right)

        op1=OptionMenu(right_frame,var,"Remove","Show")
        op1.configure(font=self.customFont)
        op1.nametowidget(op1.menuname).configure(font=self.customFont)

        op2=OptionMenu(right_frame,var2,*self.dbo.parameters)
        op2.configure(font=self.customFont)
        op2.nametowidget(op2.menuname).configure(font=self.customFont)

        op3=OptionMenu(right_frame,var3,*equality)
        op3.configure(font=self.customFont)
        op3.nametowidget(op3.menuname).configure(font=self.customFont)

        op4=Entry(right_frame)
        op4.configure(font=self.customFont)
        #op4.nametowidget(op4.menuname).configure(font=self.customFont)
        
        filter_submit=Button(right_frame,text="Submit",font=self.customFont,command=lambda:self.cur_Filter(op4,var,var2,var3,str))
        op4.bind('<Return>',lambda event:self.cur_Filter(op4,var,var2,var3,str))

        op1.grid(row=0,column=0)
        op2.grid(row=0,column=1)
        op3.grid(row=0,column=2)
        op4.grid(row=0,column=3)

        
        filter_submit.grid(row=0,column=4)
        self.flbox=Listbox(self.panel_right,font=self.customFont,height=5,selectmode="single")
        for i in self.dbo.filters:
            self.flbox.insert(END," ".join(i))

        dele=Button(self.panel_right,text="Delete",font=self.customFont,command=self.del_Filter,bg="red")

        self.flbox.selection_clear(0,last=END)
        self.flbox.activate(0)
        self.flbox.selection_set(0)

        # Pack
        #right_frame.pack(side="top")
        #self.flbox.pack(side="top")
        #dele.pack(side="top")
        right_frame.pack(side="top",fill="x")
        self.flbox.pack(side="top",fill="x")
        dele.pack(side="top",fill="x")

        # List of micrographs
        bottom = Label(self.panel_right, textvariable=self.imgcnt,font=self.customFont)

        bottom.pack(side="top",pady=2)

        self.lbox = Listbox(self.panel_right,font=self.customFont, selectmode="single", width=80)
        for i in self.dbo.imagelist:
            self.lbox.insert(END,i[0])
            self.lbox.selection_clear(0,last=len(self.dbo.imagelist))
            self.lbox.activate(self.dbo.counter)
            self.lbox.selection_set(self.dbo.counter)
            self.lbox.bind('<<ListboxSelect>>',self.update_listbox)
            self.bind('<Up>',lambda event:self.onArrowKey(0))
            self.bind('<Down>',lambda event:self.onArrowKey(1))

        s1 = Scrollbar(self.lbox,orient=HORIZONTAL)
        s = Scrollbar(self.lbox)

        s1.pack(side=BOTTOM,fill=X)
        s.pack(side=RIGHT,fill=Y)

        self.lbox.pack(side="top",pady=2,fill=BOTH,expand=True)
        s.config(command=self.lbox.yview)
        s1.config(command=self.lbox.xview)
        self.lbox.config(yscrollcommand=s.set,xscrollcommand=s1.set)

        # _boxed.png or .png choice
        choiceFrame=Frame(self.panel_right)
        self.boxvar=IntVar()
        defchoice=Radiobutton(choiceFrame,text=".png",font=self.customFont,variable=self.boxvar,value=0,command=lambda:self.update_label(self.dbo.counter))
        boxchoice=Radiobutton(choiceFrame,text="_boxed.png",font=self.customFont,variable=self.boxvar,value=1,command=lambda:self.update_label(self.dbo.counter))
        defchoice.grid(row=0,column=0)
        boxchoice.grid(row=0,column=1)
        choiceFrame.pack(side="bottom")

    def reshape_gui(self):
        self.update()
        h=min(self.winfo_width(),self.winfo_height())
        w=self.winfo_width()-16
        self.main_panel.configure(width=w,height=h)
        self.main_panel.update()
        self.canvas_01.configure(width=w*3/4,height=w*3/16)
        self.canvas_01.update()
        #self.canvas_01.create_image(0,0,anchor="nw")
        self.panel_center.configure(width=(self.winfo_width()-h)/4,height=h)
        self.panel_right.configure(width=(self.winfo_width()-h)*3/4,height=h)
        self.canvas_01.update()
        self.panel_center.update()
        self.panel_right.update()
        return w
 
    def quality(self,value):
        # update image data
        self.dbo.imagelist[self.dbo.counter][self.dbo.qloc]=value
        n=self.dbo.rawlist.index(self.dbo.imagelist[self.dbo.counter])
        self.dbo.rawlist[n][self.dbo.qloc]=value
        self.dbo.save_results(self.dbo.sortnum)
        if self.dbo.counter<len(self.dbo.imagelist)-1:
            self.dbo.counter+=1
        self.update_label(self.dbo.counter)
        
    def update_listbox(self,event):
        self.dbo.counter=int(self.lbox.curselection()[0])
        self.update_label(self.dbo.counter)

    def update_label(self,index):
        self.lbox.selection_clear(0,last=len(self.dbo.imagelist))
        self.lbox.activate(self.dbo.counter)
        self.lbox.selection_set(self.dbo.counter)
        self.lbox.see(self.dbo.counter)
        self.reset_txtbox()
        self.imgcnt.set("List of micrographs: {0} of {1} ".format(self.dbo.counter+1,len(self.dbo.imagelist)))
        self.load_image()
    
    def load_first(self):
        while True:
            self.dbo.counter=0
            try:
                self.update()
                self.update_label(self.dbo.counter)
                break
            except IOError:
                if self.dbo.counter<len(imagelist)-1:
                    self.dbo.counter+=1
                else:
                    tkMessageBox.showerror("Error", "Image files not found!")
#                    self.destroy()
                    break
 

    def configMw(self):
        self.configure(width=self.winfo_screenwidth(),height=self.winfo_screenheight())
        self.geometry("{0:d}x{1:d}+0+0".format(self.winfo_screenwidth(),self.winfo_screenheight()))
        self.resizable(1,1)
        self.title("Micrograph selection")
        self.update()

    def navigate(self,value):
        if value=="Next":
            if self.dbo.counter<len(self.dbo.imagelist)-1:
                self.dbo.counter+=1
            else:
                return 0
        if value=="Previous":
            if self.dbo.counter>0:
                self.dbo.counter-=1
            else:
                return 0
        if value=="First":
            self.dbo.counter=0
        if value=="Last":
            self.dbo.counter=len(self.dbo.imagelist)-1
        self.update_label(self.dbo.counter)

    def sort_by(self,descending):
        """send request to sort the list of images
        """
        self.dbo.sortby(self.sort_var.get(),descending)
        # invert the list
        self.lbox.delete(0,END)
        for i in self.dbo.imagelist:
            self.lbox.insert(END,i[0])
        self.sort_submit.configure(command=lambda:self.sort_by(not descending))
        self.dbo.save_results(self.dbo.sortnum)
        self.update_label(self.dbo.counter)



    def onArrowKey(self,down):
        n=-1
        if down:
            n=1
        if not 0<=self.dbo.counter+n<len(self.dbo.imagelist):
            return 0
        self.dbo.counter+=n
        self.update_label(self.dbo.counter)
 

    def update_list(self):
        self.dbo.counter=0
        self.lbox.delete(0,END)
        for i,f in enumerate(self.dbo.rawlist):
            if f[-1]:
                self.lbox.insert(END,f[0])
                if not f in self.dbo.imagelist:
                    self.dbo.imagelist.append(f)
            else:
                if f in self.dbo.imagelist:
                    self.dbo.imagelist.remove(f)
        self.lbox.selection_clear(0,END)
        self.update_label(self.dbo.counter)
        return
    



    def dofilter(self):
        self.dbo.dofilter()
        self.update_list()
        self.dbo.save_results(self.dbo.sortnum)

    def del_Filter(self):
        try:
            n=int(self.flbox.curselection()[0])
            self.dbo.filters.pop(n)  
            self.flbox.delete(n)
            self.dofilter()
        except IndexError:
            return 0


    def cur_Filter(self,op4,var,var2,var3,str):
        try:
            temp=float(op4.get())
            self.dbo.filters.append([var.get(),var2.get(),var3.get(),str(temp)])
            self.flbox.insert(END," ".join(self.dbo.filters[-1]))
            self.dofilter()
        except ValueError:
            tkMessageBox.showerror("Error", "Please enter an integer into text box!")

    def load_image(self,image_filename=""):
        w=self.reshape_gui()
        try:
            image_filename=self.suffix[self.boxvar.get()]["dir"]+self.dbo.imagelist[self.dbo.counter][0]+self.suffix[self.boxvar.get()]["suffix"]
            img = Image.open(image_filename)
            img = img.resize((w*3/4,w*3/16), Image.ANTIALIAS)
            self.newImage = ImageTk.PhotoImage(img)
            self.canvas_01.itemconfigure(1,image=self.newImage)
            #self.canvas_02.itemconfigure(1,image=self.newImage)


        except IOError, AttributeError:
            #print "File %s does not exist" % (image_filename)
            tkMessageBox.showerror("Error", image_filename+" does not exist!")
            return "error"
        self.reset_txtbox()


    def reset_txtbox(self):
        if len(self.dbo.imagelist)<1:
            return
        self.parbox.delete("1.0",END)
        start=0
        end=0
        for n,i in enumerate(self.dbo.parameters):
            self.parbox.insert(END,i.upper(),("params",))
            self.parbox.insert(END,": "+str(self.dbo.imagelist[self.dbo.counter][n]))
            if n!=len(self.dbo.parameters)-1:
                self.parbox.insert(END,"\n")
        self.parbox.tag_config("params",background="light blue")


    def __init__(self, master=None,dbfile=None):
        """Creates the main frame and widgets
        """
        Tk.__init__(self, master)
        self.customFont = tkFont.Font(family="Helvetica", size=10)
        self.dbo=autoEM(name=dbfile)
        self.dbo.get_parameters()
        self.dbo.imagelist=[]
        self.dbo.imagelist.extend(self.dbo.rawlist)
        # This is a placeholder, it will eventually replace imagelist
        self.dbo.sortorder=range(len (self.dbo.rawlist))
        self.suffix=[{"dir":"ctf/","suffix":".png"},{"dir":"box/","suffix":"_boxed.png"}]

        self.configMw()
        self.makeMenu()
        self.createWidgets()
        self.bind("<KeyPress>", self.keydown)
 

if __name__ == '__main__':


    main()



from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

from subprocess import *

import os
import json

print("This is JEditor Termial")
class JEditor():
            
    def __init__(self,app):
        if os.path.exists(os.getcwd()+"/settings.json"):
            with open("./settings.json") as file:
                configData=json.load(file)
        else:
            configTemplate = {
            "font":"cascadia code",
            "defaultfontsize":16
            }        
            with open(os.getcwd()+"/settings.json","w+") as file:
                json.dump(configTemplate,file)
                print("Settings file created please run the app again")
        self.app=app
        self.app.title("JEditor")
        self.app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(),app.winfo_screenheight()))

        # Main Frame 
        self.mainFrame=Frame(background='black',bd=5,relief=SOLID)
        self.mainFrame.pack(expand=True,fill=BOTH)
        #All Variables
        self.path_name=''
        self.font=configData["font"]
        self.default_font_size=configData["defaultfontsize"]
        self.java_template = '''public class main{
   public static void main(String[] args) {
   	System.out.println("Hello World");
   }
}
'''

        ##Menu Bar
        menuBar=Menu(self.mainFrame)
        #File Menu
        fileMenu=Menu(menuBar,tearoff=False)
        fileMenu.add_command(label='New File',accelerator='Ctrl+N',command=self.new_file)
        fileMenu.add_command(label='Open File',accelerator='Ctrl+O',command=self.open_file)
        fileMenu.add_command(label='Save As',accelerator='Alt+S',command=self.save_as_file)
        fileMenu.add_command(label='Save',accelerator='Ctrl+S',command=self.save_file)
        fileMenu.add_separator()
        fileMenu.add_command(label='Close',accelerator='Alt+F4',command=self.app.destroy)
        # Edit Menu
        editMenu=Menu(menuBar,tearoff=False)
        editMenu.add_command(label='Cut',accelerator='Ctrl+X',command=self.cut)
        editMenu.add_command(label='Copy',accelerator='Ctrl+C',command=self.copy)
        editMenu.add_command(label='Paste',accelerator='Ctrl+V',command=self.paste)
        editMenu.add_separator()
        editMenu.add_command(label='Increase Font Size',accelerator='Ctrl+P',command=self.change_fontsize_inc)
        editMenu.add_command(label='Decrease Font Size',accelerator='Ctrl+M',command=self.change_fontsize_dec)
        editMenu.add_separator()
        editMenu.add_command(label='New Class',accelerator='Ctrl+A',command=self.new_class)
        editMenu.add_command(label='Run Program',accelerator='Alt+B',command=self.run_file)
        editMenu.add_separator()
        editMenu.add_command(label='Clear Editor',accelerator='Alt+C',command=self.clear_edit)
        editMenu.add_command(label='Clear Output',accelerator='Alt+V',command=self.clear_output)
        # Theme Menu
        themeMenu=Menu(menuBar,tearoff=False)
        themeMenu.add_command(label='Dark +',command=self.dark_theme)
        themeMenu.add_command(label='Light',command=self.light_theme)
        themeMenu.add_command(label='Monokai',command=self.monakai_theme)
        themeMenu.add_command(label='One Dark',command=self.twilight_theme)


        self.app.config(menu=menuBar)

        menuBar.add_cascade(label='File',menu=fileMenu)
        menuBar.add_cascade(label='Edit',menu=editMenu)
        menuBar.add_cascade(label='Theme',menu=themeMenu)
        menuBar.add_command(label='Run Program',command=self.run_file)
        menuBar.add_command(label='Copy',command=self.copy)
        menuBar.add_command(label='Cut',command=self.cut)
        menuBar.add_command(label='Paste',command=self.paste)
        menuBar.add_command(label='New Class',command=self.new_class)

        #Editor Frame
        
        editFrame=Frame(self.app,background='white')
        editFrame.place(x=0,y=0,relwidth=1,height=500)

        scrollY=Scrollbar(editFrame,orient=VERTICAL)
        scrollY.pack(side=RIGHT,fill=Y)
        self.textFeild=Text(editFrame,background='black',foreground='white',font=(self.font,self.default_font_size,'bold'),insertbackground='white',yscrollcommand=scrollY)
        scrollY.config(command=self.textFeild.yview)
        self.textFeild.pack(expand=True,fill=BOTH)

        # Output Frame
        outputFrame=Frame(self.app,background='white')
        outputFrame.place(x=0,y=500,relwidth=1,height=220)

        scrollY=Scrollbar(outputFrame,orient=VERTICAL)
        scrollY.pack(side=RIGHT,fill=Y)
        self.outputFeild=Text(outputFrame,background='black',foreground='white',font=(self.font,self.default_font_size,'bold'),insertbackground='white',yscrollcommand=scrollY)
        scrollY.config(command=self.outputFeild.yview)
        self.outputFeild.pack(expand=True,fill=BOTH)
        # All Shorcuts Keys
        self.app.bind('<Alt-s>',self.save_as_file)
        self.app.bind('<Control-s>',self.save_file)
        self.app.bind('<Control-o>',self.open_file)
        self.app.bind('<Control-n>',self.new_file)
        self.app.bind('<Alt-c>',self.clear_edit)
        self.app.bind('<Alt-v>',self.clear_output)
        self.app.bind('<Alt-b>',self.run_file)
        self.app.bind('<Control-p>',self.change_fontsize_inc)
        self.app.bind('<Control-m>',self.change_fontsize_dec)
        self.app.bind('<Control-a>',self.new_class)

        # All Fuctions
    def light_theme(self):
        self.textFeild.config(background='white',foreground='black',insertbackground='black')  
        self.outputFeild.config(background='white',foreground='black',insertbackground='black')  
      
    def dark_theme(self):
        self.textFeild.config(background='black',foreground='white',insertbackground='white')      
        self.outputFeild.config(background='black',foreground='white',insertbackground='white')      
 

    def monakai_theme(self):
        self.textFeild.config(background='#272822',foreground='white',insertbackground='white')      
        self.outputFeild.config(background='#272822',foreground='white',insertbackground='white')      
 
    def twilight_theme(self):
        self.textFeild.config(background='#28171E',foreground='white',insertbackground='white')      
        self.outputFeild.config(background='#28171E',foreground='white',insertbackground='white')      

    def save_as_file(self,event=None):
        path=asksaveasfilename(filetypes=[('Java Class','*.java'),('All Files','*.*')],defaultextension=('.java'))
        if path!='':
            self.path_name=path
            file=open(self.path_name,'w')
            file.write(self.textFeild.get('1.0',END))
            file.close()
    def save_file(self,event=None):
        if self.path_name == "":
            self.save_as_file
        else:
            file=open(self.path_name, 'w')    
            file.write(self.textFeild.get('1.0',END))
            file.close()
    def open_file(self,event=None):
        path=askopenfilename(filetypes=[('Java File','*.java'),('All Files','*.*')],defaultextension=('.java'))
        if path!='':
            self.path_name=path
            file=open(self.path_name,'r')
            data=file.read()
            self.textFeild.delete('1.0',END)
            self.textFeild.insert('1.0',data)
            file.close()
        print(self.path_name)    
    def new_file(self,event=None):
        self.path_name=''        
        self.textFeild.delete('1.0',END)
        self.outputFeild.delete('1.0',END)

    def clear_edit(self,event=None):
       self.textFeild.delete('1.0',END)
    def clear_output(self,event=None):
       self.outputFeild.delete('1.0',END)    
        
    def run_file(self,event=None):
        if  self.path_name == '':
            showerror("Error","Please save the file first to execute")
        else:
            self.path_name=str(self.path_name)
            print(self.path_name)
            command=f'java "{self.path_name}"'
            run=Popen(command,stdout=PIPE,stderr=PIPE,shell=True)
            output,error=run.communicate()
            self.outputFeild.delete('1.0',END)
            self.outputFeild.insert('1.0',output)
            self.outputFeild.insert('1.0',error)
    def cut(self):
        self.textFeild.event_generate(("<<Cut>>"))

    def copy(self):
        self.textFeild.event_generate(("<<Copy>>"))
    
    def paste(self):
        self.textFeild.event_generate(("<<Paste>>"))   

    def change_fontsize_inc(self,event=None):
        self.default_font_size+=1
        self.textFeild.config(font=('cascadia code',self.default_font_size,'bold'))
        self.outputFeild.config(font=('cascadia code',self.font_size,'bold'))

    def change_fontsize_dec(self,event=None):
        self.default_font_size-=1
        self.textFeild.config(font=('cascadia code',self.default_font_size,'bold'))
        self.outputFeild.config(font=('cascadia code',self.font_size,'bold'))
    def new_class(self,event=None):
        self.textFeild.delete('1.0',END)
        self.textFeild.insert('1.0',self.java_template)
   
app=Tk()        
contructor=JEditor(app)
app.mainloop()
import tkinter as tk
import pymysql
from tkinter import messagebox

class car:
    def __init__(self,root):
        self.root= root
        self.root.title("Car Rental Management System")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title=tk.Label(self.root,text="Car Rental Management System",bg="light green",fg="red",bd=4,relief="ridge",font=("Arial",50,"bold"))
        title.pack(side="top",fill="x")

        self.mainFrame=tk.Frame(self.root,bg="light gray",bd=4,relief="groove")
        self.mainFrame.place(width=self.width/3, height=self.height-180,x=self.width/5-50,y=100)

        reserveBtn = tk.Button(self.mainFrame,command=self.reserve,text="Reserve Car",bg="sky blue", fg="black", bd=2, relief="raised",width=20, font=("Arial",20))
        reserveBtn.grid(padx=40, pady=60, row=0,column=0)

        returnBtn = tk.Button(self.mainFrame,command=self.returnFun,text="Return Car",bg="sky blue", fg="black", bd=2, relief="raised",width=20, font=("Arial",20))
        returnBtn.grid(padx=40, pady=50,row=1,column=0)

        closeBtn = tk.Button(self.mainFrame,command=self.closeWindow,text="Close Window",bg="sky blue", fg="black", bd=2, relief="raised",width=20, font=("Arial",20))
        closeBtn.grid(padx=40, pady=50,row=2,column=0)

        self.showFrame= tk.Frame(self.root,bg="light gray",bd=4,relief="groove")
        self.showFrame.place(width=self.width/3,height=self.height-180,x=self.width/2+50,y=100)

        lab= tk.Label(self.showFrame,text="Available Cars",bg="light gray",fg="red",font=("Arial",25,"bold"))
        lab.grid(row=0,column=1,padx=20,pady=10)

        self.list= tk.Listbox(self.showFrame,fg="white",font=("Arial",15,"bold"),bg="gray",bd=4,relief="sunken",width=35, height=15)
        self.list.grid(row=1,column=1,padx=10,pady=50,columnspan=2)
        self.retrieve()


    def db_conn(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def retrieve(self):
        self.db_conn()
        self.cur.execute("select * from car where status='Avail'")
        data = self.cur.fetchall()

        for i in data:
            line = ' : '.join(map(str,i))
            self.list.insert(tk.END,line)

    def closeWindow(self):
        self.root.destroy()

    def reserve(self):
        self.resFrame= tk.Frame(self.root,bg="sky blue",bd=4,relief="groove")
        self.resFrame.place(width=self.width/3,height=self.height-180,x=self.width/2+50,y=100)

        regLab = tk.Label(self.resFrame,text="Car No: ", bg="sky blue",fg="black", font=("Arial",15,"bold"))
        regLab.grid(row=0,column=0, padx=20, pady=50)
        self.regIn= tk.Entry(self.resFrame,bd=2, font=("Arial",15),width=20)
        self.regIn.grid(row=0, column=1, padx=20, pady=50)

        dayLab = tk.Label(self.resFrame,text="Enter Days: ", bg="sky blue",fg="black", font=("Arial",15,"bold"))
        dayLab.grid(row=1, column=0, padx=20, pady=50)
        self.dayIn = tk.Entry(self.resFrame,bd=2, font=("Arial",15),width=20)
        self.dayIn.grid(row=1,column=1,padx=20, pady=50)

        okBtn= tk.Button(self.resFrame, text="OK",command=self.resFun, font=("Arial",20),width=20, bg="light gray", bd=2)
        okBtn.grid(row=2,column=0,padx=30, pady=60,columnspan=2)

    def resFun(self):    

        reg = int(self.regIn.get())
        days= int(self.dayIn.get())

        self.db_conn()
        try:
            query = f"select rent, status from car where regNo={reg}"
            self.cur.execute(query)
            row= self.cur.fetchone()
            if row[1] == 'Avail':
                
                query2= f"update car set status='Reserved' where regNo={reg}"
                self.cur.execute(query2)
                self.con.commit()
                amount = days * row[0]
                bill= f"Amount for {reg} is: {amount}"
                tk.messagebox.showinfo("Success",bill)
                self.cur.execute("select * from car where status='Avail'")
                values = self.cur.fetchall()
                self.list.delete(0,tk.END)
                for j in values:
                    newVal= ' : '.join(map(str,j))
                    self.list.insert(tk.END,newVal)
                self.closeRes()
                self.cur.close()
                self.con.close()

            else:
                tk.messagebox.showerror("Error","Car is not available") 
                self.closeRes()
        except Exception as e:
            tk.messagebox.showerror("Error",f"DB Error: {e}")        

    def closeRes(self):
        self.resFrame.destroy() 

    def returnFun(self):
        self.retFrame= tk.Frame(self.root,bg="sky blue",bd=4,relief="groove")
        self.retFrame.place(width=self.width/3,height=self.height-180,x=self.width/2+50,y=100)   

        regLab = tk.Label(self.retFrame,text="Car No: ", bg="sky blue",fg="black", font=("Arial",15,"bold"))
        regLab.grid(row=0,column=0, padx=20, pady=50)
        self.regIn2= tk.Entry(self.retFrame,bd=2, font=("Arial",15),width=20)
        self.regIn2.grid(row=0, column=1, padx=20, pady=50)

        okBtn= tk.Button(self.retFrame, text="OK",command=self.retFun, font=("Arial",20),width=20, bg="light gray", bd=2)
        okBtn.grid(row=2,column=0,padx=30, pady=60,columnspan=2)

    def retFun(self):
        reg=int(self.regIn2.get())

        self.db_conn()
        query=f"update car set status='Avail' where regNo={reg}"
        self.cur.execute(query)
        self.con.commit()

        self.cur.execute("select * from car where status='Avail'")
        data = self.cur.fetchall()
        self.list.delete(0,tk.END)
        for i in data:
            newVal=' : '.join(map(str,i))
            self.list.insert(tk.END,newVal)
        tk.messagebox.showinfo("Sucess","Car Returned Successfuly")
        self.cur.close()
        self.con.close()
        self.closeRet()

    def closeRet(self):
        self.retFrame.destroy()



root=tk.Tk()
obj = car(root)
root.mainloop()
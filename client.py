import socket
import threading
from tkinter import *
from typing import Literal
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
import json
import webbrowser

SIGNUP = "signup"
LOGIN = "login"
FORMAT ="utf-8"
app_width = 720
app_height = 540
class client:
    def __init__(self):
        self.root = Tk()
        self.root.title('COVID-19 CASE')
        self.root.iconbitmap('c.ico')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width / 2) - (app_width / 2))
        y = int((screen_height / 2) - (app_height / 2))

        self.root.geometry(f'{app_width}x{app_height}+{x}+{y}')
        self.root.resizable(width=False, height=False)

        self.IP_frame = Frame(self.root, width=app_width, height=app_height)
        self.IP_frame.pack(fill='both', expand=1)
        self.main_frame = Frame(self.root, width=app_width, height=app_height)
        self.main_canvas = Canvas(self.main_frame, width=app_width, height=app_height)
        self.main_canvas.pack(fill="both", expand=True)
        self.login_frame = Frame(self.root, width=app_width, height=app_height)
        self.signup_frame = Frame(self.root, width=app_width, height=app_height)

        self.locations=['TP. Hồ Chí Minh', 'Bình Dương', 'Đồng Nai', 'Long An', 'Tây Ninh', 'Tiền Giang', 'An Giang', 'Đồng Tháp', 'Kiên Giang', 'Cần Thơ','Bình Thuận', 
        'Sóc Trăng', 'Bà Rịa – Vũng Tàu', 'Khánh Hòa', 'Bạc Liêu', 'Vĩnh Long', 'Hà Nội', 'Cà Mau', 'Trà Vinh', 'Đắk Lắk', 'Bến Tre', 'Bắc Giang','Bình Phước', 'Đà Nẵng', 'Hậu Giang', 
        'Bắc Ninh', 'Nghệ An', 'Hà Giang', 'Bình Định', 'Ninh Thuận', 'Phú Yên', 'Gia Lai', 'Thừa Thiên Huế', 'Quảng Nam', 'Quảng Ngãi', 'Quảng Bình', 'Thanh Hóa', 'Đắk Nông', 'Lâm Đồng', 
        'Phú Thọ', 'Hải Dương', 'Hà Nam', 'Nam Định', 'Thái Bình', 'Vĩnh Phúc', 'Hà Tĩnh', 'Quảng Trị', 'Quảng Ninh', 'Hưng Yên', 'Tuyên Quang', 'Điện Biên', 'Lạng Sơn', 'Hải Phòng', 'Kon Tum',
        'Hòa Bình', 'Sơn La', 'Ninh Bình', 'Thái Nguyên', 'Lào Cai', 'Cao Bằng', 'Yên Bái', 'Lai Châu', 'Bắc Kạn']
        
        self.logout = False
        self.ip()
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def ip(self):
        self.img2 = ImageTk.PhotoImage(Image.open('client.png'))
        p = Label(self.IP_frame, image=self.img2)
        p.place(x=327, y=30)

        self.addr_entry = Entry(self.IP_frame, width=25, font=("Calibri", 13))
        addr_label = Label(self.IP_frame, text='Add server')
        addr_label.place(x=180, y=119)
        HostName = socket.gethostname()
        HOST = socket.gethostbyname(HostName)
        self.addr_entry.insert(END, HOST)
        self.addr_entry.place(x=250, y=120)     

        self.ip_entry = Entry(self.IP_frame, width=25, font=("Calibri", 13))
        ip_label = Label(self.IP_frame, text='Port server')
        ip_label.place(x=180, y=149)
        self.ip_entry.place(x=250, y=150)

        ip_button = Button(self.IP_frame, text='OK', padx=102, pady=2, bg='#154c79', fg='white', command=self.ip_check)
        ip_button.place(x=250, y=180)

    def ip_check(self):
        try:
            ip = self.ip_entry.get()
            addr = self.addr_entry.get()
            HOST=addr
            PORT = int(ip)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST,PORT))
            
            self.loginPage()
        except:
            messagebox.showerror("ERROR", "No Server found")
    def getData(self):
        user = self.entry_user.get()
        pswd = self.entry_pswd.get()
            
        data =[]
        data.append(user)
        data.append(pswd)
        return data

    def logIn(self):
        try:
            user = self.entry_user.get()
            pswd = self.entry_pswd.get()
            if pswd == "" or user == "":
                self.label_notice["text"] = "Password or username cannot be empty"
                return
            data = self.getData()
            #notice server for starting log in
            option = LOGIN
            data.append(option)
            #send username and password to server
            self.client.send(str.encode(str(data)))
            
            # see if login is accepted
            accepted = self.client.recv(1024).decode(FORMAT)
            if accepted == "1":
                print("Sign in succeed")
                self.label_notice["text"] = ""
                name=self.client.recv(1024).decode(FORMAT)
                self.running=True
                self.layout(name)

            elif accepted == "2":
                self.label_notice["text"] = "invalid username or password"
            elif  accepted == "0":
                self.label_notice["text"] = "user already logged in"
        except:
            print("ERROR, Server is not responding")
            if messagebox.showerror("ERROR", "Server is not responding"):
                        self.hide_all()
                        self.IP_frame.pack(fill='both', expand=1)

    def signUp(self):
        try:
            user = self.new_user.get()
            pswd = self.new_pswd.get()
            pswdcf = self.entry_pswd_cf.get()

            spaces = 0
            for index in user:
                if index == ' ':
                    spaces += 1
            if spaces != 0:
                messagebox.showerror('ERROR', 'Username cannot contain spaces')
            else:
                if pswd == "" or user == "":
                    self.label_notice["text"] = "Password or username cannot be empty"
                    return
                elif pswd != pswdcf:
                    self.label_notice["text"] = "Confirm password incorrect"
                    return
                
                data =[]
                data.append(user)
                data.append(pswd)

                #notice server for starting log in
                option = SIGNUP
                data.append(option)
                #send username and password to server
                self.client.send(str.encode(str(data)))

                # see if login is accepted
                accepted = self.client.recv(1024).decode(FORMAT)
                if accepted == "1":
                    print("Sign Up Succeed")
                    if messagebox.showinfo("SUCCEED", "LET'S LOG IN NOW"):
                        self.label_notice["text"] = ""
                        self.loginPage()
                else:
                    self.label_notice["text"] = "username already exists"

        except:
            print("ERROR, Server is not responding")
            if messagebox.showerror("ERROR", "Server is not responding"):
                        self.hide_all()
                        self.IP_frame.pack(fill='both', expand=1)
    def back(self):
        self.hide_all()
        self.IP_frame.pack(fill='both', expand=1)

    def loginPage(self):
        self.hide_all()
        self.login_frame.configure(bg="white")
        self.img = ImageTk.PhotoImage(Image.open('login-rounded.png'))
        out_button = Button(self.login_frame, image=self.img, borderwidth=0, command=self.back)
        out_button.place(x=373, y=175)
        login_label = Label(self.login_frame, text='LOGIN', bg='#5885AF', fg='white', width=65, height=6, font='Calibri, 15')
        login_label.place(x=0, y=0)
        label_user = Label(self.login_frame, text="Username ",fg='black',bg="white",font='Calibri 12 bold')
        label_pswd = Label(self.login_frame, text="Password ",fg='black',bg="white",font='Calibri 12 bold')
        label_user.place(x=190, y=230)
        label_pswd.place(x=190, y=280)

        self.entry_user = Entry(self.login_frame,width=50,bg='white',font='Calibri 11')
        self.entry_user.place(x=190, y=255)

        self.entry_pswd = Entry(self.login_frame,width=50,bg='white',show='*',font='Calibri 11')
        self.entry_pswd.place(x=190, y=305)
   
        self.label_notice = Label(self.login_frame,text="",fg='red',bg="white")
        self.label_notice.place(x=190, y=330)

        button_log = Button(self.login_frame,text="LOG IN", bg='#274472', fg='white',font='Calibri 11 bold',command= self.logIn) 
        button_log.configure(width=43)
        button_log.place(x=190, y= 360)
        
        register_label = Label(self.login_frame,text ="Not registered yet? ", bg="white",font='Calibri, 11')
        register_label.place(x=250, y=400)
        signup_button = Button(self.login_frame, text='Register here', bg='white',activebackground='white', font="Calibri 12 underline", borderwidth=0,command= self.RegisterPage)
        signup_button.place(x=380, y=396)
        self.login_frame.pack(fill='both',expand=1)
    def RegisterPage(self):
        self.hide_all()
        self.signup_frame.configure(bg="white")
        label_title =Label(self.signup_frame, text="CREATE YOUR ACCOUNT",fg='white',bg="#5885AF",width=61, height=6, font='Calibri, 15 bold')
        label_title.place(x=0,y=0)
        label_user = Label(self.signup_frame, text="Username ",fg='black',bg="white",font='Calibri 12 bold')
        label_user.place(x=190, y=180)
        self.new_user = Entry(self.signup_frame,width=50,bg='white',font='Calibri 11')
        self.new_user.place(x=190, y=205)

        label_pswd = Label(self.signup_frame, text="Password ",fg='black',bg="white",font='Calibri 12 bold')
        label_pswd.place(x=190, y= 235)
        self.new_pswd = Entry(self.signup_frame,width=50,bg='white',show='*',font='Calibri 11')
        self.new_pswd.place(x=190, y=260)

        label_pswd_cf = Label(self.signup_frame, text="Confirm Password ",fg='black',bg="white",font='Calibri 12 bold')
        label_pswd_cf.place(x=190, y= 285)
        self.entry_pswd_cf = Entry(self.signup_frame,width=50,bg='white',show='*',font='Calibri 11')
        self.entry_pswd_cf.place(x=190, y=310)

        self.label_notice = Label(self.signup_frame,text="",fg='red',bg="white")
        self.label_notice.place(x=190, y=335)

        
        
        login_label = Label(self.signup_frame,text ="Already have an account? ", bg="white",font='Calibri, 11')
        login_label.place(x=190, y=360)

        Login_button = Button(self.signup_frame, text='Login here', bg='white',activebackground='white', font="Calibri 12 underline", borderwidth=0, command=self.loginPage)
        Login_button.place(x=350, y=356)

        button_log = Button(self.signup_frame,text="SUBMIT", bg='#274472', fg='white',font='Calibri 11 bold',command=self.signUp) 
        button_log.configure(width=25)
        button_log.place(x=330, y=420)

        self.signup_frame.pack(fill='both',expand=1)
    def hide_all(self):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.IP_frame.pack_forget()
    def layout(self,name):
        self.hide_all()
        
        vn = Label(self.main_frame, text='Việt Nam', font='Calibri, 15')
        vn.place(x=47, y=15)

        self.flag = ImageTk.PhotoImage(Image.open('VN.png'))
        self.main_canvas.create_image(48, 7, image=self.flag, anchor='ne')

        hello_label = Label(self.main_frame, text=f'Hello! {name}', font='Calibri, 13')
        hello_label.place(x=540, y=19)

        self.logout_icon = ImageTk.PhotoImage(Image.open('log-out.png'))

        logout_button = Button(self.main_frame, image=self.logout_icon, borderwidth=0, command=self.user_exit)
        logout_button.place(x=670, y=12)

        self.total_cases_label = Label(self.main_frame, font='Calibri 14', bg='#feb3b1', width=22, height=3)
        self.total_cases_label.place(x=18, y=59)
        self.recovered_label = Label(self.main_frame, font='Calibri 14', bg='#b1e0ae', width=22, height=3)
        self.recovered_label.place(x=245, y=59)
        self.deaths_label = Label(self.main_frame, font='Calibri 14', bg='light gray', width=22, height=3)
        self.deaths_label.place(x=472, y=59)

        self.main_canvas.create_text(105, 170, text='Tình hình dịch cả nước', font='Calibri 14 bold', fill='#303387')
        link1 = Label(self.main_frame, text="Bộ Y Tế", fg="blue", font='Calibri 10', cursor="hand2")
        link1.place(x=52, y=481)
        link1.bind("<Button-1>", lambda e: self.callback("https://covid19.gov.vn"))
        self.main_canvas.create_text(116, 500, text=rf'Theo '
                                                '\n'
                                               rf'Cập nhật liên tục trong vòng 1 giờ')
        style = ttk.Style()
        style.theme_use('vista')
        style.configure('Treeview', font='Calibri 13', rowheight=25)
        style.map('treeview')

        table_frame = Frame(self.main_frame)

        table_scroll = Scrollbar(table_frame)
        table_scroll.pack(side=RIGHT, fill=Y)

        self.my_table = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set)
        table_scroll.config(command=self.my_table.yview)
        self.my_table['columns'] = ('Tỉnh/TP','Hôm nay', 'Tổng số ca', 'Tử vong')

        self.my_table.column("#0", width=0, stretch=NO)
        self.my_table.column("Tỉnh/TP", anchor=W, width=200)
        self.my_table.column("Hôm nay", anchor=E, width=150)
        self.my_table.column("Tổng số ca", anchor=E, width=150)
        self.my_table.column("Tử vong", anchor=E, width=150)

        self.my_table.heading("#0", text="", anchor=CENTER)
        self.my_table.heading("Tỉnh/TP", text="Tỉnh/TP", anchor=W)
        self.my_table.heading("Hôm nay", text="Hôm nay", anchor=E)
        self.my_table.heading("Tổng số ca", text="Tổng số ca", anchor=E)
        self.my_table.heading("Tử vong", text="Tử vong", anchor=E)

        
        self.my_table.pack()
        table_frame.place(x=18, y=190)

        self.main_canvas.create_text(399, 172, text='Tỉnh/Thành phố', font='Calibri 13')

        
        self.cal = DateEntry(self.main_frame, width=12, bg="darkblue",date_pattern='yyyy-mm-dd', fg="white", year=2022, month=1)
        self.cal.place(x=230, y=163)

        self.search_icon = ImageTk.PhotoImage(Image.open('search.png').resize((25,25)))

        search_button = Button(self.main_frame, image=self.search_icon, borderwidth=0, command=self.Search)
        search_button.place(x=672, y=158)

        self.search_box = AutocompleteCombobox(self.main_frame, width=23, font='Calibri 12', completevalues=self.locations)

        self.search_box.place(x=460, y=160)
        if(self.running==False):
            return
        gui = threading.Thread(target=self.main,daemon=True)
        gui.start()
        
        self.main_frame.pack(fill='both', expand=1)

   
    def callback(self, url):
        webbrowser.open_new(url)

    def user_exit(self):
        if messagebox.askokcancel("Log out", "Are you sure you want to log out?"):
            self.hide_all()
            self.running=False
            self.logout = True
            self.client.send(str.encode('logout'))
            self.loginPage()
            self.logout = False
    def Search(self):
        location=self.search_box.get()
        day=self.cal.get()
        message=f'{location},{day}'
        print(f'search: {message}')
        self.send(message)
    def stop(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.running=False
            self.root.destroy()
            self.client.close()


    def send(self,msg):
        self.client.send(str.encode(msg))

    def receive(self,msg):
        try:
            message=eval(msg)
        except:
            message=str(msg)
        if(type(message)!=dict):
            messagebox.showinfo('ERROR', 'Không có dữ liệu')
        else:
            for item in self.my_table.get_children():
                self.my_table.delete(item)
            if(self.check == 0):
                total= message['total']['internal']['cases']
                deaths = message['total']['internal']['death']
                recovered = message['total']['internal']['recovered'] 
              
                self.total_cases_label.config(text=r'SỐ CA NHIỄM''\n'rf'{total:,}')
                self.recovered_label.config(text=r'KHỎI''\n'rf'{recovered:,}')
                self.deaths_label.config(text=r'SỐ CA TỬ VONG''\n'rf'{deaths:,}')
            self.count=0
            if('total' in msg):
                for location in message['locations']:
                    self.my_table.insert(parent='',index='end',iid = self.count,text='',values=(location['name'],f"+{location['casesToday']}",location['cases'],location['death']))
                    self.count += 1
            else:
                self.my_table.insert(parent='',index='end',iid = self.count,text='',values=(message['name'],f"+{message['casesToday']}",message['cases'],message['death']))
                self.count += 1
    def main(self):
        self.check=0
        while self.running:
            try:
                if(self.running==False):
                    break
                else:
                    res = self.client.recv(2048*4)
                    msg=res.decode('utf-8')
                    if(msg=="ok"): #client logout
                        return
                    self.receive(msg)
                    self.check = 1
            except:
                print("log out")
                if (self.logout==False):
                    if messagebox.showerror("ERROR", "SERVER TIMEOUT"):
                        print("Server timeout")
                        self.hide_all()
                        self.IP_frame.pack(fill='both', expand=1)
                    self.client.close()
                    break
c = client()




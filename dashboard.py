import json
import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, font, messagebox
from datetime import date
from login import Main_Window, Login
import sqlite3

class Dashboard:
    def __init__(self, window: tk.Tk) -> None:

        # DATABASE FILE OPEN
        self.con = Main_Window.create_connection()
        self.cur = self.con.cursor()

        self.check_tables()

        self.window = window
        # DASHBOARD BACKGROUND COLOR
        self.custom_bg = "#1F1A38"
        self.custom_fg = "#d3ceec"
        self.window.title("Dashboard")
        self.hovered_item = []

        # Flags
        self.add_invoice_flag = False
        self.history_invoice_flag = False
        self.add_item_flag = False
        self.IsZero = False
        self.IsLessThan = False

        # Dashboard Frame
        self.dashboard_frame = tk.Frame(self.window, bg=self.custom_bg, width=930, height=600)
        self.dashboard_frame.place(rely=0.5, relx=0.5, anchor=tk.CENTER)

        # Dashbard text # Dashboardka 2aad
        self.dashboard_text = tk.Label(self.dashboard_frame, text="Dashboard", bg=self.custom_bg, fg="#d3ceec",
                                       font=("yu gothic vi", 12, "bold") )
        self.dashboard_text.place(x=47, y=15)

        # Dashboard Icon
        self.dash_img = ImageTk.PhotoImage(Image.open("images/dashboard.png"))
        self.d_img = tk.Label(self.dashboard_frame, image=self.dash_img, bg=self.custom_bg,
                              )
        self.d_img.place(x=30, y=15.3)

        # LINE
        self.line_path = Image.open("images/line.png")
        self.line_img = ImageTk.PhotoImage(self.line_path)

        self.line = tk.Label(self.dashboard_frame, image=self.line_img, highlightthickness=0, border=0, relief=tk.FLAT)
        self.line.place(x=0, y=60)

        # ADD INVOICE
        self.add_ = ImageTk.PhotoImage(Image.open("images/plus.png").resize((200, 200)))
        
        self.add_button = tk.Button(self.dashboard_frame, bd=0, image=self.add_, bg=self.custom_bg, borderwidth=4, highlightbackground="#3480a8",
                                    activebackground=self.custom_bg, cursor="hand2", command=lambda: self.button_clicked("Button1"))
        self.add_button.place(x=40, y=140, width=200, height=200)

        self.add_text = tk.Label(self.dashboard_frame, text="NEW INVOICE", font=("yu gothic vi", 17, "bold"),
                                 fg="#d3ceec", bg="#2c7cc4", padx=22)
        self.add_text.place(x=40, y=105)
        self.add_button.bind("<Enter>", lambda event: self.button_onhover(event, self.add_button))
        self.add_button.bind("<Leave>", lambda event: self.button_onleave(event, self.add_button))

        # TRANSACTION HISTORY
        self.history = ImageTk.PhotoImage(Image.open("images/history.png").resize((180, 180)))
        self.history_button = tk.Button(self.dashboard_frame, bd=0, image=self.history, bg=self.custom_bg, borderwidth=4, highlightbackground="#3480a8",
                                    activebackground=self.custom_bg, cursor="hand2", command= lambda: self.button_clicked("Button2"))
        self.history_button.place(x=363, y=140, width=210, height=200)
        
        self.add_text = tk.Label(self.dashboard_frame, text="INVOICE HISTORY", font=("yu gothic vi", 17, "bold"),
                                 fg="#d3ceec", bg="#2c7cc4", padx=2)
        self.add_text.place(x=363, y=105)
        self.history_button.bind("<Enter>", lambda event: self.button_onhover(event, self.history_button))
        self.history_button.bind("<Leave>", lambda event: self.button_onleave(event, self.history_button))
    
        # ADD ITEM
        self.item = ImageTk.PhotoImage(Image.open("images/item.png").resize((200, 200)))
        self.item_button = tk.Button(self.dashboard_frame, bd=0, image=self.item, bg=self.custom_bg, borderwidth=4, highlightbackground="#3480a8",
                                    activebackground=self.custom_bg, cursor="hand2",
                                    command=lambda: self.button_clicked("Button3"))
        self.item_button.place(x=690, y=140, width=200, height=200)
        
        self.add_text = tk.Label(self.dashboard_frame, text="ADD ITEM", font=("yu gothic vi", 17, "bold"),
                                 fg="#d3ceec", bg="#2c7cc4", padx=42)
        self.add_text.place(x=690, y=105)
        self.item_button.bind("<Enter>", lambda event: self.button_onhover(event, self.item_button))
        self.item_button.bind("<Leave>", lambda event: self.button_onleave(event, self.item_button))
        
        
        # Lock 
        self.locked_image = ImageTk.PhotoImage(Image.open("images/locked.png"))

        self.locked = tk.Button(self.dashboard_frame, image=self.locked_image, text="LOCK SESSION", width=220, height=65, bg=self.custom_bg,
                                highlightthickness=0, relief=tk.FLAT, compound="left", font=("yu gothic UI", 14, "bold"), fg="#d3ceec",
                                activebackground=self.custom_bg, activeforeground="#4C8CB4", border=0, command=self.on_lock, cursor="hand2")
        self.locked.place(x=363, y= 500)

        # SETTING
        self.menu_icon = ImageTk.PhotoImage(Image.open("images/setting.png"))
        self.setting_button = tk.Button(self.dashboard_frame, image=self.menu_icon, bg=self.custom_bg,
                                        activebackground=self.custom_bg, border=0, cursor="hand2")
        self.setting_button.place(x=870, y=15.3)
        self.setting_button.bind("<Button-1>", lambda event: self.menu.post(event.x_root, event.y_root))
        self.menu = tk.Menu(self.dashboard_frame, tearoff=False, background="#4c8cb4", fg="#d3ceec",
                            activebackground="#4ba4cc", activeforeground="black")

        self.submenu = tk.Menu(self.menu, tearoff=False, background="#4c8cb4", fg="#d3ceec",
                            activebackground="#4ba4cc", activeforeground="black")
        self.menu.add_cascade(label="Resolution", menu=self.submenu)

        self.submenu.add_radiobutton(label="Fullscreen", command=lambda: self.set_screen_size("full"))
        self.submenu.add_separator()
        self.submenu.add_radiobutton(label="930x600", command= lambda: self.set_screen_size("930x600"))
        
        self.window.bind("<Return>", lambda event: self.check_focus(), add='+')
        self.window.bind("<Up>", lambda event: self.move_down("up"), "+")
        self.window.bind("<Down>", lambda event: self.move_down("down"), "+")

    def button_clicked(self, event):
        # print(event, " Clicked!")

        if event == "Button1":
            if not self.add_invoice_flag:
                self.handle_button_1() 
            
            else:
                self.invoice_frame.place(x=20, y=67)
                self.dashboard_text.config(text="New Invoice")
        elif event == "Button2":
            self.handle_button_2()

        elif event == "Button3":
            if not self.add_item_flag:
                self.handle_button_3() 
            
            else:
                self.item_frame.place(x=20, y=67)
                self.dashboard_text.config(text="Add Item")
    # Button color
    def button_onhover(self, event, button_name):
        button_name.configure(bg="#d3ceec")

    def button_onleave(self, event, button_name):
        button_name.configure(bg=self.custom_bg)

    def on_lock(self):
        self.dashboard_frame.place_forget()
        login.show_login()
        try: login.vector_text['text'] = "WELCOME BACK, " + open(".last_login.txt").read().split("\n")[0].upper()\
        + "\nPLEASE LOGIN TO CONTINUE ...."
        except: pass

    def check_tables(self):
        tables = ["invoices", "items"]
        
        self.con.execute("""CREATE TABLE IF NOT EXISTS {} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Customer_name TEXT NOT NULL,
        Item_name TEXT NOT NULL,
        Item_price REAL,
        Quantity INT,
        Invoice_date TEXT,
        Invoice_no INT,
        Sales_person TEXT
    )""".format(tables[0]))
        
        self.con.execute("""CREATE TABLE IF NOT EXISTS {} (
        Item_name TEXT NOT NULL,
        Description TEXT,
        Quantity REAL,
        Price REAL,
        Category TEXT,
        Date TEXT
        )""".format(tables[1]))

        self.con.commit()

    def set_screen_size(self, size):
        if size == "full":
            self.window.state("zoomed")
            self.submenu.entryconfig(0, state=tk.DISABLED)
            self.submenu.entryconfig(2, state=tk.NORMAL)
        else:
            self.window.state("normal")
            self.window.geometry(f"{size}")
            self.submenu.entryconfig(0, state=tk.NORMAL)
            self.submenu.entryconfig(2, state=tk.DISABLED)
    def move_down(self, direction):
        try:
            master = self.invoice_frame
            enteries = [i for i in master.winfo_children() if all([isinstance(i, tk.Entry), i['state'] != "disabled"])]
        except (ValueError, AttributeError):
            try:
                master = self.item_frame
                enteries = [i for i in master.winfo_children() if all([isinstance(i, tk.Entry), i['state'] != "disabled"])]
            except: return

        try: current_index = enteries.index(self.window.focus_get())
        except ValueError: return
        if current_index == 0 and direction == "up":
            return
        try: 
            next_entry = enteries[(current_index) - 1 if direction == "up" else (current_index) + 1]
        except IndexError: return
        next_entry.focus_set()

    def check_focus(self):
        try:
            if self.window.focus_get() in [entry for entry in self.invoice_frame.winfo_children() if isinstance(entry, tk.Entry)]:
                self.handle_submit(self.invoice_frame)
        except: pass

        try:
            if self.window.focus_get() in [entry for entry in self.item_frame.winfo_children() if isinstance(entry, tk.Entry)]:
                self.handle_submit(self.item_frame, isInvoie=False)
        except: pass

    def handle_button_1(self):
        self.invoice_frame = tk.Frame(self.dashboard_frame, width=880, height=400, bg=self.custom_bg)
        self.invoice_frame.place(x=20, y=67)
        self.dashboard_text.config(text="New Invoice")
        self.empty = "      "
        self.quan = tk.IntVar(value="")
        self.item_var = tk.StringVar()

        customer = self.make_entry_with_text(self.invoice_frame,"Customer Name", x=17*15, y=25)
        customer['entry'].focus_set()

        item = self.make_entry_with_text(self.invoice_frame, "Item Name", x=17*15, y=65)
        item['entry'].config(textvariable=self.item_var)
        self.item_var.trace("w", self.on_item)
        self.item_price = self.make_entry_with_text(self.invoice_frame, "Item Price", x=17*15, y=105)
        self.item_price['entry'].insert(0, "      " +"CALCULATING.....")
        self.item_price['entry'].config(state="disabled", disabledbackground=self.custom_bg, cursor= "X_cursor")

        quantity = self.make_entry_with_text(self.invoice_frame, "Quantity", x=17*15, y=145)
        quantity['entry'].config(textvariable=self.quan)
        self.quan.trace("w", self.quan_change)

        invoice_date = self.make_entry_with_text(self.invoice_frame, "Invoice Date", x=17*15, y=185)
        invoice_date['entry'].insert(0, self.empty + date.today().strftime("%Y-%m-%d"))
        invoice_date['entry'].config(state="disabled", disabledbackground=self.custom_bg, cursor= "X_cursor")

        self.invoice_number = self.make_entry_with_text(self.invoice_frame, "Invoice #", x=17*15, y=225)
        self.cur.execute("SELECT COUNT(*) FROM invoices")
        inv = str(self.cur.fetchone()[0]+1)
        self.invoice_number['entry'].insert(0, self.empty + inv)
        self.invoice_number['entry'].config(state="disabled", disabledbackground=self.custom_bg, cursor="X_cursor")

        sales_person = self.make_entry_with_text(self.invoice_frame, "Sales Person", x=17*15, y=265)
        try: name = open(".last_login.txt", "r").read().split("\n")[0].strip()
        except FileNotFoundError: name = "Unknown operator"
        sales_person['entry'].insert(0, self.empty + name.upper())
        sales_person['entry'].config(state="disabled", disabledbackground=self.custom_bg, cursor="X_cursor")

        self.submit_button = tk.Button(self.invoice_frame, width=25, text="Submit", bg="#3c9ce4", cursor="hand2", activeforeground="black",
                                       activebackground="#3c9ce4", fg="#d3ceec", command=lambda: self.handle_submit(self.invoice_frame), border=0, font=("Yu Gothic", 12, "bold"))
        
        self.submit_button.place(x=45*6.5, y=325)
        self.back_icon = ImageTk.PhotoImage(Image.open("images/arrow.png"))
        self.back_button = tk.Button(self.invoice_frame, image=self.back_icon, bg=self.custom_bg,
                                        activebackground=self.custom_bg, border=0, cursor="hand2",
                                        command= lambda: (self.invoice_frame.place_forget(), 
                                                          setattr(self, "add_invoice_flag", True),
                                                          self.dashboard_text.config(text="Dashboard"))
                                                          )
        self.back_button.place(x=60, y=15.3)

    # Button 2
    def handle_button_2(self):
        self.history_frame = tk.Frame(self.dashboard_frame, width=920, height=400, bg=self.custom_bg)
        self.history_frame.place(x=20, y=67)
        self.dashboard_text.config(text="Transaction History")
        # DELETE 
        self.delete_img = ImageTk.PhotoImage(Image.open("images/delete.png"))


        self.invoice_tree = ttk.Treeview(self.history_frame, columns=("1", "2", "3", "4", "5", "6", "7", "8"), selectmode="browse")
        self.invoice_tree.heading("1", text="ID")
        self.invoice_tree.heading("2", text="Customer Name")
        self.invoice_tree.heading("3", text="Item Name")
        self.invoice_tree.heading("4", text="Item Price")
        self.invoice_tree.heading("5", text="Quantity")
        self.invoice_tree.heading("6", text="Invoice Date")
        self.invoice_tree.heading("7", text="Invoice #")
        self.invoice_tree.heading("8", text="Sales Person")

        self.invoice_tree.bind("<Motion>", self.on_mouse_enter)
        self.invoice_tree.bind("<Button-1>", self.on_mouse_enter)

        self.invoice_tree.column("#0", width=50, anchor=tk.CENTER)
        self.invoice_tree.column("1", width=40, anchor=tk.CENTER)
        for i in range(2, 9):
            if i in [7, 5]:
               self.invoice_tree.column(i, width=93, anchor="center")
            else: self.invoice_tree.column(f"{i}", width=120, anchor="center")

        self.invoice_tree.place(x=0, y=30, relheight=0.9)
        self.scroll_bar = tk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.invoice_tree.yview)
        self.scroll_bar.place(x=881, y=25, relheight=0.92)
        self.invoice_tree.config(yscrollcommand=self.scroll_bar.set)
        self.invoice_tree.tag_configure("blueish", background="#584f92", foreground='white')
        self.invoice_tree.tag_configure("normal", background="white")
        self.invoice_tree.tag_configure('highlight', background='lightblue')

        for row in self.cur.execute("SELECT * FROM invoices"):
            tag = "blueish" if row[0] % 2 == 0 else "normal"
            self.invoice_tree.insert("", tk.END, row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),tags=(tag))

        self.refresh_items()

        self.back_icon2 = ImageTk.PhotoImage(Image.open("images/arrow.png"))
        self.back_button2 = tk.Button(self.history_frame, image=self.back_icon2, bg=self.custom_bg,
                                        activebackground=self.custom_bg, border=0, cursor="hand2",
                                        command= lambda: (self.history_frame.place_forget(), 
                                                          self.dashboard_text.config(text="Dashboard"))
                                                          )
        self.back_button2.place(x=0, y=0)

    def refresh_items(self):
        tree = self.invoice_tree
        for index, item in enumerate(tree.get_children()):
            tag = "blueish" if (index+1) % 2 == 0 else "normal"
            item_ = tree.item(item)
            tree.item(item, values=(index+1,) + tuple(item_['values'][1:]))
            tree.tk.call(tree, "tag", "remove", "blueish", item)
            tree.tk.call(tree, "tag", "remove", "normal", item)
            tree.tk.call(tree, "tag", "add", tag, item)

    def on_mouse_enter(self, event):
        tree = self.invoice_tree
        item = tree.identify_row(event.y)

        if tree.identify_column(event.x) == "#0":
            tree.config(cursor="hand2")
        else:
            tree.config(cursor="")

        if event.type == "4" and tree.identify_column(event.x) == "#0":
            result = messagebox.askyesno("Confirm", message="Are you sure you want to delete?")
            print(result)
            if result is True:
                tree.delete(item)
                self.cur.execute("DELETE FROM invoices where id=?", (item))
                self.con.commit()
                self.refresh_items()
    
        if len(self.hovered_item) == 2:
            try:
                tree.item(self.hovered_item[1], image="")
                tree.tk.call(tree, "tag", "add", self.hovered_item[0], self.hovered_item[1])
            except: pass

    
        if item:
            tree.tk.call(tree, "tag", "remove", "highlight")
            try:
                tree.tk.call(tree, "tag", "remove", "blueish", item)
                tree.tk.call(tree, "tag", "remove", "normal", item)
                
                tree.tk.call(tree, "tag", "add", "highlight", item)
                tree.item(item, image=self.delete_img)
                
                self.current_tag = ['blueish' if int(tree.item(item)['values'][0]) % 2 == 0 else 'normal']

                self.hovered_item = [self.current_tag, item]
            except: pass

    def handle_button_3(self):
        self.item_frame = tk.Frame(self.dashboard_frame, width=920, height=400, bg=self.custom_bg)
        self.item_frame.place(x=20, y=67)
        self.dashboard_text.config(text="Add Item")
        y = 25

        item_name = self.make_entry_with_text(self.item_frame, "Item Name", x=17*15, y=y)
        item_name['entry'].focus_set()
        description = self.make_entry_with_text(self.item_frame, "Description", x=17*15, y=(y:= y+40))
        quantity = self.make_entry_with_text(self.item_frame, "Quantity", x=17*15, y=(y:= y+40))
        price = self.make_entry_with_text(self.item_frame, "Price", x=17*15, y=(y:= y+40))
        category = self.make_entry_with_text(self.item_frame, "Category", x=17*15, y=(y:= y+40))
        time_ =  self.make_entry_with_text(self.item_frame, "Date", x=17*15, y=(y:= y+40))
        time_['entry'].insert(0, "      " + date.today().strftime("%Y-%m-%d"))
        time_['entry'].config(state="disabled", disabledbackground=self.custom_bg, cursor= "X_cursor")

        self.submit_button3 = tk.Button(self.item_frame, width=25, text="Submit", relief=tk.FLAT, bg="#3c9ce4", cursor="hand2", activeforeground="black",
                                       activebackground="#3c9ce4", fg="#d3ceec", command=lambda: self.handle_submit(self.item_frame, isInvoie=False), border=0, font=("Yu Gothic", 12, "bold"))
        
        self.submit_button3.place(x=45*6.5, y=280)

        self.back_icon3 = ImageTk.PhotoImage(Image.open("images/arrow.png"))
        self.back_button3 = tk.Button(self.item_frame, image=self.back_icon3, bg=self.custom_bg,
                                        activebackground=self.custom_bg, border=0, cursor="hand2",
                                        command= lambda: (self.item_frame.place_forget(), 
                                                          setattr(self, "add_item_flag", True),
                                                          self.dashboard_text.config(text="Dashboard"))
                                                          )
        self.back_button3.place(x=60, y=15.3)
    
    def fetch_database(self):
        item_name = []
        description = []
        quantity = []
        item_price = []
        category = []
        date_ = []
        for item in self.cur.execute("SELECT * FROM items"):
            item_name.append(item[0])
            description.append(item[1])
            quantity.append(item[2])
            item_price.append(item[3])
            category.append(item[4])
            date_.append(item[5])
        return {'item_name': item_name, 'description': description, 'quantity': quantity, 'item_price': item_price, 'category': category, 'date_': date_}

    def quan_change(self, *args):
        self.item_price['entry'].config(state="normal")
        self.item_price['entry'].delete(0, tk.END)
        try: 
            res = self.quan.get()
        except: res = "UNKNOWN"
        getd = self.fetch_database()
        if self.item_var.get() in getd['item_name']:
            ind = getd['item_name'].index(self.item_var.get())
            try: 
                if res > getd['quantity'][ind]:
                    messagebox.showwarning(title="Error", message=f"You don't have enought quantity for this item, you only have {int(getd['quantity'][ind])}")
                    self.item_price['entry'].insert(0, self.empty + str("UNKNOWN"))
                    self.item_price['entry'].config(state="disabled")
                    self.quan.initialize("")
                    self.IsLessThan = True
                    return 0
                elif res == 0:
                    messagebox.showwarning(title="Error", message="Quantity can't be equal to zero")
                    self.item_price['entry'].insert(0, self.empty + str("UNKNOWN"))
                    self.item_price['entry'].config(state="disabled")
                    self.quan.initialize("")
                    self.IsZero = True
                    return 0
                else:
                    self.IsZero = False
                    self.IsLessThan = False
            except TypeError: pass
            try: res = res * getd['item_price'][ind]
            except TypeError: res = 'UNKNOWN'
        else:
            res = "UNKNOWN"
        self.item_price['entry'].insert(0, self.empty + str(res))
        self.item_price['entry'].config(state="disabled")

    def on_item(self, *args):
        pass

    def handle_submit(self, frame: tk.Frame, *, isInvoie: bool = True):
        try:
            if self.quan_change() == 0:
                return
        except AttributeError: pass

        name = "invoices" if isInvoie else "items"
        data = {}

        self.cur.execute("""SELECT Item_name FROM items""")
        res = self.cur.fetchall()
        item_list = [row[0] for row in res]
    
        for children in frame.winfo_children():
            if isinstance(children, tk.Entry):
                if children.get() == '':
                    messagebox.showerror(title="Empty", message="Please fill all entries.")
                    return
                if isInvoie and children.winfo_name() == "item name" and children.get() not in item_list:
                    messagebox.showerror(title="Item Not Found", message="This item doesn't exist, please add Item first..")
                    return
                data[children.winfo_name()] = children.get().strip()
                
                
        if data and name == "items":
            self.con.execute("""INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)""", (data['item name'], data['description'],
                                data['quantity'], data['price'], data['category'], data['date']))
            self.con.commit()
            
        elif data and name == "invoices":
            self.con.execute("""INSERT INTO invoices(Customer_name, Item_name, Item_price, Quantity, Invoice_date, Invoice_no, Sales_person)
              VALUES(?, ?, ?, ?, ?, ?, ?)""", (data['customer name'], data['item name'],
                                data['item price'], data['quantity'], data['invoice date'], data['invoice #'], data['sales person']))

            ind = self.fetch_database()['item_name'].index(self.item_var.get())
            calculated_quantity = self.fetch_database()['quantity'][ind] - self.quan.get()
            self.con.execute("UPDATE items set quantity = ? where Item_name = ?", (calculated_quantity,self.item_var.get()))

            self.con.commit()

            self.invoice_number['entry'].config(state="normal")
            self.invoice_number['entry'].delete(0, tk.END)
            self.cur.execute("SELECT COUNT(*) FROM invoices")
            inv = self.cur.fetchone()[0]
            self.invoice_number['entry'].insert(0, self.empty + str(inv+1))
            self.invoice_number['entry'].config(state="disabled")

        messagebox.showinfo(title="Success", message=f"New {name} has been added successfully.")
        first_entry = min([index for index, entry in enumerate(frame.winfo_children()) if isinstance(entry, tk.Entry)])
            
        delete = [(entry.delete(0,  tk.END), entry.focus_set() if index == first_entry else entry.delete(0, tk.END))\
                       for index, entry in enumerate(frame.winfo_children()) if isinstance(entry, tk.Entry)]
            
    def make_entry_with_text(
            self,
            master: tk.Misc, 
            entry_name: str, 
            *, 
            x: str | float = ..., 
            y: str | float = ...) -> dict[str, tk.Label | tk.Entry]:
        
        self.text = tk.Label(master, text=entry_name, bg=self.custom_bg, fg=self.custom_fg, font=("Yu Gothic UI", 12, "bold"))
        self.text.place(x=x, y=y)
        self.info = [i for i in master.winfo_children() if isinstance(i, tk.Entry)]
        try: 
            self.info[0].update_idletasks()
            # print(self.info[1].winfo_width())
        except: pass

        self.customer_entry = tk.Entry(master, name=entry_name.lower(),bg=self.custom_bg, insertbackground="#3c9ce4", highlightthickness=0,
                                    fg="#cbe8fb", relief=tk.FLAT)
        
        font_  = font.Font(font=self.text['font'])
        text_width = font_.measure(entry_name)
        
        self.customer_entry.place(x=x + text_width + 8, y=y, width=250)

        self.underline = tk.Canvas(master, width=250, height=2, highlightthickness=0, bg="#737472")
        self.underline.place(x=x + text_width + 8, y= y + 21)

        return {"label": self.text, "entry": self.customer_entry}

if __name__ == "__main__":
    window = tk.Tk()

    main = Main_Window(window)
    login = Login(window, next_window=Dashboard)
    # dashboard = Dashboard(window) # For testing
    window.mainloop()


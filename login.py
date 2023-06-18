import os
import sqlite3
import threading 
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import json
import winsound



class Login:
    def __init__(self, window: tk.Tk, next_window: type =None) -> None:
        self.window = window
        self.next_window = next_window
        self.window.title("Login")
        # LOGIN BACKGROUND COLOR
        self.custom_bg = "#1F1A38"

        # LOGIN PANEL
        self.login_frame = tk.Frame(self.window, bg=self.custom_bg, width=930, height=600)
        self.login_frame.place(relx=0.5  , rely=0.5, anchor=tk.CENTER)

        # TOP NAME TEXT

        # VECTOR IMAGE
        self.vector_image = Image.open(f"images/vector{random.choice([2, 3])}.png")
        self.vector_image_resized = self.vector_image.resize((int(self.login_frame.winfo_screenwidth() // 3 * 1.4), int(self.login_frame.winfo_screenheight() // 2 * 1.4)))
        self.vector = ImageTk.PhotoImage(self.vector_image_resized)

        self.vector_panel = tk.Label(self.login_frame, image=self.vector, bg="#1F1A38")
        self.vector_panel.place(x=380, y=60)

        # VECTOR TEXT
        try: self.name = "WELCOME BACK, " + open(".last_login.txt").read().upper()
        except FileNotFoundError: self.name = "WELCOME!, "
        self.vector_text = tk.Label(self.login_frame, text=f"{self.name}\nPLEASE LOGIN TO CONTINUE ....", justify="left", bg="#1F1A38", fg="#d3ceec", font=("Yu Gothic", 17, "bold"))
        self.vector_text.place(x=475, y=30)

        # User Icon
        self.user_icon = Image.open("images/user.png")
        self.user_icon_image = ImageTk.PhotoImage(self.user_icon)

        self.user_icon_label = tk.Label(self.login_frame, image=self.user_icon_image, bg="#1F1A38")
        self.user_icon_label.place(x=120, y=120)

        # Login Text
        self.text_login = tk.Label(self.login_frame, text="Login", fg="#d3ceec", bg="#1F1A38", font=("Yu Gothic", 12, "bold"))
        self.text_login.place(x=135, y=200)

        # Username text 
        self.username_text = tk.Label(self.login_frame, text="Login", bg="#1F1A38", fg="#7c8993", font=("Yu Gothic vi", 12, "bold"))
        self.username_text.place(x=40, y=250)

        self.username_entry = tk.Entry(self.login_frame, highlightthickness=0, insertbackground="#3c9ce4", relief=tk.FLAT, bg="#1F1A38", fg="#cbe8fb", font=("Yu Gothic vi", 10, "bold"))
        self.username_entry.place(x=69, y=275, width=250)

        self.username_underline = tk.Canvas(self.login_frame, width=250, height=2, highlightthickness=0, bg="#737472")
        self.username_underline.place(x=40, y=296)

        #Username Icon
        self.username_icon_path = Image.open("images/username.png")
        self.username_icon = ImageTk.PhotoImage(self.username_icon_path)

        self.username_icon_label = tk.Label(self.login_frame, image=self.username_icon, bg=self.custom_bg)
        self.username_icon_label.place(x=40, y=275)
        # Password text 
        self.password_text = tk.Label(self.login_frame, text="Password", bg=self.custom_bg, fg="#7c8993", font=("Yu Gothic vi", 12, "bold"))
        self.password_text.place(x=40, y=320)

        self.password_entry = tk.Entry(self.login_frame, highlightthickness=0, insertbackground="#3c9ce4" ,show="*",relief=tk.FLAT, bg="#1F1A38", fg="#cbe8fb", font=("yu gothic", 10, "bold"))
        self.password_entry.place(x=69, y=345, width=250)

        self.password_underline = tk.Canvas(self.login_frame, width=250, height=2, highlightthickness=0, bg="#737472")
        self.password_underline.place(x=40, y=366)

        #Password Icon
        self.password_icon_path = Image.open("images/password.png")
        self.password_icon = ImageTk.PhotoImage(self.password_icon_path)

        self.password_icon_label = tk.Label(self.login_frame, image=self.password_icon, bg="#1F1A38")
        self.password_icon_label.place(x=40, y=345)

        # HIDE AND SHOW PASSWORD
        self.show_password_path = Image.open("images/show.png")
        self.show_password = ImageTk.PhotoImage(self.show_password_path)

        self.show_password_button = tk.Button(self.login_frame, cursor="hand1", image=self.show_password, bg="#1F1A38", border=0, activebackground="#1F1A38",highlightthickness=0, relief=tk.FLAT, command=self._show_password)
        self.show_password_button.place(x=270, y=345)

        # FOCUS SET TO EMAIL BY DEFAULT
        self.username_entry.focus_set()

        # Login Button
        self.login_button = tk.Button(self.login_frame, bg="#3c9ce4", activebackground="#3c9ce4", text="Login", font=("Yu Gothic", 12, "bold"), \
                fg="#d3ceec", width=25, cursor='hand2', highlightthickness=0, relief=tk.FLAT, border=0, activeforeground="#7c8993", command=self.on_click)
        self.login_button.place(x=40, y=400)
        self.window.bind("<Return>", lambda event: self.check_focus())

        # SETTING
        self.menu_icon = ImageTk.PhotoImage(Image.open("images/setting.png"))
        self.setting_button = tk.Button(self.login_frame, image=self.menu_icon, bg=self.custom_bg,
                                        activebackground=self.custom_bg, border=0, cursor="hand2")
        self.setting_button.place(x=870, y=15.3)
        self.setting_button.bind("<Button-1>", lambda event: self.menu.post(event.x_root, event.y_root))
        self.menu = tk.Menu(self.login_frame, tearoff=False, background="#4c8cb4", fg="#d3ceec",
                            activebackground="#4ba4cc", activeforeground="black")

        self.submenu = tk.Menu(self.menu, tearoff=False, background="#4c8cb4", fg="#d3ceec",
                            activebackground="#4ba4cc", activeforeground="black", disabledforeground="#808080")
        self.menu.add_cascade(label="Resolution", menu=self.submenu)

        self.submenu.add_radiobutton(label="Fullscreen", command=lambda: self.set_screen_size("full"))
        self.submenu.add_separator()
        self.submenu.add_radiobutton(label="930x600", command= lambda: self.set_screen_size("930x600"))

        self.window.bind("<Escape>", lambda event: self.set_screen_size("930x600"))
        self.window.bind("<Down>", lambda event: self.move_down("down"))
        self.window.bind("<Up>", lambda event: self.move_down("up"))
    
    def move_down(self, direction):
        enteries = [i for i in self.login_frame.winfo_children() if isinstance(i, tk.Entry)]

        try: current_index = enteries.index(self.window.focus_get())
        except ValueError: return
        if current_index == 0 and direction == "up":
            return

        try: next_entry = enteries[(current_index) - 1 if direction == "up" else + (current_index) + 1]
        except IndexError: return
        next_entry.focus_set()

    def check_focus(self):
        if self.window.focus_get() in (self.username_entry, self.password_entry):
            self.on_click()

    def _show_password(self):
        self.hide_password_path = Image.open("images/hide.png")
        self.hide_password = ImageTk.PhotoImage(self.hide_password_path)
        self.show_password_button.config(image=self.hide_password, command=self._hide_password)
        self.password_entry.config(show="")

    def _hide_password(self):
        self.show_password_button.config(image=self.show_password, command=self._show_password)
        self.password_entry.config(show="*")

    def on_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        admins = json.loads(open("admins.json").read())


        admin_usernames = [user["username"] for user in admins["users"]]
        admin_passwords = [password["password"] for password in admins["users"]]
        
        if username in admin_usernames and password in admin_passwords\
              and (admin_usernames.index(username) == admin_passwords.index(password)):
            try: self.label_error.destroy()
            except AttributeError: pass
            with open(".last_login.txt", "w") as file:
                file.write(username)
            self.label_success = tk.Label(self.login_frame, text="Login Successful", \
                bg="#1F1A38", fg="#3ca4e4", font=("Consolas", 13))
            self.label_success.place(relx=0.5, rely=0, anchor=tk.N)
            self.animate_success_label()
            self.login_frame.grid_forget()


        else:
            self.play_error_sound()
            self.label_error = tk.Label(self.login_frame, text="Invalid username and/or password", \
                bg="#1F1A38", fg="red", padx=34, pady=2, font=("Consolas", 10))
            self.label_error.place(x=21, y=438)
            self.label_error.after(2000, self.label_error.place_forget)
            # messagebox.showerror("Error", "Invalid username and/or password")

    def animate_success_label(self):
        current_bg = self.label_success["bg"]
        new_bg = "#32CD32" if current_bg == "#1F1A38" else "#1F1A38"  
        self.label_success.config(bg=new_bg)
        self.label_success.after(500, self.go_to_next_window)

    def go_to_next_window(self):
        self.login_frame.place_forget()
        try: dashboard = self.next_window(self.window)
        except TypeError:
            self.window.destroy()
            print("!! PLEASE RUN THE DASHBOARD FILE TO SEE EVERYTHING !!")


    def show_login(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.label_success.config(text="", bg="#1F1A38")
        self.username_entry.focus()
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def play_error_sound(self):
        def sound_thread():
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

        sound_thread = threading.Thread(target=sound_thread)
        sound_thread.start()

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

    
class Main_Window:
    def __init__(self, window: tk.Tk):
        self.window = window

        if os.path.exists(f:=".last_dimensions.txt"):
            dimensions = open(f).read().strip()
            if dimensions == "zoomed":
                self.window.state(f"{dimensions}")
            else: self.window.geometry(f"{dimensions}")
        else: self.window.state("zoomed")
        self.window.resizable(0, 0)

        # Background Imageka kaga daray halkan
        bg = random.choice(['', 2])
        self.bg_image = Image.open(f"images/bg{bg}.jpg")
        self.bg_image_resied = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg = ImageTk.PhotoImage(self.bg_image_resied)
        self.bg_panel = tk.Label(self.window, image=self.bg)
        self.bg_panel.pack()

        # ICON
        self.image = Image.open("images/icon3.png")
        self.icon = ImageTk.PhotoImage(self.image)
        self.window.iconphoto(True, self.icon)

        # ON CLOSE
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    def create_connection():
        global conn
        conn = sqlite3.connect("invoices.db")
        return conn
    def on_close(self):
        dimensions = self.window.winfo_geometry()
        if self.window.state() == "zoomed":
            dimensions = "zoomed"
        open(".last_dimensions.txt", 'w').write(dimensions)
        self.window.destroy()

if __name__ == "__main__":
    window = tk.Tk()

    # We assign the new instantce to a variable to avoid garbage collector to interfer with our class #
    main = Main_Window(window)
    login = Login(window)

    window.mainloop()
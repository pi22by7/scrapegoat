from tkinter import *
from tkinter import ttk
# import scraper


def main_win():
    root = Tk()
    root.geometry("720x480")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Scrip Scrap, This Is A Trap").grid(column=0, row=0)

    menubar = Menu(root)
    menu_file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=menu_file)
    menu_file.add_command(label="Quit", command=root.quit)
    root.config(menu=menubar)
    root.mainloop()


if __name__ == "__main__":
    main_win()

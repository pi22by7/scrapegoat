import tkinter as tk
from tkinter import filedialog, messagebox, END
from scrape_engine import ScrapeEngine


class ScrapeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraping Application")

        # URL input
        self.label_url = tk.Label(master, text="Enter the URL to scrape:")
        self.label_url.pack()
        self.entry_url = tk.Entry(master)
        self.entry_url.pack()

        # Element name input
        self.label_element = tk.Label(master, text="Enter the element name:")
        self.label_element.pack()
        self.entry_element = tk.Entry(master)
        self.entry_element.pack()

        # Class name input
        self.label_class = tk.Label(master, text="Enter the class name (optional):")
        self.label_class.pack()
        self.entry_class = tk.Entry(master)
        self.entry_class.pack()

        # ID name input
        self.label_id = tk.Label(master, text="Enter the ID name (optional):")
        self.label_id.pack()
        self.entry_id = tk.Entry(master)
        self.entry_id.pack()

        # Scrape button
        self.button_scrape = tk.Button(master, text="Scrape", command=self.scrape)
        self.button_scrape.pack()

    def scrape(self):
        # Get user input
        url = self.entry_url.get()
        element_name = self.entry_element.get()
        class_name = self.entry_class.get()
        id_name = self.entry_id.get()

        # Create an instance of the ScrapeEngine class
        engine = ScrapeEngine()
        engine.url = url
        engine.element_name = element_name
        engine.class_name = class_name
        engine.id_name = id_name

        # Prompt user to select output file
        engine.filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                       filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))

        # Perform scraping and save to CSV
        engine.request()
        print(engine.url, engine.element_name, engine.class_name, engine.id_name, engine.filename)
        # engine.write_to_csv(file_name)
        messagebox.showinfo("Scraping Complete", "Scraping has been completed successfully.")

        # Clear the entry fields
        self.entry_url.delete(0, END)
        self.entry_element.delete(0, END)
        self.entry_class.delete(0, END)
        self.entry_id.delete(0, END)


if __name__ == "__main__":
    root = tk.Tk()
    scrape_gui = ScrapeGUI(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox


class ConnectionGui:
    def __init__(self):
        self.tk = tk.Tk()
        self.client_url = None
        self.server_host = None
        self.server_port = None
        self.has_requested_connection = False
        tk.Label(text="Client URL").grid(row=0, column=0)
        tk.Label(text="Server host").grid(row=1, column=0)
        tk.Label(text="port").grid(row=1, column=2)
        self.__client_url_entry = tk.Entry(self.tk, textvariable=tk.StringVar(self.tk, 'http://localhost:5000'))
        self.__server_host_entry = tk.Entry(self.tk)
        self.__server_port_entry = tk.Entry(self.tk, textvariable=tk.StringVar(self.tk, '5000'))
        self.__client_url_entry.grid(row=0, column=1)
        self.__server_host_entry.grid(row=1, column=1)
        self.__server_port_entry.grid(row=1, column=3)
        tk.Button(self.tk, text="Connect", command=self.try_parsing_entries).grid(row=4, column=0)

    def update(self):
        self.tk.update()

    def quit(self):
        self.tk.destroy()

    def try_parsing_entries(self):
        self.client_url = self.__client_url_entry.get()
        self.server_host = self.__server_host_entry.get()
        self.server_port = self.__server_port_entry.get()
        try:
            self.server_port = int(self.server_port)
            if not (0 <= self.server_port < 65536):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Bad port value", "The port must be an integer between 0 and 65535!")
            return None
        self.has_requested_connection = True


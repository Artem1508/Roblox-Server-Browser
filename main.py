import tkinter as tk
from tkinter import ttk
import requests
import webbrowser
import random
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser

PLACE_ID = 147848991

class RobloxServerBrowser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Roblox Server Browser")
        self.root.geometry("700x550")

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('Treeview', rowheight=30, borderwidth=1, relief='solid')

        self.table = ttk.Treeview(self.root, columns=("index","players","max","visited"), show="headings")
        self.table.heading("index", text="Index",anchor=tk.W)
        self.table.heading("players", text="Players",anchor=tk.W)
        self.table.heading("max", text="Max",anchor=tk.W)
        self.table.heading("visited", text="Visited",anchor=tk.W)
        self.table.column("index", width=50, minwidth=50)
        self.table.column("players",width=100, minwidth=100)
        self.table.column("max", width=150, minwidth=150)
        self.table.column("visited", width=50, minwidth=50)
        
        self.table.tag_configure('even', background='#f0f0f0')
        self.table.tag_configure('odd', background='#ffffff')
        self.table.tag_configure('true',background="#80f585")

        self.frame = tk.Frame(self.root)
        self.last_box=tk.Label(self.frame, text="Last visited is NONE")
        self.refresh_btn = tk.Button(self.frame, text="Refresh Servers", command=self.get_servers, bg="#4CAF50", fg="#ffffff")
        self.join_btn = tk.Button(self.frame, text="Join Selected", command=self.join_selected, bg="#2196F3", fg="#ffffff")
        self.hop_btn = tk.Button(self.frame, text="Server Hop", command=self.hop_server, bg="#9C27B0", fg="#ffffff")

        self.table.grid(row=0, column=0, sticky="nsew")
        self.frame.grid(row=1, column=0, sticky="ew")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.last_box.pack(side="left", padx=5)
        self.refresh_btn.pack(side="right", padx=5)
        self.join_btn.pack(side="right", padx=5)
        self.hop_btn.pack(side="right", padx=5)
        
    def get_servers(self):
        

        self.table.delete(*self.table.get_children())
        for i, s in enumerate(data["data"]):
            self.table.insert("", "end", iid=i, values=(
                i+1,
                s["playing"],
                s["maxPlayers"],
                False
            ), tags=('even' if i % 2 == 0 else 'odd',))
            

    def join_selected(self):
        selected = self.table.selection()
        

        if not selected:
            return
        
        index = int(selected[0])
        server_id = data["data"][index]["id"]

        url = f"roblox://placeId={PLACE_ID}&gameInstanceId={server_id}"
        webbrowser.open(url)
        for i, s in enumerate(data["data"]):
            if s["id"] == server_id:
                self.table.item(i, values=(index+1,s["playing"], s["maxPlayers"], True),tags=("true"))
        last_visited=index
        self.last_box['text']=f"Last visited is with index {last_visited+1}"

    def hop_server(self):
        available = [
            s for s in data["data"]
            if s["playing"] < s["maxPlayers"]
        ]

        if not available:
            return

        server = random.choice(available)
        server_id = server['id']
        for i, s in enumerate(data["data"]):
                    if s["id"] == server_id:
                        self.table.item(i, values=(i+1,s["playing"], s["maxPlayers"], True),tags=("true"))
                        last_visited=i+1
                        self.last_box['text']=f"Last visited is with index {last_visited}"
        url = f"roblox://placeId={PLACE_ID}&gameInstanceId={server['id']}"
        webbrowser.open(url)

    def run(self):
        self.root.mainloop()
    def 
if __name__ == "__main__":
    last_visited=None
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100"
    data = requests.get(url).json()
    browser = RobloxServerBrowser()
    browser.get_servers()
    browser.run()
import tkinter as tk
import time
from tkinter import ttk
import requests
import webbrowser
import random
from PIL import Image, ImageTk
from io import BytesIO
import bbrowser

PLACE_ID = 147848991

class RobloxServerBrowser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Roblox Server Browser")
        self.root.geometry("700x750")
        self.refresh_cooldown=False
    def mainpage(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.get_game_name()
        self.get_game_image()
        
        if hasattr(self, 'photo') and self.photo:
            self.game_image = tk.Label(self.root, image=self.photo)
            self.game_image.grid(row=0, column=0, sticky="w", padx=3, pady=3)

        if hasattr(self, 'game_name') and self.game_name:
            self.game_label = tk.Label(self.root, text=self.game_name, font=("Arial", 16))
            self.game_label.grid(row=1, column=0, sticky="w", padx=3, pady=3)
            
            
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
        self.table.tag_configure('last',background="#fadb50")

        self.frame = tk.Frame(self.root)
        self.last_box=tk.Label(self.frame, text="Last visited is NONE")
        self.botpage_btn=tk.Button(self.frame, text="BotConfig", command=self.botconfigpage, bg="#AF4C4C", fg="#ffffff")
        self.refresh_btn = tk.Button(self.frame, text="Refresh Servers", command=self.get_servers, bg="#4CAF50", fg="#ffffff")
        self.join_btn = tk.Button(self.frame, text="Join Selected", command=self.join_selected, bg="#2196F3", fg="#ffffff")
        self.hop_btn = tk.Button(self.frame, text="Server Hop", command=self.hop_server, bg="#9C27B0", fg="#ffffff")
        self.rejoin_btn = tk.Button(self.frame, text="Rejoin", command=self.rejoin, bg="#27B070", fg="#ffffff")


        self.table.grid(row=2, column=0, sticky="nsew")
        self.frame.grid(row=3, column=0, sticky="ew")
        
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.last_box.pack(side="left", padx=5)
        self.botpage_btn.pack(side="right", padx=5)
        self.refresh_btn.pack(side="right", padx=5)
        self.join_btn.pack(side="right", padx=5)
        self.hop_btn.pack(side="right", padx=5)
        self.rejoin_btn.pack(side="right", padx=5)
    def botconfigpage(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.frame = tk.Frame(self.root)
        self.mainpage_btn=tk.Button(self.frame, text="MainPage", command=self.mainpage, bg="#AF4C4C", fg="#ffffff")
        self.frame.grid(row=1, column=0, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)
        self.mainpage_btn.pack(side="right", padx=5)
    def get_servers(self):
        if self.refresh_cooldown:
            return
        global data
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"API Error: {response.status_code} - {response.text}")
                return
            data = response.json()
            if 'data' not in data:
                print(f"No 'data' in response: {data}")
                return
        except Exception as e:
            print(f"Request failed: {e}")
            return
        self.table.delete(*self.table.get_children())
        for i, s in enumerate(data["data"]):
            self.table.insert("", "end", iid=i, values=(
                i+1,
                s["playing"],
                s["maxPlayers"],
                False
            ), tags=('even' if i % 2 == 0 else 'odd',))
            self.refresh_btn.config(bg="#204D22")
        self.root.after(10000, self.reset_cooldown)
        self.refresh_cooldown = True
    def reset_cooldown(self):
        self.refresh_cooldown = False
        self.refresh_btn.config(bg="#4CAF50")

    def join_selected(self):
        global last_visited
        global last_server_id
        selected = self.table.selection()
        if not selected:
            return
        
        index = int(selected[0])
        server_id = data["data"][index]["id"]
        last_server_id=data["data"][index]["id"] 
        url = f"roblox://placeId={PLACE_ID}&gameInstanceId={server_id}"
        webbrowser.open(url)
        for i, s in enumerate(data["data"]):
            if s["id"] == server_id:
                self.table.item(i, values=(index+1,s["playing"], s["maxPlayers"], True),tags=("last"))
                if last_visited is not None:
                    prev_s = data["data"][last_visited]
                    self.table.item(last_visited, values=(last_visited+1, prev_s["playing"], prev_s["maxPlayers"], True), tags=("true"))
                
        last_visited=index
        self.last_box['text']=f"Last visited is with index {last_visited+1}"

    def hop_server(self):
        global last_visited
        global last_server_id
        available = [
            s for s in data["data"]
            if s["playing"] < s["maxPlayers"]
        ]

        if not available:
            return

        server = random.choice(available)
        server_id = server['id']
        last_server_id=server['id']
        for i, s in enumerate(data["data"]):
                    if s["id"] == server_id:
                        self.table.item(i, values=(i+1,s["playing"], s["maxPlayers"], True),tags=("last"))
                        if last_visited is not None:
                            prev_s = data["data"][last_visited]
                            self.table.item(last_visited, values=(last_visited+1, prev_s["playing"], prev_s["maxPlayers"], True), tags=("true"))
                        last_visited=i+1
                        self.last_box['text']=f"Last visited is with index {last_visited}"
                        
        url = f"roblox://placeId={PLACE_ID}&gameInstanceId={server['id']}"
        webbrowser.open(url)
        
        
    def rejoin(self):
        global last_server_id
        if last_visited is not None:
            url = f"roblox://placeId={PLACE_ID}&gameInstanceId={last_server_id}"
            for i, s in enumerate(data["data"]):
                if s["id"] == last_server_id:
                    self.table.item(i, values=(i+1,s["playing"], s["maxPlayers"], True),tags=("last"))
                    last_visited=i+1
                    self.last_box['text']=f"Last visited is with index {last_visited}"
            webbrowser.open(url)
        
    def get_game_name(self):
        try:
            response = requests.get(f"https://apis.roblox.com/universes/v1/places/{PLACE_ID}/universe")
            if response.status_code == 200:
                data = response.json()
                universe_id = data["universeId"]

            game_info_url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
            game_info = requests.get(game_info_url)
            if game_info.status_code == 200:
                data = game_info.json()
                self.game_name = data["data"][0]["name"]
                return True
            return False
        except Exception as e:
            print(f"Error loading game name: {e}")
            return False
    def get_game_image(self):
        try:
            response = requests.get(f"https://apis.roblox.com/universes/v1/places/{PLACE_ID}/universe")
            if response.status_code == 200:
                data = response.json()
                universe_id = data["universeId"]
            thumbnail_url = f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&countPerUniverse=1&defaults=true&size=768x432&format=Png&isCircular=false"
            thumbnail_data = requests.get(thumbnail_url)
            if thumbnail_data.status_code == 200:
                data = thumbnail_data.json()
                image_url = data["data"][0]["thumbnails"][0]["imageUrl"]
                
                response = requests.get(image_url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((350, 250))
                    self.photo = ImageTk.PhotoImage(img)
                    return True
            return False
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    last_visited=None
    last_server_id=None
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100"
    data = requests.get(url).json()
    browser = RobloxServerBrowser()
    browser.mainpage()
    browser.get_servers()
    browser.run()
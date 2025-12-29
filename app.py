import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import COLORS, APP_TITLE, WINDOW_SIZE, DEFAULT_URL
from scraper import SofaScraper
from ui_utils import setup_app_styles, sort_column, create_stats_tree

class NHLStatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NHL Analytics Pro")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=COLORS['bg'])
        
        self.scraper = SofaScraper()
        self.all_players_data = []
        self.game_data = {}
        
        setup_app_styles()
        self.create_widgets()

    def create_widgets(self):
        self.main_container = tk.Frame(self.root, bg=COLORS['bg'])
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # --- Header ---
        header = tk.Frame(self.main_container, bg=COLORS['bg'])
        header.pack(fill='x', pady=(0, 20))
        
        tk.Label(header, text=APP_TITLE, font=('Segoe UI', 24, 'bold'),
                 fg=COLORS['text'], bg=COLORS['bg']).pack(side='left')
        
        input_group = tk.Frame(header, bg=COLORS['bg'])
        input_group.pack(side='right')
        
        self.url_entry = tk.Entry(input_group, font=('Segoe UI', 11), bg=COLORS['card'],
                                 fg=COLORS['text'], insertbackground=COLORS['primary'],
                                 relief='flat', width=45)
        self.url_entry.pack(side='left', padx=10)
        self.url_entry.insert(0, DEFAULT_URL)
        
        tk.Button(input_group, text="LOAD GAME", command=self.load_data,
                  font=('Segoe UI', 11, 'bold'), bg=COLORS['primary'], fg=COLORS['text'],
                  relief='flat', padx=20, pady=5, cursor='hand2').pack(side='left')

        # --- Score & Info Info Area ---
        self.info_frame = tk.Frame(self.main_container, bg=COLORS['card'], height=80)
        self.info_frame.pack(fill='x', pady=(0, 20))
        self.info_frame.pack_propagate(False)
        self.score_label = tk.Label(self.info_frame, text="Please load a game to see stats", 
                                   font=('Segoe UI', 12), fg=COLORS['text'], bg=COLORS['card'])
        self.score_label.pack(expand=True)

        # --- Tabs ---
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill='both', expand=True)
        
        self.setup_all_players_tab()
        self.setup_teams_tab()

    def setup_all_players_tab(self):
        tab = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.notebook.add(tab, text="ALL PLAYERS")
        
        search_frame = tk.Frame(tab, bg=COLORS['bg'])
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="SEARCH:", font=('Segoe UI', 10, 'bold'), 
                 fg=COLORS['text_secondary'], bg=COLORS['bg']).pack(side='left', padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_players)
        tk.Entry(search_frame, textvariable=self.search_var, bg=COLORS['search_bg'], 
                 fg=COLORS['text'], relief='flat', font=('Segoe UI', 11)).pack(fill='x', side='left', expand=True)
        
        cols = ['#', 'Player', 'Team', 'Points', 'PPP', 'Assists', 'Shots', 'Blocked', 'Saves']
        widths = {'#': 40, 'Player': 200, 'Team': 80}
        self.all_tree = create_stats_tree(tab, cols, widths)

    def setup_teams_tab(self):
        tab = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.notebook.add(tab, text="BY TEAMS")
        
        # Split into Away and Home
        cols = ['#', 'Player', 'Points', 'PPP', 'Assists', 'Shots', 'Blocked', 'Saves']
        widths = {'#': 40, 'Player': 150}
        
        # Away Container
        away_container = tk.Frame(tab, bg=COLORS['bg'])
        away_container.pack(side='left', fill='both', expand=True, padx=(0, 5))
        tk.Label(away_container, text="AWAY TEAM", fg=COLORS['team_away'], bg=COLORS['bg'], font=('Segoe UI', 10, 'bold')).pack()
        self.away_tree = create_stats_tree(away_container, cols, widths)
        
        # Home Container
        home_container = tk.Frame(tab, bg=COLORS['bg'])
        home_container.pack(side='right', fill='both', expand=True, padx=(5, 0))
        tk.Label(home_container, text="HOME TEAM", fg=COLORS['team_home'], bg=COLORS['bg'], font=('Segoe UI', 10, 'bold')).pack()
        self.home_tree = create_stats_tree(home_container, cols, widths)

    def load_data(self):
        url = self.url_entry.get().strip()
        eid = self.scraper.extract_event_id(url)
        if not eid:
            messagebox.showerror("Error", "Invalid SofaScore URL")
            return
            
        data = self.scraper.fetch_lineups(eid)
        if data:
            self.game_data = data
            self.process_stats()
            self.refresh_ui()
        else:
            messagebox.showerror("Error", "Could not fetch data from API")

    def process_stats(self):
        self.all_players_data = []
        for side in ['away', 'home']:
            if side in self.game_data:
                for p_data in self.game_data[side].get('players', []):
                    p_obj = p_data.get('player', {})
                    stats = p_data.get('statistics', {})
                    
                    player_dict = {
                        'number': p_obj.get('jerseyNumber', p_obj.get('shirtNumber', '0')),
                        'name': p_obj.get('name', 'N/A'),
                        'team': side.upper(),
                        'points': stats.get('point', stats.get('goals', 0) + stats.get('assists', 0)),
                        'ppp': stats.get('powerPlayPoints', stats.get('powerPlayGoals', 0) + stats.get('powerPlayAssists', 0)),
                        'assists': stats.get('assists', 0),
                        'shots': stats.get('shots', 0),
                        'blocked': stats.get('blocked', 0),
                        'saves': stats.get('saves', 0),
                        'pos': p_obj.get('position', 'N/A')
                    }
                    self.all_players_data.append(player_dict)

    def refresh_ui(self):
        for t in [self.all_tree, self.away_tree, self.home_tree]:
            t.delete(*t.get_children())
        
        home_goals = sum(p['points'] for p in self.all_players_data if p['team'] == 'HOME' and 'goals' in p) # Simplified
        self.score_label.config(text=f"Game Data Loaded: {datetime.now().strftime('%H:%M:%S')}")

        for p in self.all_players_data:
            self.all_tree.insert('', 'end', values=(
                p['number'], p['name'], p['team'], p['points'], 
                p['ppp'], p['assists'], p['shots'], p['blocked'], p['saves']
            ))
            
            target_tree = self.away_tree if p['team'] == 'AWAY' else self.home_tree
            target_tree.insert('', 'end', values=(
                p['number'], p['name'], p['points'], p['ppp'], 
                p['assists'], p['shots'], p['blocked'], p['saves']
            ))

    def filter_players(self, *args):
        term = self.search_var.get().lower()
        self.all_tree.delete(*self.all_tree.get_children())
        for p in self.all_players_data:
            if term in p['name'].lower() or term in str(p['number']) or term in p['team'].lower():
                self.all_tree.insert('', 'end', values=(
                    p['number'], p['name'], p['team'], p['points'], 
                    p['ppp'], p['assists'], p['shots'], p['blocked'], p['saves']
                ))
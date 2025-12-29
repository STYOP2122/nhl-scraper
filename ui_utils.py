from tkinter import ttk
import tkinter as tk
from config import COLORS

def setup_app_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('TNotebook', background=COLORS['bg'], borderwidth=0)
    style.configure('TNotebook.Tab',
        background=COLORS['card'],
        foreground=COLORS['text_secondary'],
        padding=[15, 5],
        font=('Segoe UI', 10, 'bold'))
    style.map('TNotebook.Tab',
        background=[('selected', COLORS['primary']), ('active', COLORS['card'])],
        foreground=[('selected', COLORS['text']), ('active', COLORS['text'])])
    
    style.configure('Treeview', background=COLORS['card'], foreground=COLORS['text'],
                    fieldbackground=COLORS['card'], rowheight=30, borderwidth=0)
    style.configure('Treeview.Heading', background=COLORS['bg'], foreground=COLORS['primary'],
                    relief='flat', font=('Segoe UI', 10, 'bold'))

def create_stats_tree(parent, columns, col_widths):
    """Universal factory for creating consistent Treeview tables."""
    tree = ttk.Treeview(parent, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
        tree.column(col, width=col_widths.get(col, 50), anchor='center')
    
    if 'Player' in columns:
        tree.column('Player', anchor='w', width=150)
        
    scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    return tree

def sort_column(tree, col, reverse):
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    try:
        l.sort(key=lambda t: float(t[0]) if t[0] else 0, reverse=reverse)
    except ValueError:
        l.sort(key=lambda t: t[0].lower(), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))
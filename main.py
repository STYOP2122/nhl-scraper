import tkinter as tk
from app import NHLStatsApp

def main():
    root = tk.Tk()
    app = NHLStatsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
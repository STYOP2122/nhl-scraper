# NHL Statistics Viewer

A Python desktop application for viewing NHL player statistics from SofaScore. Enter a match URL to load player data, compare teams, and sort the results.

## Features

- Load match lineups and player statistics from SofaScore.
- View all players together or split them by team.
- Search by player name, number, or team.
- Sort statistics by clicking table headers.
- View points, assists, power-play points, shots, blocked shots, and saves when available.

## Requirements

Python 3 with Tkinter and an internet connection. Python installations without Tkinter need the Tk package supplied by their operating system.

## Installation and launch

```bash
git clone https://github.com/STYOP2122/nhl-scraper.git
cd nhl-scraper
python -m venv .venv
```

Activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux, use `source .venv/bin/activate` instead.

```bash
python -m pip install -r requirements.txt
python main.py
```

Paste a SofaScore hockey match URL containing its event ID into the input field and click **LOAD GAME**. Data is fetched when you load a match; the application does not continuously refresh it. Available statistics depend on the match data provided by SofaScore.

## Project structure

- `main.py` — application entry point.
- `app.py` — window, tabs, match loading, and filtering.
- `scraper.py` — event ID extraction and SofaScore requests using `curl_cffi`.
- `ui_utils.py` — table styling and sorting.
- `config.py` — colors, window size, and default match URL.

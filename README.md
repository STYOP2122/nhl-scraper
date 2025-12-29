# NHL Statistics Calculation Tool

An desktop application for fetching and analyzing real-time NHL player statistics using the SofaScore API. Built with Python, Tkinter, and `curl_cffi`.

## Features
- **Real-time Data:** Fetches live lineups and player stats.
- **Advanced Scraping:** Uses `curl_cffi` to bypass TLS fingerprinting.
- **Modular Architecture:** Clean separation between UI, Scraper, and Config.
- **Dynamic Sorting:** Click on any column to sort by stats (Points, Shots, Saves, etc.).
- **Live Search:** Quick filtering by player name, number, or team.

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/STYOP2122/nhl-scraper.git](https://github.com/STYOP2122/nhl-scraper.git)
   cd nhl-scraper
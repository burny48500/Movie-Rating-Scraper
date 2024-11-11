# Movie Ratings Scraper

A Python web scraper that retrieves movie ratings from multiple popular movie review websites: Letterboxd and FilmAffinity. The script uses Selenium WebDriver to automate the process of searching for movies and extracting their ratings.

## Features

- Scrapes movie ratings from:
  - Letterboxd (rating out of 10)
  - FilmAffinity (rating out of 10)
- Handles cookie consent popups automatically
  

## Prerequisites

- Python 3.x
- Google Chrome browser installed
- Python packages:
  ```
  selenium
  ```

## Installation

1. Clone this repository or download the script
2. Install the required Python package:
   ```bash
   pip install selenium
   ```

## Usage

1. Run the script:
   ```bash
   python movie_scraper.py
   ```
2. When prompted, enter the name of the movie you want to search for
3. The script will automatically:
   - Search for the movie on each platform
   - Navigate to the movie's page
   - Extract the rating
   - Display the results

Example output:
```
Type the film you'd like to know about:
Titanic
Searching for Titanic
Letterboxd: 8.2/10
FilmAffinity: 7.6/10
```

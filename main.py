from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def setup_driver():
    """Setup and return a configured Chrome WebDriver"""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # Add these options for better stability
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Using default Chrome installation
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        sys.exit(1)

def safe_get_rating(func):
    """Decorator to handle exceptions in rating retrieval"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error getting rating from {func.__name__}: {e}")
            return None
    return wrapper

@safe_get_rating
def get_imdb_rating(film_input):
    driver = setup_driver()
    try:
        driver.get("https://www.imdb.com")
        wait = WebDriverWait(driver, 10)
        
        # Search for the film
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="q"]')))
        search_input.send_keys(film_input)
        search_input.send_keys(Keys.RETURN)
        
        # Click first result
        selected_film = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ipc-metadata-list-summary-item__t')))
        selected_film.click()
        
        # Get rating
        rating = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-bde20123-1'))).text
        return float(rating)
    finally:
        driver.quit()

@safe_get_rating
def get_letterboxd_rating(film_input):
    driver = setup_driver()
    try:
        driver.get("https://letterboxd.com")
        wait = WebDriverWait(driver, 10)
        
        # Handle cookie consent if present
        try:
            cookie_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="html"]/body/div[8]/div[2]/div[1]/div[2]/div[2]/button[2]')))
            cookie_button.click()
        except TimeoutException:
            pass  # Cookie banner might not appear
        
        # Search for the film
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-q"]')))
        search_input.send_keys(film_input)
        search_input.send_keys(Keys.RETURN)
        
        # Click first result
        selected_film = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'film-title-wrapper')))
        selected_film.click()
        
        # Get rating
        rating = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'average-rating'))).text
        return float(rating) * 2  # Convert to /10 scale
    finally:
        driver.quit()

@safe_get_rating
def get_filmaffinity_rating(film_input):
    driver = setup_driver()
    try:
        driver.get("https://www.filmaffinity.com/es/main.html")
        wait = WebDriverWait(driver, 10)
        
        # Handle cookie consent if present
        try:
            cookie_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[2]')))
            cookie_button.click()
        except TimeoutException:
            pass  # Cookie banner might not appear
        
        # Search for the film
        search_input = wait.until(EC.presence_of_element_located((By.ID, 'top-search-input-2')))
        search_input.send_keys(film_input)
        search_input.send_keys(Keys.RETURN)
        
        # Get rating
        rating_text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'avgrat-box'))).text
        return float(rating_text.replace(',', '.'))
    finally:
        driver.quit()

def main():
    print("Type the film you'd like to know about: ")
    film_input = input().strip()
    print(f"Searching for {film_input}")
    
    # Get ratings from all services
    #imdb_rating = get_imdb_rating(film_input)
    #if imdb_rating:
    #    print(f"IMDb: {imdb_rating}/10")
    
    letterboxd_rating = get_letterboxd_rating(film_input)
    if letterboxd_rating:
        print(f"Letterboxd: {letterboxd_rating}/10")
    
    filmaffinity_rating = get_filmaffinity_rating(film_input)
    if filmaffinity_rating:
        print(f"Filmaffinity: {filmaffinity_rating}/10")

if __name__ == "__main__":
    main()
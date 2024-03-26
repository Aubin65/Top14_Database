#---------------------------------------------------------------------------------------#
#----------------------------------Extract Functions------------------------------------#
#---------------------------------------------------------------------------------------#

"""
Set the functions used to extract the data from website or text file
As to know, the websites that will be scrapped are Rugbyrama, LNR website and AllRugby website. 
I would have like to scrap La Grande Mêlée to collect the lacking data from LNR but the site requires an authentification
"""

#Libraries
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os


#----------------------------------------Extract----------------------------------------#
#--------------------------------------From Website-------------------------------------#


# Webscrapping websites for LNR and AllRugby stats to extract the raw data
def scrap_lnr_allrugby(url : str) -> str :
    """
    Argument : 
        - url : url of the webpage to be scrapped
    Returns :
        - visible_text : string of the webpage text
    """
    try:
        # Set up a headless browser using Selenium
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        # Make a GET request to the URL
        driver.get(url)

        # Wait for some time to allow dynamic content to load
        driver.implicitly_wait(10)

        # Get the page source after dynamic content has loaded
        page_source = driver.page_source

        # Parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract only the visible text content
        visible_text = soup.get_text(separator='\n', strip=True)

        # Close the browser
        driver.quit()

        return visible_text

    except Exception as e:
        print(f"Error: {e}")
        return None
    

# Webscrapping lgm website to extract the raw data
def scrap_lgm(day : str) -> list:
    """
    Arguments : 
        - day : string containing the day with the format of the lgm urls source file (ex : "Day1")
    Returns : 
        - player_data_list : list of stats of the players during a day of championship with the following format : 

    ['P. Yato', '80', '1', '0', '0', '0', '2', '3', '5', '1', '12', '1', '0', '0', '77.0']
    """

    day_dict = {
        "Day1" : "Journée 1",
        "Day2" : "Journée 2",
        "Day3" : "Journée 3",
        "Day4" : "Journée 4",
        "Day5" : "Journée 5",
        "Day6" : "Journée 6",
        "Day7" : "Journée 7",
        "Day8" : "Journée 8",
        "Day9" : "Journée 9",
        "Day10" : "Journée 10",
        "Day11" : "Journée 11",
        "Day12" : "Journée 12",
        "Day13" : "Journée 13",
        "Day14" : "Journée 14",
        "Day15" : "Journée 15",
        "Day16" : "Journée 16",
        "Day17" : "Journée 17",
        "Day18" : "Journée 18",
        "Day19" : "Journée 19",
        "Day20" : "Journée 20",
        "Day21" : "Journée 21",
        "Day22" : "Journée 22",
        "Day23" : "Journée 23",
        "Day24" : "Journée 24",
        "Day25" : "Journée 25",
        "Day26" : "Journée 26"
    }

    #Get the mail and the password
    dotenv_path = "../.env"
    load_dotenv(dotenv_path)
    mail = os.environ.get("MAIL")
    password = os.environ.get("PASSWORD")

    # Initialize the driver with options
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # URL of the login page
    login_url = "https://lagrandemelee.midi-olympique.fr/#/welcome/login"
    driver.get(login_url)

    # Locate the username and password fields
    username_field = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="mail"]')
    password_field = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')

    # Enter your username and password
    username_field.send_keys(mail)
    password_field.send_keys(password)

    # Submit the form (assuming there's a submit button)
    password_field.send_keys(Keys.RETURN)

    # Wait for the welcome page to appear after successful login
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be("https://lagrandemelee.midi-olympique.fr/#/game/play/me"))

    # Navigate to the desired URL
    target_url = "https://lagrandemelee.midi-olympique.fr/#/game/play/me"
    driver.get(target_url)

    # Find the button using its class
    button_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "action-stats")))
    button_element.click()

    # Find the mat-select element by its formcontrolname
    mat_select_element = wait.until(EC.element_to_be_clickable(("css selector", 'mat-select[formcontrolname="journee"]')))
    mat_select_element.click()

    # Find the desired option based on its text content
    desired_text = day_dict[day]
    xpath_expression = f'//mat-option[normalize-space(.//span)="{desired_text}"]'
    # xpath_expression = f'//mat-option[.//span[contains(text(), "{desired_text}")]]'
    option_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
    option_element.click()

    # Initialize a list to store player data
    player_data_list = []

    #22 because 23*2*7 is the number of players and 15 the number by page
    for i in range(22):

        time.sleep(1)
        
        # Get the page source after dynamic content has loaded
        page_source = driver.page_source

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all rows in the table
        rows = soup.find_all('tr', class_='ng-star-inserted')

        # Extract data from each row
        for row in rows:
            
            # Extract player name, handling the case where the element may not be present
            player_name_element = row.select_one('.w-150 a.link')
            player_name = player_name_element.get_text(strip=True) if player_name_element else ''

            # Extract data from each cell in the row (td elements)
            data_cells = row.find_all('td', class_='mat-tooltip-trigger ng-star-inserted')
            player_data = [cell.get_text(strip=True) if cell.get_text(strip=True) != '' else '0' for cell in data_cells]

            # Append the player name and data to the list
            if [player_name] + player_data != [''] and player_data[0] != "0":
                player_data_list.append([player_name] + player_data)
                
        # Find the mat-select element by its formcontrolname
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fs-scroll-content > statistiquespage > div > div > div > statistiques > div > div.ctr-statistiques.sport.sport2 > mat-paginator > div > div > div.mat-paginator-range-actions > button.mat-focus-indicator.mat-tooltip-trigger.mat-paginator-navigation-next.mat-icon-button.mat-button-base")))
        driver.execute_script("arguments[0].click();", element)

    driver.quit()

    return player_data_list


#---------------------------------------Generate----------------------------------------#
#-----------------------------------LNR urls to scrap-----------------------------------#


def get_lnr_urls_dict(sources_path : str, scrapped_path : str) -> dict :
    """
    Argument : 
        - sources_path : path of the txt file containing the url sources
        - scrapped_path : path of the file containing the urls already scrapped

    The txt file is of the following form :

    Day1 - 09/08/2023
    https://source1.com
    ...
    https://source7.com

    Day2 - 16/08/2023
    ...

    Returns :
        - sources_dict : dictionnary containing the url sources for each day with the following format : 
    
    sources_dict = {
        "Day1" : [url1, url2, ... url7],
        ...
        "Day26" : [url1, url2, ... url7]
        }
    }
    """

    #Initialize the dictionnary
    sources_dict = {}

    #Get the today's date
    today = datetime.now()

    #Get the table with the urls
    with open(sources_path, 'r') as file:
        urls_sources = [line.strip() for line in file.readlines()]

    #Get the table with the urls already scrapped
    with open(scrapped_path, 'r') as file:
        urls_scrapped = [line.strip() for line in file.readlines()]
    
    #Get the urls that have not been scrapped
    urls_to_scrap = [i for i in urls_sources if (i not in urls_scrapped and i != "")]

    #Iterate on urls to scrap
    for idx, elem in enumerate(urls_to_scrap):
    
        #For each day
        if elem.startswith("Day"):
            #Get the day
            day = elem.split("-")[0].strip()

            #Get the date with date format
            date = elem.split("-")[1].strip()
            date = datetime.strptime(date, '%d/%m/%Y')

            #If the match has been played
            if date < today :

                #Get the list of urls
                urls = urls_to_scrap[idx+1 : idx+8]

                #Assign the values
                sources_dict[day] = urls

                #Add the day to write it in the scrapped text file
                urls.insert(0, elem)

                #Complete the scrapped file
                with open(scrapped_path, "a") as file:
                    for line in urls:
                        file.write(line + "\n")

    return sources_dict


#---------------------------------------Generate----------------------------------------#
#--------------------------------AllRugby urls to scrap---------------------------------#


def get_allrugby_urls_list(sources_path : str, scrapped_path : str) -> list :
    """
    Argument : 
        - sources_path : path of the txt file containing the url sources
        - scrapped_path : path of the file containing the urls already scrapped

    The txt file is of the following form :

    https://equipe1.com
    ...
    https://equipe14.com

    Returns :
        - urls_to_scrap : list containing the url missing 
    """

    #Get the table with the urls
    with open(sources_path, 'r') as file:
        urls_sources = [line.strip() for line in file.readlines()]

    #Get the table with the urls already scrapped
    with open(scrapped_path, 'r') as file:
        urls_scrapped = [line.strip() for line in file.readlines()]
    
    #Get the urls that have not been scrapped
    urls_to_scrap = [i for i in urls_sources if i not in urls_scrapped]

    with open(scrapped_path, "a") as file:
        for line in urls_to_scrap:
            file.write(line + "\n")

    return urls_to_scrap
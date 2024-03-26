#---------------------------------------------------------------------------------------#
#------------------------------Testing Extract Functions--------------------------------#
#---------------------------------------------------------------------------------------#

import pytest

import sys
sys.path.append('../..')
from etl_functions.extract.extract import *

#-------------------------------scrap_lnr_allrugby()---------------------------------#

def test_scrap_lnr_allrugby():

    url = "https://top14.lnr.fr/feuille-de-match/2023-2024/j1/10258-castres-pau/statistiques-du-match"

    result = scrap_lnr_allrugby(url)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a string
    assert type(result) == str

    #Assert that the function returns the right data
    assert "Section Paloise" in result

#------------------------------------scrap_lgm()-------------------------------------#

def test_scrap_lgm():

    day_test = "Day1"

    result = scrap_lgm(day_test)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a string
    assert type(result) == list

    #Assert that the function returns the right number of players
    assert len(result) == 314

    #Assert that the function returns the right length for each player
    for elem in result:
        assert len(elem) == 15

    #Assert that the right values are returned (for the first and last player)
    assert result[0] == ["N. Le Garrec","76","2","2","2","0","4","4","2","0","10","0","0","0","74.1"]
    assert result[-1] == ["M. Babillot","66","0","0","0","0","0","0","9","1","4","5","1","1","-23.6"]

#---------------------------------get_lnr_urls_dict()-----------------------------------#

def test_get_lnr_urls_dict():

    sources_path = "sources_data/test_lnr_sources_path.txt"
    scrapped_path = "sources_data/test_lnr_scrapped_path.txt"

    result = get_lnr_urls_dict(sources_path = sources_path, scrapped_path = scrapped_path)

    with open(scrapped_path, 'r') as file:
        new_scrapped_list = [line.strip() for line in file.readlines()]

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert that the dictionnary has the right format
    for key,elem in result.items():   
        
        assert key.startswith("Day")

        assert type(elem) == list

    #Assert that the function returns the urls that need to be scrapped
    assert "https://top14.lnr.fr/feuille-de-match/2023-2024/j2/10265-paris-oyonnax/statistiques-du-match" in result["Day2"]

    #Assert that the functions does not return the urls that already have been scrapped
    assert "Day1" not in result

    #Assert that the function does not return a url from a future match
    assert "Day3" not in result

    #Assert that the function has written the urls scrapped in the scrapped urls file
    assert "https://top14.lnr.fr/feuille-de-match/2023-2024/j2/10267-toulon-bayonne/statistiques-du-match" in new_scrapped_list

#------------------------------get_allrugby_urls_list()---------------------------------#

def test_get_allrugby_urls_list():

    sources_path = "sources_data/test_allrugby_sources_path.txt"
    scrapped_path = "sources_data/test_allrugby_scrapped_path.txt"

    result = get_allrugby_urls_list(sources_path = sources_path, scrapped_path = scrapped_path)

    with open(scrapped_path, 'r') as file:
        new_scrapped_list = [line.strip() for line in file.readlines()]

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a list
    assert type(result) == list
    
    #Assert that the function returns the urls that need to be scrapped
    assert "url_match_3" in result
    assert "url_match_4" in result

    #Assert that the functions does not return the urls that already have been scrapped
    assert "url_match_1" not in result
    assert "url_match_2" not in result
    assert "url_match_5" not in result

    #Assert that the function has written the urls scrapped in the scrapped urls file
    assert "url_match_3" in new_scrapped_list
    assert "url_match_4" in new_scrapped_list
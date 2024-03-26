#---------------------------------------------------------------------------------#
#---------------------------------ETL-Execution-----------------------------------#
#---------------------------------------------------------------------------------#

#Libraries
from datetime import date, timedelta
import os
from extract.extract import *
from transform.transform import *
from load.load import *

"""
Plan : 
    - Extraire et transformer les données allrugby,
    - Charger les données allrugby

    - Pour chaque journée :
        - Extraire les données lgm

        - Pour chaque match : 
            - Extraire et transformer les stats du match par équipe (Domicile et Exterieur)
            - Extraires et transformer les données générales du match
            - Charger les stats du match par equipe (utiliser home_id et away_id)
            - Utiliser les IDs des équipes pour charger les données générales du match
            - Extraire et transformer les données lnr
            - Lier avec les données lgm
            - Utiliser les IDs (match_id et player_id) pour charger les stats du joueur
"""

#-------------------------------Loading AllRugby----------------------------------#

#Path of the txt file containing the sources
allrugby_sources_path = "data_sources/allrugby_sources.txt"
allrugby_scrapped_path = "data_sources/allrugby_scrapped.txt"

#Get the urls to scrap All Rugby website
allrugby_urls_list = get_allrugby_urls_list(sources_path = allrugby_sources_path, scrapped_path = allrugby_scrapped_path)

if allrugby_urls_list != []:

    #Initialize the IDs dictionnary to link with the other tables
    allrugby_id_dict = {}

    #Iterate on teams
    for url in allrugby_urls_list:

        print(url)

        #Get the raw text of the website
        raw_text = scrap_lnr_allrugby(url)
        
        #Get the dictionnary of the values
        allrugby_dict = get_allrugby_stats(raw_text)

        #Iterate on players to load in the database
        for _, player in allrugby_dict.items():

            print(f"player : {player}")

            #Insert player in the database
            player_id = insert_player(player_dict = player)

            #Save the IDs to link with player_stats
            allrugby_id_dict[player["Nom"]] = player_id 


#-------------------------Loading match and player_stats--------------------------#

#Path of the txt file containing the sources
lnr_sources_path = "data_sources/lnr_sources.txt"
lnr_scrapped_path = "data_sources/lnr_scrapped.txt"

lnr_url_dict = get_lnr_urls_dict(sources_path = lnr_sources_path, scrapped_path = lnr_scrapped_path)

if lnr_url_dict != {}:

    #Iterate on days
    for day in lnr_url_dict:

        print(f"day : {day}")

        #Extract data from lgm considering the Day
        lgm_list = scrap_lgm(day)
        lgm_dict = lgm_list_to_dict(lgm_list)

        #Iterate on urls for each match
        for url in lnr_url_dict[day]:

            if url.startswith("https:"):

                print(f"url : {url}")

                #Get the raw text of the website
                raw_text = scrap_lnr_allrugby(url)

                #Get the stats of the match
                match_dict = extract_data_match(raw_text)

                #Get the specific data for each team
                home_dict = match_dict["Equipe_Domicile"]
                away_dict = match_dict["Equipe_Exterieur"]

                #Get the general stats of the match
                match_dict = {
                    "Date" : match_dict["Date"],
                    "Journée" : match_dict["Journée"]
                }

                #Load the stats in MongoDB and save the IDs
                home_team_id = insert_team_stats(team_stats_dict = home_dict)
                away_team_id = insert_team_stats(team_stats_dict = away_dict)
                match_id = insert_match(match_dict = match_dict, home_team_id = home_team_id, away_team_id = away_team_id)

                #Get the dictionnary of the values
                lnr_dict = extract_data_joueurs_LNR(raw_text)

                #Merge LGM and LNR stats
                merged_dict = merge_LGM_LNR(dict_LGM = lgm_dict, dict_LNR = lnr_dict)

                #Iterate for home and away team
                for team in merged_dict:

                    #Load the player_stats for home players
                    for player in merged_dict[team]:

                        #Get the mongo connection uri
                        dotenv_path = "../.env"
                        load_dotenv(dotenv_path)
                        uri = os.environ.get("MONGO_URI")
                        
                        #Connect to the database
                        client = MongoClient(uri)
                        
                        #Access the player collection
                        db = client["rugby_stats"]
                        collection = db["players"]
                        
                        #Try to find the player in the database 
                        player_mongo = collection.find_one({"Nom": player})

                        #Check if the player has been found
                        if player_mongo:

                            #Assign the ID of the player
                            player_id = player_mongo["_id"]

                            print(f"day : {day}, player : {player}")
                            
                            #Insert the stats of the player
                            insert_player_stats(player_stats_dict = merged_dict[team][player], player_id = player_id, match_id = match_id)

                        else : 
                            print(f"player unfound : {player}")
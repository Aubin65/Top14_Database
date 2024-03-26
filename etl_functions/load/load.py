#---------------------------------------------------------------------------------#
#------------------------------------MongoDB--------------------------------------#
#---------------------------------------------------------------------------------#

from dotenv import load_dotenv
import os
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


#------------------------------------Players--------------------------------------#


def insert_player(player_dict : dict) -> None :
    """
    Argument : 
        - player_dict : stats of a player with the following format : 

    Cyril BAILLE = {
           "Nom" : "Cyril BAILLE",
           "Poste_predilection" : "Pilier",
           "Age" : 30,
           "Date_de_naissance" : "15/09/1993",
           "Taille" : 182,
           "Poids" : 117,
           "Equipe" : "Stade Toulousain"
        }

    Returns :
        - inserted_id : string containing the id of the player
    """

    dotenv_path = "../.env"
    load_dotenv(dotenv_path)
    uri = os.environ.get("MONGO_URI")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    database = client["rugby_stats"]
    collection = database["players"]

    #Store the player
    id = collection.insert_one(player_dict).inserted_id

    client.close()

    return id


#-------------------------------------Match---------------------------------------#


def insert_match(match_dict : dict, home_team_id : str, away_team_id : str) -> None :
    """
    Argument : 
        - match_dict : dictionnary containing the general stats of the match with the following format : 

    match_dict = {
        "Date" : "",
        "Journée" : "",
        }

    Returns : stores the data in the MongoDB database
    """

    dotenv_path = "../.env"
    load_dotenv(dotenv_path)
    uri = os.environ.get("MONGO_URI")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    database = client["rugby_stats"]
    collection = database["match"]

    # Assign home and away teams ids in order to get the stats
    match_dict["Equipe_Domicile_id"] = home_team_id
    match_dict["Equipe_Exterieur_id"] = away_team_id

    #Store the match
    id = collection.insert_one(match_dict).inserted_id

    client.close()

    return id


#-----------------------------------Team Stats------------------------------------#


def insert_team_stats(team_stats_dict : dict) -> str:
    """
    Argument : 
        - team_stats_dict : dictionnary containing the general stats of the team with the following format : 

    team_stats_dict = {
        "Nom" : "",
        "Essais accordés" : "",
        "Score" : "",
        "Possession de la balle" : "",
        "Possession dans son camp" : "",
        "Possession dans le camp adverse" : "",
        "Possession 22m adverses" : "",
        "Occupation" : "",
        "Mêlées obtenues" : "",
        "Mêlées perdues" : "",
        "Mêlées gagnées" : "",
        "Mêlées refaites" : "",
        "Touches obtenues" : "",
        "Touches gagnées sur son propre lancer" : "",
        "Touches gagnées sur lancer adverse" : "",
        "En-avant commis" : "",
        "Pénalités réussies" : "",
        "Pénalités concédées" : "",
        "Carton jaune" : "",
        "Carton rouge" : "",
        "Plaquages réussis" : "",
        "Plaquages offensifs réussis" : "",
        "Plaquages manqués" : "",
        "Ballons joués au pied" : "",
        "Ballons passés" : ""
        }

    Returns : 
        - string containing the id of the team_stats document
    """

    dotenv_path = "../.env"
    load_dotenv(dotenv_path)
    uri = os.environ.get("MONGO_URI")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    database = client["rugby_stats"]
    collection = database["team_stats"]

    #Store the match
    id = collection.insert_one(team_stats_dict).inserted_id

    client.close()

    return id


#----------------------------------Player Stats-----------------------------------#


def insert_player_stats(player_stats_dict : dict, player_id : str, match_id : str) -> str :
    """
    Argument : 
        - player_stats_dict : dictionnary containing the statistics of a player with the following format : 

    player_stats_dict = {
            "Antoine DUPONT" : {
                "Nom" : "Antoine DUPONT",
                "Poste" : Demi de mêlée,
                "Statlnr1" : 3
                ...
                "Statlgm1" : 5,
                ...
            }
        }  

    Returns :
        - string containing the id of the player
    """

    dotenv_path = "../.env"
    load_dotenv(dotenv_path)
    uri = os.environ.get("MONGO_URI")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    database = client["rugby_stats"]
    collection = database["player_stats"]

    # Add foreign keys
    player_stats_dict["player_id"] = player_id
    player_stats_dict["match_id"] = match_id

    id = collection.insert_one(player_stats_dict)

    client.close()

    return id
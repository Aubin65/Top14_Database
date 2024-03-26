#---------------------------------------------------------------------------------------#
#------------------------------Testing Extract Functions--------------------------------#
#---------------------------------------------------------------------------------------#

from unittest.mock import patch, MagicMock
import pytest

import sys
sys.path.append('../..')
from etl_functions.load.load import *

#----------------------------------insert_player()--------------------------------------#

def test_insert_player():

    player_data = {
           "Nom" : "Test_name",
           "Poste_predilection" : "Pilier",
           "Age" : 30,
           "Date_de_naissance" : "15/09/1993",
           "Taille" : 182,
           "Poids" : 117,
           "Equipe" : "Stade Toulousain"
        }

    #Mock the MongoDB client
    with patch('etl_functions.load.load.MongoClient'):
        result = insert_player(player_data)

        #Assert that the function returns something
        assert result is not None

# #----------------------------------insert_match()---------------------------------------#

def test_insert_match():

    match_data = {
    "Date": "2023-01-01",
    "Journée": "Journée 1"
    }

    #Mock the MongoDB client
    with patch('etl_functions.load.load.MongoClient'):
        result = insert_match(match_data, "home_team_id", "away_team_id")

        #Assert that the function returns something
        assert result is not None

# #-------------------------------insert_team_stats()-------------------------------------#

def test_insert_team_stats():

    team_stats_dict = {
        "Nom" : "Test_name",
        "Essais accordés" : 3,
        "Score" : 50,
        "Possession de la balle" : 0.3,
        "Possession dans son camp" : 0.4,
        "Possession dans le camp adverse" : 0.7,
        "Possession 22m adverses" : 0.8,
        "Occupation" : 0.5,
        "Mêlées obtenues" : 4,
        "Mêlées perdues" : 2,
        "Mêlées gagnées" : 1,
        "Mêlées refaites" : 3,
        "Touches obtenues" : 7,
        "Touches gagnées sur son propre lancer" : 5,
        "Touches gagnées sur lancer adverse" : 3,
        "En-avant commis" : 3,
        "Pénalités réussies" : 1,
        "Pénalités concédées" : 3,
        "Carton jaune" : 1,
        "Carton rouge" : 1,
        "Plaquages réussis" : 100,
        "Plaquages offensifs réussis" : 7,
        "Plaquages manqués" : 25,
        "Ballons joués au pied" : 37,
        "Ballons passés" : 158
        }

    #Mock the MongoDB client
    with patch('etl_functions.load.load.MongoClient'):
        result = insert_team_stats(team_stats_dict)

        #Assert that the function returns something
        assert result is not None

# #------------------------------insert_player_stats()------------------------------------#

def test_insert_player_stats():
    
    player_stats = {'Nom': 'Antoine DUPONT',
                    'Position': 'Pilier',
                    'Minutes_jouées': 25,
                    'Points_marqués': 26,
                    'Essais_marqués': 27,
                    'Offload': 28,
                    'Franchissements': 29,
                    'Ballons_grattés': 30,
                    'Plaquages_réussis': 31,
                    'Cartons_jaunes': 32,
                    'Cartons_rouges': 33,
                    'Transformation': 2,
                    'Penalite': 3,
                    'Drop': 4,
                    'Plaquage_casse': 6,
                    'Plaquage_manque': 2,
                    'Courses': 8,
                    'Penalite_concedee': 9}
    
    #Mock the MongoDB client
    with patch('etl_functions.load.load.MongoClient'):
        result = insert_player_stats(player_stats, "player_id", "match_id")

        #Assert that the function returns something
        assert result is not None
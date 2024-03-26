#---------------------------------------------------------------------------------------#
#-----------------------------Testing Transform Functions-------------------------------#
#---------------------------------------------------------------------------------------#

import pytest

import sys
sys.path.append('../..')
from etl_functions.extract.extract import *
from etl_functions.transform.transform import *

#--------------------------------get_allrugby_stats()-----------------------------------#

def test_get_allrugby_stats():

    url_test = "https://www.allrugby.com/clubs/aviron-bayonnais/effectif"
    
    raw_text = scrap_lnr_allrugby(url_test)

    result = get_allrugby_stats(raw_text)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert that the function returns the right format
    for key,elem in result.items():
        assert type(elem["Nom"]) == str
        assert type(elem["Equipe"]) == str
        assert type(elem["Poste_predilection"]) == str
        assert type(elem["Age"]) == int
        assert type(elem["Date_de_naissance"]) == datetime
        assert type(elem["Taille"]) == int
        assert type(elem["Poids"]) == int

    #Assert that the function takes the right value for the right player

    birthdate = datetime.strptime("03/04/1989", '%d/%m/%Y')
    current_date = datetime.now()
    age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

    assert "Camille LOPEZ" in result
    assert result["Camille LOPEZ"]["Nom"] == "Camille LOPEZ"
    assert result["Camille LOPEZ"]["Equipe"] == "Aviron Bayonnais"
    assert result["Camille LOPEZ"]["Poste_predilection"] == "Ouverture"
    assert result["Camille LOPEZ"]["Age"] == age
    assert result["Camille LOPEZ"]["Date_de_naissance"] == birthdate
    assert result["Camille LOPEZ"]["Taille"] == 176
    assert result["Camille LOPEZ"]["Poids"] == 90

#---------------------------------lgm_list_to_dict()------------------------------------#

def test_lgm_list_to_dict():

    player_stats = [['J.Joseph', "80", "2", "0", "0", "0", "0", "2", "8", "2", "13", "1", "0", "0", "15.3"],
                    ['A.Gibert', "80", "1", "0", "0", "0", "3", "5", "7", "1", "14", "0", "0", "0", "7.5"],
                    ['J.Maddocks', "80", "2", "1", "4", "0", "2", "7", "5", "6", "16", "3", "30", "22", "8.6"]]

    result = lgm_list_to_dict(player_stats)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert that the function returns the right length of dictionnary
    assert len(result) == 3
    
    for key,value in result.items():
        assert len(value) == 13

    #Assert that the function returns the right type of value
    for key,value in result.items():
        assert type(value) == dict

        for _,stat in value.items():
            assert type(stat) == int 

    #Assert the right value is associated to the right key
    assert result["J.Maddocks"]["Temps_de_jeu"] == 80
    assert result["J.Maddocks"]["Essai"] == 2
    assert result["J.Maddocks"]["Transformation"] == 1
    assert result["J.Maddocks"]["Penalite"] == 4
    assert result["J.Maddocks"]["Drop"] == 0
    assert result["J.Maddocks"]["Franchissement"] == 2
    assert result["J.Maddocks"]["Plaquage_casse"] == 7
    assert result["J.Maddocks"]["Plaquage"] == 5
    assert result["J.Maddocks"]["Plaquage_manque"] == 6
    assert result["J.Maddocks"]["Courses"] == 16
    assert result["J.Maddocks"]["Penalite_concedee"] == 3
    assert result["J.Maddocks"]["Carton_jaune"] == 30
    assert result["J.Maddocks"]["Carton_rouge"] == 22

#-----------------------------------get_raw_stats()-------------------------------------#

def test_get_raw_stats():

    url = "https://top14.lnr.fr/feuille-de-match/2023-2024/j1/10258-castres-pau/statistiques-du-match"

    result = get_raw_stats(scrap_lnr_allrugby(url))

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert the function returns the right length (we cannot test the length of stats because of the subs)
    assert len(result) == 4

    #Assert the right data is in the right place
    assert "Leone NAKARAWA" in result["Effectif_Domicile"]
    assert "Sacha ZEGUEUR" in result["Effectif_Exterieur"]

#--------------------------------get_formatted_dict()-----------------------------------#

def test_get_formatted_dict():

    raw_dict = {
        "Effectif_Domicile" : ["Leone NAKARAWA", "Pierre POPELIN"],
        "Effectif_Exterieur" : ["Hugo AURADOU", "Sacha ZEGUEUR"],
        "Stats_Domicile" : ["2ème ligne","1","2","3","4","5","6","7","8","9","11","12","13","14","15","16","17","18","19"],
        "Stats_Exterieur" : ["Arrière","21","22","23","24","25","26","27","28","29","Ailier", "31","32","33","34","35","36","37","38","39"]
    }

    result = get_formatted_dict(raw_dict)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert the function returns the right types in the dictionnary
    for elem in result["Stats_Domicile"]:
        assert type(elem[0]) == str

        for stat in elem[1:] :
            assert type(stat) == int

    for elem in result["Stats_Exterieur"]:
        assert len(elem) == 10

    #Assert the function returns the right length
    assert len(result) == 4
    assert len(result["Stats_Domicile"]) == len(result["Effectif_Domicile"])
    assert len(result["Stats_Exterieur"]) == len(result["Effectif_Exterieur"])

    for elem in result["Stats_Domicile"]:
        assert len(elem) == 10

    for elem in result["Stats_Exterieur"]:
        assert len(elem) == 10

    #Assert positions are well positionned
    assert result["Stats_Domicile"][0][0] == "2ème ligne"
    assert result["Stats_Domicile"][1][0] == "Remplaçant"
    assert result["Stats_Exterieur"][0][0] == "Arrière"
    assert result["Stats_Exterieur"][1][0] == "Ailier"

    #Assert the stats are well positionned
    for i in range(1,10):
        assert result["Stats_Domicile"][0][i] == i
        assert result["Stats_Domicile"][1][i] == i+10
        assert result["Stats_Exterieur"][0][i] == i+20
        assert result["Stats_Exterieur"][1][i] == i+30

#----------------------------------get_stats_dict()-------------------------------------#

def test_get_stats_dict():

    formatted_dict = {
        "Effectif_Domicile" : ["Leone NAKARAWA", "Pierre POPELIN"],
        "Effectif_Exterieur" : ["Hugo AURADOU", "Sacha ZEGUEUR"],
        "Stats_Domicile" : [["2ème ligne","1","2","3","4","5","6","7","8","9"],["Remplaçant","11","12","13","14","15","16","17","18","19"]],
        "Stats_Exterieur" : [["Arrière","21","22","23","24","25","26","27","28","29"],["Ailier", "31","32","33","34","35","36","37","38","39"]]
    }

    result = get_stats_dict(formatted_dict)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert the function returns the right length
    assert len(result) == 2

    #Assert right players go to the right team
    assert "Leone NAKARAWA" in result["Equipe_Domicile"]
    assert "Pierre POPELIN" in result["Equipe_Domicile"]
    assert "Hugo AURADOU" in result["Equipe_Exterieur"]
    assert "Sacha ZEGUEUR" in result["Equipe_Exterieur"]

    #Assert the right values go to the right player
    liste_stats = ["Position","Minutes_jouées","Points_marqués","Essais_marqués","Offload","Franchissements","Ballons_grattés","Plaquages_réussis","Cartons_jaunes","Cartons_rouges"]
    stats_test = formatted_dict["Stats_Domicile"][1]

    for i, elem in enumerate(liste_stats):
        assert result["Equipe_Domicile"]["Pierre POPELIN"][elem] == stats_test[i]

#---------------------------------merge_LGM_LNR_AR()------------------------------------#

def test_merge_LGM_LNR_AR():

    lgm_dict = {
        "A.Dupont" : {
            "Temps_de_jeu" : 0,
            "Essai" : 1,
            "Transformation" : 2,
            "Penalite" : 3,
            "Drop" : 4,
            "Franchissement" : 5,
            "Plaquage_casse" : 6,
            "Plaquage" : 7,
            "Plaquage_manque" : 2,
            "Courses" : 8,
            "Penalite_concedee" : 9,
            "Carton_jaune" : 10,
            "Carton_rouge" : 11
        },
        "J.Danty" : {
            "Temps_de_jeu" : 12,
            "Essai" : 13,
            "Transformation" : 14,
            "Penalite" : 15,
            "Drop" : 16,
            "Franchissement" : 17,
            "Plaquage_casse" : 18,
            "Plaquage" : 19,
            "Plaquage_manque" : 20,
            "Courses" : 21,
            "Penalite_concedee" : 22,
            "Carton_jaune" : 23,
            "Carton_rouge" : 24
        }
    }

    lnr_dict = {
        "Equipe_Domicile" : {
            "Antoine DUPONT" : {
                "Nom" : "Antoine DUPONT",
                "Position" : "Pilier",
                "Minutes_jouées" : 25,
                "Points_marqués" : 26,
                "Essais_marqués" : 27,
                "Offload" : 28,
                "Franchissements" : 29,
                "Ballons_grattés" : 30,
                "Plaquages_réussis" : 31,
                "Cartons_jaunes" : 32,
                "Cartons_rouges" : 33
            }
        },
        "Equipe_Exterieur" : {
            "J. DANTY" : {
                "Nom" : "J. DANTY",
                "Position" : "Centre",
                "Minutes_jouées" : 34,
                "Points_marqués" : 35,
                "Essais_marqués" : 36,
                "Offload" : 37,
                "Franchissements" : 38,
                "Ballons_grattés" : 39,
                "Plaquages_réussis" : 40,
                "Cartons_jaunes" : 41,
                "Cartons_rouges" : 42
            }
        }
    }

    result = merge_LGM_LNR_AR(dict_LGM = lgm_dict, dict_LNR = lnr_dict)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert the function returns the right length
    assert len(result) == 2
    assert len(result["Equipe_Domicile"]["Antoine DUPONT"]) == 18
    assert len(result["Equipe_Exterieur"]["J. DANTY"]) == 18

    #Assert the right value is in the right place (there is a repetition in order to know exactly where the function fails if it does)
    assert result["Equipe_Exterieur"]["J. DANTY"]["Nom"]
    assert result["Equipe_Exterieur"]["J. DANTY"]["Position"] == "Centre"
    assert result["Equipe_Exterieur"]["J. DANTY"]["Minutes_jouées"] == 34
    assert result["Equipe_Exterieur"]["J. DANTY"]["Points_marqués"] == 35
    assert result["Equipe_Exterieur"]["J. DANTY"]["Essais_marqués"] == 36
    assert result["Equipe_Exterieur"]["J. DANTY"]["Offload"] == 37
    assert result["Equipe_Exterieur"]["J. DANTY"]["Franchissements"] == 38
    assert result["Equipe_Exterieur"]["J. DANTY"]["Ballons_grattés"] == 39
    assert result["Equipe_Exterieur"]["J. DANTY"]["Plaquages_réussis"] == 40
    assert result["Equipe_Exterieur"]["J. DANTY"]["Cartons_jaunes"] == 41
    assert result["Equipe_Exterieur"]["J. DANTY"]["Cartons_rouges"] == 42
    assert result["Equipe_Exterieur"]["J. DANTY"]["Transformation"] == 14
    assert result["Equipe_Exterieur"]["J. DANTY"]["Penalite"] == 15
    assert result["Equipe_Exterieur"]["J. DANTY"]["Drop"] == 16
    assert result["Equipe_Exterieur"]["J. DANTY"]["Plaquage_casse"] == 18
    assert result["Equipe_Exterieur"]["J. DANTY"]["Plaquage_manque"] == 20
    assert result["Equipe_Exterieur"]["J. DANTY"]["Courses"] == 21
    assert result["Equipe_Exterieur"]["J. DANTY"]["Penalite_concedee"] == 22

#--------------------------------extract_data_match()-----------------------------------#

def test_extract_data_match():
    
    url = "https://top14.lnr.fr/feuille-de-match/2023-2024/j1/10260-montpellier-la-rochelle/statistiques-du-match"
    raw_text = scrap_lnr_allrugby(url)
    result = extract_data_match(raw_text)

    #Assert that the function returns something
    assert result is not None

    #Assert that the function returns a dictionnary
    assert type(result) == dict

    #Assert the types are right
    assert type(result["Date"]) == str
    assert type(result["Journée"]) == str

    for team in ["Equipe_Domicile","Equipe_Exterieur"]:
        for key,value in result[team].items():

            if key == "Nom":
                assert type(value) == str

            else:
                assert type(value) == int or type(value) == float
    
    #Assert the length are right
    assert len(result) == 4
    assert len(result["Equipe_Domicile"]) == 25
    assert len(result["Equipe_Exterieur"]) == 25

    #Assert the right value is in the right place
    assert result["Equipe_Exterieur"]["Nom"] == "Stade Rochelais"
    assert result["Equipe_Exterieur"]["Essais accordés"] == 2
    assert result["Equipe_Exterieur"]["Score"] == 15
    assert result["Equipe_Exterieur"]["Possession de la balle"] == 0.53
    assert result["Equipe_Exterieur"]["Possession dans son camp"] == 0.84
    assert result["Equipe_Exterieur"]["Possession dans le camp adverse"] == 0.3
    assert result["Equipe_Exterieur"]["Possession 22m adverses"] == 0.66
    assert result["Equipe_Exterieur"]["Occupation"] == 0.68
    assert result["Equipe_Exterieur"]["Mêlées obtenues"] == 4
    assert result["Equipe_Exterieur"]["Mêlées perdues"] == 1
    assert result["Equipe_Exterieur"]["Mêlées gagnées"] == 3
    assert result["Equipe_Exterieur"]["Mêlées refaites"] == 0
    assert result["Equipe_Exterieur"]["Touches obtenues"] == 18
    assert result["Equipe_Exterieur"]["Touches gagnées sur son propre lancer"] == 17
    assert result["Equipe_Exterieur"]["Touches gagnées sur lancer adverse"] == 1
    assert result["Equipe_Exterieur"]["En-avant commis"] == 8
    assert result["Equipe_Exterieur"]["Pénalités réussies"] == 1
    assert result["Equipe_Exterieur"]["Pénalités concédées"] == 14
    assert result["Equipe_Exterieur"]["Carton jaune"] == 1
    assert result["Equipe_Exterieur"]["Carton rouge"] == 0
    assert result["Equipe_Exterieur"]["Plaquages réussis"] == 86
    assert result["Equipe_Exterieur"]["Plaquages offensifs réussis"] == 7
    assert result["Equipe_Exterieur"]["Plaquages manqués"] == 11
    assert result["Equipe_Exterieur"]["Ballons joués au pied"] == 26
    assert result["Equipe_Exterieur"]["Ballons passés"] == 134
#---------------------------------------------------------------------------------#
#-------------------------------Transform Functions-------------------------------#
#---------------------------------------------------------------------------------#

"""
Set the functions used to transform the data after extraction
"""

#Libraries
from datetime import datetime


#----------------------------------AllRugby-Players--------------------------------------#
#---------------------------------Transform Function-------------------------------------#


def get_allrugby_stats(raw_text : str) -> dict :
    """
    Argument :
        - raw_text : text extracted from the AllRugby website web scrapping
    Returns : 
        - allrugby_dict : dictionnary of the following format : 

    allrugby_dict = {
        "Cyril BAILLE" : {
           "Nom" : "C.BAILLE",
           "Equipe" : "Stade Toulousain",
           "Poste_predilection" : Pilier,
           "Age" : 30,
           "Date_de_naissance" : 15/09/1993,
           "Taille" : 182,
           "Poids" : 117 
        },
        "NomJoueur2" : {
            ...
        }
    }
    """ 

    allrugby_dict = {}

    #Split the lines
    raw_text = raw_text.split("\n")

    
    #Extract the team of the webscrapped page
    team_line = raw_text[0].split(" ")

    for i in range(len(team_line)):
        if team_line[i] == "de" or team_line[i] == "du":

            #La Rochelle exception (not taking only "La" in the dict for explanability)
            if team_line[i+1] == "La":
                city = team_line[i+1] + " " + team_line[i+2]

            else : 
                city = team_line[i+1]

        #Oyonnax exception
        elif team_line[i].startswith("d'"):
            city = team_line[i].split("'")[-1]

    dict_city = {
        "Pau" : "Section Paloise",
        "Clermont" : "ASM Clermont",
        "La Rochelle" : "Stade Rochelais",
        "Toulon" : "Rugby Club Toulonnais",
        "Racing" : "Racing 92",
        "Toulouse" : "Stade Toulousain",
        "Bayonne" : "Aviron Bayonnais",
        "Lyon" : "LOU Rugby",
        "Castres" : "Castres Olympique",
        "Bordeaux" : "Union Bordeaux-Bègles",
        "Perpignan" : "USA Perpignan",
        "Montpellier" : "Montpellier Hérault Rugby",
        "Paris" : "Stade Français Paris",
        "Oyonnax" : "Oyonnax Rugby"
        }

    team = dict_city[city]

    #Iterate on lines
    for i in range(len(raw_text)):
        
        #Height and weight are the only recurrent schemas : use this for every player
        if (raw_text[i].startswith("1.") or raw_text[i].startswith("2.")) and (raw_text[i+1] != "-"):

            #Get the good format for stats

            #For the name, replace é by e and get initials dot name
            name = raw_text[i-4]

            if name == "Paul BOUDEHENT": 
                name = "PA.BOUDEHENT"

            elif name == "Pierre BOUDEHENT":
                name = "PI.BOUDEHENT"

            else :
                # name = name.replace("é", "e")
                name = name.replace("É","E")
                name = name.replace("È","E")
                name = name.replace("Ë","E")
                name = name.replace("Ï","I")
                parts = name.split(" ")
                first_initial = parts[0][0]
                name = first_initial.upper() + "." + "".join(parts[1:])

            position = raw_text[i-3]
            birthdate = raw_text[i-1]
            height = int(raw_text[i][0] + raw_text[i][2:4])

            #Get the age
            if birthdate != "-":
                birthdate = datetime.strptime(birthdate, '%d/%m/%Y')
                current_date = datetime.now()
                age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

            #Separate the case where players weight more than 100kg
            if raw_text[i+1].startswith("1"):
                weight = int(raw_text[i+1][:3])

            else : 
                weight = int(raw_text[i+1][:2])

            #Implementation of the final dictionnary
            allrugby_dict[name] = {
                "Nom" : name,
                "Equipe": team,
                "Poste_predilection" : position,
                "Age" : age,
                "Date_de_naissance" : birthdate,
                "Taille" : height,
                "Poids" : weight 
            }

    return allrugby_dict


#--------------------------------------LGM-Players---------------------------------------#
#----------------------------------Transform Functions-----------------------------------#


def lgm_list_to_dict(player_stats : list) -> dict : 
    """
    Arguments : 
        - player_stats : list of lists obtained from the process_list function with the following format : 
    
    [['J.Joseph', "80", "2", "0", "0", "0", "0", "2", "8", "2", "13", "1", "0", "0"],
    ['A.Gibert', "80", "1", "0", "0", "0", "3", "5", "7", "1", "14", "0", "0", "0"],
    ['J.Maddocks', "80", "2", "0", "0", "0", "2", "7", "0", "0", "16", "0", "0", "0"]]

    Returns : 
        - lgm_dict : final dictionnary containing the players' stats with the following format :

    lgm_dict : {
        Joueur1 : {
            "Temps_de_jeu" : 3,
            "Essai" : 1,
            "Transformation" : 2,
            "Penalite" : 0,
            "Drop" : 0,
            "Franchissement" : 1,
            "Plaquage_casse" : 1,
            "Plaquage" : 7,
            "Plaquage_manque" : 2,
            "Courses" : 8,
            "Penalite_concedee" : 1,
            "Carton_jaune" : 0,
            "Carton_rouge" : 0
        },
        Joueur2 : {
            ...
        }
    }
    """

    #Initialize the result
    lgm_dict = {}

    #Get the list of attributes we need
    attributes_list = ["Temps_de_jeu","Essai","Transformation","Penalite","Drop","Franchissement","Plaquage_casse","Plaquage","Plaquage_manque","Courses","Penalite_concedee","Carton_jaune","Carton_rouge"]

    #Iterate on players
    for joueur in player_stats :
        player_name = joueur[0]

        #Initialization of each player sub-dictionnary
        lgm_dict[player_name] = {}

        #Iterate on each stat except player grade
        for stat in range(1,len(joueur)-1) :
            attribute = attributes_list[stat-1]
            value = int(joueur[stat])

            #Assignment of the value to te final dictionnary
            lgm_dict[player_name][attribute] = value 

    return lgm_dict

#--------------------------------------LNR-Players---------------------------------------#
#----------------------------------Transform Functions-----------------------------------#


def get_raw_stats(raw_text : str) -> dict :
    """
    Argument : 
        - raw_text : text extracted from the LNR website web scrapping
    Returns : 
        - raw_dict : dictionnary containing raw data of the compositions and statistics of each teams. The format is the following : 

    raw_dict = {
        "Effectif_Domicile" : [Joueur1, ...],
        "Effectif_Exterieur" : [Joueur1, ...],
        "Stats_Domicile" : [PosteJoueur1, stat1, stat2, ..., PosteJoueur2, stat1, stat2]
        "Stats_Exterieur" : [PosteJoueur1, stat1, stat2, ..., PosteJoueur2, stat1, stat2]
    }
    """ 

    #Split by line
    raw_text = raw_text.split("\n")

    #Récupération des effectifs et des stats brutes dans des listes

    #Initialize the indexes of each stats start and stop
    player_start_indices = []
    player_end_indices = []
    stats_start_indices = []

    #Iterate on lines
    for i in range(len(raw_text)):
        
        #Find the stats following a structured pattern
        if raw_text[i] == "Joueur":
            player_start_indices.append(i+1)
            stats_end_indice_home = i

        if raw_text[i] == "Position":
            player_end_indices.append(i)

        if raw_text[i] == "Cartons rouges":
            stats_start_indices.append(i+1)

        if raw_text[i] == "Les avantages":
            stats_end_indice_away = i

    stats_end_indices = [stats_end_indice_home,stats_end_indice_away]

    #Home and Away teams
    Home_Team = raw_text[player_start_indices[0]:player_end_indices[0]]
    Away_Team = raw_text[player_start_indices[1]:player_end_indices[1]]

    #Home and Away player stats
    Raw_Home_Stats = raw_text[stats_start_indices[0]:stats_end_indices[0]]
    Raw_Away_Stats = raw_text[stats_start_indices[1]:stats_end_indices[1]]

    raw_dict = {
        "Effectif_Domicile" : Home_Team,
        "Effectif_Exterieur" : Away_Team,
        "Stats_Domicile" : Raw_Home_Stats,
        "Stats_Exterieur" : Raw_Away_Stats
    }

    return raw_dict


def get_formatted_dict(raw_dict : dict) -> dict:
    """
    Args : 
        - raw_dict : dictionnary containing 4 elements obtained from the get_raw_stats function : home and away teams and stats
    Returns : 
        - formatted_dict : dictionnary containing the same statistics but with lists separated by players and sub position added

    formatted_dict = {
        "Effectif_Domicile" : [Joueur1, ...],
        "Effectif_Exterieur" : [Joueur1, ...],
        "Stats_Domicile" : [[PosteJoueur1, stat1, stat2...],[PosteJoueur2, stat1, stat2]]
        "Stats_Exterieur" : [[PosteJoueur1, stat1, stat2...],[PosteJoueur2, stat1, stat2]]
    }
    """

    #Initialization of the positions
    position = ["Pilier","Talonneur","2ème ligne","Troisième ligne aile","Troisième ligne centre","Demi de mêlée","Demi d'ouverture","Centre","Ailier","Arrière"]

    #Get the stats
    Raw_Home_Stats = raw_dict["Stats_Domicile"]
    Raw_Away_Stats = raw_dict["Stats_Exterieur"]

    #Formatted home stats
    Formatted_Home_Stats = []

    i = 0
    while i < len(Raw_Home_Stats):

        #If the post is already specified
        if Raw_Home_Stats[i] in position:
            raw_stats_joueur = Raw_Home_Stats[i:i+10]
            formatted_stats_joueur = [int(x) if x.isdigit() else x for x in raw_stats_joueur]
            Formatted_Home_Stats.append(formatted_stats_joueur)
            i += 10

        else : 
            raw_stats_joueur = ["Remplaçant"] + Raw_Home_Stats[i:i+9]
            formatted_stats_joueur = [int(x) if x.isdigit() else x for x in raw_stats_joueur]
            Formatted_Home_Stats.append(formatted_stats_joueur)
            i += 9

    #Stats Extérieur
    Formatted_Away_Stats = []

    i = 0
    while i < len(Raw_Away_Stats):

        #Si le poste est référencé
        if Raw_Away_Stats[i] in position:
            raw_stats_joueur = Raw_Away_Stats[i:i+10]
            formatted_stats_joueur = [int(x) if x.isdigit() else x for x in raw_stats_joueur]
            Formatted_Away_Stats.append(formatted_stats_joueur)
            i += 10

        else : 
            raw_stats_joueur = ["Remplaçant"] + Raw_Away_Stats[i:i+9]
            formatted_stats_joueur = [int(x) if x.isdigit() else x for x in raw_stats_joueur]
            Formatted_Away_Stats.append(formatted_stats_joueur)
            i += 9

    formatted_dict = {
        "Effectif_Domicile" : raw_dict["Effectif_Domicile"],
        "Effectif_Exterieur" : raw_dict["Effectif_Exterieur"],
        "Stats_Domicile" : Formatted_Home_Stats,
        "Stats_Exterieur" : Formatted_Away_Stats
    }

    return formatted_dict


def get_stats_dict(formatted_dict : dict) -> dict:
    """
    Argument : 
        - formatted_dict : dictionnary obtained from the function get_formatted_dict
    Returns : 
        - lnr_dict : dictionnary separated by player with the following format : 
    
    lnr_dict = {
        Equipe_Domicile : {
            Joueur1 : {
                Poste : Pilier,
                Stat1 = 3
                ...
            }
        }
        Equipe_Exterieur : {
            Joueur1 : {
                Poste : Pilier,
                Stat1 = 3
                ...
            }
        }
    }
    """

    #Match each player with each 
    Home_dict = {}
    Away_dict = {}
    
    #Extract data from the input dictionnary
    effectif_domicile = formatted_dict["Effectif_Domicile"]
    effectif_exterieur = formatted_dict["Effectif_Exterieur"]
    stats_domicile = formatted_dict["Stats_Domicile"]
    stats_exterieur = formatted_dict["Stats_Exterieur"]

    #Name of each attribute
    liste_stats = ["Position","Minutes_jouées","Points_marqués","Essais_marqués","Offload","Franchissements","Ballons_grattés","Plaquages_réussis","Cartons_jaunes","Cartons_rouges"]

    #Assign home values
    for i in range(len(effectif_domicile)):

        player_stats = dict(zip(liste_stats,stats_domicile[i]))

        if player_stats["Minutes_jouées"] != 0:
            Home_dict[effectif_domicile[i]] = player_stats

    #Assign away values
    for i in range(len(effectif_exterieur)):

        player_stats = dict(zip(liste_stats,stats_exterieur[i]))

        if player_stats["Minutes_jouées"] != 0:
            Away_dict[effectif_exterieur[i]] = player_stats
        
    #Concatenate results
    lnr_dict = {
        "Equipe_Domicile" : Home_dict,
        "Equipe_Exterieur" : Away_dict
    }
    
    return lnr_dict


def extract_data_joueurs_LNR(raw_text : str) -> dict :
    """
    Argument :
        - raw_text : string obtained from scrapping the LNR website
    Returns : 
        - lnr_dict : a dict with the info of each player with the following format : 

    lnr_dict = {
        Equipe_Domicile : {
            Joueur1 : {
                Poste : Pilier,
                Stat1 = 3
                ...
            }
        }
        Equipe_Exterieur : {
            Joueur1 : {
                Poste : Pilier,
                Stat1 = 3
                ...
            }
        }
    }
    """

    raw_dict = get_raw_stats(raw_text)

    formatted_dict = get_formatted_dict(raw_dict)

    lnr_dict = get_stats_dict(formatted_dict)
    
    return lnr_dict
    

#--------------------------------LNR/LGM/AllRugby-Players--------------------------------#
#------------------------------------Merge Functions-------------------------------------#


def get_doublons_lgm(processed_list : list) -> list:
    """
    Arguments : processed_list : liste issue de la fonction process_liste qui renvoie une liste de listes contenant les stats des joueurs
    Returns : Une liste des éléments retrouvés en double dans cette liste
    Intêret : Trouver les éléments bloquants pour le merge entre les données LNR et les données LGM
    """

    duplicates = [item for item in processed_list if processed_list.count(item) > 1]
    
    return list(set(duplicates))


def merge_LGM_LNR (dict_LGM : dict, dict_LNR : dict) -> dict:
    """
    Args : Deux dictionnaires issus des fonctions Transform pour les data issues de LGM et celles issues de LNR

    LGM est de la forme : 
    lgm_dict : {
        "A.Dupont" : {
            "Temps_de_jeu" : 35,
            "Essai" : 1,
            "Transformation" : 2,
            "Penalite" : 0,
            "Drop" : 0,
            "Franchissement" : 1,
            "Plaquage_casse" : 1,
            "Plaquage" : 7,
            "Plaquage_manque" : 2,
            "Courses" : 8,
            "Penalite_concedee" : 1,
            "Carton_jaune" : 0,
            "Carton_rouge" : 0
        },
        "J.Danty" : {
            ...
        }
    }

    LNR est de la forme : 
    lnr_dict = {
        "Equipe_Domicile" : {
            "Antoine DUPONT" : {
                "Position" : Pilier,
                "Stat1" = 3
                ...
            }
        }
        Equipe_Exterieur : {
            "Jonathan DANTY" : {
                "Position" : Centre,
                "Stat1" = 3
                ...
            }
        }
    }

    Returns : Un dictionnaire comprenant les données de la LNR concaténées avec celles de LGM pour chaque joueur pour un match donné de la forme : 
    
    final_dict = {
        Equipe_Domicile : {
            A.DUPONT : {
                "Nom" : "A.DUPONT",
                "Position" : "Pilier",
                "Statlnr1" : 3
                ...
                "Statlgm1" : 5,
                ...
            }
        }
        Equipe_Exterieur : {
            J.DANTY : {
                "Nom" : "J.DANTY",
                "Position" : "Pilier",
                "Statlnr1" : 3
                ...
                "Statlgm1" : 5,
                ...
            }
        }
    }

    Les stats à ajouter au dictionnaire LNR étant : Transformation,Penalite,Drop,Plaquage_casse,Plaquage_manque,Courses,Penalite_concedee
    """

    #Initialize the result
    final_dict = {"Equipe_Domicile": {},
                  "Equipe_Exterieur" : {}}

    #Initialize the attributes to be transfered from dict_LGM to final dict
    attributes_lgm = ["Transformation","Penalite","Drop","Plaquage_casse","Plaquage_manque","Courses","Penalite_concedee"]

    #Iterate on Home Team of LNR data
    for joueur_lnr in dict_LNR["Equipe_Domicile"]:

        if dict_LNR["Equipe_Domicile"][joueur_lnr]["Minutes_jouées"] != 0:

            #Get the name of the player and format it

            #Tackle the exception caught by get_doublons_lgm()
            if joueur_lnr == "Paul BOUDEHENT": 
                nom_joueur_lnr = "PA.BOUDEHENT"

            if joueur_lnr == "Pierre BOUDEHENT":
                nom_joueur_lnr = "PI.BOUDEHENT"

            #Rest of the players
            else : 
                parts = joueur_lnr.split(" ")
                nom_joueur_lnr = joueur_lnr.split(" ")[0][0] + "." + "".join(parts[1:])

            #Iterate on LGM data
            for joueur_lgm in dict_LGM:

                #Get the name of the player and format it
                nom_joueur_lgm = joueur_lgm.upper().replace(" ","")

                #If the names are equal on both LNR and LGM data
                if nom_joueur_lgm.startswith(nom_joueur_lnr):

                    #Add the name first and then the stats
                    if joueur_lnr not in final_dict["Equipe_Domicile"]:
                        final_dict["Equipe_Domicile"][nom_joueur_lnr] = dict_LNR["Equipe_Domicile"][joueur_lnr]
                        final_dict["Equipe_Domicile"][nom_joueur_lnr]["Nom"] = nom_joueur_lnr

                    for attribute in attributes_lgm:

                        final_dict["Equipe_Domicile"][nom_joueur_lnr][attribute] = dict_LGM[joueur_lgm][attribute]
                        
                    
    #Same as above but for Away Team
    for joueur_lnr in dict_LNR["Equipe_Exterieur"]:

        if dict_LNR["Equipe_Exterieur"][joueur_lnr]["Minutes_jouées"] != 0:

            if joueur_lnr == "Paul BOUDEHENT":
                nom_joueur_lnr = "PA.BOUDEHENT"

            if joueur_lnr == "Pierre BOUDEHENT":
                nom_joueur_lnr = "PI.BOUDEHENT"

            else : 
                parts = joueur_lnr.split(" ")
                nom_joueur_lnr = joueur_lnr.split(" ")[0][0] + "." + "".join(parts[1:])
            for joueur_lgm in dict_LGM:

                nom_joueur_lgm = joueur_lgm.upper().replace(" ","")

                if nom_joueur_lgm.startswith(nom_joueur_lnr):

                    #Add the name first and then the stats
                    if joueur_lnr not in final_dict["Equipe_Exterieur"]:
                        final_dict["Equipe_Exterieur"][nom_joueur_lnr] = dict_LNR["Equipe_Exterieur"][joueur_lnr]
                        final_dict["Equipe_Exterieur"][nom_joueur_lnr]["Nom"] = nom_joueur_lnr

                    for attribute in attributes_lgm:

                        final_dict["Equipe_Exterieur"][nom_joueur_lnr][attribute] = dict_LGM[joueur_lgm][attribute]

    return final_dict


#---------------------------------------LNR-Match----------------------------------------#
#-----------------------------------Transform Function-----------------------------------#

def extract_data_match(raw_text : str) -> dict : 
    """
    Argument : 
        - raw_text : raw text extracted from the LNR website webscrapped
    Returns : 
        - dictionnary containing general stats about the match with the format described in the variable match_dict
    """

    #Structure of the result
    match_dict = {
        "Date" : "",
        "Journée" : "",
        "Equipe_Domicile" : {
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
        },
        "Equipe_Exterieur" : {
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
        }

    #Split the lines
    text = raw_text.split("\n")

    #Iterate on lines
    for i in range(len(text)):

        #Find the pattern to extract Date, Day, Home Team score and Away Team score
        if text[i].startswith("Match terminé"):

            match_dict["Date"] = text[i].split("-")[2].replace(" ","")
            match_dict["Journée"] = text[i].split("-")[1].replace(" ","")

            #Treat the exception of offensive bonus
            if text[i+1] == "Bo" or text[i+1] == "Bd":
                match_dict["Equipe_Domicile"]["Score"] = int(text[i+2].split("-")[0].replace(" ",""))
                match_dict["Equipe_Exterieur"]["Score"] = int(text[i+2].split("-")[1].replace(" ",""))
            else:
                match_dict["Equipe_Domicile"]["Score"] = int(text[i+1].split("-")[0].replace(" ",""))
                match_dict["Equipe_Exterieur"]["Score"] = int(text[i+1].split("-")[1].replace(" ",""))

        #Extract the name of the teams
        if text[i].startswith("Vis ton match avec"):

            match_dict["Equipe_Domicile"]["Nom"] = text[i+4].split("-")[0][:-1]
            match_dict["Equipe_Exterieur"]["Nom"] = text[i+4].split("-")[1][1:]

        #For yellow and red cards, the pattern is not the same
        if text[i] == "Plaquages et ballons joués":

            match_dict["Equipe_Domicile"]["Carton jaune"] = int(text[i-8])
            match_dict["Equipe_Exterieur"]["Carton jaune"] = int(text[i-6])
            match_dict["Equipe_Domicile"]["Carton rouge"] = int(text[i-4])
            match_dict["Equipe_Exterieur"]["Carton rouge"] = int(text[i-2])

        #For the % values
        if text[i] in ["Possession de la balle","Possession dans son camp","Possession dans le camp adverse","Possession 22m adverses","Occupation"]:

            match_dict["Equipe_Domicile"][text[i]] = int(text[i+1][0:2])/100
            match_dict["Equipe_Exterieur"][text[i]] = int(text[i+2][0:2])/100

        #For the int values
        if text[i] in ["Pénalités concédées","Pénalités réussies","Essais accordés","Mêlées obtenues","Mêlées perdues","Mêlées gagnées","Mêlées refaites","Touches obtenues","Touches gagnées sur son propre lancer","Touches gagnées sur lancer adverse","En-avant commis","Plaquages offensifs réussis","Plaquages manqués","Ballons joués au pied","Ballons passés"]:

            match_dict["Equipe_Domicile"][text[i]] = int(text[i+1])
            match_dict["Equipe_Exterieur"][text[i]] = int(text[i+2])

        #Achieved tackles
        if text[i] == "Plaquages réussis" and text[i-1] == "Plaquages et ballons joués":

            match_dict["Equipe_Domicile"][text[i]] = int(text[i+1])
            match_dict["Equipe_Exterieur"][text[i]] = int(text[i+2])

    return match_dict
# Top 14 Database Creation

## <b>Overview</b>  
___
This project aims to create and update a database used to store Top 14 championship statistics about players and matches.

## <b> Motivation </b>
___ 
As a French supporter disappointed by the recent results of the national team (espacially during the world cup), I decided to create the biggest database I could create to confront the French head coach speech. Actually, the coach's belief at the beginning of his career was to gather the current most performing players.

As to know, France is composed of almost 68 million people and almost  the same amount of head coaches (or even more). That brings a lot of divergent opinions concerning the players to select on social networks. Men lie, not numbers would a lot a French people say. Let's dive a little bit into the truth of numbers !

## <b> Database Solution </b>
___
As the evolution of data within the sport field is really fast, I opted for a flexible NoSQL solution called MongoDB. This solution is hosted in the cloud by AWS and this solution is called MongoDB Atlas.

This database is fed by different websites referenced in the Sources section below.

This database is composed of 4 collections :
* match
* team_stats
* players
* player_stats

Here is an overview of the final structure of these collections in MongoDB : 

* match


## <b> Sources </b>
___
I decided to scrap 3 websites that seemed accurate for me : 
* AllRugby (put the link)
* LNR (put the link)
* LGM (put the link)

All Rugby was used to create the general information about the player. It lead to the creation of the players collection in the MongoDB 

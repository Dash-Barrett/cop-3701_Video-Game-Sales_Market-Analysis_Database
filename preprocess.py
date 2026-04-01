import pandas as pd
import random as r

loadin = pd.read_csv("Initial/vgsales.csv")
mainBody = loadin.dropna()

#Getting All of the values that need to be generated manually
Game_ID = list() # Generated Sequence
Game_Spec_ID = list()
prevPrice = list()
curPrice = list()
for i in range(len(mainBody.index)):
    Game_ID.append(i + 1000)
    Game_Spec_ID.append(i + 10000)

    if (mainBody.iloc[i]['Year'] < 2005):
        prevPrice.append(round(r.randrange(30, 50) + r.random(), 2))
        curPrice.append(round(r.randrange(1, 30) + r.random(), 2))
    else:
        prevPrice.append(round(r.randrange(40, 70) + r.random(), 2))
        curPrice.append(round(r.randrange(1, 40) + r.random(), 2))
# Generating Games Table
gamesTable = pd.DataFrame()

gamesTable['Game_Name'] = mainBody['Name']
gamesTable['Game_ID'] = Game_ID
gamesTable['Release_Year'] = mainBody['Year']
gamesTable['Publisher_Name'] = mainBody['Publisher']
gamesTable = gamesTable.iloc[:, [1, 0, 2, 3]]
gamesTable.to_csv(f"data\GamesTable.csv", index = False)
print("Created GamesTable.csv")

# print(genresTable)

# Generating Game_Specs Table
gameSpecsTable = pd.DataFrame()
gameSpecsTable['Game_ID'] = gamesTable['Game_ID']
gameSpecsTable['Game_Spec_ID'] = Game_Spec_ID
gameSpecsTable['Genre'] = mainBody['Genre']

gameSpecsTable['Prev_Price'] = prevPrice
gameSpecsTable['Cur_Price'] = curPrice

gameSpecsTable.to_csv(f"data\GameSpecsTable.csv", index = False)
print("Created GameSpecsTable.csv")

# Making Publisher Table
publisherTable = pd.DataFrame()
publisherTable['Publisher_Name'] = gamesTable['Publisher_Name'].unique()

totalGameCount = list()
yearFounded = list()
for i in range(len(publisherTable.index)):
    totalGameCount.append(r.randint(0,5000))
    yearFounded.append(r.randint(1970, 2026))

publisherTable['Founding_Year'] = yearFounded
publisherTable['Total_Games'] = totalGameCount
publisherTable = publisherTable.drop_duplicates()

publisherTable.to_csv(f"data\PublisherTable.csv", index = False)
print("Created PublisherTable.csv")

# Making Platform Table
platformTable = pd.DataFrame()
platformTable['Platform_Name'] = mainBody['Platform'].unique()
platformTable['Platform_Holder'] = ["Nintendo", "Nintendo", "Nintendo", "Nintendo", "Microsoft Gaming", 
                "Sony Interactive Entertainment", "Sony Interactive Entertainment", "Nintendo", "Nintendo", "Nintendo", 
                "Sony Interactive Entertainment", "Nintendo","Sony Interactive Entertainment", "Microsoft Gaming", None,
                "Atari SA", "Sony Interactive Entertainment", "Microsoft Gaming", "Nintendo", "Nintendo",
                "Sega Enterprises, Ltd", "Sega Enterprises, Ltd", "Sony Interactive Entertainment", "Sega Enterprises, Ltd", "Sega Enterprises, Ltd",
                "Bandai", "SNK Corporation", "Konami", "The 3DO Company", "Sega Enterprises, Ltd", "NEC Home Electronics"]
platformTable['Launch_Year'] = [2006, 1985, 1989, 2004, 2005, 
                                2006, 2000, 1990, 2001, 2011,
                                2013, 1996, 1994, 2001, 1981,
                                1977, 2004, 2013, 2001, 2012,
                                1989, 1999, 2011, 1994, 1991,
                                1999, 1990, 1987, 1993, 1990, 1994]

platformTable = platformTable.drop_duplicates()
morePlats = pd.read_csv("Initial/more_consoles.csv")
platformTable = pd.concat([platformTable, morePlats])
platformTable.to_csv(f"data\PlatformTable.csv", index = False)
print("Created PlatformTable.csv")
# print(platformTable)

# Making Publisher_Platform Table
pubPlatTable = pd.DataFrame()
pubPlatTable['Publisher_Name'] = mainBody["Publisher"]
pubPlatTable['Platform_Name'] = mainBody['Platform']
pubPlatTable.drop_duplicates(inplace = True)

ex = list()
for i in range(len(pubPlatTable.index)):
    if(r.randint(0,1) == 0):
        ex.append('Y')
    else:
        ex.append('N')
pubPlatTable['Exclusive_Contract'] = ex
pubPlatTable.to_csv(f"data\PublisherPlatformTable.csv", index = False)
print("Created PublisherPlatformTable.csv")
# print(pubPlatTable)

# Making the Game_Region_Sales Table
gameSalesTable = pd.DataFrame()
for i in range(len(mainBody.index)):
    curData = {'Game_ID' : [gamesTable.iloc[i]['Game_ID'], gamesTable.iloc[i]['Game_ID'], gamesTable.iloc[i]['Game_ID'], gamesTable.iloc[i]['Game_ID'], gamesTable.iloc[i]['Game_ID']],
               'Platform': [mainBody.iloc[i]['Platform'], mainBody.iloc[i]['Platform'], mainBody.iloc[i]['Platform'], mainBody.iloc[i]['Platform'], mainBody.iloc[i]['Platform']],
               'Sales_Rank': [mainBody.iloc[i]['Rank'], mainBody.iloc[i]['Rank'], mainBody.iloc[i]['Rank'], mainBody.iloc[i]['Rank'], mainBody.iloc[i]['Rank']],
               'Region': ["Global", "NA", "EU", "JP", "Other"],
               'Region_Sales': [mainBody.iloc[i]['Global_Sales'], mainBody.iloc[i]['NA_Sales'], mainBody.iloc[i]['EU_Sales'], mainBody.iloc[i]['JP_Sales'], mainBody.iloc[i]['Other_Sales']]
               }
    add = pd.DataFrame(curData)
    gameSalesTable = pd.concat([gameSalesTable, add], ignore_index = True)
    
gameSalesTable.to_csv(f"data\GameRegionSalesTable.csv", index = False)
print("Created GameRegionSalesTable.csv")

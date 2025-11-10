import logging
from datetime import datetime
import sqlite3

# COSE DA MIGLIORARE, IDEE ETC IN README.txt

# impostazione logger:
logger = logging.getLogger(__name__)
logging.basicConfig(filename='ROKdataUPLOAD.log', level=logging.INFO)
logger.info(f"GetData: Starting processing - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Database connection
con = sqlite3.connect("players3834.db")
con.row_factory = sqlite3.Row  # permette di accedere alle colonne per nome

# PARAMETERS:
player_info = {}
alliance_info = {}
kingdom_info = {}


def search_by_query(table, params):
    '''
    Function to retrieve specific data from the DB based on given parameters.
    '''
    query = f"SELECT * FROM {table} WHERE 1=1"
    values = []

    # aggiunge alla query solo i parametri non None
    for key, param in params.items():
        if param is not None:
            query += f" AND {key} = ?"
            values.append(param)

    # debug log
    logger.info(f"GetData: Executing query: {query} | Values: {values}")

    cur = con.cursor()
    cur.execute(query, values)   # passo lista valori, non dict
    res = cur.fetchall()

    player_data = []
    for r in res:
        # r è un oggetto sqlite3.Row, possiamo convertirlo in dict direttamente
        player_data.append({
            'player_ID': r['player_ID'] if 'player_ID' in r.keys() else None,
            'player_name': r['player_name'] if 'player_name' in r.keys() else None,
            'player_power': r['player_power'] if 'player_power' in r.keys() else None,
            'alliance': r['alliance'] if 'alliance' in r.keys() else None,
            'kingdom': r['kingdom'] if 'kingdom' in r.keys() else None,
            'datarecord': r['datarecord'] if 'datarecord' in r.keys() else None,
        })

    # debug log
    logger.info(f"GetData: Query returned {len(player_data)} records.")
    return player_data


def safe_get(lst, idx, default=None):
    return lst[idx] if idx < len(lst) else default

def get_player_info(table, player_ID):
    
    growth2d = 0
    growth7d = 0
    previus_week_growth = 0
    Nrecords = 0
    growth_list = []
    
    # All data for this player_ID
    params = {
        "player_ID": player_ID,
        "player_name": None,
        "datarecord": None,
        "alliance": None,
        "kingdom": None,
    }
    info = search_by_query(table, params)
    # logger.info(info)
    ## info player attuali, da last record (supponendo sia in ordine cronologico)
    current_name = info[-1]['player_name']
    current_power = info[-1]['player_power']
    current_alliance = info[-1]['alliance']
    current_kingdom = info[-1]['kingdom']
    

    
    for i in range(0, len(info)):
        today = info[i]
        player_ID = today["player_ID"]
        Nrecords = Nrecords + 1 # calcolo quanti record ho del player. 
        
       
        yesterday = info[i - 1]
        print( f"Player ID:", player_ID)
        print(f"Power Yesterday: ", yesterday["player_power"])
        print(f"Power Today: ", today["player_power"] )
        daily_growth = today["player_power"] - yesterday["player_power"]
            
        #risultati
        growth_list.append(daily_growth)
        
        
    #calcolo crescita
    if Nrecords > 2:
        growth2d = growth_list[-1] + growth_list[-2]
    if Nrecords > 7:
        growth7d = growth_list[-1] + growth_list[-2] + growth_list[-3] + growth_list[-4] + growth_list[-5] + growth_list[-6] + growth_list[-7]
    if Nrecords > 13:
        previus_week_growth = growth_list[-7] + growth_list[-8] + growth_list[-9] + growth_list[-10] + growth_list[-11] + growth_list[-12] + growth_list[-13]

    
    # qui contiene tutte le info in modo ordinato
    player_info = {
        "player_ID": player_ID,
        "player_name": current_name,
        "player_power": current_power,
        "player_growth_2d": growth2d,
        "player_growth_7d": growth7d,
        "player_growth_last_week": growth7d,
        "player_growth_previus_week": previus_week_growth,
        "current_alliance": current_alliance,
        "current_kingdom": current_kingdom,
        "N_records": Nrecords, # quanti record ho di questo ID.
    }

    #print(player_info) # print debug
    return player_info





def get_alliance_info(table, alliance, datarecord):

    params = {
        "player_ID": None,
        "player_name": None,
        "datarecord": None,
        "alliance": alliance,
        "kingdom": None,
    }
    # All data for this player_ID
    info = search_by_query(table, params)

    player_table = []
    alliance_power = 0
    Nrecords = 0
    for row in info:
        if row['datarecord'] == datarecord:
            player_ID = row['player_ID']
            #print(player_ID)
            print(row['player_power'])
            alliance_power = alliance_power + row['player_power'] # total power ally
            Nrecords = Nrecords + 1 # numero di record / players
            average_power = alliance_power / Nrecords
            
            #info players per tabella
            playerINFOS = get_player_info(table, player_ID)


            player_table.append({
                "player_ID": playerINFOS['player_ID'],
                "player_name": playerINFOS['player_name'],
                "player_power": playerINFOS['player_power'],
                "player_growth_2d": playerINFOS['player_growth_2d'],
                "player_growth_7d": playerINFOS['player_growth_7d'],
                "player_growth_last_week": playerINFOS['player_growth_last_week'],
                "player_growth_previus_week": playerINFOS['player_growth_previus_week'],
            })
        


       ### da finire pw growth ALLY
    growth2d = 0
    growth7d = 0
    alliance_info = {
        'alliance_tag': alliance,
        'total_power': alliance_power,
        'average_power': average_power,
        'alliance_growth2d': growth2d,
        'alliance_growth7d': growth7d,
        'player_table': player_table,
        'datarecord': datarecord,
    }



    print(alliance_info)
    return alliance_info






def get_kingdom_info(table, kingdom, datarecord):

    Nplayers = 0
    N_alliance = [] #Lista ally
    alliancesInfo = []
    KDpower = 0

    params = {
        "player_ID": None,
        "player_name": None,
        "datarecord": None,
        "alliance": None,
        "kingdom": kingdom,
    }
    # All data for this player_ID
    info = search_by_query(table, params)


    for row in info:
        if row['datarecord'] == datarecord:
            NewAlly = row['alliance']
            KDpower = row['player_power'] + KDpower
            Nplayers = Nplayers + 1
            if NewAlly not in N_alliance: # se nn è in array, lo inserisce
                N_alliance.append(NewAlly)


    KDaverage_power = KDpower / Nplayers
    for alliance in N_alliance:
        NewAlly = get_alliance_info(table=table, alliance=alliance, datarecord=datarecord)
        alliancesInfo.append(NewAlly)

    # ifnormazioni ally
    ally1_info = safe_get(alliancesInfo, 0, {})
    ally2_info = safe_get(alliancesInfo, 1, {})
    ally3_info = safe_get(alliancesInfo, 2, {})
    ally4_info = safe_get(alliancesInfo, 3, {})
    ally5_info = safe_get(alliancesInfo, 4, {})




    kingdom_info = {
        'kingdom': kingdom,
        'Nplayers': Nplayers, # quanti giocatori unici ci sono
        'N_alliance': N_alliance, # lista ally
        'KDpower': KDpower,
        'KDaverage_power': KDaverage_power,
        'Alliance1_info': ally1_info,
        'Alliance2_info': ally2_info,
        'Alliance3_info': ally3_info,
        'Alliance4_info': ally4_info,
        'Alliance5_info': ally5_info,  # semplicemente usa get_alliance_info con parametri diversi. EASY
    }

    print(kingdom_info)
    return kingdom_info


## chiamata get player info, dai in input ID e table dove cercare
table = "players_list"
alliance='Gz34'
datarecord = '2025-10-30'
kingdom = 3829
player_ID = 202928036
#get_player_info(table, player_ID)
info = (get_alliance_info(table, alliance, datarecord))
print(info)
#get_kingdom_info(table, kingdom, datarecord)

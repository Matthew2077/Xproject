from dotenv import load_dotenv
import os
import logging
from datetime import timedelta, datetime
from PIL import Image
import pytesseract
import re
import sqlite3



#COSA FA IL PROGRAMMA:
# gli screenshot vengono caricati nella cartella "inputdata" 
# il programma avrà diversi parametri: 
# - nome alliance; 
# - numero kingdom;
# - datarecord (data + numero di record di quel giorno);


# il programma dovrà elaborare ogni screenshot prendendo i dati necessari: ID, power, name. 
# ogni screenshot elaborato alimenterà un array dove verranno scritti i dati presi dallo screenshot + i parametri.
# L'array verrà usato per scrivere nel DB i nuovi dati. 



#impostazione logger:
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logdata/ROKdataUPLOAD.log', level=logging.INFO)


# Load environment variables
load_dotenv(dotenv_path="params.env")


# PARAMETERS:
FOLDER_INPUT = "inputdata"
FOLDER_LOG = "logdata"
#alliance = os.getenv("alliance")
kingdom = os.getenv("kingdom")
datarecord = os.getenv("datarecord")
table = 'players_list'  # Default table name if not set
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # Path to Tesseract OCR executable
player_data = []  
#logger.info(f"uploadTODB: Parameters loaded: {alliance}, {kingdom}, {datarecord} - time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

# Database connection
con = sqlite3.connect("3829KINGDOM.db")
cur = con.cursor()


# Coordinate for data extraction | Screenshot da PC
FIELDS = {
    "player_id": (872, 317, 997, 343), #esempio: (ID: 18443431)
    "player_name": (770, 339, 1090, 382), #esempio: (Name: SevenOilz)
    "player_power": (1004, 433, 1164, 464), #esempio: (Power: 143,762,415)
    "alliance": (789, 433, 836, 457), #esempio: (Alliance: [D29H])
}

# Coordinate di estrazione dati | Screenshot da mobile
# "player_name": (953, 255, 1289, 295),
# "player_power": (1255, 381, 1525, 427),
# "player_id": (1105, 219, 1230, 247),


# Elaborazione degli screenshot
# Qui andrà il codice per elaborare gli screenshot nella cartella FOLDER_INPUT
# e popolare l'array con i dati estratti.
def getinfofromscreenshot(file_path):
    data = {}
    img = Image.open(file_path) # immagine presa in esame


    # ciclo per estrarre i dati per ogni campo 
    for field, box in FIELDS.items():
        area = img.crop(box)
        testo = pytesseract.image_to_string(area, config="--psm 6").strip()

        # Pulizia del testo in base al campo
        if field == "player_power":
            # Rimuove virgole, punti, spazi
            testo = testo.replace(",", "").replace(".", "").replace(" ", "")
        
        if field == "alliance":
            # Rimuove virgole, punti, spazi
            testo = testo.replace(",", "").replace(".", "").replace(" ", "").replace("]", "").replace("[", "")
        
        elif field == "player_id":
            # Rimuove "ID: ", parentesi e spazi
            testo = testo.replace("ID:", "").strip()
            testo = testo.replace("-", "").strip()
            testo = re.sub(r"[()]", "", testo)  # rimuove parentesi
            testo = testo.strip()

        data[field] = testo

    return data


def insert_records(con, player_id, player_name, player_power, alliance, kingdom, datarecord, filename):
    query = f'''
        INSERT INTO {table} (player_id, player_name, player_power, alliance, kingdom, datarecord, filename)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    con.execute(query, (player_id, player_name, player_power, alliance, kingdom, datarecord, filename))
    con.commit()
    #con.close() # chiusa e salva
    
def process_screenshots():
    logger.info(f'uploadTODB: Process starting at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    
    for filename in os.listdir(FOLDER_INPUT):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(FOLDER_INPUT, filename)
            dati = getinfofromscreenshot(file_path)
            
            
            print(f"Working on: {filename}")
            logger.info(f"uploadTODB: Processing file: {filename} - time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            

            player_id = dati.get("player_id", "")
            player_name = dati.get("player_name", "")
            player_power = dati.get("player_power", "")
            alliance = dati.get("alliance", "")

            logger.info(f"uploadTODB: Extracted data - ID: {player_id}, Name: {player_name}, Power: {player_power} - time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            player_data.append({
                'player_id': player_id,
                'player_name': player_name,
                'player_power': player_power,
                'alliance': alliance,
                'kingdom': kingdom,
                'datarecord': datarecord,
                'filename': filename,
            })

            insert_records(con, player_id, player_name, player_power, alliance, kingdom, datarecord, filename)

            
            

    logger.info(f'uploadTODB: Process completed at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f"Process completed. Total records: {len(player_data)}")
    print(f"Data saved in player_data array: {player_data}")

if __name__ == '__main__':
    process_screenshots()

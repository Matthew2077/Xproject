import sys
from GetData import get_alliance_info, get_kingdom_info, get_player_info, safe_get, search_by_query
from uploadTODB import process_screenshots # il main che elabora i dati
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QFileDialog, QLabel, QTableWidget, QTableWidgetItem
)
import logging
from datetime import datetime
import sqlite3


# Cosa fa questo file:
# Il main permette all'utente, tramite una UI, di usare le funzioni del programma: 
# - visualizzazione dati (player, alleanza, regno) 
# - inserimento dati.
# 




# impostazione logger:
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logdata/ROKdataUPLOAD.log', level=logging.INFO)
logger.info(f"GetData: Starting processing - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Database connection
con = sqlite3.connect("D29H.db")
con.row_factory = sqlite3.Row  # permette di accedere alle colonne per nome

# PARAMETERS:
player_info = {}
alliance_info = {}
kingdom_info = {}



    
    
def say_hello():
    print('hello World')


def search_by_query():
    '''
    Function to retrieve specific data from the DB based on given parameters.
    '''
    table = "D29H_players"
    params = {
        "player_ID": player_ID,
        "player_name": None,
        "datarecord": None,
        "alliance": None,
        "kingdom": None,
    }
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
    print(player_data)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RoK Activity - XProject")
        self.resize(1200, 600)
        
        player_ID = 202928036
        
        layout = QVBoxLayout()
        test = ['ciao1', 'cia2o', 'ciao3']
        # Cosa deve fare:
        label = QLabel(test[0])
        label2 = QLabel(test[1])
        #label.show()
        layout.addWidget(label)
        layout.addWidget(label2)
        
        button = QPushButton('Click ME!!!')
        button.clicked.connect(lambda: get_player_info(player_ID))

        
        layout.addWidget(button)
        self.setLayout(layout)
        
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())




        # # Input testo
        # self.input_text = QLineEdit()
        # self.input_text.setPlaceholderText("Scrivi qualcosa...")
        # layout.addWidget(self.input_text)
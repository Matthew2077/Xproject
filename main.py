import tkinter as tk
from tkinter import ttk, messagebox
from GetData import get_player_info, get_alliance_info, get_kingdom_info, search_by_query

class ROKDatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ROK Database - Info Viewer")
        self.root.geometry("1200x800")
        
        # Variabile per la selezione del tipo di ricerca
        self.search_type = tk.StringVar(value="player")
        
        # Frame principale
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurazione per rendere la finestra ridimensionabile
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Titolo
        title_label = ttk.Label(main_frame, text="ROK Database Query Interface", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # Frame per la selezione del tipo di ricerca
        selection_frame = ttk.LabelFrame(main_frame, text="Select Research Type", padding="10")
        selection_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Radiobutton(selection_frame, text="player info", 
                       variable=self.search_type, value="player",
                       command=self.update_input_fields).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(selection_frame, text="alliance info", 
                       variable=self.search_type, value="alliance",
                       command=self.update_input_fields).grid(row=0, column=1, padx=10)
        ttk.Radiobutton(selection_frame, text="kingdom info", 
                       variable=self.search_type, value="kingdom",
                       command=self.update_input_fields).grid(row=0, column=2, padx=10)
        
        # Frame per i parametri di input
        self.input_frame = ttk.LabelFrame(main_frame, text="Research Parameters", padding="10")
        self.input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Variabili per gli input
        self.table_var = tk.StringVar(value="players_list")
        self.player_id_var = tk.StringVar()
        self.alliance_var = tk.StringVar()
        self.kingdom_var = tk.StringVar()
        self.datarecord_var = tk.StringVar(value="2025-08-08")
        
        # Inizializza i campi di input
        self.update_input_fields()
        
        # Bottone di ricerca
        search_button = ttk.Button(main_frame, text="Execute", 
                                   command=self.execute_search)
        search_button.grid(row=3, column=0, pady=15)
        
        # Frame per i risultati con canvas e scrollbar
        result_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        result_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # Canvas per contenere i risultati scrollabili
        self.canvas = tk.Canvas(result_frame)
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def update_input_fields(self):
        """Aggiorna i campi di input in base al tipo di ricerca selezionato"""
        # Pulisce il frame
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        # Campo tabella (comune a tutti)
        ttk.Label(self.input_frame, text="Table:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.input_frame, textvariable=self.table_var, width=30).grid(row=0, column=1, pady=5)
        
        if self.search_type.get() == "player":
            ttk.Label(self.input_frame, text="Player ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.input_frame, textvariable=self.player_id_var, width=30).grid(row=1, column=1, pady=5)
            
        elif self.search_type.get() == "alliance":
            ttk.Label(self.input_frame, text="Alliance Tag:").grid(row=1, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.input_frame, textvariable=self.alliance_var, width=30).grid(row=1, column=1, pady=5)
            
            ttk.Label(self.input_frame, text="Data Record (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.input_frame, textvariable=self.datarecord_var, width=30).grid(row=2, column=1, pady=5)
            
        elif self.search_type.get() == "kingdom":
            ttk.Label(self.input_frame, text="Kingdom Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.input_frame, textvariable=self.kingdom_var, width=30).grid(row=1, column=1, pady=5)
            
            ttk.Label(self.input_frame, text="Data Record (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
            ttk.Entry(self.input_frame, textvariable=self.datarecord_var, width=30).grid(row=2, column=1, pady=5)
    
    def execute_search(self):
        """Esegue la ricerca in base al tipo selezionato"""
        # Pulisce i risultati precedenti
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        try:
            table = self.table_var.get()
            
            if self.search_type.get() == "player":
                player_id = self.player_id_var.get()
                if not player_id:
                    messagebox.showerror("Errore", "Inserisci un Player ID")
                    return
                
                result = get_player_info(table, int(player_id))
                self.display_player_results(result, table, int(player_id))
                
            elif self.search_type.get() == "alliance":
                alliance = self.alliance_var.get()
                datarecord = self.datarecord_var.get()
                
                if not alliance or not datarecord:
                    messagebox.showerror("Errore", "Inserisci Alliance Tag e Data Record")
                    return
                
                result = get_alliance_info(table, alliance, datarecord)
                self.display_alliance_results(result)
                
            elif self.search_type.get() == "kingdom":
                kingdom = self.kingdom_var.get()
                datarecord = self.datarecord_var.get()
                
                if not kingdom or not datarecord:
                    messagebox.showerror("Errore", "Inserisci Kingdom Number e Data Record")
                    return
                
                result = get_kingdom_info(table, int(kingdom), datarecord)
                self.display_kingdom_results(result)
                
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la ricerca:\n{str(e)}")
    
    def display_player_results(self, result, table, player_id):
        """Visualizza i risultati per un giocatore"""
        # Intestazione Player Info
        header = ttk.Label(self.scrollable_frame, text="PLAYER INFO", 
                          font=('Arial', 14, 'bold'), foreground='blue')
        header.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Dati generali del player
        info_labels = [
            ("Player ID:", result['player_ID']),
            ("Player Name:", result['player_name']),
            ("Current Power:", f"{result['player_power']:,}"),
            ("Growth 2 Days:", f"{result['player_growth_2d']:,}"),
            ("Growth 7 Days:", f"{result['player_growth_7d']:,}"),
            ("Growth Last Week:", f"{result['player_growth_last_week']:,}"),
            ("Growth Previous Week:", f"{result['player_growth_previus_week']:,}"),
            ("Current Alliance:", result['current_alliance']),
            ("Current Kingdom:", result['current_kingdom']),
            ("Number of Records:", result['N_records'])
        ]
        
        row = 1
        for label, value in info_labels:
            ttk.Label(self.scrollable_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=row, column=0, sticky=tk.W, padx=10, pady=2)
            ttk.Label(self.scrollable_frame, text=str(value)).grid(
                row=row, column=1, sticky=tk.W, padx=10, pady=2)
            row += 1
        
        # Separatore
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Intestazione tabella record storici
        ttk.Label(self.scrollable_frame, text="HISTORICAL RECORDS", 
                 font=('Arial', 12, 'bold'), foreground='green').grid(
            row=row, column=0, columnspan=2, pady=10, sticky=tk.W)
        row += 1
        
        # Recupera tutti i record del player
        params = {
            "player_ID": player_id,
            "player_name": None,
            "datarecord": None,
            "alliance": None,
            "kingdom": None,
        }
        all_records = search_by_query(table, params)
        
        # Tabella con i record
        tree_frame = ttk.Frame(self.scrollable_frame)
        tree_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        columns = ('player_ID', 'player_name', 'player_power', 'alliance', 'kingdom', 'datarecord')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Definizione colonne
        tree.heading('player_ID', text='Player ID')
        tree.heading('player_name', text='Player Name')
        tree.heading('player_power', text='Power')
        tree.heading('alliance', text='Alliance')
        tree.heading('kingdom', text='Kingdom')
        tree.heading('datarecord', text='Date')
        
        tree.column('player_ID', width=100)
        tree.column('player_name', width=200)
        tree.column('player_power', width=120)
        tree.column('alliance', width=100)
        tree.column('kingdom', width=100)
        tree.column('datarecord', width=120)
        
        # Inserimento dati
        for record in all_records:
            tree.insert('', tk.END, values=(
                record['player_ID'],
                record['player_name'],
                f"{record['player_power']:,}",
                record['alliance'],
                record['kingdom'],
                record['datarecord']
            ))
        
        # Scrollbar per la tabella
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def display_alliance_results(self, result):
        """Visualizza i risultati per un'alleanza"""
        # Parte 1: Dati Generali
        header = ttk.Label(self.scrollable_frame, text="ALLIANCE INFO - GENERAL INFO", 
                          font=('Arial', 14, 'bold'), foreground='blue')
        header.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        general_info = [
            ("Alliance Tag:", result['alliance_tag']),
            ("Total Power:", f"{result['total_power']:,}"),
            ("Average Power:", f"{result['average_power']:,.2f}"),
            ("Data Record:", result['datarecord'])
        ]
        
        row = 1
        for label, value in general_info:
            ttk.Label(self.scrollable_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=row, column=0, sticky=tk.W, padx=10, pady=2)
            ttk.Label(self.scrollable_frame, text=str(value)).grid(
                row=row, column=1, sticky=tk.W, padx=10, pady=2)
            row += 1
        
        # Separatore
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Parte 2: Lista Players
        ttk.Label(self.scrollable_frame, text="PLAYER LIST", 
                 font=('Arial', 12, 'bold'), foreground='green').grid(
            row=row, column=0, columnspan=2, pady=10, sticky=tk.W)
        row += 1
        
        # Tabella players
        tree_frame = ttk.Frame(self.scrollable_frame)
        tree_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        columns = ('player_ID', 'player_name', 'player_power', 'growth_2d', 'growth_7d', 'growth_last_week', 'growth_prev_week')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        tree.heading('player_ID', text='Player ID')
        tree.heading('player_name', text='Player Name')
        tree.heading('player_power', text='Power')
        tree.heading('growth_2d', text='Growth 2D')
        tree.heading('growth_7d', text='Growth 7D')
        tree.heading('growth_last_week', text='Growth Last Week')
        tree.heading('growth_prev_week', text='Growth Prev Week')
        
        tree.column('player_ID', width=100)
        tree.column('player_name', width=180)
        tree.column('player_power', width=120)
        tree.column('growth_2d', width=100)
        tree.column('growth_7d', width=100)
        tree.column('growth_last_week', width=130)
        tree.column('growth_prev_week', width=130)
        
        for player in result['player_table']:
            tree.insert('', tk.END, values=(
                player['player_ID'],
                player['player_name'],
                f"{player['player_power']:,}",
                f"{player['player_growth_2d']:,}",
                f"{player['player_growth_7d']:,}",
                f"{player['player_growth_last_week']:,}",
                f"{player['player_growth_previus_week']:,}"
            ))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def display_kingdom_results(self, result):
        """Visualizza i risultati per un regno"""
        row = 0
        
        # Dati Generali Regno
        header = ttk.Label(self.scrollable_frame, text="KINGDOM INFO - DATI GENERALI", 
                          font=('Arial', 14, 'bold'), foreground='blue')
        header.grid(row=row, column=0, columnspan=2, pady=10, sticky=tk.W)
        row += 1
        
        general_info = [
            ("Kingdom:", result['kingdom']),
            ("Number of Players:", result['Nplayers']),
            ("Number of Alliances:", len(result['N_alliance'])),
            ("Alliance List:", ", ".join(result['N_alliance'])),
            ("Total Kingdom Power:", f"{result['KDpower']:,}"),
            ("Average Kingdom Power:", f"{result['KDaverage_power']:,.2f}")
        ]
        
        for label, value in general_info:
            ttk.Label(self.scrollable_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=row, column=0, sticky=tk.W, padx=10, pady=2)
            ttk.Label(self.scrollable_frame, text=str(value)).grid(
                row=row, column=1, sticky=tk.W, padx=10, pady=2)
            row += 1
        
        # Separatore
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Visualizza ogni alleanza
        alliance_keys = ['Alliance1_info', 'Alliance2_info', 'Alliance3_info', 'Alliance4_info', 'Alliance5_info']
        
        for key in alliance_keys:
            alliance_data = result.get(key, {})
            if alliance_data and alliance_data.get('alliance_tag'):
                # Intestazione Alleanza
                ttk.Label(self.scrollable_frame, 
                         text=f"ALLIANCE: {alliance_data['alliance_tag']}", 
                         font=('Arial', 12, 'bold'), 
                         foreground='darkgreen').grid(row=row, column=0, columnspan=2, pady=10, sticky=tk.W)
                row += 1
                
                # Dati generali alleanza
                ally_info = [
                    ("Total Power:", f"{alliance_data['total_power']:,}"),
                    ("Average Power:", f"{alliance_data['average_power']:,.2f}"),
                ]
                
                for label, value in ally_info:
                    ttk.Label(self.scrollable_frame, text=label, font=('Arial', 9, 'bold')).grid(
                        row=row, column=0, sticky=tk.W, padx=20, pady=1)
                    ttk.Label(self.scrollable_frame, text=str(value), font=('Arial', 9)).grid(
                        row=row, column=1, sticky=tk.W, padx=10, pady=1)
                    row += 1
                
                # Tabella players dell'alleanza
                tree_frame = ttk.Frame(self.scrollable_frame)
                tree_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=20, pady=5)
                row += 1
                
                columns = ('player_ID', 'player_name', 'player_power', 'growth_2d', 'growth_7d')
                tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
                
                tree.heading('player_ID', text='Player ID')
                tree.heading('player_name', text='Player Name')
                tree.heading('player_power', text='Power')
                tree.heading('growth_2d', text='Growth 2D')
                tree.heading('growth_7d', text='Growth 7D')
                
                tree.column('player_ID', width=100)
                tree.column('player_name', width=180)
                tree.column('player_power', width=120)
                tree.column('growth_2d', width=100)
                tree.column('growth_7d', width=100)
                
                for player in alliance_data.get('player_table', []):
                    tree.insert('', tk.END, values=(
                        player['player_ID'],
                        player['player_name'],
                        f"{player['player_power']:,}",
                        f"{player['player_growth_2d']:,}",
                        f"{player['player_growth_7d']:,}"
                    ))
                
                scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                
                tree.grid(row=0, column=0, sticky=(tk.W, tk.E))
                scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
                
                # Separatore tra alleanze
                ttk.Separator(self.scrollable_frame, orient='horizontal').grid(
                    row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
                row += 1

def main():
    root = tk.Tk()
    app = ROKDatabaseGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# RoKActivity XProject Documentation

Il progetto si pone l'obbiettivo di creare una mini app che permetta la visualizzazione e la gestione di un DB SQLite con i dati di alleanze/regni di rise of kingdoms. 


### Processo dell'applicazione:
1. Acquisizione (screenshot png, jpg etc);
2. Nornalizzazione dati (da screenshot a table o DB) (+ pulizia dati)
3. Elaborazione dati (da DB / table estrai le info che vuoi, tipo crescita in power etc)
4. Visualizzazione dati (grafici etc) (vedi R ...)


## Implementazione grafica: 
- visualizzazione player: incolla i dati del player attuale, i dati di oggi o della data selezionata.
Poi visualizza la crescita del player negli ultimi X giorni. 
- visualizzazione alleanza: tabella con tutti i player al suo interno. Dati aggregati ( in alto?) Crescita media etc
- visualizzazione regno: Quadratini con dati generali delle top 5 ally + Dati generali

Interazioni del player: scegliere il player da visualizzare, l'alleanza o il regno. Scegliere il giorno da cui prende i dati.

Extra: pagina per caricamento dati (magari usa quella roba filesystem che hai scaricato)




# PROCESSO DELL'APPLICAZIONE IN DETTAGLIO (Idea iniziale + altre aggiunte)
**1. ACQUISIZIONE:**
Screenshot daranno tutto ciò che serve, devo provare a farli da PC per non doverli caricare su drive e poi scaricarli. Cronometra il tempo.
Vedi come mitigare gli errori di screenshot e uniformare i dati.

Il next level è cercare di replicare ciò che fa il bot statsmaster e compagnia...
Credo che ci sia dietro un bot capace di riconoscere le schermate di gioco, riconoscimento visivo artificiale l'ha chiamato l'AI... dovrebbe essere simile a ciò che fa la telecamera del telefono quando usi il riconoscimento facciale... i think

**2. NORMALIZZAZIONE:**
Qui carichi i dati nel DB con lo script in modo da avere una tabella usabile per l'elaborazione dei dati
Crea le table DB predisposte ...
player_ID, player_name, player-power, player_helps, datarecord,  filename

filemane potrebbe essere normalizzato pure...
datarecord: fallo diventare un numero fatto dalla data + numero di attempt... così se fai due scan al giorno, puoi distinguerli
esempio: 2025081401 = 2025 08 14 + attempt 1
2025081402 = 2025 08 14 + attempt 2

**3.Elaborazione dati:**
- Select tutti i dati di un player (per ID)
- Select tutti i dati di un'alleanza
- Select tutti i dati secondo più condizioni: un certo datetime e un certo nome. 
- Select tutti i dati di un certo periodo di tempo: 7 giorni, 30 giorni, un mese. 

L'idea è di mettere su un sistema di ricerca fatto come le api di odoo: campi selezionati, condizioni particolari.

Creo una funzione concentrata sulla potenza. Prende in parametri due date: data di inizio e data di fine.  E, table e ID 
Deve prendere dati di un determinato player in un lasso di tempo per creare un array con sola potenza

Una volta fatto ciò, calcolo diverse cose:
- Quanto è cresciuto ogni giorno (rispetto al giorno prima)
- quanto è la crescita media del player
- crescita totale player da data 1 a data 2


**Come output vorrei avere:**
- ranking (JSON or xlsx) di ogni player con ID, nome, alleanza, regno, potere day inizio, potere day fine, crescita media, crescita più alta. 
- ranking di ogni player con ID, nome, alleanza, regno,  potere day 1, potere day 2, potere day 3, potere day 4, potere day 5, potere day 6, potere day 7.

quando avrò più dati potrò fare crescita totale in 30 giorni, crescita settiana scorsa e così fare il confronto.
possibilmente potrei anche capire se ci son stati picchi ? probabilmente.

controllo da fare quando i dati non sono in fila.   
















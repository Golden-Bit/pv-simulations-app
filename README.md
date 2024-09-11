Ecco una versione aggiornata e dettagliata della guida all'uso della UI per la configurazione e simulazione del sistema fotovoltaico, con l'integrazione dei valori di output e il relativo significato, inclusa la tabella finale con i valori medi di esempio:

---

### Guida all'Uso della UI per la Configurazione e Simulazione del Sistema Fotovoltaico

#### Panoramica
Questa applicazione Streamlit consente di configurare e simulare un sistema fotovoltaico, inclusi i parametri del generatore, del carico, dello stoccaggio e i dettagli finanziari. Dopo aver completato i moduli di configurazione, puoi eseguire la simulazione e visualizzare i risultati.

### 1. **Configurazione del Generatore**

**Descrizione delle Voci di Input:**
- **Efficienza dei Pannelli (%)**: Percentuale di efficienza dei pannelli solari. Valore di default: 20%.
- **Altezza del Pannello (m)**: Altezza del pannello solare. Valore di default: 1.722 metri.
- **Larghezza del Pannello (m)**: Larghezza del pannello solare. Valore di default: 1.11 metri.
- **Tipo di Disposizione**: Disposizione dei pannelli, orizzontale o verticale.
- **Inclinazione (gradi)**: Angolo di inclinazione dei pannelli. Valore di default: 30°.
- **Orientamento (gradi)**: Angolo di orientamento dei pannelli rispetto al nord. Valore di default: 180°.
- **Regione**: Regione geografica di installazione (nord, centro, sud).
- **Potenza Nominale (kW)**: Potenza nominale del sistema fotovoltaico in kW. Valore di default: 6.0 kW.
- **Unità di Misura della Potenza Oraria**: Unità di misura della potenza oraria, predefinita su "kWh".

**Descrizione dell'Output:**
- **Area Totale Pannelli (m²)**: Calcolata sulla base delle dimensioni del pannello e della potenza nominale. Indica l'area complessiva necessaria per installare i pannelli solari.

### 2. **Configurazione del Carico**

**Descrizione delle Voci di Input:**
- **Numero di Profili di Carico**: Numero di profili di carico da inserire. Valore di default: 1.
- **Consumo Totale Giornaliero (kWh)**: Consumo totale giornaliero per ciascun profilo. Valore di default: 15.0 kWh.
- **Modello Profilo**: Tipo di distribuzione del consumo (campana o uniforme).
- **Picco Profilo**: Valore di picco per il profilo di carico. Valore di default: 12.0.
- **Ampiezza Profilo**: Ampiezza del profilo di carico. Valore di default: 4.0.

**Descrizione dell'Output:**
- **Load Profiles**: Profilo di carico dettagliato, incluso il consumo orario. Mostra come varia il consumo energetico durante il giorno.

### 3. **Configurazione dello Stoccaggio**

**Descrizione delle Voci di Input:**
- **Capacità della Batteria (kWh)**: Capacità totale della batteria in kWh. Valore di default: 10.0 kWh.
- **Efficienza della Batteria (%)**: Percentuale di efficienza della batteria. Valore di default: 90%.
- **Potenza Massima di Carica (kW)**: Potenza massima di carica della batteria in kW. Valore di default: 5.0 kW.
- **Potenza Massima di Scarica (kW)**: Potenza massima di scarica della batteria in kW. Valore di default: 5.0 kW.

**Descrizione dell'Output:**
- **Capacità della Batteria**: Capacità totale utilizzata per il calcolo dell'autoconsumo e della gestione dell'energia. Indica quanta energia può essere immagazzinata e utilizzata dalla batteria.

### 4. **Configurazione Finanziaria**

**Descrizione delle Voci di Input:**
- **Costo del Modulo per kW (€)**: Costo per kW del modulo fotovoltaico. Valore di default: 250.0 €.
- **Costo dell'Inverter per kW (€)**: Costo per kW dell'inverter. Valore di default: 200.0 €.
- **Costo della Struttura per kW (€)**: Costo per kW della struttura di supporto. Valore di default: 200.0 €.
- **Costo Fisso per kW di Installazione (€)**: Costo fisso per kW per l'installazione. Valore di default: 300.0 €.
- **Costo Fisso di Progettazione (€)**: Costo fisso per la progettazione. Valore di default: 500.0 €.
- **Costo Annuo di Manutenzione per kW (€)**: Costo annuo di manutenzione per kW. Valore di default: 50.0 €.
- **Anni di Funzionalità**: Durata utile dell'impianto in anni. Valore di default: 20 anni.
- **Costo per kWh della Batteria (€)**: Costo per kWh della batteria. Valore di default: 500.0 €.
- **Costo Installazione per kWh della Batteria (€)**: Costo fisso per kWh per l'installazione della batteria. Valore di default: 50.0 €.
- **Valore Energia Acquistata (€)**: Costo dell'energia acquistata per kWh. Valore di default: 0.2 €.
- **Valore Energia Scambiata (€)**: Valore dell'energia scambiata per kWh. Valore di default: 0.15 €.
- **Valore Energia Venduta (€)**: Valore dell'energia venduta per kWh. Valore di default: 0.1 €.
- **Incentivi sull'Installazione (% Detrazione)**: Percentuale di detrazione per l'installazione. Valore di default: 45%.
- **Incentivi sui Beni Materiali (% Detrazione)**: Percentuale di detrazione sui beni materiali. Valore di default: 45%.
- **Incentivi sulla Manutenzione (% Detrazione)**: Percentuale di detrazione sulla manutenzione. Valore di default: 0%.

### 5. **Esecuzione della Simulazione**

Quando tutti i moduli sono completati e salvati, puoi fare clic sul pulsante "Esegui Simulazione" per avviare la simulazione. I risultati visualizzati includeranno:

- **Risultati della Simulazione**: Informazioni dettagliate sui risultati della simulazione, inclusi consumi, produzioni e metriche finanziarie.
- **Visualizzazione JSON**: Risultati della simulazione visualizzati in formato JSON.

**Sezioni Dettagliate dei Risultati:**

1. **Dati Generali**: Mostra i dettagli di configurazione del generatore e dello stoccaggio, rinominati e organizzati in base alle mappature fornite.

2. **Valori Orari**: Include dati su energia generata, consumo totale, energia usata dal generatore, energia usata dalla batteria, energia immessa in rete e energia prelevata dalla rete su base oraria.

3. **Valori Medi**:
   - **Media Giornaliera**: Mostra i valori medi giornalieri per energia generata, consumo totale, energia usata dal generatore e dalla batteria, energia immessa in rete e prelevata dalla rete.
   - **Media Mensile**: Riporta i valori medi mensili per gli stessi parametri.
   - **Media Annuale**: Fornisce i valori medi annuali.

4. **Analisi dei Guadagni**: Fornisce dettagli sull'energia totale prodotta, autoconsumata, immessa in rete, assorbita dalla rete, scambiata e venduta. Include anche l'analisi dei costi senza e con fotovoltaico, risparmio netto annuale e valore totale di scambio, vendita e acquisto.

5. **Costi**: Dettagli sui costi totali, costi dei moduli, inverter, struttura, installazione, progettazione, manutenzione e batterie, inclusi i costi di monitoraggio e installazione batterie.

6. **Guadagno per Metro Quadrato**: Calcola e visualizza il costo totale per metro quadrato, guadagno lordo per metro quadrato e guadagno netto per metro quadrato, fornendo una panoramica chiara dei costi e dei benefici per unità di area.

### 6. **Tabella Finale di Esempio**

| **Parametro**                                       | **Valore**        |
|-----------------------------------------------------|-------------------|
| **Costo Totale per Metro Quadrato (senza accumulo)** | €400 / kW         |
| **ROI Annuale**                                   | 9%                |
| **Tempo di Ritorno dell'Investimento**            | 10 anni           |
| **ROI Medio su 20 Anni**                          | 180%              |
| **Ciclo di Vita (anni)**                          | 20 anni           |

Questa tabella riassume i parametri finanziari principali per un sistema fotovoltaico simulato, fornendo informazioni chiave sui costi e sul ritorno dell'investimento nel lungo periodo.

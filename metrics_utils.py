def calcola_risparmio_annuo(
    E_totale, E_autoconsumata, E_fabbisogno,
    prezzo_energia_rete, prezzo_scambio, prezzo_vendita):
    """
    Calcola il risparmio annuo netto in bolletta e fornisce ulteriori dettagli sull'energia prodotta,
    autoconsumata, scambiata, venduta e acquistata dalla rete.

    :param E_totale: Energia totale prodotta dall’impianto fotovoltaico (kWh).
    :param E_autoconsumata: Energia autoconsumata (kWh).
    :param E_fabbisogno: Consumo totale annuo (kWh).
    :param prezzo_energia_rete: Prezzo dell’energia acquistata dalla rete (€/kWh).
    :param prezzo_scambio: Prezzo dell’energia scambiata (€/kWh).
    :param prezzo_vendita: Prezzo dell’energia venduta (€/kWh).
    :return: Dizionario contenente tutte le informazioni di calcolo.
    """

    # Calcolo dell'energia immessa in rete
    E_immessa = max(E_totale - E_autoconsumata, 0)

    # Calcolo dell'energia assorbita dalla rete
    E_assorbita = max(E_fabbisogno - E_autoconsumata, 0)

    # Calcolo dell'energia scambiata e venduta
    if E_immessa <= E_assorbita:
        E_scambio = E_immessa
        E_eccesso = 0
    else:
        E_scambio = E_assorbita
        E_eccesso = E_immessa - E_assorbita

    # Calcolo del costo senza impianto fotovoltaico
    C_senza_FV = E_fabbisogno * prezzo_energia_rete

    # Calcolo del costo con impianto fotovoltaico
    C_con_FV = (E_assorbita * prezzo_energia_rete) + (E_scambio * prezzo_scambio) - (E_eccesso * prezzo_vendita)

    # Calcolo del risparmio annuo netto
    risparmio_annuo = C_senza_FV - C_con_FV

    # Valore totale dell'energia scambiata
    valore_scambio = E_scambio * prezzo_scambio

    # Valore totale dell'energia venduta
    valore_vendita = E_eccesso * prezzo_vendita

    # Valore totale dell'energia acquistata dalla rete
    valore_acquistata = E_assorbita * prezzo_energia_rete

    # Creazione del dizionario con tutte le informazioni
    risultato = {
        'energia_totale_prod': round(E_totale, 2),
        'energia_autoconsumata': round(E_autoconsumata, 2),
        'energia_immessa_rete': round(E_immessa, 2),
        'energia_assorbita_rete': round(E_assorbita, 2),
        'energia_scambiata': round(E_scambio, 2),
        'energia_venduta': round(E_eccesso, 2),
        'costo_senza_fv': round(C_senza_FV, 2),
        'costo_con_fv': round(C_con_FV, 2),
        'risparmio_annuo_netto': round(risparmio_annuo, 2),
        'valore_totale_scambio': round(valore_scambio, 2),
        'valore_totale_vendita': round(valore_vendita, 2),
        'valore_totale_acquisto': round(valore_acquistata, 2),
        'prezzo_acqusito_energia': round(prezzo_energia_rete, 2),
        'prezzo_scambio_energia': round(prezzo_scambio, 2),
        'prezzo_vendita_energia': round(prezzo_vendita, 2),
        }

    return risultato


def calcola_punto_di_ritorno(costo_investimento_totale, risparmio_annuo_netto):
    """Calcola il punto di ritorno (Break-Even Point)"""
    if risparmio_annuo_netto <= 0:
        raise ValueError("Il risparmio annuo netto deve essere maggiore di zero.")
    punto_di_ritorno = costo_investimento_totale / risparmio_annuo_netto
    return punto_di_ritorno

def calcola_roi(costo_investimento_totale, risparmio_annuo_netto, anni):
    """Calcola il Return on Investment (ROI) semplice e totale"""
    if costo_investimento_totale <= 0:
        raise ValueError("Il costo dell'investimento deve essere maggiore di zero.")
    if anni <= 0:
        raise ValueError("Il numero di anni deve essere maggiore di zero.")

    # ROI semplice
    roi = (risparmio_annuo_netto / costo_investimento_totale) * 100

    # ROI totale sul ciclo di vita
    risparmio_totale = risparmio_annuo_netto * anni
    roi_totale = (risparmio_totale / costo_investimento_totale) * 100

    return roi, roi_totale


def calcola_metrica_finanziaria(costi, risparmio_annuo_netto, anni):
    """Calcola varie metriche finanziarie, inclusi ROI e punto di ritorno"""
    # Costi totali di investimento
    costo_investimento_totale = costi.get("costo_totale", 0)


    # Calcolo ROI e ROI totale
    roi, roi_totale = calcola_roi(costo_investimento_totale, risparmio_annuo_netto, anni)

    # Calcolo Punto di Ritorno
    punto_di_ritorno = calcola_punto_di_ritorno(costo_investimento_totale, risparmio_annuo_netto)

    return {
        "ROI Semplice (% su 1 anno)": round(roi, 2),
        f"ROI Totale (% su {anni} anni)": round(roi_totale, 2),
        "Punto di Ritorno (anni)": round(punto_di_ritorno, 2)
    }


def calcola_fattore_di_autoconsumo_prodotta(energia_autoconsumata, energia_totale_prodotta):
    """Calcola il fattore di autoconsumo valutato sull'energia prodotta (%)"""
    if energia_totale_prodotta <= 0:
        raise ValueError("L'energia totale prodotta deve essere maggiore di zero.")
    return (energia_autoconsumata / energia_totale_prodotta) * 100


def calcola_fattore_di_autoconsumo_consumo(energia_autoconsumata, energia_totale_consumo):
    """Calcola il fattore di autoconsumo valutato sull'energia consumata (%)"""
    if energia_totale_consumo <= 0:
        raise ValueError("L'energia totale consumata deve essere maggiore di zero.")
    return (energia_autoconsumata / energia_totale_consumo) * 100


if __name__ == "__main__":
    # Esempio di utilizzo della funzione

    # Dati iniziali
    E_totale = 10000    # kWh
    E_autoconsumata = 4000  # kWh
    E_fabbisogno = 6000    # kWh

    prezzo_energia_rete = 0.24  # €/kWh
    prezzo_scambio = 0.18  # €/kWh
    prezzo_vendita = 0.10  # €/kWh

    # Calcolo del risparmio annuo e delle altre informazioni
    risultati = calcola_risparmio_annuo(
        E_totale, E_autoconsumata, E_fabbisogno,
        prezzo_energia_rete, prezzo_scambio, prezzo_vendita)

    # Stampa dei risultati
    for key, value in risultati.items():
        print(f"{key}: {value:.2f}")

    ####################################################################################################################

    # Esempio di costi e risparmio annuo netto
    costi = {
        "costo_totale": 10000,
        "costo_modulo_totale": 2500,
        "costo_inverter_totale": 2000,
        "costo_struttura_totale": 500,
        "costo_fisso_installazione_totale": 5000,
        "costo_fisso_progettazione": 1000,
        "costo_annuo_manutenzione_totale": 200,
        "costo_per_kwh_batteria_totale": 3000,
        "costo_fisso_installazione_batterie_totale": 500,
        "costo_annuo_monitoraggio_totale": 100,
        "costo_annuo_manutenzione_batterie_totale": 50,
        "altri_costi": 500
    }

    risparmio_annuo_netto = 3237.62  # Risparmio annuo netto calcolato
    anni = 25  # Durata dell'investimento in anni

    metriche_finanziarie = calcola_metrica_finanziaria(costi, risparmio_annuo_netto, anni)

    print("Metriche Finanziarie:")
    for chiave, valore in metriche_finanziarie.items():
        print(f"{chiave}: {valore:.2f}")





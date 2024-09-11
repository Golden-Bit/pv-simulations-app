def costo_moduli(potenza_moduli_kw, costo_modulo_per_kw):
    """
    Calcola il costo totale dei moduli fotovoltaici.

    :param potenza_moduli_kw: Potenza nominale totale installata dei moduli in kilowatt (kW).
    :param costo_modulo_per_kw: Costo per kilowatt di picco dei moduli in €/kW.
    :return: Costo totale dei moduli in euro.
    """
    return potenza_moduli_kw * costo_modulo_per_kw


def costo_inverter(potenza_nominale_kw, costo_inverter_per_kw):
    """
    Calcola il costo totale degli inverter.

    :param potenza_nominale_kw: Potenza nominale dell'impianto in kilowatt (kW).
    :param costo_inverter_per_kw: Costo per kilowatt dell'inverter in €/kW.
    :return: Costo totale degli inverter in euro.
    """
    return potenza_nominale_kw * costo_inverter_per_kw


def costo_struttura(potenza_nominale_kw, costo_struttura_per_kw):
    """
    Calcola il costo delle strutture e dei supporti basato sulla potenza nominale.

    :param potenza_nominale_kw: Potenza nominale dell'impianto in kilowatt (kW).
    :param costo_struttura_per_kw: Costo per kW di potenza nominale per le strutture in €/kW.
    :return: Costo totale delle strutture in euro.
    """
    return potenza_nominale_kw * costo_struttura_per_kw


def costo_installazione_fisso(potenza_nominale_kw, costo_fisso_per_kw):
    """
    Calcola il costo di installazione come valore fisso moltiplicato per la potenza nominale in kW.

    :param potenza_nominale_kw: Potenza nominale dell'impianto in kilowatt (kW).
    :param costo_fisso_per_kw: Costo fisso per kW installato.
    :return: Costo totale di installazione in euro.
    """
    return potenza_nominale_kw * costo_fisso_per_kw


def costo_batterie(capacita_batterie_kwh, costo_per_kwh_batteria):
    """
    Calcola il costo totale delle batterie in funzione della capacità totale in kWh.

    :param capacita_batterie_kwh: Capacità totale delle batterie in kWh.
    :param costo_per_kwh_batteria: Costo per kWh delle batterie in €/kWh.
    :return: Costo totale delle batterie in euro.
    """
    return capacita_batterie_kwh * costo_per_kwh_batteria


def costo_installazione_batterie(capacita_batterie_kwh, costo_fisso_per_kwh_batteria):
    """
    Calcola il costo di installazione delle batterie in funzione della capacità totale in kWh.

    :param capacita_batterie_kwh: Capacità totale delle batterie in kWh.
    :param costo_fisso_per_kwh_batteria: Costo fisso per kWh di capacità installata in €/kWh.
    :return: Costo totale di installazione delle batterie in euro.
    """
    return capacita_batterie_kwh * costo_fisso_per_kwh_batteria


def costo_progettazione(costo_fisso_progettazione, costo_base_progettazione):
    """
    Restituisce il costo fisso per la progettazione e i permessi, comprensivo di un costo base.

    :param costo_fisso_progettazione: Costo fisso di progettazione in euro.
    :param costo_base_progettazione: Costo base per la progettazione in euro.
    :return: Costo totale della progettazione in euro.
    """
    return costo_fisso_progettazione + costo_base_progettazione


def costo_manutenzione(potenza_nominale_kw, costo_annuo_manutenzione_per_kw, anni_di_funzionalita,
                       capacita_batterie_kwh, costo_annuo_manutenzione_batterie_per_kwh,
                       costo_base_manutenzione):
    """
    Calcola il costo totale della manutenzione durante l'intero ciclo di vita dell'impianto,
    basato sulla potenza nominale in kW e sulla capacità delle batterie in kWh, aggiungendo un costo base.

    :param potenza_nominale_kw: Potenza nominale dell'impianto in kilowatt (kW).
    :param costo_annuo_manutenzione_per_kw: Costo annuo di manutenzione per kW in euro.
    :param anni_di_funzionalita: Numero di anni di funzionamento stimati dell'impianto.
    :param capacita_batterie_kwh: Capacità totale delle batterie in kWh.
    :param costo_annuo_manutenzione_batterie_per_kwh: Costo annuo di manutenzione per kWh di batterie in euro.
    :param costo_base_manutenzione: Costo base per la manutenzione in euro.
    :return: Costo totale della manutenzione in euro.
    """
    manutenzione_impianto = (potenza_nominale_kw * costo_annuo_manutenzione_per_kw * anni_di_funzionalita)
    manutenzione_batterie = (capacita_batterie_kwh * costo_annuo_manutenzione_batterie_per_kwh * anni_di_funzionalita)
    return manutenzione_impianto + manutenzione_batterie + costo_base_manutenzione



def costo_monitoraggio(potenza_nominale_kw, costo_annuo_monitoraggio_per_kw):
    """
    Calcola il costo totale del monitoraggio basato sulla potenza nominale in kW.

    :param potenza_nominale_kw: Potenza nominale dell'impianto in kilowatt (kW).
    :param costo_annuo_monitoraggio_per_kw: Costo annuo di monitoraggio per kW in euro.
    :return: Costo totale del monitoraggio in euro.
    """
    return potenza_nominale_kw * costo_annuo_monitoraggio_per_kw


def costo_totale(potenza_moduli_kw, costo_modulo_per_kw, potenza_nominale_kw, costo_inverter_per_kw,
                 costo_struttura_per_kw, costo_fisso_per_kw_installazione, costo_fisso_progettazione,
                 costo_annuo_manutenzione_per_kw, anni_di_funzionalita, capacita_batterie_kwh=0,
                 costo_per_kwh_batteria=0, costo_fisso_per_kwh_batteria_installazione=0,
                 costo_annuo_monitoraggio_per_kw=0, costo_annuo_manutenzione_batterie_per_kwh=0,
                 incentivi_installazione=0.0, incentivi_beni_materiali=0.0, incentivi_manutenzione=0.0,
                 altri_costi=0, costo_base_progettazione=0, costo_base_manutenzione=0):
    """
    Calcola il costo totale di un impianto fotovoltaico, incluse le batterie, installazione,
    manutenzione e monitoraggio, applicando incentivi per ridurre i costi.

    :param potenza_moduli_kw: Potenza nominale totale installata dei moduli in kilowatt (kW).
    :param costo_modulo_per_kw: Costo per kilowatt di picco dei moduli in €/kW.
    :param potenza_nominale_kw: Potenza nominale dell'impianto in kilowatt (kW).
    :param costo_inverter_per_kw: Costo per kW dell'inverter in €/kW.
    :param costo_struttura_per_kw: Costo per kW di potenza nominale per le strutture in €/kW.
    :param costo_fisso_per_kw_installazione: Costo fisso per kW per l'installazione dell'impianto in euro/kW.
    :param costo_fisso_progettazione: Costo fisso per la progettazione e i permessi in euro.
    :param costo_annuo_manutenzione_per_kw: Costo annuo di manutenzione per kW in euro.
    :param anni_di_funzionalita: Numero di anni di funzionalità dell'impianto.
    :param capacita_batterie_kwh: Capacità totale delle batterie in kWh.
    :param costo_per_kwh_batteria: Costo per kWh di capacità delle batterie in €/kWh.
    :param costo_fisso_per_kwh_batteria_installazione: Costo fisso per kWh di capacità installata delle batterie in €/kWh.
    :param costo_annuo_monitoraggio_per_kw: Costo annuo di monitoraggio per kW in euro.
    :param costo_annuo_manutenzione_batterie_per_kwh: Costo annuo di manutenzione per kWh di batterie in euro.
    :param incentivi_installazione: Percentuale di incentivo applicata ai costi di installazione.
    :param incentivi_beni_materiali: Percentuale di incentivo applicata ai costi dei beni materiali.
    :param incentivi_manutenzione: Percentuale di incentivo applicata ai costi di manutenzione.
    :param altri_costi: Eventuali altri costi aggiuntivi, come sistemi di monitoraggio.
    :param costo_base_progettazione: Costo base per la progettazione in euro.
    :param costo_base_manutenzione: Costo base per la manutenzione in euro.
    :return: Un dizionario con il costo totale e i costi per ogni singola voce.
    """
    # Calcolo dei singoli costi
    C_moduli = costo_moduli(potenza_moduli_kw, costo_modulo_per_kw)
    C_inverter = costo_inverter(potenza_nominale_kw, costo_inverter_per_kw)
    C_struttura = costo_struttura(potenza_nominale_kw, costo_struttura_per_kw)
    C_installazione = costo_installazione_fisso(potenza_nominale_kw, costo_fisso_per_kw_installazione)
    C_progettazione = costo_progettazione(costo_fisso_progettazione, costo_base_progettazione)
    C_manutenzione = costo_manutenzione(potenza_nominale_kw, costo_annuo_manutenzione_per_kw, anni_di_funzionalita,
                                        capacita_batterie_kwh, costo_annuo_manutenzione_batterie_per_kwh,
                                        costo_base_manutenzione)
    C_monitoraggio = costo_monitoraggio(potenza_nominale_kw, costo_annuo_monitoraggio_per_kw)

    # Calcolo dei costi delle batterie (se presenti)
    C_batterie = costo_batterie(capacita_batterie_kwh, costo_per_kwh_batteria)
    C_installazione_batterie = costo_installazione_batterie(capacita_batterie_kwh,
                                                            costo_fisso_per_kwh_batteria_installazione)

    # Somma totale di tutte le componenti
    C_totale_materiali = (C_moduli + C_inverter + C_struttura + C_batterie + C_installazione_batterie)
    C_totale_installazione = (C_installazione + C_progettazione)
    C_totale_manutenzione = C_manutenzione + C_monitoraggio

    C_totale_materiali = C_totale_materiali * (1 - incentivi_beni_materiali)
    C_totale_installazione = C_totale_installazione * (1 - incentivi_installazione)
    C_totale_manutenzione = C_totale_manutenzione * (1 - incentivi_manutenzione)

    C_totale_incentivato = C_totale_materiali + C_totale_installazione + C_totale_manutenzione + altri_costi

    return {
        'costo_totale': C_totale_incentivato,
        'costo_moduli': C_moduli * (1 - incentivi_beni_materiali),
        'costo_inverter': C_inverter * (1 - incentivi_beni_materiali),
        'costo_struttura': C_struttura * (1 - incentivi_beni_materiali),
        'costo_installazione': C_installazione * (1 - incentivi_installazione),
        'costo_progettazione': C_progettazione * (1 - incentivi_installazione),
        'costo_manutenzione': C_manutenzione * (1 - incentivi_manutenzione),
        'costo_monitoraggio': C_monitoraggio * (1 - incentivi_manutenzione),
        'costo_batterie': C_batterie * (1 - incentivi_beni_materiali),
        'costo_installazione_batterie': C_installazione_batterie * (1 - incentivi_beni_materiali),
        'altri_costi': altri_costi
    }

# Esempio di utilizzo dello script con i dati dell'esempio fornito
if __name__ == "__main__":
    # Parametri dell'esempio
    parametri = {
        'potenza_moduli_kw': 10,  # 10 kW
        'costo_modulo_per_kw': 250,  # €/kW
        'potenza_nominale_kw': 10,  # 10 kW
        'costo_inverter_per_kw': 200,  # €/kW
        'costo_struttura_per_kw': 50,  # €/kW per la struttura
        'costo_fisso_per_kw_installazione': 500,  # € per kW
        'costo_fisso_progettazione': 1000,  # € fissi
        'costo_annuo_manutenzione_per_kw': 20,  # €/kW per anno
        'anni_di_funzionalita': 25,  # anni
        'capacita_batterie_kwh': 20,  # kWh di batterie
        'costo_per_kwh_batteria': 300,  # €/kWh per le batterie
        'costo_fisso_per_kwh_batteria_installazione': 50,  # €/kWh
        'costo_annuo_monitoraggio_per_kw': 10,  # €/kW per anno
        'costo_annuo_manutenzione_batterie_per_kwh': 5,  # €/kWh per anno
        'incentivi_installazione': 0.2,  # 20% di incentivo
        'incentivi_beni_materiali': 0.15,  # 15% di incentivo sui beni materiali
        'incentivi_manutenzione': 0.1,  # 10% di incentivo sulla manutenzione
        'altri_costi': 500,  # Altri costi aggiuntivi
        'costo_base_progettazione': 200,  # € costo base progettazione
        'costo_base_manutenzione': 100,  # € costo base manutenzione
    }

    costi = costo_totale(**parametri)
    for voce, costo in costi.items():
        print(f"{voce}: {costo:.2f} €")


import numpy as np
import matplotlib.pyplot as plt


def distribuzione_uniforme(consumo_totale_giornaliero, ore=24):
    """Distribuisce il consumo giornaliero uniformemente nelle ore del giorno"""
    return np.full(ore, consumo_totale_giornaliero / ore)


def distribuzione_campana(consumo_totale_giornaliero, ore=24, picco=12, ampiezza=6):
    """Distribuisce il consumo giornaliero in una distribuzione a campana (Gaussiana) centrata intorno al picco"""
    x = np.linspace(0, ore - 1, ore)
    campana = np.exp(-0.5 * ((x - picco) / ampiezza) ** 2)
    campana_normalizzata = campana / np.sum(campana)  # Normalizza la distribuzione per sommare a 1
    return consumo_totale_giornaliero * campana_normalizzata


def distribuzione_normale(consumo_totale_giornaliero, ore=24, media=12, deviazione_standard=4):
    """Distribuisce il consumo giornaliero seguendo una distribuzione normale"""
    x = np.linspace(0, ore - 1, ore)
    normale = np.exp(-0.5 * ((x - media) / deviazione_standard) ** 2)
    normale_normalizzata = normale / np.sum(normale)  # Normalizza la distribuzione per sommare a 1
    return consumo_totale_giornaliero * normale_normalizzata


def distribuzione_personalizzata(consumo_totale_giornaliero, ore=24, pesi=None, normalize=False):
    """Distribuisce il consumo giornaliero in base a pesi personalizzati (la somma dei pesi deve essere 1)"""
    if pesi is None:
        pesi = np.ones(ore) / ore
    elif np.sum(pesi) != 1 and normalize:
        pesi = pesi / np.sum(pesi)
    elif np.sum(pesi) != 1 and not normalize:
        raise ValueError("La somma dei pesi deve essere 1.")
    return consumo_totale_giornaliero * pesi


def genera_consumo_orario(consumo_totale_giornaliero, modello='uniforme', **kwargs):
    """Genera i valori orari del consumo energetico secondo il modello selezionato"""
    if modello == 'uniforme':
        return distribuzione_uniforme(consumo_totale_giornaliero, **kwargs)
    elif modello == 'campana':
        return distribuzione_campana(consumo_totale_giornaliero, **kwargs)
    elif modello == 'normale':
        return distribuzione_normale(consumo_totale_giornaliero, **kwargs)
    elif modello == 'personalizzato':
        return distribuzione_personalizzata(consumo_totale_giornaliero, **kwargs)
    else:
        raise ValueError("Modello di distribuzione sconosciuto.")


def somma_distribuzioni(lista_distribuzioni):
    """
    Somma una lista di distribuzioni orarie e restituisce la distribuzione totale risultante.

    :param lista_distribuzioni: Lista di array contenenti le distribuzioni orarie (es. distribuzioni campana, uniforme, etc.)
    :return: Array che rappresenta la somma delle distribuzioni orarie
    """
    if not lista_distribuzioni:
        raise ValueError("La lista delle distribuzioni non può essere vuota.")

    # Controlla che tutte le distribuzioni abbiano la stessa lunghezza
    lunghezze = [len(distribuzione) for distribuzione in lista_distribuzioni]
    if len(set(lunghezze)) != 1:
        raise ValueError("Tutte le distribuzioni devono avere la stessa lunghezza.")

    # Somma le distribuzioni
    distribuzione_totale = np.sum(lista_distribuzioni, axis=0)

    return distribuzione_totale


def get_load(load_profiles):

    load = somma_distribuzioni([genera_consumo_orario(**load_profile) for load_profile in load_profiles])

    return load


def visualizza_consumo(consumi_orari, modello):
    """Visualizza il consumo orario usando un grafico"""
    ore = np.arange(1, len(consumi_orari) + 1)
    plt.figure(figsize=(10, 6))
    plt.plot(ore, consumi_orari, marker='o')
    plt.title(f"Consumo Orario - Modello {modello.capitalize()}")
    plt.xlabel("Ora del giorno")
    plt.ylabel("Consumo (kWh)")
    plt.grid(True)
    plt.show()


def main():
    # Input utente
    consumo_totale_giornaliero = 24  # Consumo medio giornaliero totale in kWh
    ore_giornaliere = 24

    # Scelta del modello e dei parametri
    modello = 'doppia_campana'  # Scegli tra 'uniforme', 'campana', 'normale', 'personalizzato'

    # Parametri personalizzati per il modello scelto
    if modello == 'campana':
        consumi_orari = genera_consumo_orario(consumo_totale_giornaliero, modello=modello, picco=13, ampiezza=5)

    elif modello == 'doppia_campana':
        campana_1 = genera_consumo_orario(consumo_totale_giornaliero, modello='campana', picco=12, ampiezza=1)
        campana_2 = genera_consumo_orario(consumo_totale_giornaliero, modello='campana', picco=19, ampiezza=1)
        consumi_orari = somma_distribuzioni([campana_1, campana_2])

    elif modello == 'normale':
        consumi_orari = genera_consumo_orario(consumo_totale_giornaliero, modello=modello, media=14,
                                              deviazione_standard=3)
    elif modello == 'personalizzato':
        pesi = np.array(
            [0.01, 0.02, 0.03, 0.03, 0.04, 0.05, 0.1, 0.15, 0.15, 0.1, 0.06, 0.05, 0.04, 0.04, 0.03, 0.02, 0.01, 0.01,
             0.01, 0.02, 0.03, 0.04, 0.03, 0.02])
        consumi_orari = genera_consumo_orario(consumo_totale_giornaliero, modello=modello, pesi=pesi, normalize=True)
    else:
        consumi_orari = genera_consumo_orario(consumo_totale_giornaliero, modello=modello)

    # Visualizzazione
    visualizza_consumo(consumi_orari, modello)


if __name__ == "__main__":
    main()

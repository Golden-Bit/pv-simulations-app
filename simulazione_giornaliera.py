import json

import numpy as np

from metrics_utils import calcola_fattore_di_autoconsumo_consumo, calcola_fattore_di_autoconsumo_prodotta
from simulation_utils import get_prod_data, calcola_superficie_minima


def stampa_riga_tabella(ora, E_prod, E_cons, E_autoconsumata, E_scaricata, energia_ceduta_ora, E_batteria, energia_rete_ora):
    """
    Stampa una riga della tabella in formato allineato con le colonne.
    """
    print(f"{ora:<9}{E_prod:<15.2f}{E_cons:<17.2f}{E_autoconsumata:<17.2f}"
          f"{E_scaricata:<15.2f}{energia_ceduta_ora:<16.2f}{E_batteria:<18.2f}{energia_rete_ora:<18.2f}")


def simula_giornata_(E_batteria_inizio, generator_kwargs, load_kwargs, storage_kwargs, verbose=0):
    """
    Simula l'andamento energetico durante una giornata considerando un sistema con produzione da fonti rinnovabili,
    consumo energetico, una batteria di accumulo e l'energia assorbita dalla rete.

    :param E_batteria_inizio: Energia iniziale nella batteria (kWh).
    :param produzione: Array di produzione energetica oraria (kWh per ogni ora).
    :param load_kwargs: Array di consumo energetico orario (kWh per ogni ora).
    :param C_batteria: Capacità massima della batteria (kWh).
    :param eta_batteria: Efficienza della batteria per carica/scarica (tra 0 e 1).
    :return: Energia finale nella batteria, autoconsumo diretto, autoconsumo indiretto, energia ceduta, energia assorbita dalla rete.
    """

    C_batteria = storage_kwargs["C_batteria"]
    eta_batteria = storage_kwargs["eta_batteria"]
    P_max_carica = storage_kwargs["P_max_carica"]
    P_max_scarica = storage_kwargs["P_max_scarica"]

    produzione = get_prod_data(**generator_kwargs)["hourly_pv_prod"]

    consumo = load_kwargs["hourly_values"]

    # Stato iniziale della batteria
    E_batteria = E_batteria_inizio

    # Variabili per tracciare i risultati
    autoconsumo_diretto = 0
    autoconsumo_indiretto = 0
    energia_ceduta = 0
    energia_rete = 0  # Energia assorbita dalla rete

    panels_area = calcola_superficie_minima(generator_kwargs["pv_nominal_power"],
                                            generator_kwargs["panels_efficiency"],
                                            generator_kwargs["inclinazione"],
                                            generator_kwargs["altezza_pannello"],
                                            generator_kwargs["larghezza_pannello"],
                                            generator_kwargs["tipo_di_disposizione"], )

    generator_kwargs["panels_area"] = panels_area

    simulation_result = {

        "generator_kwargs": generator_kwargs,
        "storage_kwargs": storage_kwargs,

        "hourly_values": [],

        "daily_average_values": {

        },

        "monthly_average_values": {

        },

        "annual_average_values": {

        }
    }

    simulation_result["daily_average_values"]["energy_by_generator"] = 0
    simulation_result["daily_average_values"]["total_load_energy"] = 0
    simulation_result["daily_average_values"]["energy_load_from_generator"] = 0
    simulation_result["daily_average_values"]["energy_load_from_battery"] = 0
    simulation_result["daily_average_values"]["energy_to_grid"] = 0
    simulation_result["daily_average_values"]["energy_to_battery"] = 0
    simulation_result["daily_average_values"]["hourly_energy_in_battery"] = []
    simulation_result["daily_average_values"]["energy_load_from_grid"] = 0

    if verbose:
        print("\n\n")
        print("Ora\tProdotta (kWh)\tConsumo (kWh)\tAutoc. Diretto\tAutoc. Indiretto\tCeduta\t\tBatteria (kWh)\tAssorbita dalla Rete")


    # Itera attraverso le 24 ore della giornata
    for h in range(24):
        E_prod = produzione[h]  # Energia prodotta nell'ora h
        E_cons = consumo[h]  # Energia consumata nell'ora h

        # Calcola l'autoconsumo diretto, cioè la parte della produzione che viene consumata immediatamente
        E_autoconsumata = min(E_prod, E_cons)
        autoconsumo_diretto += E_autoconsumata

        # Energia in eccesso (non consumata direttamente) disponibile per essere immagazzinata o ceduta
        E_eccesso = E_prod - E_autoconsumata

        # Se c'è energia in eccesso, proviamo a immagazzinarla nella batteria

        if E_eccesso > 0:
            # Calcoliamo quanta energia può essere immagazzinata nella batteria (tenendo conto dell'efficienza)
            E_immagazzinata = min(C_batteria - E_batteria, min(E_eccesso * eta_batteria, P_max_carica))
            E_batteria += E_immagazzinata  # Aggiorniamo l'energia nella batteria

            # L'energia che non può essere immagazzinata nella batteria viene ceduta alla rete
            energia_ceduta_ora = E_eccesso - (E_immagazzinata / eta_batteria)
            energia_ceduta += energia_ceduta_ora
        else:
            E_immagazzinata = 0
            energia_ceduta_ora = 0

        # Se il consumo supera la produzione, usiamo l'energia accumulata nella batteria (autoconsumo indiretto)
        if E_cons > E_prod:
            # Calcoliamo quanta energia è necessaria dalla batteria per soddisfare il consumo
            E_necessaria = E_cons - E_prod

            if E_batteria > 0:
                # Scarichiamo la batteria fino a coprire la richiesta o fino a svuotare la batteria
                E_scaricata = min(E_batteria, min(E_necessaria, P_max_scarica))

                E_batteria -= E_scaricata  # Aggiorniamo l'energia nella batteria

                # L'energia scaricata dalla batteria contribuisce all'autoconsumo indiretto
                autoconsumo_indiretto += E_scaricata
            else:
                E_scaricata = 0

            # Se la batteria non ha abbastanza energia, il resto viene assorbito dalla rete
            energia_rete_ora = E_necessaria - E_scaricata
            energia_rete += energia_rete_ora
        else:
            E_scaricata = 0
            energia_rete_ora = 0

        hourly_value = {
            "h": h,
            "energy_by_generator": round(E_prod, 2),
            "total_load_energy": round(E_cons, 2),
            "energy_load_from_generator": round(E_autoconsumata, 2),
            "energy_load_from_battery": round(E_scaricata, 2),
            "energy_to_grid": round(energia_ceduta_ora, 2),
            "energy_to_battery": round(E_immagazzinata, 2),
            "energy_in_battery": round(E_batteria, 2),
            "energy_load_from_grid": round(energia_rete_ora, 2),
        }

        simulation_result["hourly_values"].append(hourly_value)

        simulation_result["daily_average_values"]["energy_by_generator"] += round(E_prod, 2)
        simulation_result["daily_average_values"]["total_load_energy"] += round(E_cons, 2)
        simulation_result["daily_average_values"]["energy_load_from_generator"] += round(E_autoconsumata, 2)
        simulation_result["daily_average_values"]["energy_load_from_battery"] += round(E_scaricata, 2)
        simulation_result["daily_average_values"]["energy_to_grid"] += round(energia_ceduta_ora, 2)
        simulation_result["daily_average_values"]["energy_to_battery"] += round(E_immagazzinata, 2)
        simulation_result["daily_average_values"]["hourly_energy_in_battery"].append(round(E_batteria, 2))
        simulation_result["daily_average_values"]["energy_load_from_grid"] += round(energia_rete_ora, 2)

        # Stampa dettagliata dell'ora corrente
        if verbose:
            stampa_riga_tabella(h, E_prod, E_cons, E_autoconsumata, E_scaricata, energia_ceduta_ora, E_batteria, energia_rete_ora)

    fattore_di_autoconsumo_consumo = calcola_fattore_di_autoconsumo_consumo(
        simulation_result["daily_average_values"]["energy_load_from_generator"] + simulation_result["daily_average_values"]["energy_load_from_battery"],
        simulation_result["daily_average_values"]["total_load_energy"],
    )

    fattore_di_autoconsumo_prodotta = calcola_fattore_di_autoconsumo_prodotta(
        simulation_result["daily_average_values"]["energy_load_from_generator"] + simulation_result["daily_average_values"]["energy_load_from_battery"],
        simulation_result["daily_average_values"]["energy_by_generator"],
    )

    simulation_result["daily_average_values"]["autoconsumo %(energia consumata)"] = round(fattore_di_autoconsumo_consumo, 2)
    simulation_result["daily_average_values"]["autoconsumo %(energia prodotta)"] = round(fattore_di_autoconsumo_prodotta, 2)

    simulation_result["daily_average_values"]["energy_by_generator"] = round(simulation_result["daily_average_values"]["energy_by_generator"], 2)
    simulation_result["daily_average_values"]["total_load_energy"] = round(simulation_result["daily_average_values"]["total_load_energy"], 2)
    simulation_result["daily_average_values"]["energy_load_from_generator"] = round(simulation_result["daily_average_values"]["energy_load_from_generator"], 2)
    simulation_result["daily_average_values"]["energy_load_from_battery"] = round(simulation_result["daily_average_values"]["energy_load_from_battery"], 2)
    simulation_result["daily_average_values"]["energy_to_grid"] = round(simulation_result["daily_average_values"]["energy_to_grid"], 2)
    simulation_result["daily_average_values"]["energy_to_battery"] = round(simulation_result["daily_average_values"]["energy_to_battery"], 2)
    simulation_result["daily_average_values"]["energy_load_from_grid"] = round(simulation_result["daily_average_values"]["energy_load_from_grid"], 2)

    simulation_result["monthly_average_values"]["energy_by_generator"] = round(simulation_result["daily_average_values"]["energy_by_generator"] * 30, 2)
    simulation_result["monthly_average_values"]["total_load_energy"] = round(simulation_result["daily_average_values"]["total_load_energy"] * 30, 2)
    simulation_result["monthly_average_values"]["energy_load_from_generator"] = round(simulation_result["daily_average_values"]["energy_load_from_generator"] * 30, 2)
    simulation_result["monthly_average_values"]["energy_load_from_battery"] = round(simulation_result["daily_average_values"]["energy_load_from_battery"] * 30, 2)
    simulation_result["monthly_average_values"]["energy_to_grid"] = round(simulation_result["daily_average_values"]["energy_to_grid"] * 30, 2)
    simulation_result["monthly_average_values"]["energy_to_battery"] = round(simulation_result["daily_average_values"]["energy_to_battery"] * 30, 2)
    simulation_result["monthly_average_values"]["energy_load_from_grid"] = round(simulation_result["daily_average_values"]["energy_load_from_grid"] * 30, 2)

    simulation_result["annual_average_values"]["energy_by_generator"] = round(simulation_result["monthly_average_values"]["energy_by_generator"] * 12, 2)
    simulation_result["annual_average_values"]["total_load_energy"] = round(simulation_result["monthly_average_values"]["total_load_energy"] * 12, 2)
    simulation_result["annual_average_values"]["energy_load_from_generator"] = round(simulation_result["monthly_average_values"]["energy_load_from_generator"] * 12, 2)
    simulation_result["annual_average_values"]["energy_load_from_battery"] = round(simulation_result["monthly_average_values"]["energy_load_from_battery"] * 12, 2)
    simulation_result["annual_average_values"]["energy_to_grid"] = round(simulation_result["monthly_average_values"]["energy_to_grid"] * 12, 2)
    simulation_result["annual_average_values"]["energy_to_battery"] = round(simulation_result["monthly_average_values"]["energy_to_battery"] * 12, 2)
    simulation_result["annual_average_values"]["energy_load_from_grid"] = round(simulation_result["monthly_average_values"]["energy_load_from_grid"] * 12, 2)

    return simulation_result


def simula_giornata(max_iter, generator_kwargs, load_kwargs, storage_kwargs, verbose=0):

    E_batteria_inizio = 0
    simulation_result = None

    for i in range(max_iter):

        simulation_result = simula_giornata_(
            E_batteria_inizio, generator_kwargs, load_kwargs, storage_kwargs, verbose
        )

        E_batteria_fine = simulation_result["daily_average_values"]["hourly_energy_in_battery"][-1]

        if abs(E_batteria_fine - E_batteria_inizio) < 0.01:
            return simulation_result
        else:
            E_batteria_inizio += (E_batteria_fine - E_batteria_inizio)/2

    return simulation_result


# Funzione principale per eseguire la simulazione
if __name__ == "__main__":

    # TODO:
    #  - [x] aggiungi info su efficienza moduli
    #  - [x] determina la superficie minima necessaria al fine di non creare ombreggiamenti reciproci
    #  - [ ] inserisci anche fattori parassiti

    generator_kwargs = {
        "panels_efficiency": 0.207,
        "altezza_pannello": 1.722,
        "larghezza_pannello": 1.11,
        "tipo_di_disposizione": "orizzontale",
        "inclinazione": 30,
        "orientamento": 180,
        "region": "sud",  # ["nord", "centro", "sud"]"
        "pv_nominal_power": 100,
        "hourly_power_unit_measure": "kWh"}  # "w"

    consumo = [1, 1, 1, 1, 1, 1, 2, 3, 4, 4, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 2, 2, 1, 1]  # kWh

    storage_kwargs = {
        "C_batteria": 100, # Capacità della batteria in kWh
        "eta_batteria": 0.9, # Efficienza della batteria (90%)
        "P_max_carica": 50, # Potenza massima di carica della batteria in kW
        "P_max_scarica": 50, # Potenza massima di scarica della batteria in kW
    }

    simulation_result = simula_giornata(
        100, generator_kwargs, consumo, storage_kwargs
    )

    print("\n")
    print(json.dumps(simulation_result, indent=2))
    print("\n")


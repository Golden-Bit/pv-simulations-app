import json

from financial_utils import costo_totale
from load_utils import get_load, visualizza_consumo
from metrics_utils import calcola_risparmio_annuo, calcola_metrica_finanziaria
from simulazione_giornaliera import simula_giornata


def main(generator_kwargs, storage_kwargs, load_kwargs, financial_kwargs):

    ####################################################################################################################
    # simulazione giornaliera

    load = get_load(**load_kwargs)

    visualizza_consumo(load, "Custom Load Model")

    load_kwargs = {"hourly_values": load}

    simulation_result = simula_giornata(
        100, generator_kwargs, load_kwargs, storage_kwargs, verbose=1,
    )

    print("\n")
    print(json.dumps(simulation_result, indent=2))
    print("\n")
    ####################################################################################################################
    print("\n")
    print("#" * 120)
    print("\n")
    ####################################################################################################################
    # calcolo del risparmio in bolletta (annuale)

    # Dati iniziali
    E_totale = simulation_result["annual_average_values"]["energy_by_generator"]  # kWh

    E_autoconsumata = (simulation_result["annual_average_values"]["energy_load_from_generator"] +
                       simulation_result["annual_average_values"]["energy_load_from_battery"]) # kWh

    E_fabbisogno = simulation_result["annual_average_values"]["total_load_energy"]  # kWh

    prezzo_energia_rete = financial_kwargs["valore_energia_acquistata"]
    prezzo_scambio = financial_kwargs["valore_energia_scambiata"]
    prezzo_vendita = financial_kwargs["valore_energia_venduta"]

    del financial_kwargs["valore_energia_acquistata"]
    del financial_kwargs["valore_energia_scambiata"]
    del financial_kwargs["valore_energia_venduta"]

    # Calcolo del risparmio annuo e delle altre informazioni
    gain_analysis = calcola_risparmio_annuo(
        E_totale, E_autoconsumata, E_fabbisogno,
        prezzo_energia_rete, prezzo_scambio, prezzo_vendita)

    # Stampa dei risultati
    for key, value in gain_analysis.items():
        print(f"{key}: {value:.2f}")

    ####################################################################################################################
    print("\n")
    print("#" * 120)
    print("\n")
    ####################################################################################################################
    # calcolo dei costi annuali

    financial_kwargs["potenza_moduli_kw"] = generator_kwargs["pv_nominal_power"]
    financial_kwargs["potenza_nominale_kw"] = generator_kwargs["pv_nominal_power"]
    financial_kwargs["capacita_batterie_kwh"] = storage_kwargs["C_batteria"]

    costi = costo_totale(**financial_kwargs)

    costi["input_parameters"] = financial_kwargs

    for voce, costo in costi.items():
        if isinstance(costo, dict):
            print(f"{voce}: {json.dumps(costo, indent=2)}")
        else:
            print(f"{voce}: {costo:.2f} €")

    financial_kwargs["valore_energia_acquistata"] = prezzo_energia_rete
    financial_kwargs["valore_energia_scambiata"] = prezzo_scambio
    financial_kwargs["valore_energia_venduta"] = prezzo_vendita

    ####################################################################################################################
    print("\n")
    print("#" * 120)
    print("\n")
    ####################################################################################################################
    # calcolo delle metriche di investimento

    risparmio_annuo = gain_analysis["risparmio_annuo_netto"]
    anni_funzionamento = financial_kwargs["anni_di_funzionalita"]

    financial_analysis = calcola_metrica_finanziaria(costi, risparmio_annuo, anni_funzionamento)

    ####################################################################################################################

    return {
        "financial_kwargs": financial_kwargs,
        "simulation_result": simulation_result,
        "gain_analysis": gain_analysis,
        "financial_analysis": financial_analysis,
        "costs": costi
    }

    ####################################################################################################################


if __name__ == "__main__":

    generator_kwargs = {
        "panels_efficiency": 0.207,
        "altezza_pannello": 1.722,
        "larghezza_pannello": 1.11,
        "tipo_di_disposizione": "orizzontale",
        "inclinazione": 30,
        "orientamento": 180,
        "region": "sud",  # ["nord", "centro", "sud"]"
        "pv_nominal_power": 6,
        "hourly_power_unit_measure": "kWh"}  # "w"

    load_kwargs = {"load_profiles":
        [
            {
                "consumo_totale_giornaliero": 5,
                "modello": "campana",
                "picco":12,
                "ampiezza": 2
            },
            {
                "consumo_totale_giornaliero": 5,
                "modello": "campana",
                "picco": 19,
                "ampiezza": 2
            }
        ]
    }

    storage_kwargs = {
        "C_batteria": 10, # Capacità della batteria in kWh
        "eta_batteria": 0.9, # Efficienza della batteria (90%)
        "P_max_carica": 10, # Potenza massima di carica della batteria in kW
        "P_max_scarica": 10, # Potenza massima di scarica della batteria in kW
    }

    financial_kwargs = {
        'valore_energia_acquistata': 0.24,  # €/kWh
        'valore_energia_scambiata': 0.18,  # €/kWh
        'valore_energia_venduta': 0.10,  # €/kWh
        'costo_modulo_per_kw': 250,  # €/kW
        'costo_inverter_per_kw': 200,  # €/kW
        'costo_struttura_per_kw': 50,  # €/kW per la struttura
        'costo_fisso_per_kw_installazione': 500,  # € per kW
        'costo_fisso_progettazione': 1000,  # € fissi
        'costo_annuo_manutenzione_per_kw': 20,  # €/kW per anno
        'anni_di_funzionalita': 25,  # anni
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

    result = main(generator_kwargs, storage_kwargs, load_kwargs, financial_kwargs)

    print(json.dumps(result, indent=2))


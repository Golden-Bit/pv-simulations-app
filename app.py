import streamlit as st
import json

from financial_utils import costo_totale
from load_utils import get_load, visualizza_consumo
from metrics_utils import calcola_risparmio_annuo, calcola_metrica_finanziaria
from simulazione_giornaliera import simula_giornata
from visualization_app import load_and_display_json


def run_simulation(generator_kwargs, storage_kwargs, load_kwargs, financial_kwargs):
    # Simulazione giornaliera
    #load = get_load(**load_kwargs)
    #visualizza_consumo(load, "Custom Load Model")
    #load_kwargs = {"hourly_values": load}

    simulation_result = simula_giornata(
        100, generator_kwargs, load_kwargs, storage_kwargs, verbose=1,
    )

    # Calcolo del risparmio in bolletta (annuale)
    E_totale = simulation_result["annual_average_values"]["energy_by_generator"]
    E_autoconsumata = (simulation_result["annual_average_values"]["energy_load_from_generator"] +
                       simulation_result["annual_average_values"]["energy_load_from_battery"])
    E_fabbisogno = simulation_result["annual_average_values"]["total_load_energy"]

    prezzo_energia_rete = financial_kwargs["valore_energia_acquistata"]
    prezzo_scambio = financial_kwargs["valore_energia_scambiata"]
    prezzo_vendita = financial_kwargs["valore_energia_venduta"]

    del financial_kwargs["valore_energia_acquistata"]
    del financial_kwargs["valore_energia_scambiata"]
    del financial_kwargs["valore_energia_venduta"]

    gain_analysis = calcola_risparmio_annuo(
        E_totale, E_autoconsumata, E_fabbisogno,
        prezzo_energia_rete, prezzo_scambio, prezzo_vendita
    )

    # Calcolo dei costi annuali
    financial_kwargs["potenza_moduli_kw"] = generator_kwargs["pv_nominal_power"]
    financial_kwargs["potenza_nominale_kw"] = generator_kwargs["pv_nominal_power"]
    financial_kwargs["capacita_batterie_kwh"] = storage_kwargs["C_batteria"]

    # Assicurati che i parametri passati a costo_totale corrispondano a quelli definiti nella funzione
    try:
        costi = costo_totale(
            **financial_kwargs
        )
    except TypeError as e:
        st.error(f"Errore nei parametri finanziari: {e}")
        return

    costi["input_parameters"] = financial_kwargs

    # Ripristina i valori originali
    financial_kwargs["valore_energia_acquistata"] = prezzo_energia_rete
    financial_kwargs["valore_energia_scambiata"] = prezzo_scambio
    financial_kwargs["valore_energia_venduta"] = prezzo_vendita

    # Calcolo delle metriche di investimento
    risparmio_annuo = gain_analysis["risparmio_annuo_netto"]
    anni_funzionamento = financial_kwargs["anni_di_funzionalita"]

    financial_analysis = calcola_metrica_finanziaria(costi, risparmio_annuo, anni_funzionamento)

    return {
        "financial_kwargs": financial_kwargs,
        "simulation_result": simulation_result,
        "gain_analysis": gain_analysis,
        "financial_analysis": financial_analysis,
        "costs": costi
    }

def main():
    st.title("Configurazione e Simulazione del Sistema Fotovoltaico")

    # Inizializzazione dello stato della sessione
    if 'generator_kwargs' not in st.session_state:
        st.session_state.generator_kwargs = {}
    if 'storage_kwargs' not in st.session_state:
        st.session_state.storage_kwargs = {}
    if 'load_kwargs' not in st.session_state:
        st.session_state.load_kwargs = {}
    if 'financial_kwargs' not in st.session_state:
        st.session_state.financial_kwargs = {}

    # Form per il Generatore
    with st.form(key='generator_form'):
        st.header("Parametri del Generatore")
        panels_efficiency = st.slider("Efficienza dei Pannelli (%)", 0, 100, 20) / 100
        altezza_pannello = st.number_input("Altezza del Pannello (m)", min_value=0.0, value=1.722)
        larghezza_pannello = st.number_input("Larghezza del Pannello (m)", min_value=0.0, value=1.11)
        tipo_disposizione = st.selectbox("Tipo di Disposizione", ["orizzontale", "verticale"])
        inclinazione = st.slider("Inclinazione (gradi)", 0, 90, 30)
        orientamento = st.slider("Orientamento (gradi)", 0, 360, 180)
        region = st.selectbox("Regione", ["nord", "centro", "sud"])
        pv_nominal_power = st.number_input("Potenza Nominale (kW)", min_value=0.0, value=6.0)
        hourly_power_unit_measure = "kWh" # st.selectbox("Unità di Misura della Potenza Oraria", ["kWh", "w"])

        generator_submit = st.form_submit_button("Submit Generatore", use_container_width=True)
        if generator_submit:
            st.session_state.generator_kwargs = {
                "panels_efficiency": panels_efficiency,
                "altezza_pannello": altezza_pannello,
                "larghezza_pannello": larghezza_pannello,
                "tipo_di_disposizione": tipo_disposizione,
                "inclinazione": inclinazione,
                "orientamento": orientamento,
                "region": region,
                "pv_nominal_power": pv_nominal_power,
                "hourly_power_unit_measure": hourly_power_unit_measure
            }
            st.success("Dati del Generatore salvati con successo!")

    # Form per il Carico
    with st.form(key='load_form'):
        st.header("Parametri del Carico")
        load_profiles = []
        num_profiles = st.number_input("Numero di Profili di Carico", min_value=1, max_value=100, value=1)
        for i in range(num_profiles):
            st.subheader(f"Profilo {i + 1}")
            consumo_totale_giornaliero = st.number_input(f"Consumo Totale Giornaliero (kWh) Profilo {i + 1}", min_value=0.0, value=15.0)
            modello = st.selectbox(f"Modello Profilo {i + 1}", ["campana", "uniforme"])
            picco = st.number_input(f"Picco Profilo {i + 1}", min_value=0.0, value=12.0)
            ampiezza = st.number_input(f"Ampiezza Profilo {i + 1}", min_value=0.0, value=4.0)
            load_profiles.append({
                "consumo_totale_giornaliero": consumo_totale_giornaliero,
                "modello": modello,
                "picco": picco,
                "ampiezza": ampiezza
            })

        load_submit = st.form_submit_button("Submit Carico", use_container_width=True)
        if load_submit:
            st.session_state.load_kwargs = {"load_profiles": load_profiles}
            load = get_load(**st.session_state.load_kwargs)
            st.session_state.load_kwargs = {"hourly_values": load}
            st.success("Dati del Carico salvati con successo!")

    # Form per lo Stoccaggio
    with st.form(key='storage_form'):
        st.header("Parametri di Stoccaggio")
        C_batteria = st.number_input("Capacità della Batteria (kWh)", min_value=0.0, value=10.0)
        eta_batteria = st.slider("Efficienza della Batteria (%)", 0, 100, 90) / 100
        P_max_carica = st.number_input("Potenza Massima di Carica (kW)", min_value=0.0, value=5.0)
        P_max_scarica = st.number_input("Potenza Massima di Scarica (kW)", min_value=0.0, value=5.0)

        storage_submit = st.form_submit_button("Submit Stoccaggio", use_container_width=True)
        if storage_submit:
            st.session_state.storage_kwargs = {
                "C_batteria": C_batteria,
                "eta_batteria": eta_batteria,
                "P_max_carica": P_max_carica,
                "P_max_scarica": P_max_scarica
            }
            st.success("Dati di Stoccaggio salvati con successo!")

    # Form per la Finanza
    with st.form(key='financial_form'):
        st.header("Parametri Finanziari")
        costo_modulo_per_kw = st.number_input("Costo del Modulo per kW (€)", min_value=0.0, value=250.0)
        costo_inverter_per_kw = st.number_input("Costo dell'Inverter per kW (€)", min_value=0.0, value=200.0)
        costo_struttura_per_kw = st.number_input("Costo della Struttura per kW (€)", min_value=0.0, value=200.0)
        costo_fisso_per_kw_installazione = st.number_input("Costo Fisso per kW di Installazione (€)", min_value=0.0, value=300.0)
        costo_fisso_progettazione = st.number_input("Costo Fisso di Progettazione (€)", min_value=0.0, value=500.0)
        costo_annuo_manutenzione_per_kw = st.number_input("Costo Annuo di Manutenzione per kW (€)", min_value=0.0, value=50.0)
        anni_di_funzionalita = st.number_input("Anni di Funzionalità", min_value=0, value=20)
        costo_per_kwh_batteria = st.number_input("Costo per kWh della Batteria (€)", min_value=0.0, value=500.0)
        costo_batteria = st.number_input("Costo Installazione per kWh della Batteria (€)", min_value=0.0, value=50.0)
        valore_energia_acquistata = st.number_input("Valore Energia Acquistata (€)", min_value=0.0, value=0.2)
        valore_energia_scambiata = st.number_input("Valore Energia Scambiata (€)", min_value=0.0, value=0.15)
        valore_energia_venduta = st.number_input("Valore Energia Venduta (€)", min_value=0.0, value=0.1)
        incentivi_installazione = st.number_input("Incentivi sull'Installazione (% Detrazione)", min_value=0.0, value=0.45)
        incentivi_beni_materiali = st.number_input("Incentivi sui Beni Materiali (% Detrazione)", min_value=0.0, value=0.45)
        incentivi_manutenzione = st.number_input("incentivi sulla Manutenzione (% Detrazione)", min_value=0.0, value=0.0)


        financial_submit = st.form_submit_button("Submit Finanza", use_container_width=True)
        if financial_submit:
            st.session_state.financial_kwargs = {
                "costo_modulo_per_kw": costo_modulo_per_kw,
                "costo_inverter_per_kw": costo_inverter_per_kw,
                "costo_struttura_per_kw": costo_struttura_per_kw,
                "costo_fisso_per_kw_installazione": costo_fisso_per_kw_installazione,
                "costo_fisso_progettazione": costo_fisso_progettazione,
                "costo_annuo_manutenzione_per_kw": costo_annuo_manutenzione_per_kw,
                "anni_di_funzionalita": anni_di_funzionalita,
                "costo_per_kwh_batteria": costo_per_kwh_batteria,
                "costo_fisso_per_kwh_batteria_installazione": costo_batteria,
                "valore_energia_acquistata": valore_energia_acquistata,
                "valore_energia_scambiata": valore_energia_scambiata,
                "valore_energia_venduta": valore_energia_venduta,
                'incentivi_installazione': incentivi_installazione,
                'incentivi_beni_materiali': incentivi_beni_materiali,
                'incentivi_manutenzione': incentivi_manutenzione,
            }
            st.success("Dati Finanziari salvati con successo!")

    # Esecuzione della simulazione
    if st.button("Esegui Simulazione", use_container_width=True):
        if all(k in st.session_state for k in ('generator_kwargs', 'storage_kwargs', 'load_kwargs', 'financial_kwargs')):
            results = run_simulation(
                st.session_state.generator_kwargs,
                st.session_state.storage_kwargs,
                st.session_state.load_kwargs,
                st.session_state.financial_kwargs
            )
            if results:
                st.write("Risultati della Simulazione:")
                #st.json(results)
                print(json.dumps(results, indent=2))
                load_and_display_json(results)
        else:
            st.error("Completa tutti i moduli prima di eseguire la simulazione.")

if __name__ == "__main__":
    main()

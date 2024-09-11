import streamlit as st
import pandas as pd
import json

# Mappatura delle etichette
label_mapping = {
    "generator_kwargs": {
        "panels_efficiency": "Efficienza Pannelli (%)",
        "altezza_pannello": "Altezza Pannello (m)",
        "larghezza_pannello": "Larghezza Pannello (m)",
        "tipo_di_disposizione": "Disposizione Pannelli",
        "inclinazione": "Inclinazione (°)",
        "orientamento": "Orientamento (°)",
        "region": "Regione",
        "pv_nominal_power": "Potenza Nominale (kW)",
        "hourly_power_unit_measure": "Unità di Misura Energia Oraria",
        "panels_area": "Area Totale Pannelli (m²)"
    },
    "storage_kwargs": {
        "C_batteria": "Capacità Batteria (kWh)",
        "eta_batteria": "Efficienza Batteria (%)",
        "P_max_carica": "Potenza Massima Carica (kW)",
        "P_max_scarica": "Potenza Massima Scarica (kW)"
    },
    "financial_kwargs": {
        "costo_modulo_per_kw": "Costo per kW del modulo fotovoltaico",
        "costo_inverter_per_kw": "Costo per kW dell'inverter",
        "costo_struttura_per_kw": "Costo per kW della struttura di supporto",
        "costo_fisso_per_kw_installazione": "Costo fisso per kW per l'installazione",
        "costo_fisso_progettazione": "Costo fisso per la progettazione",
        "costo_annuo_manutenzione_per_kw": "Costo annuo per manutenzione per kW",
        "anni_di_funzionalita": "Durata utile dell'impianto in anni",
        "costo_per_kwh_batteria": "Costo per kWh della batteria",
        "costo_fisso_per_kwh_batteria_installazione": "Costo fisso per kWh per l'installazione della batteria",
        "potenza_moduli_kw": "Potenza nominale dei moduli fotovoltaici in kW",
        "potenza_nominale_kw": "Potenza nominale dell'impianto in kW",
        "capacita_batterie_kwh": "Capacità delle batterie in kWh",
        "valore_energia_acquistata": "Costo dell'energia acquistata per kWh",
        "valore_energia_scambiata": "Valore dell'energia scambiata per kWh",
        "valore_energia_venduta": "Valore dell'energia venduta per kWh",
        'incentivi_installazione': "incentivi installazione (% detrazione)",  # 20% di incentivo
        'incentivi_beni_materiali': "incentivi beni materiali (% detrazione)",  # 15% di incentivo sui beni materiali
        'incentivi_manutenzione': "incentivimanutenzione  (% detrazione)",  # 10% di incentivo sulla manutenzione
    },
    "hourly_values": {
        "energy_by_generator": "Energia Generata (kWh)",
        "total_load_energy": "Consumo Totale (kWh)",
        "energy_load_from_generator": "Energia Usata dal Generatore (kWh)",
        "energy_load_from_battery": "Energia Usata dalla Batteria (kWh)",
        "energy_to_grid": "Energia Immessa in Rete (kWh)",
        "energy_to_battery": "Energia Immagazzinata in Batteria (kWh)",
        "energy_in_battery": "Energia in Batteria (kWh)",
        "energy_load_from_grid": "Energia Prelevata dalla Rete (kWh)"
    },
    "daily_average_values": {
        "energy_by_generator": "Energia Media Giornaliera Generata (kWh)",
        "total_load_energy": "Consumo Medio Giornaliero (kWh)",
        "energy_load_from_generator": "Energia Media Giornaliera Usata dal Generatore",
        "energy_load_from_battery": "Energia Media Giornaliera Prelevata dalla Batteria",
        "energy_to_grid": "Energia Media Giornaliera Immessa in Rete",
        "energy_to_battery": "Energia Media Giornaliera Immagazzinata in Batteria",
        "hourly_energy_in_battery": "Energia Residua in Batteria",
        "energy_load_from_grid": "Energia Media Giornaliera Prelevata dalla Rete",
        "autoconsumo %(energia consumata)": "Autoconsumo (% sull'Energia Consumata)",
        "autoconsumo %(energia prodotta)": "Autoconsumo (% sull'Energia Prodotta)"
    },
    "monthly_average_values": {
        "energy_by_generator": "Energia Media Mensile Generata (kWh)",
        "total_load_energy": "Consumo Medio Mensile (kWh)",
        "energy_load_from_generator": "Energia Media Mensile Usata dal Generatore",
        "energy_load_from_battery": "Energia Media Mensile Prelevata dalla Batteria",
        "energy_to_grid": "Energia Media Mensile Immessa in Rete",
        "energy_to_battery": "Energia Media Mensile Immagazzinata in Batteria",
        "energy_load_from_grid": "Energia Media Mensile Prelevata dalla Rete"
    },
    "annual_average_values": {
        "energy_by_generator": "Energia Media Annuale Generata (kWh)",
        "total_load_energy": "Consumo Medio Annuale (kWh)",
        "energy_load_from_generator": "Energia Media Annuale Usata dal Generatore",
        "energy_load_from_battery": "Energia Media Annuale Prelevata dalla Batteria",
        "energy_to_grid": "Energia Media Annuale Immessa in Rete",
        "energy_to_battery": "Energia Media Annuale Immagazzinata in Batteria",
        "energy_load_from_grid": "Energia Media Annuale Prelevata dalla Rete"
    },
    "gain_analysis": {
        "energia_totale_prod": "Energia Totale Prodotta (kWh)",
        "energia_autoconsumata": "Energia Autoconsumata (kWh)",
        "energia_immessa_rete": "Energia Immessa in Rete (kWh)",
        "energia_assorbita_rete": "Energia Assorbita dalla Rete (kWh)",
        "energia_scambiata": "Energia Scambiata (kWh)",
        "energia_venduta": "Energia Venduta (kWh)",
        "costo_senza_fv": "Costo Senza Fotovoltaico (€)",
        "costo_con_fv": "Costo con Fotovoltaico (€)",
        "risparmio_annuo_netto": "Risparmio Netto Annuale (€)",
        "valore_totale_scambio": "Valore Totale dello Scambio (€)",
        "valore_totale_vendita": "Valore Totale della Vendita (€)",
        "valore_totale_acquisto": "Valore Totale dell'Acquisto (€)",
        "prezzo_acqusito_energia": "Prezzo Energia Acquistata (€ per kWh)",
        "prezzo_scambio_energia": "Prezzo Energia Scambiata (€ per kWh)",
        "prezzo_vendita_energia": "Prezzo Energia Venduta (€ per kWh)"
    },
    "costs": {
        "costo_totale": "Costo Totale (€)",
        "costo_moduli": "Costo Moduli (€)",
        "costo_inverter": "Costo Inverter (€)",
        "costo_struttura": "Costo Struttura (€)",
        "costo_installazione": "Costo Installazione (€)",
        "costo_progettazione": "Costo Progettazione (€)",
        "costo_manutenzione": "Costo Manutenzione (€)",
        "costo_monitoraggio": "Costo Monitoraggio (€)",
        "costo_batterie": "Costo Batterie (€)",
        "costo_installazione_batterie": "Costo Installazione Batterie (€)",
        "altri_costi": "Altri Costi (€)"
    },
    #"financial_analysis": {
    #    "roi": "Ritorno dell'Investimento (%)",
    #    "payback_period": "Periodo di Rientro (anni)"
    #}
}


# Funzione per calcolare i guadagni per metro quadrato
def calculate_metrics_per_square_meter(generator_kwargs, costs, gain_analysis):
    area = generator_kwargs.get("panels_area", 0)  # Area totale dei pannelli

    if area <= 0:
        return pd.DataFrame()

    # Calcolo dei costi per metro quadrato
    costo_totale_per_mq = costs.get("costo_totale", 0) / area

    # Calcolo dei guadagni lordi e netti per metro quadrato
    #guadagno_lordo_per_mq = gain_analysis.get("energia_totale_prod", 0) / area
    guadagno_lordo_per_mq = gain_analysis.get("risparmio_annuo_netto", 0) / area

    # Calcolo del risparmio per metro quadrato
    risparmio_per_mq = (gain_analysis.get("risparmio_annuo_netto", 0) / area) if area > 0 else 0

    # Crea un DataFrame con i risultati
    df_metrics = pd.DataFrame({
        "Metri Quadrati": [area],
        "Costo Totale / m² (€)": [round(costo_totale_per_mq/12,2)],
        #"Guadagno Lordo / m² (€)": [guadagno_lordo_per_mq],
        "Guadagno Lordo / m² (€)": [guadagno_lordo_per_mq],
        "Guadagno Netto / m² (€)": [round(guadagno_lordo_per_mq - costo_totale_per_mq/12, 2)],
    })

    return df_metrics


# Funzione per rinominare le colonne usando la mappatura
def rename_columns(df, key):
    if key in label_mapping:
        df = df.rename(columns=label_mapping[key])
    return df

# Funzione per caricare e visualizzare i dati JSON
# Funzione per filtrare e rinominare le colonne dei parametri finanziari
def filter_and_rename_financial_columns(df):
    # Lista delle colonne da mantenere
    columns_to_keep = [
        "costo_modulo_per_kw",
        "costo_inverter_per_kw",
        "costo_struttura_per_kw",
        "costo_fisso_per_kw_installazione",
        "costo_fisso_progettazione",
        "costo_annuo_manutenzione_per_kw",
        "anni_di_funzionalita",
        "costo_per_kwh_batteria",
        "costo_fisso_per_kwh_batteria_installazione",
    ]

    # Filtrare solo le colonne specificate
    df_filtered = df[columns_to_keep]
    return rename_columns(df_filtered, "financial_kwargs")


# Modifica nella visualizzazione dei Parametri di Costo
def load_and_display_json(data):
    if not isinstance(data, dict):
        data_dict = json.loads(data)
    else:
        data_dict = data

    st.markdown("---")
    st.header("Risultati della Simulazione")

    # 1. Dati Generali
    st.subheader("1. Dati Generali")
    generator_kwargs = data_dict['simulation_result']['generator_kwargs']
    storage_kwargs = data_dict['simulation_result']['storage_kwargs']
    st.write("Dati Generali Generatore", rename_columns(pd.DataFrame([generator_kwargs]), "generator_kwargs"))
    st.write("Dati Generali Stoccaggio", rename_columns(pd.DataFrame([storage_kwargs]), "storage_kwargs"))

    # 2. Valori Orari
    st.subheader("2. Valori Orari")
    hourly_values = data_dict['simulation_result']['hourly_values']
    df_hourly = rename_columns(pd.DataFrame(hourly_values).drop(columns='h'), "hourly_values")
    st.write(df_hourly)

    # 3. Valori Medi (Media Giornaliera, Mensile e Annuale)
    st.subheader("3. Valori Medi")

    st.write("Media Giornaliera")
    daily_avg = data_dict['simulation_result']['daily_average_values']
    st.write(rename_columns(pd.DataFrame([daily_avg]), "daily_average_values"))

    st.write("Media Mensile")
    monthly_avg = data_dict['simulation_result']['monthly_average_values']
    st.write(rename_columns(pd.DataFrame([monthly_avg]), "monthly_average_values"))

    st.write("Media Annuale")
    annual_avg = data_dict['simulation_result']['annual_average_values']
    st.write(rename_columns(pd.DataFrame([annual_avg]), "annual_average_values"))

    # 4. Analisi dei Guadagni
    st.subheader("4. Analisi dei Guadagni")
    st.write(rename_columns(pd.DataFrame([data_dict['gain_analysis']]), "gain_analysis"))

    # 5. Parametri Finanziari
    st.subheader("5. Parametri di Costo")
    financial_kwargs = data_dict['financial_kwargs']
    st.write("Parametri Finanziari", filter_and_rename_financial_columns(pd.DataFrame([financial_kwargs])))

    # 6. Costi
    st.subheader("6. Analisi Costo")
    st.write(rename_columns(pd.DataFrame([data_dict['costs']]), "costs"))

    # 7. Analisi Finanziaria
    st.subheader("7. Analisi dell'Investimento")
    st.write(rename_columns(pd.DataFrame([data_dict['financial_analysis']]), "financial_analysis"))

    # 8. Guadagno per Metro Quadrato
    st.subheader("8. Guadagno per Metro Quadrato")

    metrics_df = calculate_metrics_per_square_meter(
        generator_kwargs, data_dict['costs'], data_dict['gain_analysis']
    )

    st.write("Metriche Annuali")
    st.write(metrics_df)  # Mostra la tabella con i risultati per metro quadrato

# Main app
def main():
    st.title("Visualizzazione Dati della Simulazione")

    # Inserisci il JSON come stringa
    json_data = st.text_area("Inserisci il JSON della simulazione", height=300)



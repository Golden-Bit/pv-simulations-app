import math
from typing import Any

global average_annual_pv_prod_per_kw
average_annual_pv_prod_per_kw = {"nord": 1050, "centro": 1250, "sud": 1450}


def get_prod_data(
        panels_efficiency: float = None,
        altezza_pannello: float = None,
        larghezza_pannello: float = None,
        tipo_di_disposizione: str = None,
        panels_area: float = None,
        inclinazione: float = 30.0,
        orientamento: float = 180.0,
        region: str = "sud",
        pv_nominal_power=1,
        hourly_power_unit_measure: str = "w",
):

    for key, value in average_annual_pv_prod_per_kw.items():
        average_annual_pv_prod_per_kw[key] = calcola_produzione_annuale_fissata(value, inclinazione,orientamento)

    average_daily_pv_prod = dict()
    for _region in average_annual_pv_prod_per_kw:
        average_daily_pv_prod[_region] = float(average_annual_pv_prod_per_kw[_region] * pv_nominal_power) / 365.0

    average_relative_hourly_pv_prod = {
        '0': 0.0,
        '1': 0.0,
        '2': 0.0,
        '3': 0.0,
        '4': 0.0,
        '5': 0.0,
        '6': 0.0,
        '7': 0.009900990099009901,
        '8': 0.019801980198019802,
        '9': 0.0594059405940594,
        '10': 0.0891089108910891,
        '11': 0.1188118811881188,
        '12': 0.1485148514851485,
        '13': 0.1485148514851485,
        '14': 0.13861386138613863,
        '15': 0.1188118811881188,
        '16': 0.07920792079207921,
        '17': 0.039603960396039604,
        '18': 0.019801980198019802,
        '19': 0.009900990099009901,
        '20': 0.0,
        '21': 0.0,
        '22': 0.0,
        '23': 0.0
    }

    average_absolute_hourly_pv_prod = dict()

    for key, value in average_relative_hourly_pv_prod.items():

        average_absolute_hourly_pv_prod[key] = value * average_daily_pv_prod[region]

    sum_over_hourly_absolute_prod = sum(list(average_absolute_hourly_pv_prod.values()))
    average_annual_pv_prod = sum_over_hourly_absolute_prod * 365

    for key in list(average_relative_hourly_pv_prod.keys()):

        if hourly_power_unit_measure == "w":
            average_absolute_hourly_pv_prod[key] *= 1000

    return {
        "hourly_pv_prod": list(average_absolute_hourly_pv_prod.values()),
        "average_daily_pv_prod": average_daily_pv_prod[region],
        "average_annual_pv_prod": average_annual_pv_prod,
    }


def calcola_produzione_annuale_fissata(produzione_riferimento, inclinazione, orientamento):
    # In questo esempio semplice, ipotizziamo che la variazione di produzione
    # sia funzione lineare dell'inclinazione e dell'orientamento.

    # L'orientamento, in questo contesto, si riferisce alla direzione cardinale verso cui sono rivolti i moduli
    # fotovoltaici. È misurato in gradi rispetto al nord geografico, dove:
    #
    # 0° indica che il modulo è rivolto a nord.
    # 90° indica che il modulo è rivolto a est.
    # 180° indica che il modulo è rivolto a sud.
    # 270° indica che il modulo è rivolto a ovest.
    #
    # L'orientamento ottimale per la massima produzione di energia solare in un dato emisfero è solitamente verso
    # l'equatore (ad esempio, a sud nell'emisfero nord).
    #
    # Di seguito è riportato uno script Python aggiornato che utilizza l'orientamento dei moduli fotovoltaici insieme
    # all'inclinazione per calcolare la variazione percentuale della produzione energetica annuale in diverse regioni d'Italia.

    # Fattore di correzione per l'inclinazione (ipotizziamo ±0.5% per grado di deviazione dall'ottimale)
    correzione_inclinazione = 0.005 * abs(inclinazione - 30)

    # Fattore di correzione per l'orientamento (ipotizziamo ±0.2% per grado di deviazione dall'ottimale)
    correzione_orientamento = 0.002 * abs(orientamento - 180)

    # Calcolo della produzione annuale con le nuove inclinazioni e orientamenti
    produzione_annuale = produzione_riferimento * (1 - correzione_inclinazione - correzione_orientamento)

    return produzione_annuale


def calcola_superficie_minima(potenza_nominale_kw, efficienza, inclinazione, altezza_modulo, larghezza_modulo,
                              orientamento='orizzontale'):
    """
    Calcola la superficie minima necessaria per i moduli fotovoltaici considerando l'inclinazione e l'orientamento.

    :param potenza_nominale_kw: Potenza nominale totale del sistema (kW).
    :param efficienza: Efficienza dei moduli fotovoltaici.
    :param inclinazione: Inclinazione dei moduli rispetto al suolo (gradi).
    :param altezza_modulo: Altezza del modulo (m).
    :param larghezza_modulo: Larghezza del modulo (m).
    :param orientamento: Orientamento del modulo, 'lunghezza' o 'altezza'.
    :return: Superficie minima necessaria (m^2).
    """

    # Calcola l'area del modulo
    area_modulo = altezza_modulo * larghezza_modulo

    # Effetto inclinazione sull'area del modulo
    inclinazione_rad = math.radians(inclinazione)
    area_effettiva = area_modulo / math.cos(inclinazione_rad)

    # Calcola la superficie totale necessaria per ottenere la potenza nominale
    superficie_necessaria = potenza_nominale_kw / efficienza

    # Calcola la superficie minima per evitare ombre
    # Utilizza l'orientamento per decidere quale dimensione è la lunghezza
    if orientamento == 'verticale':
        spacing = altezza_modulo * 0.1  # Spazio necessario per evitare ombre
        larghezza_totale = larghezza_modulo + spacing
        altezza_totale = altezza_modulo
    elif orientamento == 'orizzontale':
        spacing = larghezza_modulo * 0.1  # Spazio necessario per evitare ombre
        altezza_totale = altezza_modulo + spacing
        larghezza_totale = larghezza_modulo

    # Superficie necessaria per evitare ombre
    superficie_minima_ombra = (larghezza_totale * altezza_totale) / efficienza

    return round(superficie_necessaria, 2)


if __name__ == "__main__":

    kwargs = {
        "inclinazione": 30,
        "orientamento": 180,
        "region": "sud", # ["nord", "centro", "sud"]"
        "pv_nominal_power": 1,
        "hourly_power_unit_measure": "kWh"} # "w"

    #prod_data = get_prod_data(region="sud",
    #                          pv_nominal_power=3)

    prod_data = get_prod_data(**kwargs)

    average_absolute_hourly_pv_prod = prod_data["hourly_pv_prod"]
    average_daily_pv_prod = prod_data["average_daily_pv_prod"]
    average_annual_pv_prod = prod_data["average_annual_pv_prod"]

    print(average_absolute_hourly_pv_prod)
    print(average_daily_pv_prod)
    print(average_annual_pv_prod)

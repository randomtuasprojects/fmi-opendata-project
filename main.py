# Project is based largely on fmiopendata by Panu Lahtinnen https://github.com/pnuu/fmiopendata/
import datetime as dt
import requests
from fmiopendata.wfs import download_stored_query

# Määritellään tunnin mittainen aika
end_time = dt.datetime.utcnow()
start_time = end_time - dt.timedelta(hours=1)

# Muunnetaan ajat isoformat -muotoon
start_time = start_time.isoformat(timespec="seconds") + "Z"
end_time = end_time.isoformat(timespec="seconds") + "Z"

# luodaan fmiopednata-olio joka saa viimeisen tunnin tiedot Ilmatieteenlaitokselta dictionary-tyylisenä tietueena
ennuste = download_stored_query("fmi::forecast::hirlam::surface::obsstations::multipointcoverage", args=["starttime=" + start_time, "endtime=" + end_time])

# latest_tstep = viimeisin "aika"
latest_tstep = max(ennuste.data.keys())

valinta1 = input("Haluatko luettelon havaintoasemista? (k/e)")
if valinta1=="k":
    for key, value in sorted(ennuste.data[latest_tstep].items()): # tämä tulostaa kaikki havaintoasemat aakkosjärjestyksessä
        print(key)
    print()
    loc = input("Havaintoaseman nimi: ")
if valinta1=="e":
    loc=input("Havaintoaseman nimi: ") # havaintoaseman nimen on täsmättävä tunnettuneihin havaintoasemiin (luettelosta)

print("Havaintoaseman", loc, "sijainti on:") # Tulostetaan Ilmatieteenlaitoksen ilmoittamat koordinantit havaintoasemalle
print(ennuste.location_metadata[loc]['latitude'])
print(ennuste.location_metadata[loc]['longitude'])
print()
print("Havaintoaseman FMISID:")
print(ennuste.location_metadata[loc]['fmisid']) # Tulostetaan havaintoaseman tunniste
print()

print("Havaintoaseman", loc,  "viimeisimmät havainnot:")

# Tästä eteenpäin tulostetaan ennuste-olion dictionary -tyylisestä tietueesta haluttuja arvoja
print("Lämpötila: ", ennuste.data[latest_tstep][loc]["Air temperature"]["value"], "astetta") # Tulostetaan avaimen Air Temperature arvo
print("Ilmanpaine: ", ennuste.data[latest_tstep][loc]["Air pressure"]["value"], "hPa")
print("Pilvisyys: ", ennuste.data[latest_tstep][loc]["Total cloud cover"]["value"], "%")
print("Kuluneen tunnin sademäärä: ", ennuste.data[latest_tstep][loc]["Precipitation amount 1 hour"]["value"], "mm/h")
print("Tuulen nopeus: ", ennuste.data[latest_tstep][loc]["Wind speed"]["value"], "m/s")
print("Tuulen suunta: ", ennuste.data[latest_tstep][loc]["Wind direction"]["value"], "astetta")

import json
import requests as req
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


def analyse_country(covid_pd, country_name, flg_write = True):

    filtered_rows = covid_pd[covid_pd['countriesAndTerritories'].str.contains(country_name)]
    
    t = filtered_rows["deltaTime_since_start_of_recording"].to_numpy()
    t_days = t/(60*60*24)
    
    # get incidence
    incidence_s = filtered_rows["14d-incidence"].to_numpy()
    incidence_l = []
    for i in range(len(incidence_s)):
        incidence_l.append(float(incidence_s[i]))
    incidence = np.asarray(incidence_l)

    # get death rate
    death_s = filtered_rows["deaths_weekly"].to_numpy()
    death_l = []
    for i in range(len(death_s)):
        death_l.append(float(death_s[i]))
    death = np.asarray(death_l)
    
    
    # find max and min derivatives of incidence
    der_max = 0
    der_min = 0
    for i in range(len(incidence)-1):
        num = (incidence[i+1] - incidence[i])
        den = t_days[i+1]-t_days[i]

        if den != 0:
            der_incidence = (num/den)
            if der_incidence > der_max:
                der_max = der_incidence
    
            if der_incidence < der_min:
                der_min = der_incidence
    
    mi = np.min(t_days)
    ma = np.max(t_days)
    
    dimday = np.int32(ma-mi)+1
    t_allday = np.linspace(mi, ma, dimday)
    
    incidence_allday = np.interp(t_allday, t_days, incidence)
    death_allday = np.interp(t_allday, t_days, death)
    kernel = np.ones(90)/90
    kernel_death = np.ones(14)/14
    incidence_smoothed = np.convolve(incidence_allday, kernel, 'same')
    death_smoothed = np.convolve(death_allday, kernel_death, 'same')

    incidence_fluctuation = np.std(incidence_allday)

    
    if flg_write == True:
        print("The most drastic increase of the incidence in " + str(country_name) + " is: ")
        print(str("%.1f" % der_max) + " new cases per 100000 people per day")
        print("The most drastic decrease of the incidence in " + str(country_name) + " is: ")
        print(str("%.1f" % der_min) + " new cases per 100000 people per day")



    
    return der_min, der_max, t_days, incidence, t_allday, incidence_smoothed, death_smoothed, incidence_fluctuation


def analyse_continent(covid_pd, name_countries, flg_write_countries = True, flg_write_der = True, flg_write_inc = True):
    der_min = []
    der_max = []
    incidence_fluctuation = []
    for name in name_countries:
        der_mini, der_maxi, t_days, incidence, t_allday, incidence_smoothed, death_smoothed, incidence_fluctuationi = analyse_country(covid_pd, name, flg_write_countries)
        der_min.append(der_mini)
        der_max.append(der_maxi)
        incidence_fluctuation.append(incidence_fluctuationi)
    
    incidence_fluctuation = np.asarray(incidence_fluctuation)
    der_min = np.asarray(der_min)
    der_max = np.asarray(der_max)

    
    print()
    
    if flg_write_der == True:

        der_minimum = np.amin(der_min)
        ind = np.where(der_min == der_minimum)
        country_min = name_countries[ind[0][0]]
        print("The most drastic decrease of the incidence in " + str(country_min) + " is: ")
        print(str("%.1f" % der_minimum) + " new cases per 100000 people per day")
        
        der_maximum = np.amax(der_max)
        ind = np.where(der_max == der_maximum)
        country_max = name_countries[ind[0][0]]
        print("The most drastic decrease of the incidence in " + str(country_max) + " is: ")
        print(str("%.1f" % der_maximum) + " new cases per 100000 people per day")

    if flg_write_inc == True:
        der_maximum = np.amax(incidence_fluctuation)
        ind = np.where(incidence_fluctuation == der_maximum)
        country_max = name_countries[ind[0][0]]
        print("The highest fluctuation in 14d incidence is in " + str(country_max) + " and is: ")
        print(str("%.1f" % der_maximum) + " new cases per 100000 people")
        

        der_maximum = np.amin(incidence_fluctuation)
        ind = np.where(incidence_fluctuation == der_maximum)
        country_max = name_countries[ind[0][0]]
        print("The lowest fluctuation in 14d incidence is in " + str(country_max) + " and is: ")
        print(str("%.1f" % der_maximum) + " new cases per 100000 people")

    return  der_min, der_max, incidence_fluctuation



covid_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"

resp = req.get(covid_url)
covid_json = json.loads(resp.text)
covid_pd = pd.DataFrame(covid_json["records"])

covid_pd = covid_pd.replace(r'^\s*$', np.nan, regex=True)
covid_pd = covid_pd.dropna(axis = 0)

old_name = "notification_rate_per_100000_population_14-days"
new_name = "14d-incidence"
covid_pd.rename(columns={(old_name): (new_name)}, inplace=True)

old_name = "dateRep"
new_name = "date"
covid_pd.rename(columns={(old_name): (new_name)}, inplace=True)

# convert to seconds
dateRep = covid_pd["date"].to_list()

dateRep_sec = []
for n in range(len(dateRep)):
    dateRep_sec.append(datetime.strptime(dateRep[n], '%d/%m/%Y').timestamp())

dateRep_sec = np.asarray(dateRep_sec)
min = dateRep_sec.min()

dateRep_sec = dateRep_sec - min
covid_pd["deltaTime_since_start_of_recording"] = dateRep_sec

covid_pd = covid_pd.sort_values("deltaTime_since_start_of_recording")
print(covid_pd)
print(covid_pd.columns)


covid_pd = covid_pd.replace('Falkland_Islands_(Malvinas)', "Falkland_Islands_Malvinas")
covid_pd = covid_pd.replace('Micronesia_(Federated_States_of)', "Micronesia")

# only European countries
covid_pd2 =  covid_pd[covid_pd['continentExp']=="Europe"]
countries = covid_pd2["countriesAndTerritories"]
freq_countries = countries.value_counts()
name_countries = freq_countries.index.to_list()
print()
print("-----------------")

# create list of death rates
country_list = ["Italy", "Germany", "Sweden", "Greece"]
t_allday2 = []
death_smoothed2 = []
for n in range(len(country_list)):
    der_min, der_max, t_days, incidence, t_allday, incidence_smoothed, death_smoothed, incidence_fluctuation = analyse_country(covid_pd, country_list[n], False)
    t_allday2.append(t_allday)
    death_smoothed2.append(death_smoothed)

min_t_allday2 = np.min(np.min(t_allday2))
max_t_allday = np.max(np.max(t_allday2))

t_allday_total = np.linspace(min_t_allday2, max_t_allday, np.int32(max_t_allday-min_t_allday2 +1))

for n in range(len(country_list)):
    death_smoothed2[n] = np.interp(t_allday_total, t_allday2[n], death_smoothed2[n])

# create plot for all countries in country_list
df = pd.DataFrame(list(zip(t_allday_total)), 
               columns =["time (days)"])
for n in range(len(country_list)):
    df[country_list[n]] = death_smoothed2[n]
fig = px.line(df, x='time (days)', y=country_list, title="Death rate")
fig.write_html((str("figure_") + str("fig_index") + ".html"), auto_open=True)


df = px.data.wind()
df = pd.DataFrame(list(zip(t_allday, death_smoothed)), 
               columns =["t_allday", "death_smoothed"])
fig = px.scatter_polar(df, r="death_smoothed", theta="t_allday")
fig.write_html((str("figure_") + str("fig_index2") + ".html"), auto_open=True)


continents = covid_pd['continentExp']
freq_continents = continents.value_counts()
name_continents = freq_continents.index.to_list()

print(name_continents)
for n in range(len(name_continents)):
    covid_pd2 =  covid_pd[covid_pd['continentExp']==name_continents[n]]
    countries = covid_pd2["countriesAndTerritories"]
    freq_countries = countries.value_counts()
    name_countries = freq_countries.index.to_list()
    print()
    print("-----------------")
    print("In the continent " + str(name_continents[n])+" :")
    analyse_continent(covid_pd2, name_countries, False, True, False)



print()
print("-----------------")
countries = covid_pd["countriesAndTerritories"]
freq_countries = countries.value_counts()
name_countries = freq_countries.index.to_list()
analyse_continent(covid_pd, name_countries, False, False, True)



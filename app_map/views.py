from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
import folium
from .models import placa

import mygeotab
import pandas as pd
from datetime import datetime, timedelta

def Locali_placa(Placa):
    # api = mygeotab.API(username='gerencia@rodaryrodar.com.co', password='Rodaryrodar2021*', database='rodaryrodar')
    api = mygeotab.API(username='telematicarodar@gmail.com', password='Rodaryrodar2021*', database='rodaryrodar')
    api.authenticate()
    Fecha_Leida = datetime.now() + timedelta(hours=5)
    ano = Fecha_Leida.year
    mes = Fecha_Leida.month
    dia = str(Fecha_Leida.day)
    if len(dia) == 1:
        dia = "0" + dia
    hora = str(Fecha_Leida.hour)
    if len(hora) == 1:
        hora = "0" + hora
    minuto = str(Fecha_Leida.minute)
    if len(minuto) == 1:
        minuto = "0" + minuto
    segundo = str(Fecha_Leida.second)
    if len(segundo) == 1:
        segundo = "0" + segundo
    savetime = str(ano) + '-' + str(mes) + '-' + str(dia) + 'T' + str(hora) + ':' + str(minuto) + ':' + str(
        segundo) + ".000Z"

    # devices = api.call('Get', typeName = 'Device')
    # devices = api.call('Get', typeName = 'Device', search={"licensePlate":"DFRL43"})
    # Id_Buscado=devices[0]['id']
    devices = api.call('Get', typeName='Device')
    logs = api.get("LogRecord", search={"fromDate": savetime})
    # logs = api.get("LogRecord", search = {"fromDate": savetime,"deviceSearch": {"id":'bA'}})
    longitud = []
    latitud = []
    Fecha = []
    ID = []
    hora = []
    ##########INICIA MODIFICACIONES#########################################
    placas = []
    Id_Dive = []
    for i in range(len(devices)):
        placas.append(devices[i]['licensePlate'])
        Id_Dive.append(devices[i]['id'])
    for i in range(len(logs)):
        longitud.append(logs[i]['longitude'])
        latitud.append(logs[i]['latitude'])
        Fecha.append((logs[i]['dateTime'] - timedelta(hours=5)).date())
        hora.append((logs[i]['dateTime'] - timedelta(hours=5)).time().strftime('%H:%M:%S'))
        ID.append(logs[i]['device']['id'])
    df_placa = pd.DataFrame({'ID': Id_Dive, 'Placa': placas})
    df = pd.DataFrame({'ID': ID, 'longitud': longitud,
                       'latitud': latitud,
                       'Fecha': Fecha, 'Hora': hora
                       })
    # Se realiza joiner de las dos tablas
    df_cd = pd.merge(df, df_placa, how='inner', on='ID')
    df_cd = df_cd.drop(['ID'], axis=1)
    # Se coloca Df como se espera guardar
    df = df_cd.rename(columns={'Placa': 'ID'})

    df['latitud'][1]
    df['longitud'][1]
    df['ID'][1]
    # df['Tiempo'] = df['Tiempo'].dt.tz_localize(None)
    ##############FIN MODIFICACIONES#######################################

    pos = (list(df["ID"]).index(Placa))

    longitud = df[pos:pos + 1]['longitud']
    latitud = df[pos:pos + 1]['latitud']

    return longitud, latitud




def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_placas=placa.objects.all().count()
    if(len(request.user.username)> 2):
            usuario= request.user.username#User.objects.get(id=1).username
            grupo=request.user.groups.values_list('name', flat=True).first()
            # lat = num1#6.210605
            # lng = -75.596756
            lng, lat = Locali_placa(grupo)

            cordenadas = str(lat) + "," + str(lng)
            m = folium.Map(location=[lat, lng], zoom_start='18', control_scale=False, zoom_control=False)
            folium.Marker([lat, lng], icon=folium.Icon(icon='car', prefix='fa'),
                          popup=cordenadas).add_to(m)
            # Get HTML Representation of Map Object
            m = m._repr_html_()
    else:
        usuario = 'Unknown'
        grupo = 'Unknown'
        lng=0
        lat=0

        cordenadas = str(lat) + "," + str(lng)
        m = folium.Map(location=[lat, lng], zoom_start='18', control_scale=False, zoom_control=False)
        folium.Marker([lat, lng], icon=folium.Icon(icon='car', prefix='fa'),
                      popup=cordenadas).add_to(m)
        # Get HTML Representation of Map Object
        m = m._repr_html_()
    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_placas': num_placas,'usuario':usuario,'grupo':grupo,'m': m},
    )


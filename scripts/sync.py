import MySQLdb
import requests
import grequests
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='log.txt', level=logging.DEBUG)


def dlog(v): logging.debug(v)


def ilog(v): logging.info(v)


def wlog(v): logging.warning(v)


def elog(v): logging.error(v)


HOUR_TO_ID = {'01:15': 7, '02:00': 10, '20:45': 85, '09:00': 38, '06:30': 28, '04:15': 19, '18:15': 75, '11:30': 48, '02:30': 12, '11:15': 47, '23:15': 95, '12:45': 53, '13:15': 55, '17:00': 70, '03:15': 15, '09:45': 41, '12:30': 52, '09:15': 39, '01:30': 8, '10:15': 43, '19:15': 79, '02:15': 11, '19:45': 81, '04:45': 21, '01:00': 6, '20:30': 84, '12:15': 51, '10:45': 45, '03:30': 16, '05:30': 24, '20:00': 82, '14:15': 59, '15:30': 64, '14:30': 60, '18:00': 74, '10:00': 42, '16:30': 68, '07:30': 32, '19:00': 78, '22:45': 93, '22:15': 91, '19:30': 80, '14:45': 61, '00:30': 4, '08:45': 37, '10:30': 44, '07:45': 33, '06:45': 29, '23:30': 96, '03:00': 14, '22:00': 90, '21:15': 87, '05:15': 23, '21:00': 86, '06:00': 26, '04:00': 18, '14:00': 58, '00:45': 5, '18:45': 77, '15:00': 62, '06:15': 27, '00:00': 2, '23:00': 94, '17:30': 72, '05:45': 25, '16:00': 66, '13:00': 54, '07:15': 31, '16:15': 67, '21:45': 89, '03:45': 17, '15:45': 65, '12:00': 50, '08:30': 36, '02:45': 13, '13:45': 57, '13:30': 56, '05:00': 22, '11:45': 49, '11:00': 46, '09:30': 40, '22:30': 92, '16:45': 69, '08:15': 35, '18:30': 76, '08:00': 34, '07:00': 30, '00:15': 3, '17:15': 71, '01:45': 9, '20:15': 83, '17:45': 73, '04:30': 20, '15:15': 63, '21:30': 88, '23:45': 97}

YEAR_TO_ID = {'2013': 1, '2017': 5, '2016': 4, '2018': 6, '2015': 3, '2014': 2}

MONTH_TO_ID = {'11': 11, '01': 1, '03': 3, '07': 7, '02': 2, '10': 10, '04': 4, '09': 9, '05': 5, '06': 6, '12': 12, '08': 8}

DAY_TO_ID = {'11': 11, '23': 23, '03': 3, '02': 2, '10': 10, '16': 16, '29': 29, '13': 13, '17': 17, '09': 9, '05': 5, '28': 28, '20': 20, '25': 25, '01': 1, '07': 7, '15': 15, '30': 30, '14': 14, '04': 4, '26': 26, '21': 21, '19': 19, '24': 24, '27': 27, '18': 18, '22': 22, '06': 6, '12': 12, '08': 8}



def ws_exception_handler(req, exc):
    elog('ERROR EN PETICION ' + str(req))
    elog(exc)


def postAllDemandas(wsparam, demand_list, url):
    h = {'Authorization':'Token %s'%(wsparam['WS_TOKN'])}
    rs = (grequests.post(url, data=d, headers=h) for d in demand_list)
    grequests.map(rs, size=2, exception_handler=ws_exception_handler)


def tuple2Dict(tuple):
    # ORDEN DE TUPLA
    # nodo, fecha_hora, energia_activa, energia_aparente, demanda
    return {
        'node': tuple[0],
        'fecha_hora': tuple[1],
        'energia_activa': tuple[2],
        'energia_aparente': tuple[3],
        'demanda': tuple[4],
    }

def get_all_node_meditions(bdparam, tablename, node_id, min_date_time, reg_modifier=None):
    sql = "SELECT %d as nodo, Fecha_hora as fecha_hora, " \
              "WhTot as energia_activa, VAhTot as energia_aparente, " \
              "Pos_Watts_3ph_Av as demanda FROM %s "%(node_id, tablename)
    sql += "WHERE Fecha_hora>%s limit 50;"
    try:
        db=MySQLdb.connect(host=bdparam['DB_HOST'],
                           port=int(bdparam['DB_PORT']),
                           user=bdparam['DB_USER'],
                           passwd=bdparam['DB_PASS'],
                           db=bdparam['DB_NAME'])
        ilog('SQL TO EXECUTE')
        ilog(sql%(min_date_time.replace('T',' ').replace('Z',''),))
        c=db.cursor()
        c.execute(sql, (min_date_time.replace('T',' ').replace('Z',''),))
        l = [reg_modifier(e) for e in c.fetchall()]
        c.close()
    except Exception as e:
        l=[]
        elog('ERROR AL EJECUTAR SQL' + sql)
        elog(e)
    return l

def start(dbparam, wsparam, conv):
    # Paso 0: obtener el token para enviar los datos al WS
    url = wsparam['WS_HOST']+'/api-token-auth/'
    login_data={'username':wsparam['WS_USER'],
                'password':wsparam['WS_PASS']}
    response = requests.post(url, data=login_data)
    if response.status_code!=200:
        elog('ERROR AL INICIAR SESION EN EL WS, REVISAR DATOS DE INICIO DE SESION')
        ilog(response.text)
        return
    token = response.json()['token']
    wsparam['WS_TOKN'] = token
    # Paso 1: Por cada elemento en conv, obtener
    # La fecha_hora maxima de mediciones del nodo
    # usando el WS en /rest-api/mediciones/<nodo_id>/max/
    ws_host = wsparam['WS_HOST']
    for c in conv:
        url = ws_host+'/rest-api/mediciones/%d/max/'%(c[0])
        response = requests.get(url)
        if response.status_code != 200:
            wlog('Could\'nt download max datetime for node %d, HTTP status %s' % (c[0],response.status_code))
            continue
        ilog('Downloaded max datetime for node %d' % (c[0]))
        # Paso 2: Obtener todas las mediciones del nodo
        # en la base de datos fuente a partir de la fecha
        # obtenida en el WS
        demanda = response.json()
        jsons = get_all_node_meditions(dbparam, c[1], c[0], demanda['fecha_hora'], tuple2Dict)
        # Paso 3: Enviar cada medicion obtenida al WS
        # en /rest-api/mediciones/ usando POST
        postAllDemandas(wsparam, jsons, ws_host+'/rest-api/mediciones/')



if __name__=='__main__':
    # PARAMETROS DE CONEXION DE BASE DE DATOS FUENTE (SDB)
    DB_HOST = 'lennin92.mysql.pythonanywhere-services.com'
    # DB_HOST = 'localhost'
    DB_PORT = '3306'
    DB_USER = 'lennin92'
    DB_PASS = 'asdf123321fdsa'
    DB_NAME = 'lennin92$uesendash'

    SDBP = {'DB_HOST':DB_HOST, 'DB_PORT':DB_PORT, 'DB_USER':DB_USER,
            'DB_PASS':DB_PASS, 'DB_NAME':DB_NAME}

    # PARAMETROS DE CONEXION DE SERVICIO WEB (WS)
    WS_USER = 'updater'
    WS_PASS = 'updater123'
    WS_HOST = 'http://lennin92.pythonanywhere.com'

    WSP = {'WS_USER':WS_USER, 'WS_PASS':WS_PASS, 'WS_HOST':WS_HOST}


    # TABLA DE CONVERSION TABLA (EN SDB) A NODO (EN WS)
    # FORMATO: LISTA DE TUPLAS, LA TUPLA DEBE TENER EL
    # FORMATO SIGUIENTE:
    #   (<ID NODO EN WS>, <NOMBRE DE TABLA EN SDB>)
    CONVERSIONES = [
        (15, 'Agronomia'), (16, 'AgronomiaDecanato'), (32, 'AgronomiaGalera'), 
        (13, 'AuditoriumMarmol'), (28, 'Cafetetines'), (27, 'ComedorUES'), 
        (11, 'Derecho'), (23, 'Economia1'), (22, 'Economia2'), (21, 'Economia3'), 
        (20, 'Economia4'), (19, 'Economia5'), (17, 'Humanidades1'), (18, 'Humanidades2'), 
        (26, 'Humanidades3'), (25, 'Humanidades4'), (14, 'MecanicaComplejo'), 
        (38, 'Medicina'), (35, 'Odontologia1'), (36, 'Odontologia2'), (37, 'Odontologia3'), 
        (34, 'OdontologiaImprenta'), (29, 'Periodismo'), (12, 'PrimarioFIA'), (30, 'Quimica'), 
        (31, 'AgronomiaQuimica'), 
    ]



    start(SDBP, WSP, CONVERSIONES)

import MySQLdb
import requests
import grequests
import logging
import datetime


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='log.txt', level=logging.DEBUG)


def dlog(v): logging.debug(v)


def ilog(v): logging.info(v)


def wlog(v): logging.warning(v)


def elog(v): logging.error(v)


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
    tm = tuple[1]
    time = tm.strftime("%Y-%m-%d %H:%M:%S")
    year = time[0:4]
    month = time[5:7]
    day = time[8:10]
    time_hour = time[11:13]
    time_mins = int(time[14:16])
    # minute round to 15 mins
    if time_mins%15 != 0:
        tmod15 = time_mins%15
        t15 = tmod15%15
        if t15 > 0.5:
            tm += datetime.timedelta(minutes=15-tmod15)
        else:
            tm -= datetime.timedelta(minutes=tmod15)
            # time_mins -= tmod15
    # time_mins = str(time_mins).zfill(2)
    # datetime_str = '%s-%s-%s %s:%s'%(year, month, day, time_hour, time_mins)
    datetime_str = tm.strftime("%Y-%m-%d %H:%M:%S")
    return {
        'node_id': tuple[0],
        'datetime_str': datetime_str,
        'year_id': '',
        'month_id': '',
        'day_id': '',
        'time_id': '',
        'active': tuple[2],
        'apparent': tuple[3],
        'demand': tuple[4],
    }


def get_all_node_meditions(bdparam, tablename, node_id, min_date_time, reg_modifier=None):
    sql = "SELECT %d as nodo, Fecha_hora as fecha_hora, " \
              "WhTot as energia_activa, VAhTot as energia_aparente, " \
              "Pos_Watts_3ph_Av as demanda FROM %s "%(node_id, tablename)
    sql += "WHERE Fecha_hora>%s limit 25;"
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
        if reg_modifier is not None: l = [reg_modifier(e) for e in c.fetchall()]
        else: l = [e for e in c.fetchall()]
        c.close()
    except Exception as e:
        l=[]
        elog('ERROR AL EJECUTAR SQL' + sql)
        elog(e)
    return l


def start(dbparam, wsparam, conv):
    # Paso 0: obtener el token para enviar los datos al WS
    url = wsparam['WS_HOST']+'/api/token-auth/'
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
    # usando el WS en /api/nodes/<Nodo>/measures/last/
    ws_host = wsparam['WS_HOST']
    for c in conv:
        # url = ws_host+'/rest-api/mediciones/%d/max/'%(c[0])
        url = ws_host + '/api/nodes/%d/measures/last/'%(c[0])
        response = requests.get(url)
        if response.status_code != 200:
            wlog('Could\'nt download max datetime for node %d, HTTP status %s' % (c[0],response.status_code))
            continue
        ilog('Downloaded max datetime for node %d' % (c[0]))
        # Paso 2: Obtener todas las mediciones del nodo
        # en la base de datos fuente a partir de la fecha
        # obtenida en el WS
        demanda = response.json()
        jsons = get_all_node_meditions(dbparam, c[1], c[0], demanda['datetime_str'], tuple2Dict)
        # Paso 3: Enviar cada medicion obtenida al WS
        # en //api/nodes/%d/measures/ usando POST
        url = ws_host + '/api/nodes/%d/measures/' % (c[0])
        postAllDemandas(wsparam, jsons, url)#ws_host+'/rest-api/mediciones/')



if __name__=='__main__':
    # PARAMETROS DE CONEXION DE BASE DE DATOS FUENTE (SDB)
    # DB_HOST = 'lennin92.mysql.pythonanywhere-services.com'
    # DB_HOST = 'localhost'
    DB_HOST = '192.168.2.2'
    DB_PORT = '3306'
    DB_USER = 'lennin92$uesendash'
    DB_PASS = 'asdf123321fdsa'
    DB_NAME = 'lennin92$uesendash'

    SDBP = {'DB_HOST':DB_HOST, 'DB_PORT':DB_PORT, 'DB_USER':DB_USER,
            'DB_PASS':DB_PASS, 'DB_NAME':DB_NAME}

    # PARAMETROS DE CONEXION DE SERVICIO WEB (WS)
    WS_USER = 'updater'
    WS_PASS = 'updater123'
    # WS_HOST = 'http://lennin92.pythonanywhere.com'
    WS_HOST = 'http://localhost:8000'

    WSP = {'WS_USER':WS_USER, 'WS_PASS':WS_PASS, 'WS_HOST':WS_HOST}


    # TABLA DE CONVERSION TABLA (EN SDB) A NODO (EN WS)
    # FORMATO: LISTA DE TUPLAS, LA TUPLA DEBE TENER EL
    # FORMATO SIGUIENTE:
    #   (<ID NODO EN WS>, <NOMBRE DE TABLA EN SDB>)
    CONVERSIONES = [
        (15,'Agronomia'), (16,'AgronomiaDecanato'), (32,'AgronomiaGalera'),
        (13,'AuditoriumMarmol'), (28,'Cafeterias'), (27,'ComedorUES'),
        (11,'Derecho'), (24,'Derecho'), (23,'Economia1'), (22,'Economia2'),
        (21,'Economia3'), (20,'Economia4'), (19,'Economia5'), (17,'Humanidades1'),
        (18,'Humanidades2'), (26,'Humanidades3'), (25,'Humanidades4'),
        (14,'MecanicaComplejo'), (38,'Medicina'), (39,'Odontologia1'), (36,'Odontologia2'),
        (37,'Odontologia3'), (34,'OdontologiaImprenta'), (29L,'Periodismo'), (12,'PrimarioFIA'),
        (30,'Quimica'), (31,'QuimicaAgronomia'), # (33,'QuimicaOdontologia')
    ]

    start(SDBP, WSP, CONVERSIONES)



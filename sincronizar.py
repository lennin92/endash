
import MySQLdb
import requests
import grequests
import logging

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
    return {
        'nodo': tuple[0],
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
        (1, 'Agronomia'), (2, 'AgronomiaDecanato'), (32, 'Rectoria'),
        (3, 'AgronomiaGalera'), (4, 'AgronomiaQuimica'),
        (5, 'Artes'), (6, 'AuditoriumMarmol'), (7, 'Cafetines'),
        (8, 'ComedorUES'), (9, 'Derecho'), (10, 'Economia1'),
        (11, 'Economia2'), (12, 'Economia3'), (13, 'Economia4'),
        (14, 'Economia5'), (15, 'Economia6'),
        (17, 'Humanidades1'), (18, 'Humanidades2'), (19, 'Humanidades3'),
        (20, 'Humanidades4'), (21, 'MecanicaComplejo'), (22, 'Medicina'),
        (23, 'Odontologia1'), (24, 'Odontologia2'), (25, 'Odontologia3'),
        (26, 'OdontologiaImprenta'), (27, 'Periodismo'), (28, 'PrimarioFIA'),
        (29, 'Psicologia'), (30, 'Quimica'), (31, 'QuimicaImprenta'),
    ]


    start(SDBP, WSP, CONVERSIONES)



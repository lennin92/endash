
import MySQLdb
import requests

def start(bdparam, wsparam, conv):
    # Paso 1: Por cada elemento en conv, obtener
    # La fecha_hora maxima usando el WS en
    # /rest-api/mediciones/<nodo_id>/max/
    # Paso 2: Obtener todas las mediciones del nodo
    # en la base de datos fuente a partir de la fecha
    # obtenida en el WS
    # Paso 3: Enviar cada medicion obtenida al WS
    # en /rest-api/mediciones/ usando POST
    pass

if __name__=='__main__':
    # PARAMETROS DE CONEXION DE BASE DE DATOS FUENTE (SDB)
    DB_HOST = ''
    DB_PORT = ''
    DB_USER = ''
    DB_PASS = ''
    DB_NAME = ''

    SDBP = {'DB_HOST':DB_HOST, 'DB_PORT':DB_PORT, 'DB_USER':DB_USER,
            'DB_PASS':DB_PASS, 'DB_NAME':DB_NAME}

    # PARAMETROS DE CONEXION DE SERVICIO WEB (WS)
    WS_USER = ''
    WS_PASS = ''
    WS_HOST = ''

    WSP = {'WS_USER':WS_USER, 'WS_PASS':WS_PASS, 'WS_HOST':WS_HOST}


    # TABLA DE CONVERSION TABLA (EN SDB) A NODO (EN WS)
    CONVERSIONES = [
        ('', 1),  ('', 2),  ('', 3),  ('', 4),
    #    ('', 5),  ('', 6),  ('', 7),  ('', 8),
    #    ('', 9),  ('', 10), ('', 11), ('', 12),
    #    ('', 13), ('', 14), ('', 15), ('', 16),
    #    ('', 17), ('', 18), ('', 19), ('', 20),
    #    ('', 21), ('', 22), ('', 23), ('', 24),
    #    ('', 25), ('', 26), ('', 27), ('', 28),
    #    ('', 29), ('', 30), ('', 31), ('', 32)
    ]


    start(SDBP, WSP, CONVERSIONES)



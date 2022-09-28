import math
import json
import googlemaps
from config import settings
from logs import logger


def is_on_home_street(lat, lon):
REMOVED
    reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
    for i in reverse_geocode_result:
        if 'Arcuri Court' in i['address_components'][0]['long_name']:
            return True
    return False


def tesla_prox(request):
    #lat, lon = 0, 0
    try:
        request_json = request.get_json()
        lat = float(request_json['lat'])
        lon = float(request_json['lon'])
    except Exception as e:
        logger.error('tesla_prox::::: Issue with function inputs :::::' + str(e))
        raise

    radius = 6371
    d_lat = math.radians(lat - settings['production']['LAT_HOME'])
    d_lon = math.radians(lon - settings['production']['LON_HOME'])
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.cos(math.radians(settings['production']['LAT_HOME'])) * math.cos(math.radians(lat)) * \
        math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    difference = radius * c
    str_difference = float(difference)
    data = {'difference': str_difference}

    if difference < settings['production']['HOME_RADIUS']\
            or math.isclose(difference, settings['production']['HOME_RADIUS']):
        data['is_close'] = True
        if is_on_home_street(lat, lon):
            data['is_on_arcuri'] = True
        else:
            data['is_on_arcuri'] = False

        json_data = json.dumps(data)
        return json_data
    else:
        data['is_close'] = False
        data['is_on_arcuri'] = False
        json_data = json.dumps(data)
        return json_data

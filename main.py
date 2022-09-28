import math
import json
import googlemaps
import constant


def is_on_home_street(lat, lon):
REMOVED
    reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
    for i in reverse_geocode_result:
        if 'Arcuri Court' in i['address_components'][0]['long_name']:
            return True
    return False


def tesla_prox(request):
    lat, lon = 0, 0
    request_json = request.get_json()
    if request_json and 'lat' in request_json:
        lat = float(request_json['lat'])
    if request_json and 'lon' in request_json:
        lon = float(request_json['lon'])

    radius = 6371
    dlat = math.radians(lat-constant.LATHOME)
    dlon = math.radians(lon-constant.LONHOME)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(constant.LATHOME)) * math.cos(math.radians(lat)) * \
        math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    difference = radius * c
    str_difference = float(difference)
    data = {'difference': str_difference}

    if difference < constant.HOMERADIUS or math.isclose(difference, constant.HOMERADIUS):
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

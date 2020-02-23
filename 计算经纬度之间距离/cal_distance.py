from math import asin,pow,sin,cos,sqrt,pi


EARTH_REDIUS = 6378.137

def rad(d):
    return d * pi / 180.0

def getDistance(lat1, lng1, lat2, lng2):
    """
    a=Lat1 – Lat2 为两点纬度之差  b=Lung1 -Lung2 为两点经度之差；
    6378.137为地球半径，单位为千米；
    计算出来的结果单位为千米。
    :param lat1: A经度
    :param lng1: A维度
    :param lat2: B经度
    :param lng2: B维度
    :return: distance
    """
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * asin(sqrt(pow(sin(a/2), 2) + cos(radLat1) * cos(radLat2) * pow(sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s

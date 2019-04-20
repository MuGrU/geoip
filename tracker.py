#!/usr/bin/python3

import geoip2.database
import sys
import tarfile
import os.path
from os import path

usage = "Run the script: ./tracker.py IPAddress"

def extract_db(ipaddress):
    tf1 = tarfile.open("./DB/GeoLite2-ASN_20190416.tar.gz")
    tf1.extractall(path="./DB/")
    tf2 = tarfile.open("./DB/GeoLite2-City_20190416.tar.gz")
    tf2.extractall(path="./DB/")
    track_ip(ipaddress)


def track_ip(ip):

    reader = geoip2.database.Reader('./DB/GeoLite2-City_20190416/GeoLite2-City.mmdb')

    response = reader.city(ip)
    print(60 *'_')
    print('IP address: {}'.format(response.traits.ip_address))
    print(60 * '_')
    print("\nCountry Code: {}".format(response.country.iso_code))
    print('Most Specific Name: {}'.format(response.subdivisions.most_specific.name))
    print('Most Specific code: {}'.format(response.subdivisions.most_specific.iso_code))
    print('City Name: {}'.format(response.city.name))
    print('Postal Code: {}'.format(response.postal.code))
    print('Latitude: {}'.format(response.location.latitude))
    print('Longitude: {}'.format(response.location.longitude))
    reader.close()
    track_asn(ip)

def track_asn (ip):

    reader = geoip2.database.Reader('./DB/GeoLite2-ASN_20190416/GeoLite2-ASN.mmdb')

    response = reader.asn(ip)
    print(60 *'_')
    print('ISP: {}'.format(response.autonomous_system_organization))
    print(60 *'_')
    reader.close()


def main():
    citydb = "./DB/GeoLite2-City_20190416"
    asndb = "./DB/GeoLite2-ASN_20190416"


    if len(sys.argv)!=2:
        print(60 *'_')
        print(usage)
        print(60 *'_')
        sys.exit(0)

    if len(sys.argv) > 1:
        ipaddress = sys.argv[1]
        if not (os.path.exists(citydb) and os.path.exists(asndb)):
            extract_db(ipaddress)
        else:
            track_ip(ipaddress)
main()

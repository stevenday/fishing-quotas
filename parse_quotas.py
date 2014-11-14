#!/usr/bin/python
import csv
from operator import itemgetter

import geocoder

output_headings = ['Ship name', 'Home port', 'Lat', 'Lng', 'Total quota']
output = []

missing_quotas = []

with open('quotas.csv', 'r') as quota_file:
    quotas = csv.DictReader(quota_file)
    quota_count = 1
    for quota in quotas:
        print "Processing quota {0}".format(quota_count)
        # Open the file multiple times because DictReader won't go back to the start
        with open('ships.csv', 'r') as ships_file:
            ships = csv.DictReader(ships_file)
            ship_name = quota['Vessel name'].lower().strip()
            ship_count = 1
            for ship in ships:
                if ship['Vessel name'].lower().strip() == ship_name:
                    print "Found matching ship: {0}".format(ship['Vessel name'])
                    geocode_result = geocoder.google(ship['Home port'])
                    if geocode_result.status == "OK":
                        row = [ship['Vessel name'], ship['Home port'], geocode_result.lat, geocode_result.lng, int(quota['Total FQA units held'])]
                    else:
                        print "Couldn't geocode the home port, status: {0}".format(geocode_result.status)
                        row = [ship['Vessel name'], ship['Home port'], None, None, int(quota['Total FQA units held'])]
                    output.append(row)
                    break
                ship_count += 1
            else:
                missing_quotas.append(quota)
        quota_count += 1

with open('combined.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(output_headings)
    sorted_output = sorted(output, key=itemgetter(2), reverse=True)
    writer.writerows(sorted_output)

print "Missing quotas:"
for quota in missing_quotas:
    print quota
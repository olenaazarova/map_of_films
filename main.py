""" create map with films locations"""
import folium
import argparse
from geopy.geocoders import Nominatim
from haversine import haversine
from geopy.exc import GeocoderUnavailable

parser = argparse.ArgumentParser()
parser.add_argument('year', type= int, help='year of films')
parser.add_argument('latitude', type= float, help= 'latitude')
parser.add_argument('longitude', type= float, help= 'longitude')
parser.add_argument('path', type= str, help= 'path to file')
args = parser.parse_args()

if __name__ == "__main__":
    path_to_file = args.path
    year = args.year
    latitude = args.latitude
    longitude = args.longitude
    try:
        with open(path_to_file, 'r', encoding='utf-8') as file:
            geolocator = Nominatim(user_agent="location")
            films = []
            lines = file.readlines()[14:]
            for line in lines:
                line = line.replace('"', '')
                new_line = line.replace('\t', ' ').strip('\n').split(') ')
                current_year = new_line[0][-4:]
                year = str(year)
                if current_year == year:
                    try:
                        name = new_line[0][:new_line[0].find(' (')]
                        film_line = line.strip('\n').split('\t')
                        i = -1
                        if film_line[i][0] == '(':
                            i -= 1
                        location = film_line[i]
                        address = geolocator.geocode(location)
                        lat = address.latitude
                        lon = address.longitude
                        distance = haversine((lat, lon), (latitude, longitude), unit='mi')
                        info = (distance, lat, lon, name)
                        films.append(info)
                    except (AttributeError, GeocoderUnavailable):
                        continue
            films = sorted(films, key=lambda x: x[0])
            i = 0
            data = []
            for film in films:
                if i > 9:
                    break
                i += 1
                tpl = (film[1], film[2], film[3])
                data.append(tpl)
            start_lat = latitude
            start_lon = longitude
            feature_group = folium.FeatureGroup(name='My Feature Group')
            map_of_films = folium.Map(location=[start_lat, start_lon], zoom_start=10)
            map_of_films = folium.Map(tiles="stamenwatercolor")

            for elem in data:
                lat = elem[0]
                lon = elem[1]
                name = elem[2]
                marker=folium.Marker(location=[lat, lon],popup=name, icon=folium.Icon(color='pink'))
                feature_group.add_child(marker)

            map_of_films.add_child(feature_group)
            file_name = 'Map_Of_Films_' + year + '.html'
            map_of_films.save(file_name)
    except (FileExistsError, FileNotFoundError):
        print('File not found')

import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
import csv
import sys


def get_soup(url):
    try:
        response = requests.get(url)
        soup = BS(response.text, 'html.parser')
    except:
        print('Connection error.')
        sys.exit()
    else:
        return soup


def select_district(url='https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ'):
    district = input('Choose district to be processed: ')
    soup = get_soup(url)
    td = soup.find('td', string=district)
    if td:
        siblings = td.find_next_siblings('td')
        return siblings[1].find('a').attrs.get('href')
    else:
        print('District not found.')
        return


def get_tables(url):
    soup = get_soup(url)
    tables = soup.find_all('table')
    return tables


def get_rows(table):
    rows = table.find_all('tr')
    return rows


def get_cities(url):
    cities = []
    tables = get_tables(url)
    for table in tables:
        rows = get_rows(table)
        for row in rows[2:]:
            try:
                tds = row.find_all('td')
                cities.append([tds[0].string, tds[1].string, tds[0].find('a').attrs.get('href')])
            except AttributeError:
                pass
    return cities


def envelope_stats(table):
    rows = table.find_all('tr')
    tds = rows[2].find_all('td')
    env_stats = {
        'registered': tds[3].string,
        'envelopes': tds[6].string,
        'valid': tds[7].string
        }
    return env_stats


def write_csv(header, data, filename='election_results.csv'):
    try:
        with open(filename,'w', newline='') as file:
            writer = csv.DictWriter(file, header)
            writer.writeheader()
            writer.writerows(data)
    except PermissionError:
        print('File is opened by another program.')
    else:
        print('Report created.')


def main():
    partial_url = 'https://volby.cz/pls/ps2017nss/'
    district = select_district()
    if district:
        url = urljoin(partial_url, district)
        header = ['code', 'location', 'registered', 'envelopes', 'valid']
        data = []
        list_of_cities = get_cities(url)

        for city in list_of_cities:
            data.append({'code': int(city[0]), 'location': city[1]})
            city_url = urljoin(partial_url, city[2])

            tables = get_tables(city_url)
            city_envelopes = envelope_stats(tables[0])
            data[-1].update(city_envelopes)

            for table in tables[1:]:
                rows = get_rows(table)
                for row in rows[2:]:
                    tds = row.find_all('td')
                    party = tds[1].string
                    votes = tds[2].string
                    if party not in header:
                        header.append(party)
                    data[-1].update({party: votes})
        write_csv(header, data)


if __name__ == '__main__':
    main()

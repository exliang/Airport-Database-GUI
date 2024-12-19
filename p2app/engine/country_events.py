
# Module including functions for all the country-related
# events called in process_events generator function in main.py

from p2app.events import *
from .helpers import *

def start_country_search(connection, event):
    try:
        country_code = event.country_code()
        country_name = event.name()
        country_id = 0

        # check that name & country_code match one in the table & get country_id and continent_id
        cursor = connection.execute('SELECT * FROM country;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            code = row[1]
            name = row[2]
            if country_code == code and country_name == name:
                country_id = row[0]
                continent_id = row[3]
                wiki_link = row[4]
                keywords = row[5]
                if country_id:  # only return the event if the country is found
                    yield CountrySearchResultEvent(
                        Country(country_id, country_code, country_name, continent_id, wiki_link,
                                keywords))
                break
            elif country_code == code and country_name == None:
                country_id = row[0]
                country_name = name
                continent_id = row[3]
                wiki_link = row[4]
                keywords = row[5]
                if country_id:  # only return the event if the country is found
                    yield CountrySearchResultEvent(
                        Country(country_id, country_code, country_name, continent_id, wiki_link,
                                keywords))
                break
            elif country_name == name and country_code == None:
                country_id = row[0]
                country_code = code
                continent_id = row[3]
                wiki_link = row[4]
                keywords = row[5]
                if country_id:  # only return the event if the country is found
                    yield CountrySearchResultEvent(
                        Country(country_id, country_code, country_name, continent_id, wiki_link,
                                keywords))
                country_code = event.country_code()
    except Exception as e:
        yield ErrorEvent(f"Error: {e}")

def load_country(connection, event):
    try:
        country_id = event.country_id()
        country_code = 0
        country_name = ''
        # get country_code & country_name
        cursor = connection.execute('SELECT * FROM country;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            id = row[0]
            if country_id == id:
                country_code = row[1]
                country_name = row[2]
                continent_id = row[3]
                wiki_link = row[4]
                keywords = row[5]
        yield CountryLoadedEvent(
            Country(country_id, country_code, country_name, continent_id, wiki_link, keywords))
    except Exception as e:
        yield ErrorEvent(f'Error: {e}')

def save_new_country(connection, event):
    try:
        country_codee = event.country().country_code
        country_name = event.country().name
        country_c_id = event.country().continent_id
        country_wiki_link = event.country().wikipedia_link
        country_keywords = event.country().keywords

        # check if this country alr exists in the table
        cursor = connection.execute('SELECT * FROM country;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            code = row[1]
            name = row[2]
            wiki_link = row[4]
            # can't save a country that alr exists or has an invalid country_id
            if code == country_codee or not valid_continent_id(connection, country_c_id):
                yield SaveCountryFailedEvent(
                    "This country already exists or the continent id doesn't exist.")
                break
        else:  # only runs if break is not hit
            if country_keywords == '':
                country_keywords = None
            connection.execute(
                'INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES (?,?,?,?,?)',
                (country_codee, country_name, country_c_id, country_wiki_link, country_keywords))
            connection.commit()  # allow changes to show up in database

            # getting the country index from database to get it appear on gui
            cursor2 = connection.execute('SELECT country_id FROM country where name = :name',
                                              {'name': country_name})
            country_index = cursor2.fetchone()[0]
            yield CountrySavedEvent(
                Country(country_index, country_codee, country_name, country_c_id, country_wiki_link,
                        country_keywords))
    except Exception as e:
        yield SaveCountryFailedEvent(f'Error: {e}')

def save_country(connection, event):
    try:
        country_id = event.country().country_id
        modified_ctry_code = event.country().country_code
        modified_ctry_name = event.country().name
        modified_ctry_c_id = event.country().continent_id
        modified_link = event.country().wikipedia_link
        modified_kwords = event.country().keywords

        # fail condition: after modification, country code and name overlaps with another one in the table or nothing was modified, valid continent_id
        cursor = connection.execute(
            'SELECT country_code, name, continent_id, wikipedia_link, keywords FROM country;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            code = row[0]
            name = row[1]
            country_c_id = row[2]
            link = row[3]
            keywords = row[4]
            if (no_modifications_on_gui_country(code, name, country_c_id, link, keywords,
                                                modified_ctry_code, modified_ctry_name,
                                                modified_ctry_c_id, modified_link, modified_kwords)
                    or not valid_continent_id(connection, modified_ctry_c_id)
                    or empty_responses_on_gui_country(modified_ctry_code, modified_ctry_name, modified_ctry_c_id, modified_link)):
                yield SaveCountryFailedEvent(
                    "This country already exists/no modifications were made to the original country, invalid continent id, or one of the attributes or all was not typed in.")
                break
        else:  # only runs if break is not hit
            if modified_kwords == '':
                modified_kwords = None
            modified_dict = {'code': modified_ctry_code, 'name': modified_ctry_name,
                             'c_id': modified_ctry_c_id, 'link': modified_link,
                             'kw': modified_kwords, 'id': country_id}
            connection.execute(
                'UPDATE country SET country_code = :code, name = :name, continent_id = :c_id, wikipedia_link = :link, keywords = :kw WHERE country_id = :id',
                modified_dict)
            connection.commit()  # allow changes to show up in database
            yield CountrySavedEvent(
                Country(country_id, modified_ctry_code, modified_ctry_name, modified_ctry_c_id,
                        modified_link, modified_kwords))
    except Exception as e:
        yield SaveCountryFailedEvent(f'Error: {e}')
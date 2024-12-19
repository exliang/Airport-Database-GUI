
# Module including functions for all the region-related
# events called in process_events generator function in main.py

from p2app.events import *
from .helpers import *

def start_region_search(connection, event):
    try:
        region_code = event.region_code()
        local_code = event.local_code()
        region_name = event.name()

        # check that name, region & local codes match one in the table & get rest of attributes
        cursor = connection.execute('SELECT * FROM region;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            r_code = row[1]
            l_code = row[2]
            name = row[3]
            continent_id, country_id, wiki_link, keywords = set_region_attributes(row)
            if region_code == r_code and local_code == l_code and region_name == name:
                region_id = row[0]
                yield RegionSearchResultEvent(
                    Region(region_id, region_code, local_code, region_name, continent_id,
                           country_id, wiki_link, keywords))
                break
            elif region_code == r_code and local_code == l_code and region_name == None:  # region & local code
                region_id = row[0]
                region_name = name
                yield RegionSearchResultEvent(
                    Region(region_id, region_code, local_code, region_name, continent_id,
                           country_id, wiki_link, keywords))
                region_name = event.name()
            elif local_code == l_code and region_name == name and region_code == None:  # local code & name
                region_id = row[0]
                region_code = r_code
                yield RegionSearchResultEvent(
                    Region(region_id, region_code, local_code, region_name, continent_id,
                           country_id, wiki_link, keywords))
                region_code = event.region_code()
            elif region_code == r_code and region_name == name and local_code == None:  # region code & name
                region_id = row[0]
                local_code = l_code
                yield RegionSearchResultEvent(
                    Region(region_id, region_code, local_code, region_name, continent_id,
                           country_id, wiki_link, keywords))
                local_code = event.local_code()
            elif region_code == r_code and local_code == None and region_name == None:  # region code
                region_id = row[0]
                local_code = l_code
                region_name = name
                yield RegionSearchResultEvent(
                    Region(region_id, region_code, local_code, region_name, continent_id,
                           country_id, wiki_link, keywords))
                break
            elif local_code == l_code and region_code == None and region_name == None:  # local code
                region_id = row[0]
                region_code = r_code
                region_name = name
                yield RegionSearchResultEvent(
                    Region(region_id, region_code, local_code, region_name, continent_id,
                           country_id, wiki_link, keywords))
                region_code = event.region_code()
                region_name = event.name()
            elif region_name == name and region_code == None and local_code == None:  # region name
                region_id = row[0]
                region_code = r_code
                local_code = l_code
                yield RegionSearchResultEvent(
                    Region(region_id, region_code, local_code, region_name, continent_id,
                           country_id, wiki_link, keywords))
                region_code = event.region_code()
                local_code = event.local_code()
            else:  # none of the attributes match, just continue
                continue
    except Exception as e:
        yield ErrorEvent(f'Error: {e}')

def load_region(connection, event):
    try:
        region_id = event.region_id()

        # get the rest of the attributes
        cursor = connection.execute('SELECT * FROM region;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            id = row[0]
            if region_id == id:
                r_code = row[1]
                l_code = row[2]
                name = row[3]
                continent_id = row[4]
                country_id = row[5]
                wiki_link = row[6]
                keywords = row[7]

        yield RegionLoadedEvent(
            Region(region_id, r_code, l_code, name, continent_id, country_id, wiki_link, keywords))
    except Exception as e:
        yield ErrorEvent(f'Error: {e}')

def save_new_region(connection, event):
    try:
        region_code = event.region().region_code
        local_code = event.region().local_code
        region_name = event.region().name
        r_continent_id = event.region().continent_id
        r_country_id = event.region().country_id
        wiki_link = event.region().wikipedia_link
        keywords = event.region().keywords

        # check if this region alr exists in the table
        cursor = connection.execute('SELECT * FROM region;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            r_code = row[1]
            l_code = row[2]
            name = row[3]
            continent_id = row[4]
            country_id = row[5]
            link = row[6]
            kwords = row[7]
            # can't save a region that alr exists, has an invalid country_id or continent_id, or is missing a column
            if (r_code == region_code
                    or not valid_continent_id(connection, r_continent_id)
                    or not valid_country_id(connection, r_country_id)):
                yield SaveRegionFailedEvent(
                    "This region already exists, the country or continent id doesn't exist.")
                break
            if not check_valid_continent_and_country_id(connection, r_continent_id,
                                                        r_country_id):  # invalid continent for country id
                yield SaveRegionFailedEvent(
                    "The given country id is not a country in the continent given the continent id.")
                break
        else:  # only runs if break is not hit
            if wiki_link == '':
                wiki_link = None
            if keywords == '':
                keywords = None
            connection.execute(
                'INSERT INTO region(region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?,?,?,?,?,?,?)',
                (region_code, local_code, region_name, r_continent_id, r_country_id, wiki_link,
                 keywords))
            connection.commit()  # allow changes to show up in database

            # getting the region index from database to get it appear on gui
            cursor2 = connection.execute('SELECT region_id FROM region where name = :name',
                                              {'name': region_name})
            region_index = cursor2.fetchone()[0]
            yield RegionSavedEvent(
                Region(region_index, region_code, local_code, region_name, r_continent_id,
                       r_country_id, wiki_link, keywords))
    except Exception as e:
        yield SaveRegionFailedEvent(f'Error: {e}')

def save_region(connection, event):
    try:
        region_id = event.region().region_id
        modified_region_code = event.region().region_code
        modified_local_code = event.region().local_code
        modified_region_name = event.region().name
        modified_r_continent_id = event.region().continent_id
        modified_r_country_id = event.region().country_id
        modified_link = event.region().wikipedia_link
        modified_kwords = event.region().keywords

        # fail condition: after modification, country code and name overlaps with another one in the table or nothing was modified, valid continent_id
        cursor = connection.execute(
            'SELECT region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords FROM region;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            r_code = row[0]
            l_code = row[1]
            name = row[2]
            continent_id = row[3]
            country_id = row[4]
            link = row[5]
            kwords = row[6]
            if no_modifications_on_gui_region(r_code, l_code, name, continent_id, country_id, link,
                                              kwords,
                                              modified_region_code, modified_local_code,
                                              modified_region_name,
                                              modified_r_continent_id, modified_r_country_id,
                                              modified_link, modified_kwords):
                yield SaveRegionFailedEvent("No modifications were made to the original region.")
                break
            if not valid_continent_id(connection, modified_r_continent_id) or not valid_country_id(connection,
                                                                                             modified_r_country_id):
                yield SaveRegionFailedEvent("Invalid continent or country id.")
                break
            if not check_valid_continent_and_country_id(connection, modified_r_continent_id,
                                                        modified_r_country_id):  # invalid continent for country id
                yield SaveRegionFailedEvent(
                    "The given country id is not a country in the continent given the continent id.")
                break
            if empty_responses_on_gui_region(modified_region_code, modified_local_code,
                                             modified_region_name, modified_r_continent_id,
                                             modified_r_country_id):
                yield SaveRegionFailedEvent(
                    "One or more of the necessary region attributes were not filled in.")
                break
        else:  # only runs if break is not hit
            modified_dict = {'rcode': modified_region_code, 'lcode': modified_local_code,
                             'name': modified_region_name, 'ctnt_id': modified_r_continent_id,
                             'ctry_id': modified_r_country_id, 'link': modified_link,
                             'kw': modified_kwords, 'id': region_id}
            connection.execute(
                'UPDATE region SET region_code = :rcode, local_code = :lcode, name = :name, continent_id = :ctnt_id, country_id = :ctry_id, wikipedia_link = :link, keywords = :kw WHERE region_id = :id',
                modified_dict)
            connection.commit()  # allow changes to show up in database
            yield RegionSavedEvent(
                Region(region_id, modified_region_code, modified_local_code, modified_region_name,
                       modified_r_continent_id, modified_r_country_id,
                       modified_link, modified_kwords))
    except Exception as e:
        yield SaveRegionFailedEvent(f"Error: {e}")

# Module including all the helper functions used
# for the process_event generator function in main.py

import sqlite3

def set_region_attributes(row):
    """Helper function to set
    some region attributes"""
    continent_id = row[4]
    country_id = row[5]
    wiki_link = row[6]
    keywords = row[7]
    return continent_id, country_id, wiki_link, keywords

def valid_continent_id(connection, country_c_id):
    """Helper function for checking if the
    continent_id is in the continent table or not
    for country & region-related events"""
    # getting a list of all the continent ids
    continent_id_count = connection.execute('SELECT COUNT (continent_id) FROM continent;')
    max_continent_index = continent_id_count.fetchone()[0]
    continent_ids = [i for i in range(1, max_continent_index + 1)]
    return country_c_id in continent_ids

def valid_country_id(connection, country_id):
    """Helper function for checking if the
    country_id is in the country table or not
    for region-related events"""
    get_country_ids = connection.execute('SELECT country_id FROM country;')
    all_country_ids = get_country_ids.fetchall()
    for id in all_country_ids:
        if id[0] == country_id:
            return True
    return False

def empty_responses_on_gui_country(code, name, continent_id, link):
    """Helper function for checking if any attributes
    were not typed in by the user on the gui for country-related events"""
    return any(not col for col in [code, name, continent_id, link])

def no_modifications_on_gui_country(code, name, continent_id, link, keywords, modified_ctry_code, modified_ctry_name, modified_ctry_c_id, modified_link, modified_kwords):
    """Helper function for checking if no modifications
    were made to the country attributes"""
    m_code = modified_ctry_code == code
    m_name = modified_ctry_name == name
    m_id = modified_ctry_c_id == continent_id
    m_lk = modified_link == link
    m_kw = modified_kwords == keywords
    return m_code and m_name and m_id and m_lk and m_kw

def no_modifications_on_gui_region(r_code, l_code, name, continent_id, country_id, link, kwords,
                                    modified_region_code, modified_local_code, modified_region_name,
                                    modified_r_continent_id, modified_r_country_id, modified_link, modified_kwords):
    """Helper function for checking if no modifications
    were made to the region attributes"""
    m_r_code = modified_region_code == r_code
    m_l_code = modified_local_code == l_code
    m_name = modified_region_name == name
    m_ctnt_id = modified_r_continent_id == continent_id
    m_ctry_id = modified_r_country_id == country_id
    m_lk = modified_link == link
    m_kw = modified_kwords == kwords
    return m_r_code and m_l_code and m_name and m_ctnt_id and m_ctry_id and m_lk and m_kw

def empty_responses_on_gui_region(region_code, local_code, region_name, r_continent_id, r_country_id):
    """Helper function for checking if any attributes
       were not typed in by the user on the gui for region-related events"""
    return any(not col for col in [region_code, local_code, region_name, r_continent_id, r_country_id])

def check_valid_continent_and_country_id(connection, r_continent_id, r_country_id):
    """Helper function that ensures the country_id typed in by the user
    on gui is a country on a continent with the continent_id typed in"""
    # create a dict of continent & country_ids {1: [id1, id2...], 2: [id1, id2...],...}
    id_dict = {}
    cursor = connection.execute("SELECT continent_id, country_id FROM region;")
    all_rows = cursor.fetchall()
    for row in all_rows:
        continent_id = row[0]
        country_id = row[1]
        if continent_id in id_dict and country_id not in id_dict[continent_id]:  # only add country_id if it's not alr in there
            id_dict[continent_id].append(country_id)
        elif continent_id not in id_dict:
            id_dict[continent_id] = []
    for continent_id, country_ids in id_dict.items():
        if continent_id == r_continent_id:
            for country_id in country_ids:
                if country_id == r_country_id:
                    return True
    return False

def valid_database_file(file):
    """Function to check if the file
    selected is a valid sql db file"""
    if file.endswith('.db'):
        try:  # testing if db file is a valid db by trying to execute an sql statement
            connection = sqlite3.connect(file)
            cursor = connection.execute("SELECT * FROM sqlite_master")
        except sqlite3.DatabaseError: # file is not a valid db
            return False
        except Exception as e:
            print(f'Error: {e}')
        else:
            return True
    else:
        return False

def tables_exist_in_dbfile(file):
    """Function to verify that the necessary tables:
    continent, country, and region exist in the db file"""
    continent_exists = False
    country_exists = False
    region_exists = False

    connection = sqlite3.connect(file)
    cursor = connection.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='continent';")
    continent = cursor.fetchone()
    if continent is not None:
        continent_exists = True

    cursor2 = connection.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='country';")
    country = cursor2.fetchone()
    if country is not None:
        country_exists = True

    cursor3 = connection.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='region';")
    region = cursor3.fetchone()
    if region is not None:
        region_exists = True

    return continent_exists and country_exists and region_exists
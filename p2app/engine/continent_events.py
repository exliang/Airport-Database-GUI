
# Module including functions for all the continent-related
# events called in process_events generator function in main.py

from p2app.events import *

def start_continent_search(connection, event):
    try:
        continent_code = event.continent_code()
        continent_name = event.name()
        continent_id = 0
        # check that name & continent_code match one in the table & get continent_id
        cursor = connection.execute('SELECT * FROM continent;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            code = row[1]
            name = row[2]
            if continent_code == code and continent_name == name:
                continent_id = row[0]
                if continent_id:  # only return the event if the continent is found
                    yield ContinentSearchResultEvent(
                        Continent(continent_id, continent_code, continent_name))
                break
            elif continent_code == code and continent_name == None:
                continent_id = row[0]
                continent_name = name
                if continent_id:  # only return the event if the continent is found
                    yield ContinentSearchResultEvent(
                        Continent(continent_id, continent_code, continent_name))
                continent_name = event.name()
                break
            elif continent_name == name and continent_code == None:  # name is not unique
                continent_id = row[0]
                continent_code = code
                if continent_id:  # only return the event if the continent is found
                    yield ContinentSearchResultEvent(
                        Continent(continent_id, continent_code, continent_name))
                continent_code = event.continent_code()
    except Exception as e:
        yield ErrorEvent(f'Error: {e}')

def load_continent(connection, event):
    try:
        continent_id = event.continent_id()
        continent_code = 0
        continent_name = ''
        # get continent_code & continent_name
        cursor = connection.execute('SELECT * FROM continent;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            id = row[0]
            if continent_id == id:
                continent_code = row[1]
                continent_name = row[2]
        yield ContinentLoadedEvent(Continent(continent_id, continent_code, continent_name))
    except Exception as e:
        yield ErrorEvent(f'Error: {e}')

def save_new_continent(connection, event):
    try:
        get_continent_id = connection.execute('SELECT COUNT (continent_id) FROM continent;')
        continent_index = get_continent_id.fetchone()[0] + 1  # getting the continent_id
        continent_codee = event.continent().continent_code
        continent_name = event.continent().name

        # check if this continent alr exists in the table
        cursor = connection.execute('SELECT * FROM continent;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            id = row[0]
            code = row[1]
            name = row[2]
            # can't save a continent that alr exists (only continent_code is unique)
            if code == continent_codee:
                yield SaveContinentFailedEvent(
                    "This continent already exists.")
                break
        else:  # only runs if break is not hit
            connection.execute('INSERT INTO continent (continent_code, name) VALUES (?,?)',
                                    (continent_codee, continent_name))
            connection.commit()  # allow changes to show up in database
            yield ContinentSavedEvent(Continent(continent_index, continent_codee, continent_name))
    except Exception as e:
        yield SaveContinentFailedEvent(f'Error: {e}')

def save_continent(connection, event):
    try:
        continent_id = event.continent().continent_id
        modified_continent_code = event.continent().continent_code
        modified_continent_name = event.continent().name

        # fail condition: after modification, continent code and name overlaps with another one in the table or nothing was modified
        cursor = connection.execute('SELECT continent_code, name FROM continent;')
        all_rows = cursor.fetchall()
        for row in all_rows:
            code = row[0]
            name = row[1]
            if modified_continent_code == '' or modified_continent_name == '':
                yield SaveContinentFailedEvent(
                    "This continent already exists/no modifications were made to the original continent or the continent code or name or both was not typed in.")
                break
        else:  # only runs if break is not hit
            connection.execute(
                'UPDATE continent SET continent_code = :code, name = :name WHERE continent_id = :id',
                {'code': modified_continent_code, 'name': modified_continent_name,
                 'id': continent_id})
            connection.commit()  # allow changes to show up in database
            yield ContinentSavedEvent(
                Continent(continent_id, modified_continent_code, modified_continent_name))
    except Exception as e:
        yield SaveContinentFailedEvent(f'Error: {e}')
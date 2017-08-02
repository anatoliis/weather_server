import requests
import sqlite3
import re
import time


def establish_db_connection(db_name):
    return sqlite3.connect(db_name)


def create_table(connection):
    try:
        connection.cursor().execute(
            '''CREATE TABLE weather (t1 real, t2 real, t3 real, t4 real, tc real, t0 real, pr real, hm real, fr real, ml real, ts real, time real, footprint real unique)'''
            )
    except sqlite3.OperationalError as exc:
        pass

def get_raw_data(url):
    r = requests.get(url=url, timeout=7)
    return r.text


def calculate_footprint(line):
    t1, t2, t3, t4, tc, t0, pr, hm, fr, ml, ts, mtime = line
    return (t1 + t2 + t3 + t4 + tc + t0) * 100 + pr * 1000 + hm * 1000 + ml * 1000 + ts * 10000


def parse(raw_data):
    lines = raw_data.split('\n')[1:]
    arduino_fetch_timestamp = float(lines.pop())
    lines = [list(map(float, line.split(','))) for line in lines]
    for line in lines:
        arduino_measurement_timestamp = line[-1]
        seconds_ago = (arduino_fetch_timestamp - arduino_measurement_timestamp) / 1000. + 1.5
        timestamp = time.time() - seconds_ago
        line.append(timestamp)
        line.append(calculate_footprint(line))
    return lines


def store(connection, lines):
    stored_lines_number = 0
    for line in lines:
        instruction_line = "INSERT INTO weather VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % tuple(line)
        try:
            connection.cursor().execute(instruction_line)
            stored_lines_number += 1
        except sqlite3.IntegrityError as exc:
            if 'UNIQUE' not in str(exc):
                raise exc
    connection.commit()
    return stored_lines_number


def main():
    connection = establish_db_connection('weather.db')
    create_table(connection)
    counter = 0
    while True:
        request_successful = False
        stored_lines_number = 0
        try:
            raw_data = get_raw_data('http://192.168.0.195/data_all')
            parsed_data = parse(raw_data)
            stored_lines_number = store(connection, parsed_data)
            counter += 1
            request_successful = True
            
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as exc:
            pass

        timeout = 5
        if request_successful:
            if counter == 0:
                timeout = 3
            print("Request #%s. Got %s new measurement(s), next request after %s seconds.." % (counter, stored_lines_number, timeout))
        else:
            print("Error requesting data (%s), next request after %s seconds.." % (counter, timeout))
        
        time.sleep(timeout)


if __name__ == '__main__':
    main()

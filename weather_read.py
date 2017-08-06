import sqlite3
import datetime
import xlwt


def excel_date(date1):
    temp = datetime.datetime(1899, 12, 30)
    delta = datetime.datetime.fromtimestamp(date1) - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


def get_start_of_the_day():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day)
    return start.timestamp()


conn = sqlite3.connect('weather.db')
c = conn.cursor()
rows = c.execute('SELECT * FROM weather')

prepared_rows = []
start = get_start_of_the_day()
for row in rows:
    t1, t2, t3, t4, tc, t0, pr, hm, fr, ml, ts, mtime, footprint = row
    if mtime < start:
        continue
    prepared_rows.append([t1, t2, t3, t4, tc, t0, pr, hm, excel_date(mtime)])


wb = xlwt.Workbook()
ws = wb.add_sheet('weather')
ws.write(0, 0, 'T1')
ws.write(0, 1, 'T2')
ws.write(0, 2, 'T3')
ws.write(0, 3, 'T4')
ws.write(0, 4, 'Коллектор')
ws.write(0, 5, 'Контроллер')
ws.write(0, 6, 'Давление')
ws.write(0, 7, 'Влажность')
ws.write(0, 8, 'Время')

for i, row in enumerate(prepared_rows):
    for j, el in enumerate(row):
        ws.write(i + 1, j, row[j])

wb.save('weather.xls')

import sqlite3
import sys
import os
import argparse
import random

CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS (?)
                (id INTEGER PRIMARY KEY, ethernetMac TEXT UNIQUE, wirelessMac TEXT UNIQUE)'''
TABLE_NAME= "macid"

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("dbname", help="name for the database, where the dataset will be stored")
    parser.add_argument("N", type=int, help="Number of devices")
    args = parser.parse_args()
    return args


def randomMAC():
    #set the locally administered and clear the multicast bit
	mac = [
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac))


def getcurrentsize(cursor):
    cursor.execute(''' SELECT COUNT(*) FROM macid''')
    result = cursor.fetchone()
    return result[0]


def getMacPair():
    ethernetMac = randomMAC()
    wirelessMac = randomMAC()
    while wirelessMac == ethernetMac:
        wirelessMac = randomMAC()
    return (ethernetMac, wirelessMac)


def main(dbname, N):
    with sqlite3.connect(dbname) as conn:
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS macid
                (id INTEGER PRIMARY KEY, ethernetMac TEXT UNIQUE, wirelessMac TEXT UNIQUE)''')

        currentNumberOfId = getcurrentsize(cursor)
        for id in range(currentNumberOfId, N):
            res = False
            while not res:
                ethernetMac, wirelessMac = getMacPair()
                try:
                    cursor.execute('INSERT INTO macid VALUES (?,?,?)', (id,ethernetMac, wirelessMac))
                    res = cursor.rowcount
                except sqlite3.IntegrityError:
                    res = cursor.rowcount                                


if __name__ == "__main__":
    args = get_options()
    print(args.dbname, args.N)
    main(args.dbname, args.N)
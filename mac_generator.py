#!/usr/bin/python3

import random
#
def randomMAC():
    #set the locally administered and clear the multicast bit
	mac = [ 0x02, 0x00, 0x00,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac))

def main(n):
    print("id, ethernet address, wireless address")
    for i in range(n):
        ethernetMac = randomMAC()
        wirelessMac = randomMAC()
        while wirelessMac == ethernetMac:
            wirelessMac = randomMAC()
        print("{0},{1},{2}".format(i, ethernetMac, wirelessMac))

if __name__ == "__main__":
    n = int(input())
    main(n)
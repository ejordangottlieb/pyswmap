#!/usr/bin/python3

# There is still a great deal of work required on this module.  Please
# use with caution.
# -Jordan 

import sys
from ipaddress import (
        IPv6Address,
        IPv6Network,
        ip_network,
        ip_address,
        )
from math import (
        log,
        )

class MapCalc(object):

    def __init__(self,rulev6,rulev4):
        self.ealen = False
        self.psidoffset = False
        self.ratio = False
        self.portranges = False
        try:
            self.rulev4mask = ip_network(
                        rulev4,
                        strict=False
                        ).prefixlen
        except ValueError: 
            print("Invalid IPv4 prefix {}".format(rulev4))
            sys.exit(1)
        try:
            self.rulev6mask = IPv6Network(
                        rulev6,
                        strict=False
                        ).prefixlen
        except ValueError:
            print("Invalid IPv6 prefix {}".format(rulev6))
            sys.exit(1)

        self.rulev4 = rulev4
        self.rulev6 = rulev6

    def _psid_range(self,x):
        rset = []
        for i in range(0,x+1):
            rset.append(2**i)
        return rset

    def calc_ea(self):
        if self.ratio not in ( self._psid_range(16) ):
            sys.exit(1)

        if ( 1 == self.ratio):
            self.psidbits = 0
        else:
            self.psidbits = int(log(self.ratio,2))
        self.ealen = self.psidbits + ( 32 - self.rulev4mask )
        self.portbits = 16 - self.psidoffset - self.psidbits

    def calc_ratio(self):
        self.psidbits = self.ealen - ( 32 - self.rulev4mask )
        self.ratio = 2**self.psidbits
        self.portbits = 16 - self.psidoffset - self.psidbits

    def gen_psid(self,portnum):
        if ( portnum < self.start_port() ):
            print("port value is less than allowed by PSID Offset")
            sys.exit(1)
        self.psid = (portnum & ((2**self.psidbits - 1) << self.portbits)) \
                    >> self.portbits
        return self.psid

    def port_ranges(self):
        return 2**self.psidoffset - 1

    def start_port(self):
        return 2**(16 - self.psidoffset)

    def port_list(self):
        startrange = self.psid * (2**self.portbits) + self.start_port()
        increment = (2**self.psidbits) * (2**self.portbits)
        portlist = [ ]
        for port in range(startrange,startrange + 2**self.portbits):
            portlist.append(port)
        for x in range(1,self.port_ranges()):
            startrange += increment
            for port in range(startrange,startrange + 2**self.portbits):
                portlist.append(port)
        self.portlist = portlist
        return portlist

    def ipv4_index(self,ipv4addr):
        if ip_address(ipv4addr) in ip_network(self.rulev4):
            x = ip_address(ipv4addr)
            y = ip_network(self.rulev4,strict=False).network_address
            self.ipv4addr = x
            return ( int(x) - int(y) )
        else:
            print("Error: IPv4 address {} not in Rule IPv4 subnet {}".format(
                  ipv4add,
                  ip_network(self.rulev4,strict=False).network_address))
            sys.exit(1)

    def gen_mapaddr(self,ipv4index):
        addroffset = 128 - (self.rulev6mask + ( self.ealen - self.psidbits))
        psidshift = 128 - ( self.rulev6mask + self.ealen )
        mapaddr = IPv6Network(self.rulev6,strict=False).network_address
        mapaddr = int(mapaddr) | ( ipv4index << addroffset )
        mapaddr = mapaddr | ( self.psid << psidshift)
        self.pd = "{}/{}".format(
                                   IPv6Address(mapaddr),
                                   self.rulev6mask + self.ealen
                                )
        mapce = mapaddr | ( int(self.ipv4addr) << 16 )
        mapce = mapce | self.psid
        self.mapce = "{}".format(IPv6Address(mapce))

if __name__ == "__main__":
    # A quick example showing current module capabilities:
    # The next four lines are used to supply the BMR
    # The MAP IPv4 and IPv6 rule prefixes
    m = MapCalc("fd80::/48","24.50.100.0/24")
    # Set the PSID offset utilized in the forthcoming calculations
    m.psidoffset = 6
    # Supply ratio instead of EA length.  Either will work
    m.ratio = 64

    # Ratio was given so calculate EA length.  Also calc PSID and Port Bits
    m.calc_ea()

    # Using EA length value instead of ratio
    # m.ealen = 5
    # m.calc_ratio()

    # Supply arbitrary layer-4 port that is valid given PSID Offset used
    # to calculate the PSID.
    portvalue = 1024
    m.gen_psid(portvalue)

    # Supply an IPv4 address from IPv4 rule prefix and use it and the 
    # PSID calculated in the previous statement to generate the MAP CE
    # address and parent PD.  We must first feed it to the ipv4_index()
    # method in order to get the integer index value for the IPv4 address.
    sharedv4 = "24.50.100.100"
    m.gen_mapaddr(m.ipv4_index(sharedv4))

    # Print out some of the pertinent information
    print("\n\n")
    print("################################################")
    print("BMR:")
    print("    Rule IPv6 Prefix: {}".format(m.rulev6))
    print("    Rule IPv4 Prefix: {}".format(m.rulev4))
    print("    PSID Offset:      {}".format(m.psidoffset))
    print("    Sharing Ratio:    {} to 1".format(m.ratio))
    print("    EA Length:        {}".format(m.ealen))
    print("Shared IPv4 and Port Session State:")
    print("    Shared IPv4:      {}".format(sharedv4))
    print("    Port:             {}".format(portvalue))
    print("Other Calculated Values:")
    print("    Port Bits:        {}".format(m.portbits))
    print("    Ranges Allocated: {}".format(2**m.psidoffset - 1))
    print("    PSID Bits:        {}".format(m.psidbits))
    print("################################################")
    print("------------------------------------------------")
    print("PSID: {}".format(m.psid))
    print("PD for this client is: {}".format(m.pd))
    print("MAP CE Address is: {}".format(m.mapce))
    print("------------------------------------------------")
    print("Output to follow will include the full range of ports assigned")
    print("to calculated PSID.")
    print("Note: This can result in a really long list up to 2^16")
    raw_input = vars(__builtins__).get('raw_input',input)
    raw_input("Press the ENTER/RETURN key to continue")
    print("\n")
    print(m.port_list())
    

    

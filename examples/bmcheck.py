#!/usr/bin/env python3

import sys
from pyswmap import MapCalc

# This script calculates the originating IPv6 prefix and MAP IPv6
# address for a particular flow in and out of the BR towards the
# IPv4 domain (typically the Internet).
#
# This script is intended to demonstrate how to programatically associate
# a MAP customer with a particular network flow out on the IPv4 Internet. 
# For instance, this could be used to link a particular abuse complaint
# with a particular broadband MAP installation.  

# Syntax is as follows:
#  bmcheck.py [originating IP] [originating port]

# Define MAP domain characteristics.  The values may be changed to suite
# a alternate MAP domain configurations.
m = MapCalc( rulev6='fd80::/48',
             rulev4='24.50.100.0/24',
             #psidoffset=6,
             ratio=64,
             #ealen=14,
                   )

# Extract the port value from the second command line variable.  This can be
# any TCP/UDP port or ICMP identifier.
portvalue = int(sys.argv[2])

# Obtain the PSID given a particular port value.
psid = m.gen_psid(portvalue)

# Extract the originating public IPv4 address from the first command line
# variable.  This should be an address from the rule IPv4 prefix.
sharedv4 = sys.argv[1]

# Generate the IPv6 MAP CE address
mapce = m.get_mapce_addr(sharedv4,psid)

# Generate the IPv6 MAP end-user prefix
pd = m.get_mapce_prefix(sharedv4,psid)

# Print out some of the pertinent user supplied and calculated values
print("\n\n")
print("------------------------------------------------")
print("PD for this client is: {}".format(pd))
print("MAP CE Address is: {}".format(mapce))
print("------------------------------------------------")
print("\n")

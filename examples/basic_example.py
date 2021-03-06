#!/usr/bin/env python
import sys
sys.path.append('..')

from pyswmap import MapCalc

# A quick example showing current module capabilities:
# We create a new instance of class MapCalc and supply the BMR
# with the following values:
# 1.  The IPv6 rule prefix: rulev6      (a string) 
# 2.  The IPv4 rule prefix: rulev4      (a string)
# 3.  The PSID Offset:      psidoffset  (an integer)
#     Note: In the absence of this value a default of 6 will be used 
#
# One of the two following values:
# 4a. The Sharing Ratio:    ratio       (an integer)
#                    or
# 4b. The EA Length:        ealen       (an integer)
#
# This will result in the both calculated and validated class variables:
#
#                  m.rulev4:     The IPv4 rule prefix used by a particular
#                                mapping rule.
#
#                  m.rulev6:     The IPv6 rule prefix used by a particular
#                                mapping rule.
#
#                  m.rulev4mask: The number of bits in the IPv4 rule subnet
#                                mask.
#
#                  m.rulev6mask: The number of bits in the IPv6 rule subnet
#                                mask.
#
#                  m.ealen:      The number of Embedded Address (EA) bits.
#
#                  m.ratio:      The sharing ratio of # of users per IPv4
#                                address.  This is 2 to the power of bits
#                                in the PSID field.
#
#                  m.psidoffset: The PSID Offset value.  Defined as the
#                                "A" field in the IETF MAP specification.
#
#                  m.portbits:   The number of contiguous ports as defined
#                                by the "m bits" in the IETF MAP 
#                                specification.
#
#                  m.psidbits:   The length in bits of the PSID field.  It
#                                is defined as the "k bits" in the IETF MAP
#                                specification.
#
m = MapCalc( rulev6='fd80::/48',
             rulev4='24.50.100.0/24',
             #psidoffset=6,
             ratio=64,
             #ealen=14,
                   )
# Supply arbitrary layer-4 port that is valid given PSID Offset to 
# gen_psid method.  This will return the following value:
#                  psid:         The port-set ID which defines the
#                                algorithmically assigned ports unique to
#                                a particular MAP CE.
portvalue = 40000
psid = m.gen_psid(portvalue)


# A single address from the IPv4 rule prefix
sharedv4 = '24.50.100.100'

# Supply the IPv4 address from IPv4 rule prefix and PSID to get_mapce_addr
# method and use them to return:
#                      
#                  mapece:       The MAP IPv6 address.  This address
#                                is used to reach the MAP functions
#                                of a provisioned/configured MAP CE.
mapce = m.get_mapce_addr(sharedv4,psid)

# Supply an IPv4 address from IPv4 rule prefix and PSID to get_mapce_prefix
# method and use them to return:
#                  pd:           The end-user IPv6 prefix. Typically,
#                                but not exclusively DHCPv6 PD.  Can
#                                also be assigned via SLAAC or configured
#                                manually.  

pd = m.get_mapce_prefix(sharedv4,psid)

# Detailed definitions are available in draft-ietf-softwire-map.

# Print out some of the pertinent user supplied and calculated values
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
print("PSID: {}".format(psid))
print("PD for this client is: {}".format(pd))
print("MAP CE Address is: {}".format(mapce))
print("------------------------------------------------")
print("Output to follow will include the full range of ports assigned")
print("to calculated PSID.")
print("Note: This can result in a really long list up to 2^16")
raw_input = vars(__builtins__).get('raw_input',input)
raw_input("Press the ENTER/RETURN key to continue")
print("\n")
# Print out list of ports for session PSID
print(m.port_list(psid))

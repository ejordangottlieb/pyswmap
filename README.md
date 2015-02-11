pyswmap
=======

This is a IETF Softwires Working Group MAP (MAP-E and MAP-T) Python 3 module.  It currently accepts BMR entry in using either or both "Sharing Ratio" and "EA length."  It can also calculate the PSID by BMR and session IPv4 port.  Session end-user IPv6 PD and MAP CE address can be calculated by supplied BMR, IPv4 session port, and IPv4 session address.

Usage and Example
=================

A quick example showing current module capabilities:
We create a new instance of class MapCalc and supply the BMR
with the following values:

1.  The IPv6 rule prefix: rulev6      (a string) 
2.  The IPv4 rule prefix: rulev4      (a string)
3.  The PSID Offset:      psidoffset  (an integer)
    Note: In the absence of this value a default of 6 will be used 
4.  One of the two following values (both can be supplied if the resulting
calculations is equivalent):

- The Sharing Ratio:    ratio       (an integer)
<p>or</p>
- The EA Length:        ealen       (an integer)
 
This will result in the both calculated and validated class variables:
- m.rulev4: The IPv4 rule prefix used by a particular mapping rule.
- m.rulev6: The IPv6 rule prefix used by a particular mapping rule.
- m.rulev4mask: The number of bits in the IPv4 rule subnet mask.
- m.rulev6mask: The number of bits in the IPv6 rule subnet mask.
- m.ealen: The number of Embedded Address (EA) bits.
- m.ratio: The sharing ratio of # of users per IPv4
address.  This is 2 to the power of bits in the PSID field.
- m.psidoffset: The PSID Offset value.  Defined as the
"A" field in the IETF MAP specification.
- m.portbits: The number of contiguous ports as defined
by the "m bits" in the IETF MAP specification.
- m.psidbits: The length in bits of the PSID field.  It
is defined as the "k bits" in the IETF MAP specification.
 
```python
m = pyswmap.MapCalc( rulev6='fd80::/48',
                     rulev4='24.50.100.0/24',
                     #psidoffset=6,
                     ratio=64,
                     #ealen=14,
                   )
```

Supply arbitrary layer-4 port that is valid given PSID Offset to 
gen_psid method.  This will calculate the following values:
- m.psid: The port-set ID which defines the
algorithmically assigned ports unique to
a particular MAP CE.
- m.port_list:  The full list of ports assigned by a 
particular PSID.  This attribute is
a Python list.

```python
portvalue = 40000
m.gen_psid(portvalue)
```

Supply an IPv4 address from IPv4 rule prefix and PSID to gen_mapaddr
method and use them to calculate the following values:

- m.pd: The end-user IPv6 prefix. Typically,
but not exclusively DHCPv6 PD.  Can
also be assigned via SLAAC or configured manually.
- m.mapce: The MAP IPv6 address.  This address
is used to reach the MAP functions
of a provisioned/configured MAP CE.
                                 
Detailed definitions for all the variables discussed in this README
are available in https://tools.ietf.org/html/draft-ietf-softwire-map.

```python
sharedv4 = '24.50.100.100'
m.gen_mapaddr(sharedv4,m.psid)
```

Print out some of the pertinent user supplied and calculated values
```python
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
```

Print out list of ports for session PSID

```python
print(m.port_list)
```

 
ACKNOWLEDGEMENTS
================

This code has been inspired or uses some parts of the following:

* Cisco MAP Simulation Tool

  http://map46.cisco.com

* Stateless NAT46 Linux kernel module implementation by Andrew Yourchenko

  https://github.com/ayourtch/nat46

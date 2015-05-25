pyswmap
=======

This is a IETF Softwires Working Group MAP (MAP-E and MAP-T) Python 3 module.  It currently contains two classes:

- MapCalc: This class provides a set of medthods and attributes derived from the definition of a Base Mapping Rule(BMR).
- DmrCalc: This class provides a set of methods and attributes in support of a MAP-T Defualt Mapping Rule (DMR)

## Using the MapCalc Class ##

### Initial Steps ###
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
 
The code following code snippet demonstrates the creation of a new MapCalc
object.  The optional attributes have been included in this example but have been commented out.  The psidoffset reflects the default value of 6 while the ealen has been set to reflect the caclulated value given a ratio of 64.
 
```python
m = pyswmap.MapCalc( rulev6='fd80::/48',
                     rulev4='24.50.100.0/24',
                     #psidoffset=6,
                     ratio=64,
                     #ealen=14,
                   )
```

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

### Calculating Values Based on BMR  ###

#### Given a Layer-4 Port Return the PSID Which Contains it ####
Supply arbitrary layer-4 port that is valid given PSID Offset to 
gen_psid method.  This will calculate the following values:
- m.psid: The port-set ID which defines the
algorithmically assigned ports unique to
a particular MAP CE.

```python
portvalue = 40000
psid = m.gen_psid(portvalue)
```

#### Determine the Originating IPv6 End-User Prefix and MAP Address ####
Supply an IPv4 address from IPv4 rule prefix and PSID to gen_mapaddr
method and use them to calculate the following values:

- m.pd: The end-user IPv6 prefix. Typically,
but not exclusively DHCPv6 PD.  Can
also be assigned via SLAAC or configured manually.
- m.mapce: The MAP IPv6 address.  This address
is used to reach the MAP functions
of a provisioned/configured MAP CE.

In the example below we assume the PSID has been obtain by issuing the
gen_psid() method as shown in the preceeding example.
                                 
```python
sharedv4 = '24.50.100.100'       # An address from the IPv4 rule prefix
m.gen_mapaddr(sharedv4,m.psid)
print(m.pd)                      # Print the end-user IPv6 prefix
print(m.mapce)                   # Print the MAP IPv6 address
```

#### Obtain the List of Ports Assigned to a Particular PSID ####
This method will return a Python list with a complete list of ports for the instance's psid attribute.

```python
m.psid = 4                       # Set the PSID value (need to write "setter")
psidlist = m.port_list()         # Obtain the set of ports for the PSID
```

Detailed definitions for all the variables discussed in this README
are available in https://tools.ietf.org/html/draft-ietf-softwire-map.

 
ACKNOWLEDGEMENTS
================

This code has been inspired or uses some parts of the following:

* Cisco MAP Simulation Tool

  http://map46.cisco.com

* Stateless NAT46 Linux kernel module implementation by Andrew Yourchenko

  https://github.com/ayourtch/nat46

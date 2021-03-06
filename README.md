pyswmap
=======

This is a IETF Softwires Working Group MAP (MAP-E and MAP-T) Python module.  It currently contains two classes:

- MapCalc: This class provides a set of medthods and attributes derived from the definition of a Base Mapping Rule(BMR).
- DmrCalc: This class provides a set of methods and attributes in support of a MAP-T Defualt Mapping Rule (DMR). 

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
from pyswmap import MapCalc

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
gen_psid method.  This will return the following value:
- psid: The port-set ID which defines the
algorithmically assigned ports unique to
a particular MAP CE.

```python
portvalue = 40000
psid = m.gen_psid(portvalue)
```

#### Determine the Originating IPv6 End-User Prefix and MAP Address ####
Supply an IPv4 address from IPv4 rule prefix and a unique PSID to get_mapce_addr
and get_mapce_prefix methods and use them to calculate the following values:

- mapce: The MAP IPv6 address.  This address
is used to reach the MAP functions
of a provisioned/configured MAP CE.
- pd: The end-user IPv6 prefix. Typically,
but not exclusively DHCPv6 PD.  Can
also be assigned via SLAAC or configured manually.

In the example below we supply a valid IPv4 address from the IPv4 rule prefix (sharedv4)
and a valid PSID value (psid) to allow us to obtain the mapce and pd values:
                                 
```python
sharedv4 = '24.50.100.100'       # An address from the IPv4 rule prefix
psid = 4                         # A PSID integer value of 4
mapce = m.get_mapce_addr(sharedv4,psid)
pd = m.get_mapce_prefix(sharedv4,psid)
print(mapce)                   # Print the MAP IPv6 address
print(pd)                      # Print the end-user IPv6 prefix
```

#### Obtain the List of Ports Assigned to a Particular PSID ####
This method will return a Python list with a complete list of ports for the instance's psid attribute.

```python
psid = 10                        # An example PSID value 
psidlist = m.port_list(psid)     # Obtain the set of ports for the PSID
```

Detailed definitions for all the variables discussed in this README
are available in https://tools.ietf.org/html/draft-ietf-softwire-map.

## Using the DmrCalc Class ##

### Basic Example ###
We create a new instance of class DmrCalc and supply the DMR
with the BR prefix:

```python
from pyswmap import DmrCalc

brprefix = '2001:0db8:85a3::/64'       # The instance's BR prefix
ipv4addr  = '192.0.0.1'                # An arbitrary IPv4 address to embed
m = DmrCalc(brprefix)               
embedded = m.embed_6052addr(ipv4addr)  # An RFC6052 compliant IPv6 address
```

 
ACKNOWLEDGEMENTS
================

This code has been inspired or uses some parts of the following:

* Cisco MAP Simulation Tool

  http://map46.cisco.com

* Stateless NAT46 Linux kernel module implementation by Andrew Yourchenko

  https://github.com/ayourtch/nat46

#!/usr/bin/env python

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

    def __init__(self,**bmr):
        #rulev6,rulev4):
        self.portranges = False

        # Validate and set BMR and BMR derived values 
        self._check_bmr_values(bmr)

    def _check_bmr_values(self,bmr):
        # Assume these values have not been supplied.  Validate later.
        self.ealen = False
        self.ratio = False

        # Validate that a proper PSID Offset has been set
        if 'psidoffset' not in bmr:
            # Set Default PSID Offset of 6 if it is not set 
            self.psidoffset = 6
        else:
            self.psidoffset = self._psid_offset(bmr['psidoffset'])

        # Validate that a proper IPv4 rule prefix is defined
        if 'rulev4' not in bmr:
            print("The rule IPv4 prefix has not been set")
            sys.exit(1)
        else:
            self.rulev4 = self._ipv4_rule(bmr['rulev4'])

        # Validate that a proper IPv6 rule prefix is defined
        if 'rulev6' not in bmr:
            print("The rule IPv6 prefix has not been set")
            sys.exit(1)
        else:
            self.rulev6 = self._ipv6_rule(bmr['rulev6'])

        # Check if EA length was passed
        if 'ealen' not in bmr:
            self.ealen = False
        else:
            self.ealen = bmr['ealen']
            self.ratio = self._calc_ratio(bmr['ealen'])

        # Check if sharing ratio was passed or calculated by _calc_ratio
        if 'ratio' not in bmr:
            # Skip if we have already calculated ratio
            if not (self.ratio):
                self.ratio = False
        else:
            if (self.ealen):
                # Check to see if supplied EA length contradicts supplied ratio
                if ( bmr['ratio'] != self.ratio ):
                    eavalue = "EA value {}".format(self.ealen)
                    sharingratio = "sharing ratio {}".format(bmr['ratio'])
                    print("Supplied {} and {} are contradictory".format(
                                                                  eavalue,
                                                                  sharingratio)
                         )
                    sys.exit(1)
            else:
                self.ratio = bmr['ratio']
                self.ealen = self._calc_ea(bmr['ratio'])

        # EA length or sharing ratio must be set
        if not ( self.ealen or self.ratio):
            print("The BMR must include an EA length or sharing ratio")
            sys.exit(1)

        # Since we have not hit an exception we can calculate the port bits
        self.portbits = self._calc_port_bits()

    def _ipv4_rule(self,rulev4):
        try:
            self.rulev4mask = ip_network(
                        rulev4,
                        strict=False
                        ).prefixlen
        except ValueError: 
            print("Invalid IPv4 prefix {}".format(rulev4))
            sys.exit(1)

        self.rulev4object = ip_network(rulev4)

        return rulev4

    def _ipv6_rule(self,rulev6):
        try:
            self.rulev6mask = IPv6Network(
                        rulev6,
                        strict=False
                        ).prefixlen
        except ValueError:
            print("Invalid IPv6 prefix {}".format(rulev6))
            sys.exit(1)

        return rulev6

    def _psid_offset(self,psidoffset):
        PSIDOFFSET_MAX = 6
        if psidoffset in range(0,PSIDOFFSET_MAX+1):
            return psidoffset
        else:
            print("Invalid PSID Offset value: {}".format(psidoffset))
            sys.exit(1)

    def _psid_range(self,x):
        rset = []
        for i in range(0,x+1):
            rset.append(2**i)
        return rset

    def _calc_port_bits(self):
        portbits = 16 - self.psidoffset - self.psidbits
        return portbits

    def _calc_ea(self,ratio):
        if ratio not in ( self._psid_range(16) ):
            print("Invalid ratio {}".format(ratio))
            print("Ratio between 2 to the power of 0 thru 16")
            sys.exit(1)

        if ( 1 == ratio):
            self.psidbits = 0
        else:
            self.psidbits = int(log(ratio,2))
        ealen = self.psidbits + ( 32 - self.rulev4mask )
        return ealen

    def _calc_ratio(self,ealen):
        maskbits = 32 - self.rulev4mask
        if ( ealen < maskbits ):
            print("EA of {} incompatible with rule IPv4 prefix {}".format(
              ealen,
              self.rulev4,
              )
            )
            print("EA length must be at least {} bits".format(
              maskbits,
              )
            )
            sys.exit(1)

        self.psidbits = ealen - ( 32 - self.rulev4mask )
        if ( self.psidbits > 16):
            print("EA length of {} is too large".format(
              ealen,
              )
            )
            print("EA should not exceed {} for rule IPv4 prefix {}".format(
              maskbits + 16,
              self.rulev4,
              )
            )
            sys.exit(1)
        ratio = 2**self.psidbits
        return ratio

    def gen_psid(self,portnum):
        if ( portnum < self.start_port() ):
            print("port value is less than allowed by PSID Offset")
            sys.exit(1)
        psid = (portnum & ((2**self.psidbits - 1) << self.portbits))
        psid = psid >> self.portbits
        return psid

    def port_ranges(self):
        return 2**self.psidoffset - 1

    def start_port(self):
        if self.psidoffset == 0: return 0  
        return 2**(16 - self.psidoffset)

    def port_list(self,psid):
        startrange = psid * (2**self.portbits) + self.start_port()
        increment = (2**self.psidbits) * (2**self.portbits)
        portlist = [ ]
        for port in range(startrange,startrange + 2**self.portbits):
            if port >= 65536: continue
            portlist.append(port)
        for x in range(1,self.port_ranges()):
            startrange += increment
            for port in range(startrange,startrange + 2**self.portbits):
                portlist.append(port)
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

    def _calc_ipv6bit_pos(self):
        addroffset = 128 - (self.rulev6mask + ( self.ealen - self.psidbits))
        psidshift = 128 - ( self.rulev6mask + self.ealen )
        return [addroffset,psidshift]

    def _append_map_eabits(self,ipv4index,addroffset,psidshift,psid):
        rulev6base = IPv6Network(self.rulev6,strict=False).network_address
        map_prefix = int(rulev6base) | ( ipv4index << addroffset )
        map_fullprefix = map_prefix | ( psid << psidshift)
        return map_fullprefix
        

    def get_mapce_addr(self,ipv4addr,psid):
        ipv4index = self.ipv4_index(ipv4addr)
        (addroffset,psidshift) = self._calc_ipv6bit_pos()
        map_fullprefix = self._append_map_eabits(ipv4index,
                                                 addroffset,
                                                 psidshift,
                                                 psid)
        mapv4iid = map_fullprefix | ( int(self.ipv4addr) << 16 )
        map_full_address = mapv4iid | psid
        mapce_address = "{}".format(IPv6Address(map_full_address))
        return mapce_address

    def get_mapce_prefix(self,ipv4addr,psid):
        ipv4index = self.ipv4_index(ipv4addr)
        (addroffset,psidshift) = self._calc_ipv6bit_pos()
        map_fullprefix = self._append_map_eabits(ipv4index,
                                                 addroffset,
                                                 psidshift,
                                                 psid)
        mapce_prefix = "{}/{}".format(
                                   IPv6Address(map_fullprefix),
                                   self.rulev6mask + self.ealen
                                )
        return mapce_prefix

    def get_ceea_bits(self,mapce_address):
        mask = 2**(self.ealen) - 1
        maskshift = ( 128 - self.rulev6mask - self.ealen)
        eabits = (int(IPv6Address(mapce_address)) & 
                 ( mask << maskshift )) >> maskshift 
        return eabits 

    def get_map_ipv4(self,mapce_address):
        eabits = self.get_ceea_bits(mapce_address)
        ipv4 = (int(IPv6Address(mapce_address)) & ( 0xffffffff << 16 )) >> 16
        address4 = '{}'.format(ip_address(ipv4))
        if ( self.rulev4mask == 32 ):
            rule4addr = '{}'.format(self.rulev4object[0])
            if ( rule4addr != address4 ):
                return None
                #print('{} in IID does not match rule IPv4 {}/32'.format(
                #      address4, rule4addr))
                #sys.exit(1)
        else:
            addrbits = self.ealen - self.psidbits
            addrmask = 2**addrbits - 1
            addrindex = ( ( eabits & ( addrmask << self.psidbits ))
                         >> self.psidbits )
            rule4addr = '{}'.format(self.rulev4object[addrindex])
            if ( rule4addr != address4 ):
                return None
                #print('{} in IID does not match EA bits IPv4 {}'.format(
                #      address4, rule4addr))
                #sys.exit(1)
            
        return address4

    def get_map_psid(self,mapce_address):
        iid = (int(IPv6Address(mapce_address)) & 0xffff )
        eabits = self.get_ceea_bits(mapce_address)
        if ( self.psidbits == 0 ):
            if ( iid != 0):
                return None
                #print('Number of PSID bits is 0 while IID contains {}'.format(
                #      iid))
                #sys.exit(1)
        else:
            psidmask = 2**self.psidbits - 1
            eapsid = eabits & psidmask
            if ( iid != eapsid ):
                return None
                #print('IID PSID contains {} different from EA {}'.format(
                #      iid, eapsid))
                #sys.exit(1)
            
        return int(iid)

    def get_mapce_bmr(self,mapce_address):

        try:
            v6addr = IPv6Address(mapce_address)
        except:
            return None

        ipv4addr = self.get_map_ipv4(mapce_address)
        if ( ipv4addr == None):
            return None

        psidval = self.get_map_psid(mapce_address)
        if ( psidval == None):
            return None

        # Check to see if MAP CE Address belongs to the base 64 prefix.
        # I am not supporting a user prefix with a prefix length > 64
        v6userprefix = IPv6Network(self.get_mapce_prefix(ipv4addr,psidval))
        v6base64 = '{}/64'.format(v6userprefix.network_address)
        if ( v6addr not in IPv6Network(v6base64) ):
            return None
        
         
        return ( { ipv4addr: psidval } )


class DmrCalc(object):

    def __init__(self,dmr):

        # Validate and set BMR and BMR derived values 
        self.dmrprefix = self._check_dmr_prefix(dmr)

    def embed_6052addr(self,ipv4addr):

        try:
            ipv4addrint = int(ip_address(ipv4addr))
        except ValueError:
            print("Invalid IPv4 address {}".format(ipv4addr))
            sys.exit(1)

        if ( self.dmrprefix.prefixlen == 64 ):
            ipv6int = ipv4addrint << 24
            ipv6int += int(self.dmrprefix.network_address)
            return IPv6Address(ipv6int)

    def _check_dmr_prefix(self,dmrprefix):
        try:
            self.dmrmask = IPv6Network(
                        dmrprefix,
                        strict=False
                        ).prefixlen
        except ValueError:
            print("Invalid IPv6 prefix {}".format(prefix))
            sys.exit(1)

        if self.dmrmask not in (32,40,48,56,64,96):
            print("Invalid prefix mask /{}".format(self.dmrmask))
            sys.exit(1)

        return IPv6Network(dmrprefix)

if __name__ == "__main__":
    m = DmrCalc('fd80::/48')
    print(m.dmrprefix)

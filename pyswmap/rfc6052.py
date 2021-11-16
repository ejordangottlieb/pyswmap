#!/usr/bin/env python3

from ipaddress import IPv4Network
from ipaddress import IPv6Network


def gen_iid(ipv4, style):
    if ( style == 64):
        return ( int(ipv4) << 24)

def gen_4mapped6(net4,ipv6,iid):
    if (net4.prefixlen == 32):
        print("{} {}".format(str(net4), ipv6[iid].compressed))
    else:
        addr6 = str(ipv6[iid].exploded)
        prefixlen = (128 - 24) - (32 - net4.prefixlen)
        prefix6 = "{}/{}".format(addr6,prefixlen)
        mprefix = IPv6Network(prefix6)
        print("{} {}".format(str(net4),mprefix))

if __name__ == "__main__":
    dmrs = [ "64:ff9b:1::/64", 
             "64:ff9b:1:fff0::/64", 
             "64:ff9b:1:fff1::/64" ]
    ip4s = [ "96.37.171.48/32",
             "96.37.171.49/32",
             "96.37.171.50/32",
             "96.37.171.51/32",
             "96.37.171.52/32",
             "96.37.171.53/32",
             "96.37.171.54/32",
             "96.37.171.55/32",
             "96.37.171.0/24" ]
    for ip4 in ip4s:
        net4 = IPv4Network(ip4)
        ipv4 = net4[0]
        iid = gen_iid(ipv4, 64)
        for dmr in dmrs:
            ipv6 = IPv6Network(dmr)
            gen_4mapped6(net4,ipv6,iid)

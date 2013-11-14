

def iptoint(ip):
    hexn = ''.join(["%02X" % long(i) for i in ip.split('.')])

    return long(hexn, 16)


def inttoip(n):
    d = 256 * 256 * 256
    q = []
    while d > 0:
        m, n = divmod(n,d)
        q.append(str(m))
        d /= 256

    return '.'.join(q)

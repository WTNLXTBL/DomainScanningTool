#!/usr/bin/env python

import binascii
import socket
import random
import os

DEFAULT_SERVER = '1.1.1.1'
DEFAULT_PORT = 53
AUTHOR = 'dynos01'
EMAIL = 'i@dyn.im'
VERSION = '1.0.3'

def send(message, server, port):
    """
    Sends UDP packet to server and waits for response.

    Args:
        message: Encoded data, which will be sent.
        server: DNS server address. both IPv4 and IPv6 are supported.
        port: DNS server port.

    Returns:
        A string containing raw response.
    """
    message = message.strip()
    addr = (server, port)

    if '.' in server:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    try:
        s.sendto(binascii.unhexlify(message), addr)
        data, address = s.recvfrom(4096)
    finally:
        s.close()

    return binascii.hexlify(data).decode()

def buildMessage(domain):
    """
    Creates a DNS request according to RFC2929. Attributes other than domain name are hard-coded.

    Args:
        domain: The domain name to be checked.

    Returns:
        A string containing raw DNS request.
    """
    message = '{:04x}'.format(random.randint(0, 65535)) #Generate an random request ID
    message += '01000001000000000000'

    #Encode parts of the given domain name into our request
    addr = domain.split('.')
    for i in addr:
        length = '{:02x}'.format(len(i))
        addr = binascii.hexlify(i.encode())
        message += length
        message += addr.decode()

    message += '0000060001'

    return message

def validateServer(ip, port):
    """
    Checks if the given IP-port combination is valid.

    Args:
        ip: IPv4 or IPv6 address.
        port: Port number.

    Returns:
        A bool value. True for valid and False for invalid.
    """
    if port <= 0 or port > 65535:
        return False

    try:
        if '.' in ip:
            socket.inet_pton(socket.AF_INET, ip)
        else:
            socket.inet_pton(socket.AF_INET6, ip)
    except:
        return False

    return True

def check(domain, server, port):
    """
    Sends the request, reads the raw response and checks the ANCOUNT attribute according to RFC2929.

    Args:
        domain: Domain name to be checked.
        server: DNS server to check against.
        port: DNS server port.

    Returns:
        A bool value representing if the domain exists.

    """
    message = buildMessage(domain)
    response = send(message, server, port)
    rcode = '{:b}'.format(int(response[4:8], 16)).zfill(16)[12:16]
    return False if rcode == '0011' else True

def main():
    print('域名扫描工具 版本 %s' % VERSION)
    print('作者: %s <%s>' % (AUTHOR, EMAIL))

    server = []
    port = []
    dns = input('请输入DNS服务器列表（IPv4或IPv6），该列表将用于检查： ')
    if len(dns) == 0:
        server.append(DEFAULT_SERVER)
        port.append(DEFAULT_PORT)
    else:
        dns = dns.split(',')
        for i, item in enumerate(dns):
            item = item.strip()
            if '[' in item:
                s = item.split(']')[0][1:]
                p = item.split(']')[1][1:]
            else:
                s = item.split(':')[0]
                p = item.split(':')[1]
            p = int(p)
            if not validateServer(s, p):
                print('无效DNS服务器')
                return
            server.append(s)
            port.append(p)

    tld = input('请输入要扫描的后缀。如果要一次扫描多个后缀，请使用逗号分隔列表。 \n')
    tld = tld.split(',')
    for i, item in enumerate(tld):
        tld[i] = item.strip()

    dictFile = input('请输入字典文件路径 \n')
    if not os.access(dictFile, os.R_OK):
        print('无法读取字典文件 ')
        return

    resultFile = input('如果要将结果保存到文件，请输入其路径。否则，请按Enter键 \n')
    if len(resultFile) > 0:
        result = open(resultFile, 'a')

    verbose = False
    v = input('想要显示不可用域名吗？ [y/N]: ')
    if v.lower() == 'y':
        verbose = True

    input('信息收集完毕，回车开始扫描 ')

    for line in open(dictFile):
        for suffix in tld:
            domain = line.strip() + '.' + suffix
            i = random.choice(range(len(server)))
            if not check(domain, server[i], port[i]):
                print(domain + ' 可用 ')
                if len(resultFile) > 0:
                    result.write(domain + ' 可用 \n')
            elif verbose:
                print(domain + ' 不可用 ')
                if len(resultFile) > 0:
                    result.write(domain + ' 不可用 \n')

    print('扫描完成 ')
    if len(resultFile) > 0:
        print('结果已保存到 ' + resultFile + '.')

if __name__ == '__main__':
    main()

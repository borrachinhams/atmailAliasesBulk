#!/usr/bin/python3
import requests
import re

def authentication(proxy, target):
    url = 'http://{0}/index.php/admin/index/login'.format(target)
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate'}
    user = input("Usarname: ")
    password = input("Password: ")
    payload = {'Username': user, 'Password': password, 'Language': '', 'login.x': 0, 'login.y': 0, 'send': 1}

    if len(proxy) > 2:
        req = requests.post(url, headers=header, proxies=proxy, data=payload)
    else:
        req = requests.post(url, headers=header, data=payload)

    return req.cookies.get_dict()

def createAliases(cookieAtmail, proxy, target):
    url = 'http://{0}/index.php/admin/services/aliascreate'.format(target)
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate'}

    arq1 = input("Email Aliases list: ")
    domain = input("New domain for aliases\nEx: agetec.campogrande.ms.gov.br: ")

    for mail in open(str(arq1)):
        exchangeDomain = re.findall(r'[\w\._-]+@', mail)
        newMail = exchangeDomain[0] + domain
        payload = {'aliasType': 'Local', 'aliasFilter': '', 'EmailAlias': 'Local',
                   'AliasNameLocal': mail[:-1], 'AliasToLocal': newMail, 'AliasNameDeliver': '',
                   'AliasToDeliver': '', 'AliasNameDomain': '', 'AliasToDomain': '',
                   'AliasNameVirtual': '', 'AliasToVirtual': '', 'AliasNameMailDir': '',
                   'AliasMailDir': ''}

        try:
            if len(proxy) > 2:
                req = requests.post(url, headers=header, cookies=cookieAtmail, proxies=proxy, data=payload)
            else:
                req = requests.post(url, headers=header, cookies=cookieAtmail, data=payload)

            if 'addError' in req.text:
                print("Error: {0} for {1}".format(mail[:-1], newMail))
                print(req.text)
            else:
                print("Creating...\n{0} --> {1}".format(mail[:-1], newMail))
        except:
            print("Impossivel criar Aliases")


def checkAliases(cookieAtmail, proxy, target):
    url = 'http://{0}/index.php/admin/services/aliaslist'.format(target)
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate'}

    if len(proxy) > 2:
        req = requests.post(url, headers=header, cookies=cookieAtmail, proxies=proxy)
    else:
        req = requests.post(url, headers=header, cookies=cookieAtmail)
    return print(req.text)

if __name__ == '__main__':
    try:
        proxy = input("Using Proxy?(Y/N) ")
        target = input("URL Domain: ")

        if proxy.upper() == "Y" or proxy.upper() == "YES":
            proxy = {'http': 'http://127.0.0.1:8080'}
            cookieAtmail = authentication(proxy, target)
            createAliases(cookieAtmail, proxy, target)
            #checkAliases(cookieAtmail, proxy)
        else:
            proxy = 'N'
            cookieAtmail = authentication(proxy, target)
            createAliases(cookieAtmail, proxy, target)
            #checkAliases(cookieAtmail, proxy)
    except Exception as err:
        with open('errors.log', 'a') as f:
            f.write("{0}".format(err))
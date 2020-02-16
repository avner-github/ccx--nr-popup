# Contact Center Express not ready popup application for windows
# Created by Avner Izhar, 2020
# Licensed under GNU open source, for issues contact me at avner.izhar@gmail.com
#
#

import requests
import sys
from requests.auth import HTTPBasicAuth
import getpass
import ctypes
import time
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
if __name__ == '__main__':
    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    if len(sys.argv) < 2:
        print ('Syntax Error, missing server FQDN, please use: ccx-nr-popup.exe host.domain.suffix')
        sys.exit()
    usr01 = input('Please enter your finesse username:')
    pass01 = getpass.getpass('Please enter your finesse Password:')
    hostname1 = str(sys.argv[1])
    url = "https://"+ hostname1 +":8445/finesse/api/User/"+ usr01
    #print (url)
    counter1 = 1
    while True:
        try:
            response = requests.get(url=url, auth=HTTPBasicAuth(usr01, pass01),verify=False)
            #print (response)
            #print (response.text)
            print (str(counter1) +' checking agent status ...')
            counter1 = counter1+1
            info2parse = response.text
            if 'NOT_READY' in info2parse and 'Offhook' not in info2parse:
                nrstart = time.time()
                while 'NOT_READY' in info2parse and 'Offhook' not in info2parse:
                    time.sleep(2)
                    response = requests.get(url=url, auth=HTTPBasicAuth(usr01, pass01), verify=False)
                    info2parse = response.text
                    #print (nrstart)
                    #print (time.time() - nrstart)
                    if time.time() - nrstart > 30:
                        Mbox('Presidio Finnesse Not-Ready Alert',
                            'Agent is in not ready state !!!\n\nPlease change to ready or logout', 0x1000)
                        break
            if 'custom Cisco error page' in info2parse:
                Mbox('Presidio Finnesse Not-Ready Alert',
                     'Incorrect username or password !!!\n\nPlease re-run the application and try to login again',0x1000)
                sys.exit()

            time.sleep(10)


        except:
           errorMsg = str(sys.exc_info())
           print (errorMsg)
           if 'ConnectionError' in errorMsg:
               Mbox('Presidio Finnesse Not-Ready Alert',
                    'Unable to contact CCX server ...\n\n'+errorMsg,0x1000)
           sys.exit()


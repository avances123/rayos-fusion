#!/usr/bin/env python
import libxml2, sys, zipfile, os, os.path
import re
 
def FormateaFecha(fecha_orig):
	p = re.compile('(\d\d\d\d)/(\d\d)/(\d\d) (\d\d):(\d\d) UTC')
	resl = p.findall(fecha_orig)
	res = resl[0]
	return res[0] + '-' + res[1] + '-' + res[2] + ' ' + res[3] + ':' + res[4] + ':00'



def ParseaDescripcion(desc):
	p = re.compile('<li>(.+)</li>')
	m = p.findall(desc)
	lista = []
	resm = re.compile("Residual: (.+) us")
	res = resm.findall(m[2])[0]
	strokem = re.compile("at (\d+) WWLLN ")
	sensores = strokem.findall(m[3])[0]
	
	lista = [res,sensores]
	return lista
	

##### MAIN ######


from authorization.clientlogin import ClientLogin
from sql.sqlbuilder import SQL
import ftclient
username = 'avances123@gmail.com'
password = 'XXXXXXXXX'
token = ClientLogin().authorize(username, password)
ft_client = ftclient.ClientLoginFTClient(token)



kmz = zipfile.ZipFile(sys.argv[1])
prueba = kmz.read('lightning_src.kml')
doc = libxml2.parseDoc(prueba)
ctxt = doc.xpathNewContext()
ctxt.xpathRegisterNs('kml', "http://www.opengis.net/kml/2.2")
root = doc.getRootElement()
res = ctxt.xpathEval("//kml:Placemark")
i = 0
for e in res:
    i = i + 1
    print "Item: " + str(i) + "/" + str(len(res))
    ctxt.setContextNode(e)
    nodes = ctxt.xpathEval('kml:name')
    description = ctxt.xpathEval('kml:description')[0].content
    fecha = FormateaFecha(nodes[0].content)
    if len(nodes) > 0:
        #if nodes[0].content.strip().startswith('cp'):
	coord = ctxt.xpathEval('kml:Point/kml:coordinates')
	if len(coord) > 0:
		#tupla = [fecha] + coord[0].content.split(',') + ParseaDescripcion(description)
		tupla = ParseaDescripcion(description)
		if int(tupla[1]) <= 9: 
			print "Desechado por tener un numero de sensores menor que 8: " + tupla[1]
			continue
		lonlat = coord[0].content.split(',')[1] + ',' + coord[0].content.split(',')[0]
		print fecha + " " + lonlat + " " + str(tupla)
		rowid = int(ft_client.query(SQL().insert('1300472', {'TimeStamp':fecha, 'Location': lonlat, 'Residual':tupla[0], 'Sensors':tupla[1]})).split("\n")[1])
		print rowid
					 
doc.freeDoc()
ctxt.xpathFreeContext()


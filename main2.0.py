# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from MultimodeQt import Ui_MainWindow
import sys
import csv, requests, json, math, time, mmap, sys, os, datetime
import datetime
from key import keytpvp, keytpvelo, keytpmarche,keytrafic,keytptransit,  token
import requests.certs
build_exe_options = {"include_files":[(requests.certs.where(),'cacert.pem')]}
appver = "IDD Multimode 2.0"

class Multimode: # Définition de la classe OD
    """Classe regroupant les fonctions d'appel
    des API et de calcul des temps"""

    def __init__(self): # Notre méthode constructeur
        self.s_id = ""

    def tpvp(self, s_id, s_olat, s_olng, s_dlat, s_dlng, keytpvp):
        """Fonction de recherche des temps voiture
        theorique avec l'API Google Map"""
        #Appel des variables
        self.keytpvp = keytpvp        
        self.s_id = s_id
        self.s_olat = s_olat
        self.s_olng = s_olng
        self.s_dlat = s_dlat
        self.s_dlng = s_dlng
        self.s_destination = str(self.s_dlat+','+self.s_dlng)
        self.s_origine = str(self.s_olat+','+self.s_olng)
        self.s_ndestination = str(self.s_dlng+';'+self.s_dlat)
        self.s_norigine = str(self.s_olng+';'+self.s_olat)
        #Construction de l'URL
        self.url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
        self.urlb = '&destinations='
        self.urlc = '&mode=driving&language=en-EN&sensor=false'
        self.urlk = '&key='
        self.urlq = self.url+self.s_origine+self.urlb+self.s_destination+self.urlk+self.keytpvp+self.urlc
        self.resp = requests.get(self.urlq)
        #Traitement de la réponse
        self.dic = json.loads(self.resp.text)
        self.maps_output = self.resp.json()
        self.maps_output_str = json.dumps(self.maps_output, sort_keys=True, indent=2)
        self.results_list = self.maps_output['rows']
        self.Element = self.results_list[0]['elements']
        self.statu = self.Element[0]['status']
        print (self.urlq)

        try:
            self.statu == 'OK'
            self.distance = self.Element[0]['distance']['value']
            self.vpdistkm = "{:.2f}".format(self.distance/1000)
            self.duree = self.Element[0]['duration']['value']
            self.vpdureemin = "{:.2f}".format(self.duree/60)
            self.msggmap = "ok"
            return (self.s_id, self.vpdistkm, self.vpdureemin, self.msggmap)
             
        except:
            self.msggmap = self.statu
            return (self.s_id,'', '',self.msggmap)

    def trafic(self, timestamp, s_id, s_olat, s_olng, s_dlat, s_dlng, keytrafic):
        """Fonction de recherche du temps de trajet voiture en fonction d'une heure de départ
        et de l'historique du trafic
        !! L'heure de depart s'exprime en timestamp"""
        self.timestamp = timestamp #'1509396860' #str(ss) #'1505716200'  
        self.keytrafic = keytrafic        
        self.s_id = s_id
        self.s_olat = s_olat
        self.s_olng = s_olng
        self.s_dlat = s_dlat
        self.s_dlng = s_dlng
        self.s_destination = str(self.s_dlat+','+self.s_dlng)
        self.s_origine = str(self.s_olat+','+self.s_olng)
        self.url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
        self.urlb = '&destinations='
        self.urlc = '&mode=driving&language=en-EN&sensor=false&traffic_model=pessimistic&departure_time='
        self.urlk = '&key='
        self.urlq = self.url+self.s_origine+self.urlb+self.s_destination+self.urlc+timestamp+self.urlk+self.keytrafic
        print (self.urlq)
        self.resp = requests.get(self.urlq)
        self.dic = json.loads(self.resp.text)
        self.maps_output = self.resp.json()
        self.maps_output_str = json.dumps(self.maps_output, sort_keys=True, indent=2)
        self.results_list = self.maps_output['rows']
        self.statu = self.maps_output['status']
        self.Element = self.results_list[0]['elements']
        self.statu = self.Element[0]['status']
        print (self.urlq)

        try:
            self.statu == 'OK'
            self.distance = self.Element[0]['distance']['value']
            self.vpdistkm = "{:.2f}".format(self.distance/1000)
            self.dureet = self.Element[0]['duration_in_traffic']['value']
            self.vpdureetmin = "{:.2f}".format(self.dureet/60)
            self.msggmapt = "ok"
            return (self.vpdureetmin)
        
        except:
            vide=""
            return vide
        

    def tpmarche(self, s_id, s_olat, s_olng, s_dlat, s_dlng, keytpmarche):
        """Fonction de recherche des temps marche
        theorique avec l'API Google Map"""
        
        self.keytpmarche = keytpmarche               
        self.s_id = s_id
        self.s_olat = s_olat
        self.s_olng = s_olng
        self.s_dlat = s_dlat
        self.s_dlng = s_dlng
        self.s_destination = str(self.s_dlat+','+self.s_dlng)
        self.s_origine = str(self.s_olat+','+self.s_olng)
        self.s_ndestination = str(self.s_dlng+';'+self.s_dlat)
        self.s_norigine = str(self.s_olng+';'+self.s_olat)
        self.url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
        self.urlb = '&destinations='
        self.urlc = '&mode=walking&language=en-EN&sensor=false'
        self.urlk = '&key='
        self.urlq = self.url+self.s_origine+self.urlb+self.s_destination+self.urlk+self.keytpmarche+self.urlc
        self.resp = requests.get(self.urlq)
        self.dic = json.loads(self.resp.text)
        self.maps_output = self.resp.json()
        self.maps_output_str = json.dumps(self.maps_output, sort_keys=True, indent=2)
        self.results_list = self.maps_output['rows']
        self.Element = self.results_list[0]['elements']
        self.statu = self.Element[0]['status']

        try:
            self.statu == 'OK'
            self.distance = self.Element[0]['distance']['value']
            self.distkm = "{:.2f}".format(self.distance/1000)
            self.duree = self.Element[0]['duration']['value']
            self.mdureemin = "{:.2f}".format(self.duree/60)
            return (self.mdureemin)
                        
        except:
            vide=""
            return vide

    def tpgvelo(self, s_id, s_olat, s_olng, s_dlat, s_dlng, keytpvelo):
        """Fonction de recherche des temps marche
        theorique avec l'API Google Map"""
        
        self.keytpvelo = keytpvelo   
        self.s_id = s_id
        self.s_olat = s_olat
        self.s_olng = s_olng
        self.s_dlat = s_dlat
        self.s_dlng = s_dlng
        self.s_destination = str(self.s_dlat+','+self.s_dlng)
        self.s_origine = str(self.s_olat+','+self.s_olng)
        self.s_ndestination = str(self.s_dlng+';'+self.s_dlat)
        self.s_norigine = str(self.s_olng+';'+self.s_olat)
        self.url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
        self.urlb = '&destinations='
        self.urlc = '&mode=bicycling&language=en-EN&sensor=false'
        self.urlk = '&key='
        self.urlq = self.url+self.s_origine+self.urlb+self.s_destination+self.urlk+self.keytpvelo+self.urlc
        self.resp = requests.get(self.urlq)
        self.dic = json.loads(self.resp.text)
        self.maps_output = self.resp.json()
        self.maps_output_str = json.dumps(self.maps_output, sort_keys=True, indent=2)
        self.results_list = self.maps_output['rows']
        self.Element = self.results_list[0]['elements']
        self.statu = self.Element[0]['status']

        try:
            self.statu == 'OK'
            self.distance = self.Element[0]['distance']['value']
            self.distkm = "{:.2f}".format(self.distance/1000)
            self.duree = self.Element[0]['duration']['value']
            self.mdureemin = "{:.2f}".format(self.duree/60)
            return (self.mdureemin)
                        
        except:
            vide=""
            return vide

        
    def tptransit(self, timestamp, s_id, s_olat, s_olng, s_dlat, s_dlng, keytptransit):
        """Fonction de recherche des temps marche
        theorique avec l'API Google Map"""

        self.timestamp = timestamp
        self.keytptransit = keytptransit               
        self.s_id = s_id
        self.s_olat = s_olat
        self.s_olng = s_olng
        self.s_dlat = s_dlat
        self.s_dlng = s_dlng
        self.s_destination = str(self.s_dlat+','+self.s_dlng)
        self.s_origine = str(self.s_olat+','+self.s_olng)
        self.s_ndestination = str(self.s_dlng+';'+self.s_dlat)
        self.s_norigine = str(self.s_olng+';'+self.s_olat)
        self.url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
        self.urlb = '&destinations='
        self.urlc = '&mode=transit&language=en-EN&sensor=false&&arrival-time='+self.timestamp
        self.urlk = '&key='
        self.urlq = self.url+self.s_origine+self.urlb+self.s_destination+self.urlk+self.keytptransit+self.urlc
        self.resp = requests.get(self.urlq)
        self.dic = json.loads(self.resp.text)
        self.maps_output = self.resp.json()
        self.maps_output_str = json.dumps(self.maps_output, sort_keys=True, indent=2)
        self.results_list = self.maps_output['rows']
        self.Element = self.results_list[0]['elements']
        self.statu = self.Element[0]['status']

        try:
            self.statu == 'OK'
            self.distance = self.Element[0]['distance']['value']
            self.distkm = "{:.2f}".format(self.distance/1000)
            self.duree = self.Element[0]['duration']['value']
            self.mdureemin = "{:.2f}".format(self.duree/60)
            return (self.mdureemin)
                        
        except:
            vide=""
            return vide

    #fonction de recherche navitia.io

        
    def navjourney(self, timenavitia, distmax, s_id, s_olat, s_olng, s_dlat, s_dlng, token):
        """Fonction de recherche du premier temps TC
        théorique fournis par l'API Navitia.io"""
        self.token = token       
        self.s_id = s_id
        self.s_olat = s_olat
        self.s_olng = s_olng
        self.s_dlat = s_dlat
        self.s_dlng = s_dlng
        self.distmmax = distmax
        self.s_ndestination = str(self.s_dlng+';'+self.s_dlat)
        self.s_norigine = str(self.s_olng+';'+self.s_olat)
        self.urlcov = 'https://api.navitia.io/v1/coord/'
        self.urlqcov = self.urlcov+self.s_norigine
        self.respcov = requests.get(self.urlqcov, headers={'Authorization':self.token})
        print (self.urlqcov)
        self.cov_output = self.respcov.json()
        try:
            self.coverage = str(self.cov_output['message']).strip('""')
            self.coverage = ""

            
        except:
            self.coverage = str(self.cov_output['regions']).strip("[]")
            self.coverage = self.coverage.strip("'")

        self.timenavitia = timenavitia
        self.urla = 'https://'
        self.urlaa = 'api.navitia.io/v1/coverage/'
        self.urlaaa = '/journeys?from='
        self.urlaaaa = '&datetime='
        
        self.urlb = '&to='
        self.urlc = '&max_duration_to_pt='
        self.urlcc = str(self.distmmax * 60)
        #selfurlq = 'https://api.navitia.io/v1/coverage/'+self.coverage+'/journeys?from='+self.s_norigine+'&to='+self.s_ndestination+self.timenavitia+'&max_duration_to_pt=900'
        self.urlq = self.urla+self.urlaa+self.coverage+self.urlaaa+self.s_norigine+self.urlb+self.s_ndestination+self.urlc+self.urlcc+self.urlaaaa+self.timenavitia
        print (self.urlq)
        self.resp = requests.get(self.urlq, headers={'Authorization':self.token})
        try:
            self.nav_output = self.resp.json()
            self.lena = len(self.nav_output)
            if self.lena >1:
            
                self.journey_list = self.nav_output['journeys']
                i=0
                self.nresult =[]
                for i in range(len(self.journey_list)):
                    self.nduration ="{:.2f}".format(self.journey_list[0]['duration']/60)
                    self.corres = self.journey_list[0]['nb_transfers']
                    self.type = self.journey_list[0]['type'] #ne donne que le premier résultat - TODO changer [0] en [i] et le return pour avoir une liste
                    i=+1
                
                return (self.nduration,self.corres,self.type)
            else:
                self.error = [self.nav_output['error']['message']]
                return '','',self.error
                
        except:
            self.error = [self.nav_output['error']['message']]
            return '','',self.error
       

class IDDMulti(QtGui.QMainWindow):
    def __init__(self, title = "Default", parent = None):
        super (IDDMulti, self).__init__(parent)
        self.title = title
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(self.title)
        self._initSlotButtons()
        self.isFileOpen = False
        self.salvalid = 0
        self.testsave = 0
        self.testdate = 0
        self.testdate2 = 0
        self.testheure = 0
        self.testdist = 0
        self.consol("<br><br><div align='center'><h1>Bienvenue</h1><p>Pour commencer, selectionner un fichier Origines - Destinations</p>")
        

    def _initSlotButtons(self):
        self.ui.btSource.clicked.connect(self.chargerfichier)
        self.ui.btSave.clicked.connect(self.exportresult)
        self.ui.btSource_2.clicked.connect(self.chargeDate)
        self.ui.btSource_2.clicked.connect(self.chargeDateNavitia)
        self.ui.btSource_2.clicked.connect(self.chargeDist)
        self.ui.btSource_2.clicked.connect(self.BtExecuter)

        self.ui.calendar.clicked.connect(self.chargeDateNavitia)



    def consol(self, message):
        """Fonction de gestion de l'affichage des consignes
        dans la console"""
        self.txt0 = message
        print (self.txt0)
        self.ui.console.setHtml(self.txt0)

    def consolresult(self, message):
        """Fonction de gestion de l'affichage des resultats
        dans la console"""
        self.txt0 = message
        print (self.txt0)
        self.ui.console.append(self.txt0)
        QtGui.QApplication.processEvents()

    def progressBar(self, passe):
        """Fonction de gestion de l'affichage de la barre de progression"""
        self.passeactu = self.passe
        print (self.passeactu)
        self.ui.progressBar.increaseValue(self.passeactu)
        QtGui.QApplication.processEvents()

    def chargeDist(self):
        self.dist = self.ui.DistMax.value()
        self.distmax = int(self.dist)
        print (self.distmax)
        self.testdist = 1
        return self.distmax
       
    def chargeDate(self):
        self.cal = self.ui.calendar.selectedDate()
        self.date = (self.cal.toString("dd/MM/yyyy")) 

        if self.date != "":
            self.testdate = 1
            self.time = self.ui.hArrivee.time()
            self.heure = (self.time.toString())
            self.date = (self.cal.toString("dd/MM/yyyy"))
            a = (self.date+self.heure)
            now = datetime.datetime.now()
            now = now.strftime("%d/%m/%Y%H:%M:%S")
            print(now)
            s = time.mktime(datetime.datetime.strptime(a, "%d/%m/%Y%H:%M:%S").timetuple())
            n = time.mktime(datetime.datetime.strptime(now, "%d/%m/%Y%H:%M:%S").timetuple())
            if s>n:                
                ss = int(s)
                self.timestamp = str(ss)
                self.ui.console.setHtml(self.consol(a+'<br>'+self.timestamp))
                self.testdate2 = 1
                return self.timestamp
            else :
                self.consol("La date est dépassées")
        else:
            self.ui.console.setHtml(self.consol("La date est vide"))

    def chargeDateNavitia(self):
        self.cal = self.ui.calendar.selectedDate()
        self.time = self.ui.hArrivee.time()
        self.heure = (self.time.toString("HHmm"))
        self.date = (self.cal.toString("yyyyMMdd")) #YYYYMMDDTHHMM
        b = (self.date+'T'+self.heure)
        b = b.replace(":", "")
        self.timenavitia = str(b)
        self.ui.console.setHtml(b+'<br>'+self.timenavitia)
        return self.timenavitia
        

    



    
    def chargerfichier(self):
        """Fonction de chargement des données en entree"""
        self.pbarval = 0
        try:
            self.fichiersal = QtGui.QFileDialog.getOpenFileName(self, "Selectionnez le fichiers sources", "/sources", "*.csv")
            with open(self.fichiersal, "r+") as f:
                
                self.buf = mmap.mmap(f.fileno(), 0)
                self.lines = 0
                self.readline = self.buf.readline
                while self.readline():
                    self.lines += 1
                self.line_result = str(self.lines)
                self.msgcharge = ('Ce fichier compte '+self.line_result+' trajets') #Tester si la dernière ligne est vide
                self.consol(self.msgcharge)
                self.salvalid = 1
                self.pbarmax = int(self.line_result)
                
        except IOError as e:
            self.salvalid = 0
            self.msgcharge = "<h2>Impossible d'ouvrir le fichier</h2>"+"I/O error({0}): {1}".format(e.errno, e.strerror)+"<br>Erreure lors de l'ouverture du fichier.<br><br>Est-il déjà ouvert dans Excel ou une autre application ?"
            self.consol(self.msgcharge)
            

    def exportresult(self):
        """Fonction de chargement de l'emplacement des resultats"""
        try:
            self.resultfichier = QtGui.QFileDialog.getSaveFileName(self, "Selectionnez l'emplacement et donnez un nom", "/results", "*.csv")
            ext = self.resultfichier[-4:]
            #print (ext)
            try:
                ext != ".csv"
                self.resultfichier = self.resultfichier
            except :
                self.resultfichier = self.resultfichier.replace('.csv','')

            self.msgcharge = ('Les résultats seront enregistrés dans le fichier :<br>'+self.resultfichier)
            self.consol(self.msgcharge)
            self.testsave = 1
        except IOError as e:
            self.msgcharge = ("Impossible d'enregistrer le fichier<br>"+"I/O error({0}): {1}".format(e.errno, e.strerror)+"<br>Erreure lors de l'écriture du fichier.<br>Est-il déjà ouvert dans Excel\nou une autre application ?")
            self.consol(self.msgcharge)



    def chekParam(self):
        self.testsalValid = self.salvalid
        self.testsaveValid = self.testsave
        self.testsaveValidmsg = ""
        self.chargeDate()
        self.testdateValid = self.testdate
        self.testdateValidmsg = ""
        self.testdate2Valid = self.testdate2
        self.testdate2Validmsg = ""
        self.testdistValid = self.testdist
        sommevalid = 0

        if self.testsalValid != 1:
            self.testsalValidmsg = "Pas de fichier OD sélectionné"
            
        else:
            sommevalid += 1

        if self.testsaveValid != 1:
            self.testsaveValidmsg = "Pas de fichier d'enregistrement sélectionné"
        else:
            sommevalid += 1
            
        if self.testdateValid != 1:
            self.testsaveValidmsg = "Pas de date sélectionnée"
        else:
            sommevalid += 1
            
        if self.testdate2Valid != 1:
            self.testdateValidmsg = "La date choisie est dépassée"
        else:
            sommevalid += 1
            
        if self.testdistValid != 1:
            self.testdistValidmsg = "Pas de distance max sélectionnée"
        else:
            sommevalid += 1

        if sommevalid != 5:
            self.consol("<h2>Attention !</h2><p>Des paramètres sont manquants ou incorrectes :</p><ul><li>"+self.testsalValidmsg+"</li><li>"+self.testsaveValidmsg+"</li><li>"+self.testdateValidmsg+"</li></ul>")
        else:
                self.consol("<h2>Tous les paramètres sont correctes :</h2><ul><li>Nombre de trajets : "+str(self.pbarmax)+"</li><li>Date d'arrivée : "+str(self.date)+" à "+str(self.heure)+"h.</li><li></ul>")
                self.consolresult('\n\n\nDébut de la recherche le:\n\n'+time.strftime('%d/%m/%y %H:%M',time.localtime())+'\n\n\n')
                self.rechercher()


    def BtExecuter(self):
        """Action sur le Boutont Executer"""
        self.consol("Validation des paramètres de la requête...")
        self.chekParam()
       
            


    def testdate(self):
        testdate = str(self.timestamp())
        try:
            testdate != ""
        except IOError as e:
            self.msgcharge = (e)
            self.consol(self.msgcharge)
            print (e)
        self.rechercher()

      
    
    def rechercher(self):
        """Fonction de construction du resultat"""
        self.consol('\n\n\nDébut de la recherche le:\n\n'+time.strftime('%d/%m/%y %H:%M',time.localtime())+'\n\n\n')
        sal = Multimode()

        with open(self.fichiersal) as f:
            try:
                with open(self.resultfichier, 'w')as sortie:
                    csv_out=csv.writer(sortie, delimiter=';', lineterminator='\n')

            except IOError as e:
                self.msgcharge = ("<h2>Impossible d'enregistrer le fichier</h2><br>"+"I/O error({0}): {1}".format(e.errno, e.strerror)+"<br><br>Erreure lors de l'écriture des résultats.<br><br>Est-il déjà ouvert dans Excel\nou une autre application ?")
                self.consol(self.msgcharge)
                
            with open(self.resultfichier, 'w')as sortie:

                csv_out=csv.writer(sortie, delimiter=';', lineterminator='\n')
                csv_out.writerow(['sid',
                                  'latitude',
                                  'longitude',
                                  'latitudeD',
                                  'longitudeD',
                                  'distvp',
                                  'tpvp',
                                  'tptrafic',
                                  'tpmarche',
                                  'MsgGmap',
                                  'tpVelo',
                                  'tpTCU',
                                  'nbCoresp',
                                  'msgNavitia',
                                  'tpTransit'])
                reader = csv.reader(f, delimiter = ";")
                next (reader, None)
                self.lstresult=[]
                for row in reader:
                    self.pbarval = self.pbarval ++ 1
                    self.pbarpc = (self.pbarval -- self.pbarmax)/100
                    self.ui.progressBar.setValue(self.pbarpc)
                    #time.sleep(.500)
                    s_id = row[0]
                    s_olat = row[1]
                    s_olng = row[2]
                    s_dlat = row[3]
                    s_dlng = row[4]

                    idsal ,distkm, tpvp, mgmap = sal.tpvp(s_id,s_olat,s_olng,s_dlat,s_dlng, keytpvp)
                    tptrafic = sal.trafic(self.timestamp, s_id,s_olat,s_olng,s_dlat,s_dlng,keytrafic)
                    tpmarche = sal.tpmarche(s_id,s_olat,s_olng,s_dlat,s_dlng,keytpmarche)
                    gvtime = sal.tpgvelo(s_id,s_olat,s_olng,s_dlat,s_dlng,keytpvelo)
                    nduration, ncorres, ntype = sal.navjourney(self.timenavitia, self.distmax, s_id,s_olat,s_olng,s_dlat,s_dlng,token)
                    tptransit = sal.tptransit(self.timestamp, s_id,s_olat,s_olng,s_dlat,s_dlng,keytptransit)

                    result = idsal,s_olat,s_olng,s_dlat,s_dlng,distkm,tpvp,tptrafic,tpmarche,gvtime,nduration,ncorres,ntype
                    resultmessage_idtra = str(idsal)
                    resultmessage_gmap = str(mgmap)
                    resultmessage_navitia = str(ntype)
                    resultmessage_navitia = str(resultmessage_navitia).strip('['']')
                    self.line_resultv = int(self.line_result) - 1
                    self.resultgui = ("Trajet " + resultmessage_idtra + " sur " + (str(self.line_resultv)) + ". Temps Gmaps : " + resultmessage_gmap + ". Temps Navitia : " + resultmessage_navitia)
                    self.progresspc = ((int(self.line_result) - int(s_id))/100)
                    self.progressBar = self.progresspc
                    #self.resultgui = str(result).strip('()')
                    #self.resultgui = str(self.resultgui).replace("'",'')
                    #self.resultgui = str(self.resultgui).replace(" ",'')
                    #self.resultgui = str(self.resultgui).replace(",",';')                    

                    #print(self.resultgui)
                    csv_out.writerow((idsal,s_olat,s_olng,s_dlat,s_dlng,distkm,tpvp,tptrafic,tpmarche,mgmap,gvtime,nduration,ncorres,ntype,tptransit))
                    self.line_result = str(self.lines)
                    self.msgcharge = (self.resultgui)
                    #self.lblresult.insert(0.0, '\n'+str(self.msgcharge))
                    self.consolresult(self.msgcharge)
                    
                        

                    
                    
           
        f.close()
        sortie.close()
        self.consolresult("<p><h1>Bien.</h1></p><p>votre recherche s'est achevée le<br>"+time.strftime('%d/%m/%y %H:%M',time.localtime()) +"</p><p>Les résultats sont enregistrés dans le fichier "+self.resultfichier+"</p>")

    
        
if __name__ == "__main__" :
    app = QtGui.QApplication(sys.argv)
    w = IDDMulti("IDD Multimode 1.3")
    w.show()
    sys.exit(app.exec_())
    

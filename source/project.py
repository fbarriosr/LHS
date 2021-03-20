from source.myPrint import *
import subprocess
import os

class Project:
    def __init__(self, name):
	aux 	= name[::-1]
	t1  	= aux.find('_')
	t1 	= len(aux)-1 -t1
	self.name = name[0:t1]
	self.N 	= name[t1+1]
	self.files = []
	self.filesLog = []
	self.filesCub = []
	self.p = 0
	self.q = 0
	self.status = False
	self.statusDenCub = False
	self.statusLog = False
	self.errorMsg = "No message"
	
    def findFile(self,name, file):
	if name in file:
	    return name
	else:
	    return 'False'
	    
    def existFile(self, name, file):
	if name in file:
	    return True
	else:
	    return False

    def getNamePosFile(self):
	aux = self.name + '_'+ self.N +'+'+ str( self.p) +'.fchk'
	return self.findFile(aux, self.files)

    def getNameNegFile(self):
	aux = self.name + '_'+ self.N +'-'+ str(self.q) +'.fchk'
	return self.findFile(aux, self.files)

    def getNameMainFile(self):
	aux = self.name + '_'+ self.N +'.fchk'
	return self.findFile(aux, self.files)
			
    def getNameDenCubFile(self):
	aux = self.name + '_'+ self.N + '+' + str(self.p) +'_den.cub'
	return self.findFile(aux, self.filesCub)
			
    def getNameLogP2File(self):
	aux = self.name + '_'+ self.N + '+2' + '.log'
	return self.findFile(aux, self.filesLog)
			
    def getNameLogP1File(self):
	aux = self.name + '_'+ self.N + '+1' + '.log'
	return self.findFile(aux, self.filesLog)
	
    def getNameLogFile(self):
	aux = self.name + '_' + self.N +'.log'
	return self.findFile(aux, self.filesLog)
	
    def getNameLogN1File(self):
	aux = self.name + '_'+ self.N + '-1' + '.log'
	return self.findFile(aux, self.filesLog)
	
    def getNameLogP2File(self):
	aux = self.name + '_'+ self.N + '-2' + '.log'
	return self.findFile(aux, self.filesLog)

    def getP(self):
	return self.p

    def getQ(self):
	return self.q
		
    def getN(self):
	return self.N

    def getName(self):
	return self.name
		
    def viewName(self):
	print('Name:',self.name)

    def view(self):
	printElement('-',40)
	print('Name:',self.name)
	print('N:',self.N)
	print('p:',self.p)
	print('q:',self.q)
	print('files:',self.files)
	print('filesLog:', self.filesLog)
	print('filesCub:', self.filesCub)
	print('status:',self.status)
	print('statusDenCub:',self.statusDenCub)
	print('statusLog:', self.statusLog)
	print('error:',self.errorMsg)
	printElement('-',40)
	return

    def set_P(self,name):
	aux = name[::-1]
	t1 = aux.find('+')
	t1 = len(aux)-1 - t1   # arreglo el puntero
	t2 = name.find('.')
	self.p = name[t1+1:t2]
	return

    def set_Q(self,name):
	aux = name[::-1]
	t1 = aux.find('-')
	t1 = len(aux)-1 -t1    #arreglo el puntero
	t2 = name.find('.')
	self.q = name[t1+1:t2]
	return

    def loadingFiles(self, allFilesNames):
	self.files =[]
	self.filesLog= []
	for i in range (len(allFilesNames)):
	    if self.name in allFilesNames[i][0:len(self.name)]:
		aux = allFilesNames[i]
		if '.log' in aux:
		    self.filesLog.append(aux)
		elif '.cub' in aux:
		    self.filesCub.append(aux)
		elif '.fchk' in aux:
		    self.files.append(aux)
	return
	
    def checkUnique(self):
	countP	 = 0
	countQ	 = 0
	posP 	 = 0
	posQ 	 = 0


	for i in range (len(self.files)):
	    aux = self.files[i].replace(self.name+'_'+self.N,'')
	    
	    if '+' in aux: 
		countP=countP+1
		posP = i 
	    elif '-' in aux: 
		countQ=countQ+1
		posQ = i 

	    #print('file:',self.files)
	    #print('countP:',countP, 'countQ:',countQ, 'countDen:',countDen)


	    if (countP == 1) and (countQ == 1) and (len(self.files)== 3):
		self.status = True
		self.set_P(self.files[posP])
		self.set_Q(self.files[posQ])
		self.errorMsg = "No hay errores en los nombres de los archivos"
			
	    elif (countP == 1) and (countQ == 1) and (len(self.files) == 4) and (countDen == 1):
		self.status = True
		self.statusDen = True
		self.set_P(self.files[posP])
		self.set_Q(self.files[posQ])
		self.errorMsg = 'No hay errores en los nombres de los arhivos'
	
	    elif len(self.files) > 3:
		self.status = False
		archivo1 = self.name 
		archivo2 = self.name + "+P"
		archivo3 = self.name + "-Q"
		self.errorMsg = "Hay errores, se encontraron multiples archivos, solo debes tener 3:"+archivo1+', '+archivo2 + 'y'+ archivo3 
		
	    else:
		self.status = False
		archivo1 = self.name 
		archivo2 = self.name + "+P"
		archivo3 = self.name + "-Q"
		self.errorMsg = "Faltan archivos, solo debes tener 3:"+archivo1+', '+archivo2 + ','+ archivo3 
		
	self.statusLog = self.checkUniqueLog()
	self.statusDenCub = self.checkUniqueCub()
	
	
	return
	
    def checkUniqueCub(self):
	file1 = self.existFile( self.name + '_'+ self.N +'+'+str(self.p) + '_den.cub', self.filesCub)
	return file1
	
    def checkUniqueLog(self):
    
	file1 = self.existFile( self.name + '_'+ self.N + '-2' + '.log', self.filesLog)
	file2 = self.existFile( self.name + '_'+ self.N + '-1' + '.log', self.filesLog)
	file3 = self.existFile( self.name + '_'+ self.N +        '.log', self.filesLog)
	file4 = self.existFile( self.name + '_'+ self.N + '+1' + '.log', self.filesLog)
	file5 = self.existFile( self.name + '_'+ self.N + '+2' + '.log', self.filesLog)

	if file1 and file2 and file3 and file4 and file5:
	    return True
	else:
	    return False



import os
import subprocess
from myPrint import *
from stages import *
from filesFunc import *
from project import *

class Operaciones:
    def __init__(self):
	self.paso = 0
	# datos de usuario
	self.X = 0
	self.Y = 0
	self.density = ''
	self.theory = ''
	
	# nombre de archivos
	
	self.MainDen = 0
	self.NegDen  = 0
	self.PosDen  = 0
	
	self.FPosF_FDA  = 0
	self.FNegF_FDA  = 0
	
	self.FF_FDA     = 0
	self.DD_FDA     = 0
	
	# Indicadores Archivos log
	
	self.Energy = {
	    'E(N+2)':0.0,
	    'E(N+1)':0.0,
	    'E(N)'  :0.0,
	    'E(N-1)':0.0,
	    'E(N-2)':0.0
	    }
	
	self.Indicadores = {
	    'A2':0.0,
	    'A1':0.0,
	    'I2':0.0,
	    'I1':0.0,
	    'mu':0.0,
	    'gamma':0.0,
	    'S':0.0,
	    'eta':0.0
	    }
	
	self.tempFiles   = []
	self.deleteFiles = []
	
    def viewDen(self):
	printElementName('Den','-',40)
	print self.MainDen
	print self.PosDen
	print self.NegDen
	
    def getX(self):
	if self.X == 0:
	    printElementName('Number Cores X', '-',40)
	    print('Recommended 16, but you choose 4,8 or 12')
	    while True:
		answer = checker('Insert Cores')
		if answer <1 or answer > 16:
		    print('Action not valid: ', answer)
		else:
		    self.X = answer
		    break
	return self.X
    
    def getY(self):
	if self.Y == 0:
	    printElementName('Resolution Y','-',40)
	    print('Recommended 3, but you can choose:')
	    print('Low   : 2')
	    print('Medium: 3')
	    print('High  : 4')
	    while True:
		answer = checker('Insert Resolution')
		if answer <2 or answer >4:
		    print('Action not valid: ', answer)
		else:
		    self.Y = answer
		    break
	return self.Y
		
    def getDensity(self):
	if self.density == '':
	    printElementName('Choose Density','-',40)
	    print(' 1: Density')
	    print(' \t Corresponding to that formed by the external electrons, excluding the electronic density given by internal electrons (also called core electrons)')
	    print(' 2: FDensity')
	    print(' \t Full density (considering core electrons and those that are external) ')
	    while True:
		answer = checker('Insert Density')
		if answer <1 or answer >2:
		    print('Action not valid: ', answer)
		else:
		    if answer == 1:
			self.density = 'density'
		    elif answer == 2:
			self.density = 'fdensity'
		    break
	return self.density
	      
    def getTheory(self, project):
	if self.theory == '':
	    self.theory = getTheoryFile(project.files[0])
	    if self.theory == 'None':
		print('Problem with theory in files fchk')
		print('Valid Theories: MP2, SCF, CC, CI')
		sys.exit(0)
	    else:
		print('Theory Detected:'+ self.theory)
	return self.theory
    
    def operacion1(self, project):
	printElementName('OP1','-',40)
	input1 = project.getNameMainFile()
	input2 = project.getNameDenCubFile()
	output = project.getName()+'_'+project.getN()+'_den'+'.cub'
	
	#print('input2', input2)
	x = self.getX()
	y = -1
	
	density = self.getDensity()
	
	theory = self.getTheory(project)
	
	op1_a = CubeGenDens2Files(input1, input2, output, y , x , density, theory )
	#op1_a.view()
	 
	op1_a.viewQuery()
	#print op1_a.cube()
	
	op1_a.cube()
	 
	self.MainDen = output
	#op1_a.view()
	
	if op1_a.getStatus():
	    input1 = project.getNameNegFile()
	    output = project.getName()+'_'+ project.getN()+'-'+ project.getQ()+'_den'+'.cub'
	    
	    op1_b = CubeGenDens2Files(input1, input2, output, y, x,  density, theory)
	    op1_b.viewQuery()
	    op1_b.cube()
	    
	    self.NegDen = output
	    
	else:
	    printElementName('Error','-',40)
	    self.paso = 0
	    sys.exit(0)
	    
    def operacion2(self, project):
	printElementName('OP2','-',40)
	input1  = project.getNamePosFile()
	output = project.getName() + '_'+ project.getN()+'+'+project.getP()+'_den.cub'
	
	x = self.getX()
	
	y = self.getY()
	
	density = self.getDensity()
	
	theory = self.getTheory(project)
	
	op2 = CubeGenDens(input1, output, y, x, density, theory)
	

	op2.viewQuery()
	
	op2.cube()
	
	project.statusDen = True
	self.PosDen = output
	
	project.filesCub.append(output)
	
	self.tempFiles.append(output)
	
	#op2.view()
	

    def getEnergy(self, filename):
	energy = 0.0
	with open(filename) as f:
	    lines = f.readlines()  
	    f.close()
	#print('filename',filename)    
	#print('theory:',self.theory)
	if self.theory == 'SCF':
	    for line in lines:
		if line.upper().find('SCF DONE')!= -1:
		    t = line.split()
		    energy = float(t[4])
		    break
	elif self.theory == 'MP2':
	    for line in lines:
		if line.upper().find('EUMP2')!= -1:
		    t = line.split()
		    number = t[5]
		    #print('len:', len(t))
		    #print('line:',t)
		    #print('Energy:',number)
		    energy = float(number.replace("D", "E"))
		    break
		    
	elif self.theory == 'CC':
	    for line in lines:
		if line.upper().find('E(CORR)=')!= -1:
		    t = line.split()
		    if line.upper().find('CONVERGED')!=-1:
			number = t[4]
		    else:
			number = t[3]
		    #print('line:',t)
		    #print('Energy:',number)
		    energy = float(number)
	
	elif self.theory == 'CI':
	    #print(filename)
	    for line in lines:
		if line.upper().find('E(CI)=')!= -1:
		    t = line.split()
		    if line.upper().find('CONVERGED')!=-1:
			number = t[4]
		    else:
			number = t[3]
		    #print('len:', len(t))
		    #print('line:',t)
		    #print('Energy:',number)		    
		    energy = float(number)

	#print('energy:',energy)
	return energy
	
    def subEnergy(self, value1, value2, aprox):
	return round(value1-value2,aprox)
    
    def addEnergy(self,value1, value2, aprox):
	return round(value1+value2,aprox)
	
    def factorEnergy(self,value,factor, aprox):
	return round(value*factor, aprox)
	
    def powEnergy(self, value, ex, aprox):
	return round( pow(value, ex), aprox)
    
    
    
    def paso1(self, project, name,step,maxStep):
	info = name +' '+step+'/'+maxStep
	printElementName(info,'-',40)
	
	if project.statusDenCub == False:
	    while True:
		printElementName('_N+p_den.cub File is missing!', '*',40)
		printElementName('Create it :)','-',40)
		self.operacion2(project)
	        #project.view()
		self.operacion1(project)
		break
	else:
	    #print('OP1',project.statusDenCub)
	    self.PosDen = project.getName() + '_'+ project.getN()+'+'+project.getP()+'_den.cub'
	    self.operacion1(project)
	    
    	
    def paso2a(self, value, action,inputFile1, inputFile2, outputFile ):
    
	#print ('value:',value)
	print('inputFile1:', inputFile1)
	print('inputFile2:', inputFile2)
	print('outputFile:', outputFile)
	
	
	if value == 1:

	    t= CubeManP3NoScale(inputFile1, inputFile2,outputFile, action)
	    t.viewQuery()
	    t.cube()
	
	elif value > 1:
	    outputFilePro = outputFile.replace('_F-F_FDA.cub','_pro_F-F_FDA.cub')
	    outputFilePro = outputFilePro.replace('_F+F_FDA.cub','_pro_F+F_FDA.cub')
	    
	    t1 = CubeManP3NoScale(inputFile1, inputFile2, outputFilePro, action)
	    t1.viewQuery()
	    t1.cube()
	    
	    aprox = 8
	    factor = round(1./value,aprox)
	    #print( value, factor)
	    
    	    t2 = CubeManP3Scale(outputFilePro, outputFile, factor)
    	    t2.viewQuery()
    	    t2.cube()
    	    
    	    self.deleteFiles.append(outputFilePro)
    	    
    	return outputFile

    def paso2(self,project, name, step, maxStep):
    
	info = name +' '+ step+'/'+maxStep
	printElementName(info,'-',40)
	
	
	self.FPosF_FDA = self.paso2a(int(project.getP()), 'SU', self.PosDen , self.MainDen  ,  project.getName()+'_F+F_FDA.cub')

	self.FNegF_FDA = self.paso2a(int(project.getQ()), 'SU', self.MainDen , self.NegDen   ,  project.getName()+'_F-F_FDA.cub') 
    
	self.paso = 2
	
    def paso3(self, project, name, step, maxStep):
	info = name+' '+ step+'/'+maxStep
	printElementName(info,'-',40)
	line = 'Nucleophilic Fukui function by means of the finite difference approximation'
	
	printElementName('Writing','*',40)
	print self.FPosF_FDA
	
	editL1L2(self.FPosF_FDA, self.FPosF_FDA, line)
	
	print self.FNegF_FDA
	line = line.replace('Nucleophilic','Electrophilic')
	editL1L2(self.FNegF_FDA, self.FNegF_FDA, line)
	
	self.paso = 3
	
    def paso4b(self, action, inputFile1, inputFile2, outputFile ):
    
	print('inputFile1:', inputFile1)
	print('inputFile2:', inputFile2)
	print('outputFile:', outputFile)
    
	t = CubeManP3NoScale(inputFile1, inputFile2, outputFile, action)
	t.viewQuery()
	t.cube()
	return outputFile
	
    def paso4a(self, action, inputFile1, inputFile2, outputFile):
	
	print('inputFile1:', inputFile1)
	print('inputFile2:', inputFile2)
	print('outputFile:', outputFile)
    
	outputFilePro = outputFile.replace('_FF_FDA.cub','_pro_FF_FDA.cub')
	
	t1= CubeManP3NoScale(inputFile1, inputFile2, outputFilePro, action)
	t1.viewQuery()
	t1.cube()
	
	scale = 0.5
	t2 = CubeManP3Scale(outputFilePro, outputFile, scale)
	t2.viewQuery()
	t2.cube()
	
	self.deleteFiles.append(outputFilePro)
	
	return outputFile
	
    def paso4(self,project, name, step, maxStep):
	info = name +' '+ step+'/'+maxStep
	printElementName(info, '-', 40)
	
	
	self.DD_FDA = self.paso4b('SU', self.FPosF_FDA, self.FNegF_FDA, project.getName()+'_DD_FDA.cub' )
	self.FF_FDA = self.paso4a( 'A', self.FPosF_FDA, self.FNegF_FDA, project.getName()+'_FF_FDA.cub' )
	
	self.paso = 4
	
    def paso5(self, name, step, maxStep):
	info = name+' '+step+'/'+maxStep
	printElementName(info,'-',40)
	
	line = 'Fukui function by means of finite difference approximation'
	
	printElementName('Writing','*',40)
	print self.FF_FDA
	
	editL1L2(self.FF_FDA, self.FF_FDA, line)
	
	line = line.replace('Fukui function','Dual descriptor')
    
	print self.DD_FDA
	
	editL1L2(self.DD_FDA, self.DD_FDA, line)
	
	self.paso = 5
	
	
	
    def paso6(self, name, step, maxStep):
	info = name +''+step+'/'+maxStep
	printElementName(info,'-',40)
	printElementName('Delete Files','*',40)
	for t in self.deleteFiles:
	    print t
	removeFiles(self.deleteFiles)
	
	self.deleteFiles = []  # vaciar la lista
	printElementName('Temporal Files','-',40)
	for t in self.tempFiles:
	    print t
	    while True:
		answer = str(raw_input('Do you want delete it? y/n\n'))
		if answer == 'y':
		    self.deleteFiles.append(t)
		    break
		elif answer == 'n':
		    break
		else:
		    print('Action not valid',answer)
	    
	printElementName('Delete Files','*',40)
	for t in self.deleteFiles:
	    print t
	removeFiles(self.deleteFiles)
	
	
	self.paso = 6
	
	return 0
    
    def paso7(self, name, step, maxStep, files):
    
	info = name +''+step+'/'+maxStep
	printElementName(info,'-',40)
	# find energies
	for f in files:
	    if 'N+2.log' in f:
		self.Energy['E(N+2)'] = self.getEnergy(f)
	    elif 'N+1.log' in f:
		self.Energy['E(N+1)'] = self.getEnergy(f)
	    elif 'N.log' in f:
		self.Energy['E(N)'] = self.getEnergy(f)
	    elif 'N-1.log' in f:
		self.Energy['E(N-1)'] = self.getEnergy(f)
	    elif 'N-2.log' in f:
		self.Energy['E(N-2)'] = self.getEnergy(f)
	aprox = 8
	
	if self.Energy['E(N)'] == 0.0 and self.Energy['E(N-1)'] == 0.0 and self.Energy['E(N-2)'] == 0.0 and self.Energy['E(N+1)'] == 0.0 and  self.Energy['E(N+2)'] == 0.0:
	    sys.exit('Problem with get Energies')
	
	printElementName('Extract - Energies','*',40)
	
	for key, value in self.Energy.items():
	    print(str(key) +'\t = '+ str(value))
	
	printElementName('Loading - Parameters','*',40)
	
	self.Indicadores['A2'] = self.subEnergy( self.Energy['E(N+1)'],self.Energy['E(N+2)'] , aprox)
	self.Indicadores['A1'] = self.subEnergy( self.Energy['E(N)']   ,self.Energy['E(N+1)'] , aprox)
	
	self.Indicadores['I1'] = self.subEnergy( self.Energy['E(N-1)']   ,self.Energy['E(N)'] , aprox)
	self.Indicadores['I2'] = self.subEnergy( self.Energy['E(N-2)']   ,self.Energy['E(N-1)'] , aprox)
	
		
	self.Indicadores['mu'] = self.factorEnergy( self.addEnergy(self.Indicadores['A1'] , self.Indicadores['I1'], aprox)  ,-0.5,aprox)
	
	self.Indicadores['eta']= self.subEnergy(self.Indicadores['I1'] ,self.Indicadores['A1'], aprox)
	
	self.Indicadores['S']  = self.powEnergy(self.Indicadores['eta'] , -1, aprox  )
	
	self.Indicadores['gamma']= self.factorEnergy(
			 self.subEnergy( 
			    self.subEnergy( self.addEnergy( self.Indicadores['I1'] , self.Indicadores['A1']  , aprox), 
					    self.Indicadores['I2'] ,
					    aprox),
			    self.Indicadores['A2'] ,
			    aprox),
			 0.5   ,
			  aprox)
			  
	#print('Energies:',self.Energy)
	#print('Indicadores:', self.Indicadores)
	
	
	for key, value in self.Indicadores.items():
	    print(str(key) +'\t = '+ str(value))
	
	
	self.paso = 7
	
	return 0


	
    def paso8(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	aprox = 8
	
	inputFile  = self.DD_FDA
	outputFile =  project.getName()+'_'+'LHS1_FDA.cub'
	factor = round(pow(self.Indicadores['S'],2),aprox)
	#print(self.Indicadores['S'],factor)
	print('Factor (S^2)=\t'+str(factor) )
	t1 = CubeManP3Scale(inputFile,outputFile,factor)
	t1.viewQuery()
	t1.cube()
	
	
	self.paso = 8

	
	return 0     
	
    def paso9(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	aprox = 8
	
	inputFile  = self.FF_FDA
	outputFile =  project.getName()+'_'+'LHS2_FDA.cub'
	factor = round(self.Indicadores['gamma']*pow(self.Indicadores['S'],3),aprox)
	#print(self.Indicadores['gamma'],self.Indicadores['S'] ,factor)
	print('Factor (gamma*S^3)=\t'+str(factor) )
	t1 = CubeManP3Scale(inputFile,outputFile,factor)
	t1.viewQuery()
	t1.cube()
	
	
	self.paso = 9

	
	return 0 
	
    def paso10(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	aprox = 8
	
	inputFile1  = project.getName()+'_'+'LHS1_FDA.cub'
	
	inputFile2 =  project.getName()+'_'+'LHS2_FDA.cub'
	
	outputFile =  project.getName()+'_'+'LHS_FDA.cub'
	
	action = 'Su'
	print('inputFile1:', inputFile1)
	print('inputFile2:', inputFile2)
	print('outputFile:', outputFile)
	
	t1 = CubeManP3NoScale(inputFile1, inputFile2,outputFile, action)
	t1.viewQuery()
	t1.cube()
	
	
	self.paso = 10

	
	return 0 
	
    def paso11(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	file_1 = project.getName()+'_'+'LHS1_FDA.cub'
	info = name +step+'/'+maxStep
	

	line = 'First component of the local hypersoftness by means of the finite difference approximation.'
	    
	printElementName('Writing','*',40)
	print file_1

	editL1L2(file_1,file_1 , line)

	line = line.replace('First','Second')
	
	file_1 = project.getName()+'_'+'LHS2_FDA.cub'
	print file_1


	editL1L2(file_1,file_1, line)
	
	line = line.replace('Second component of the local','Local')

	file_1 = project.getName()+'_'+'LHS_FDA.cub'
	print file_1

	editL1L2(file_1, file_1, line)

	self.paso = 11

	   
    def paso12(self,name, step, maxStep, filename):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	msn = 'Export Energies and Parameters'
	printElementName(msn,'*',40)
	csv(filename,self.Energy,self.Indicadores)
	print(filename)

	
	self.paso = 12
	return 0

	
	
	
	

	


	
	
	
	
    
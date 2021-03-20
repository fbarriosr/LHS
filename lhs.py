import os
import sys

from source.filesFunc import *
from source.operaciones import *
from source.myPrint import *
from source.project import *

nameProgram = 'LHS'

printElement('-',40)
printElementName(nameProgram.upper(),'-',40)
printElement('-',40)

filesType = ['.fchk', '_den.cub','.log']

if len(filesType) > 1:
    cmd  ='$|\\'.join(filesType)
elif len(filesType) == 1:
    cmd = filesType[0]

cmd = '\"\\'+cmd+'$\"'
cmd = 'ls | egrep '+ cmd
#print cmd
myCmd = os.popen(cmd).read()

allFilesNames = myCmd.split()

if len(allFilesNames)==0:
    printElementName(' No Files *'+' and *'.join(filesType),'"',51)
    sys.exit(0)


# List for Projects

projectName 		= []	# Project List Name
projectBadName	 	= []	# Project Bad List Name

projectDDP 		= []	# List DDP
projectIncompleteDDP 	= []	# List DDP Incomplete


# load the projectName

for i in range(len(allFilesNames)):
    name = allFilesNames[i]
    for f in filesType:
	name = name.replace(f,'')
    
    name = name[::-1]
    t1   = name.find('_')
    
    
    if t1 != -1:
	t1 = len(name)-1 -t1
	aux = allFilesNames[i][0:t1+2]
	if not(aux in projectName):
	    projectName.append(aux)
    else:
	projectBadName.append(name[::-1])
	

#printList('all',allFilesNames)
#printList('good',projectName)
#printList('bad', projectBadName)


for data in projectName :
    a = Project(data)
    a.loadingFiles(allFilesNames)
    #a.view()
    a.checkUnique()
    #a.view()
    if a.status == True:
	projectDDP.append(a)
    else:
	projectIncompleteDDP.append(a)

#printListDDP('ProjectDDP', projectDDP)
#printListDDP('Incompletos', projectIncompleteDDP)

if len(projectDDP) != 0:
    printElementName('Project List',' ',40)
    for i in range( len(projectDDP) ):
	print(i,projectDDP[i].getName())
    printElement('-',40)
else:
    printElementName('No project :(','=',40)
    sys.exit(0)
    

# Choose the project to work


while True:
    answer = checker('Choose Project')
    if (answer<0) or (answer > len(projectDDP) -1):
	print('Action not valid:',answer)
    else:
	break

project = projectDDP[answer]

maxStep = '12'

op = Operaciones()
op.paso1(project, 'Step','1',maxStep)
op.paso2(project, 'Step','2',maxStep)
op.paso3(project, 'Step','3',maxStep)
op.paso4(project, 'Step','4',maxStep)

op.paso5('Step','5',maxStep)

op.paso7( 'Step','7',maxStep, project.filesLog)

op.paso8(project, 'Step','8', maxStep)

op.paso9(project, 'Step','9', maxStep)

op.paso10(project, 'Step','10', maxStep)

op.paso11(project, 'Step','11', maxStep)


op.paso12('Step','12',maxStep,project.name+ '.csv')

op.paso6('Step','6',maxStep)



    
    


from source.myPrint import *
import subprocess
import os


def removeFiles(filesList):
    if len(filesList) == 0:
	print('No Files')
	return 4

    filesList.insert(0,'rm')
    #printElementName('Delete','*',40)
    query = ' '.join(filesList)
    #print query
    try:
	res = subprocess.Popen(filesList,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
	output,error = res.communicate()
	if output:
	    print "Output Code:",res.returncode
	    print "Succefull:",output
	    printElement('*',40)
	    return 0
	if error:
	    print "Output Code:",res.returncode
	    print "Error: ",error.strip()
	    printElement('*',40)
	    return 1
    except OSError as e:
	print "Output Code: ",e.errno
	print "Error:",e.strerror
	print "ErrorFile: ",e.filename
	printElement('*',40)
	return 2
    except:
	print "Error:", sys.exc_info()[0]
	printElement('*',40)
	return 3
    #printElement('*',40)
    

    
def checker(message):
    if message == "":
	inputt = raw_input()
    else:
	inputt = raw_input(message+'\n')
    try:
	return int(inputt)
    except ValueError:
	print "Error!, Enter a number!"
	return checker("")


def editL1L2(fileName, line1, line2):
    with open(fileName) as f:
	lines = f.readlines() #read
	f.close()

    lines[0] = line1 +'\n'
    lines[1] = line2 +'\n'
				
    with open(fileName, "w") as f:
	f.writelines(lines) #write back
	f.close()
    return 0

def editL2(fileName, line):
    with open(fileName) as f:
	lines = f.readlines() 
	f.close()
	
    lines[1] = line + '\n'
    
    with open(fileName,'w') as f:
	f.writelines(lines)
	f.close()
    return


def getTheoryFile(fileName):
    theory = ''
    with open(fileName) as f:
	lines = f.readlines()
	f.close()
	print(lines[1])
	if 'MP2' in lines[1]:
	    theory = 'MP2' 
	elif 'HF' in lines[1]:
	    theory = 'SCF'
	elif 'CC' in lines[1]:
	    theory = 'CC' 
	elif 'CI' in lines[1]:
	    theory = 'CI'
	else:
	    theory = 'SCF'
    return theory



def csv(fileName,dic1, dic2):
    
    str1 = []
    str2 = []
    
    dic1 =  sorted(dic1.items())   
    dic2 =  sorted(dic2.items())
    
    
    for k , v in dic1:
	str1.append(k)
	str2.append(str(v))    
	
    for k , v in dic2:
	str1.append(k)
	str2.append(str(v))
	

    with open(fileName, 'w') as f:
	#line1 = ';'.join(dic1.keys())+';'  + ';'.join(dic2.keys())
	
	
	#line2 = ';'.join( map(str , dic1.values() ) )+';' + ';'.join( map(str , dic2.values() ) )
	line1 = ';'.join(str1)
	line2 = ';'.join(str2)
	
	f.write(line1 +'\n')
	f.write(line2)
	
	f.close()
    return 0
	
    

	
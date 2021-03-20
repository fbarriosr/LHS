def printElement(element, large):
	print element.replace(element, element * large,1)
	return 0
		
def printElementName(name,element, large):
	s = element.replace(element, element * large,1)
	name = ' '+name+' '
	t1 = len(name)
	t2 = len(s)

	position = t2/2 - t1/2 -1

	s = s[:position] + name + s[position+t1:]
	print s

	return 0

	
def printList(name,lista):
    printElementName(name,'-',40)
    if len(lista) == 0:
	printElementName('Lista Vacia','*',40)
    else:
	for data in lista:
	    print(data)
    printElement('-',40)
    return  0
    
    
def printListDDP(name,lista):
    printElementName(name,'-',40)
    if len(lista) == 0:
	printElementName('Lista Vacia','*',40)
    else:
	for data in lista:
	    data.view()
    printElement('-',40)
    return 0
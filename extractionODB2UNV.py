import os,time
from odbAccess import *
import numpy as np

fnom_odb='Job-10.odb'

myodb=openOdb(fnom_odb)

instances = myodb.rootAssembly.instances
halfnbrenode = len(myodb.rootAssembly.instances['LOWER'].nodes)
halfnbreelement = len(myodb.rootAssembly.instances['LOWER'].elements)
id_node = 1;
print "-1"
print "2411"
for instance in instances.keys():
	for node in myodb.rootAssembly.instances[instance].nodes:
		print "	"+str(id_node)+"	1	1	11"
		print " "+str(node.coordinates[0]*1E3)+" 0 "+str(node.coordinates[1]*1E3)
		#print "ID: "+str(id_node)+" X: "+str(node.coordinates[0])+" Z:"+str(node.coordinates[1])+" label:"+node.instanceName+"/"+str(node.label)
		id_node+=1

print "-1"
print "-1"
print "2412"
id_element = 1;
for instance in instances.keys():
	for element in myodb.rootAssembly.instances[instance].elements:
		new_connectivity = []
		for a in range(0,len(element.connectivity)):
			if element.instanceNames[a]=='UPPER':
				new_connectivity.append(str(halfnbrenode+element.connectivity[a]))
			else:
				new_connectivity.append(str(element.connectivity[a]))
		print "\t"+str(id_element)+"	94         1         1        11         8"
		print " "+"\t".join(new_connectivity)
		#print "ID: "+str(id_elements)+" Connectivity: "+str(new_connectivity)+" / Old: "+str(element.instanceNames)+"/ "+str(element.connectivity)+" - label:"+element.instanceName+"/"+str(element.label)
		id_element+=1
print "-1"
print "-1"
print "Temperature"
data,id_element = 0,0
tmpField=myodb.steps['Step-1'].frames[-1].fieldOutputs['TEMP'].values
for results in tmpField:
	instance = results.instance.name
	if instance=="UPPER":
		id_element = halfnbreelement+results.elementLabel
	else:
		id_element = results.elementLabel
		
	data = (data*(results.integrationPoint-1)+results.data)/results.integrationPoint
	if results.integrationPoint==4:
		print "\t"+str(id_element)+"\t 1"
		print " "+str(data)
print "-1"
"-1"
print "StressTensor"
data,id_element = np.array([0.0,0.0,0.0,0.0]),0
tmpField=myodb.steps['Step-1'].frames[-1].fieldOutputs['S'].values
for results in tmpField:
	instance = results.instance.name
	if instance=="UPPER":
		id_element = halfnbreelement+results.elementLabel
	else:
		id_element =results.elementLabel
		
	data +=results.data
	if results.integrationPoint==4:
		data = data/4
		print "\t"+str(id_element)+"\t 6"
		print " "+str(data[0]*1E-6)+" 0 "+str(data[2]*1E-6)+" "+str(data[3]*1E-6)+" 0 "+str(data[1]*1E-6)
		data =np.array([0.0,0.0,0.0,0.0])
print -1


myodb.close()

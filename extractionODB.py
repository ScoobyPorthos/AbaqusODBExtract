import os,time
from odbAccess import *
import numpy as np
import sys

fnom_odb=sys.argv[1]
fnom_disp1=sys.argv[2]


myodb=openOdb(fnom_odb)
dispFile1=open(fnom_disp1,'w')


#nodes = myodb.rootAssembly.instances['LOWER'].nodes
#elements = myodb.rootAssembly.instances['LOWER'].elements
	
#mySetBANDE = myodb.rootAssembly.instances['LOWER']

tmpField=myodb.steps['Step-1'].frames[-1].fieldOutputs['S'].values

elementID, temperature=0,[]
data = np.array([[0.0,0.0,0.0,0.0]]);
for results in tmpField:
	if results.integrationPoint==1:
		nodes = myodb.rootAssembly.instances[results.instance.name].nodes
		elements = myodb.rootAssembly.instances[results.instance.name].elements
		data = np.array([[0.0,0.0,0.0,0.0]]);
		elementID=results.elementLabel
		connectivity = np.array([[0.0,0.0,0.0]])
		for node in elements[results.elementLabel-1].connectivity:
				connectivity=np.concatenate((connectivity,[nodes[node-1].coordinates]),axis=0)	
		data = np.concatenate((data,[results.data]),axis=0)
	elif results.integrationPoint==4:
		data = np.concatenate((data,[results.data]),axis=0)
		connectivity=np.average(connectivity,axis=0, weights=[0,1,1,1,1,1,1,1,1])
		data=np.average(data,axis=0, weights=[0,1,1,1,1])
		dispFile1.write('%10.6E %10.6E %10.6E %10.6E %10.6E %10.6E\n' % \
					(connectivity[0],connectivity[1],data[0],data[1],data[2],data[3]))
	else:
		data=np.concatenate((data,[results.data]),axis=0)
	
print "Ok "+fnom_disp1+" written"
dispFile1.close()
myodb.close()
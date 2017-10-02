import os,time
from odbAccess import *
import numpy as np
import sys

fnom_odb=sys.argv[1]
fnom_disp1=sys.argv[2]

myodb=openOdb(fnom_odb)
dispFile1=open(fnom_disp1,'w')

tmpField=myodb.steps['Step-1'].frames[-1].fieldOutputs['TEMP'].values

elementID, temperature=0,[]
data = 0;
for results in tmpField:
	if results.integrationPoint==1:
		nodes = myodb.rootAssembly.instances[results.instance.name].nodes
		elements = myodb.rootAssembly.instances[results.instance.name].elements
		elementID=results.elementLabel
		connectivity = np.array([[0.0,0.0,0.0]])
		for node in elements[results.elementLabel-1].connectivity:
				connectivity=np.concatenate((connectivity,[nodes[node-1].coordinates]),axis=0)	
		data = [results.data]
	elif results.integrationPoint==4:
		data.append(results.data)
		connectivity=np.average(connectivity,axis=0, weights=[0,1,1,1,1,1,1,1,1])
		dispFile1.write('%10.6E %10.6E %10.6E\n' % \
					(connectivity[0],connectivity[1],np.average(data)))
	else:
		data.append(results.data)
	
print "Ok "+fnom_disp1+" written"
dispFile1.close()
myodb.close()

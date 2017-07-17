import os,time
from odbAccess import *
import numpy as np

fnom_odb='Job_5_temp.odb'
fnom_disp1='Output_temp.txt'
#fnom_disp2='Output_mean_strain_contrainte_imposee_f1.txt'

myodb=openOdb(fnom_odb)
dispFile1=open(fnom_disp1,'w')
#dispFile2=open(fnom_disp2,'w')

nodes = myodb.rootAssembly.instances['UWP-1'].nodes

elements = myodb.rootAssembly.instances['UWP-1'].elements
	
mySetBANDE = myodb.rootAssembly.instances['UWP-1'].elementSets['UWP']

tmpField=myodb.steps['Step-1'].frames[-1].fieldOutputs['TEMP'].getSubset(region=mySetBANDE).values
elementID, temperature=0,[]
maximum =0;
for results in tmpField:
	if elementID!=results.elementLabel:
		elementID=results.elementLabel
		connectivity = []
		for node in elements[results.elementLabel-1].connectivity:
				connectivity.append(nodes[node-1].coordinates)		
		c = np.array([connectivity[0],connectivity[1],connectivity[2],connectivity[3]])
		
		X = 0
		for x in c[:,0]:
			X +=x
		Y = 0
		for y in c[:,1]:
			Y +=y
	
		temp = results.data
	else:
		temp = (temp*(results.integrationPoint-1)+results.data)/results.integrationPoint
	
	if results.integrationPoint==4:
		temperature.append((X/4,Y/4,temp))
	
for i in range(0,len(temperature)):
	print str(i)+" - X : "+str(temperature[i][0])+" - Y: "+str(temperature[i][1])+" T:"+str(temperature[i][2])
	dispFile1.write('%10.6E %10.6E %10.6E %10.6E\n' % \
					(i,temperature[i][0], temperature[i][1],temperature[i][2]))

print "Ok file written"
dispFile1.close()
#dispFile2.close()
myodb.close()

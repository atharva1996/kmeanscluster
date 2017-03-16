import sys
import math
def distance(px,py,p,index):
	dist = math.sqrt((p[0] - px[index])**2 + (p[1] - py[index])**2)
	return dist
def comp(list1, list2):
    for val in list1:
        if val in list2:
            return True
    return False
px = [1, 1.5, 3, 5, 3.5, 4.5, 3.5]
py = [1, 2, 4, 7, 5, 5, 4.5]
print("Point\t\X\tY")
for index in range(len(px)):
	print(index+1,"\t",px[index],"\t",py[index])
print
print ("3 Clusters are to be formed")
n = int(input("Enter first point: "))
m = int(input("Enter second point: "))
o = int(input("Enter third point: "))
n -= 1
m -= 1
o -= 1

a = [px[n], py[n]]
b = [px[m], py[m]]
c = [px[o], py[o]]

cluster1 = []
cluster2 = []
cluster3 = []
while True:
	temp1 = cluster1
	temp2 = cluster2
	temp3 = cluster3
	del cluster1[:]
	del cluster2[:]
	del cluster3[:]
	for index in range(len(px)):
		d1 = distance(px,py,a,index)
		d2 = distance(px,py,b,index)
		d3 = distance(px,py,c,index)
		if (d1<=d2) and (d1<=d3):
			cluster1.append(index+1)
		if (d2<d1) and (d2<=d3):
			cluster2.append(index+1)
		if (d3<d2) and (d3<d1):
			cluster3.append(index+1)
	
	cluster1.sort()
	cluster2.sort()
	cluster3.sort()
	
	c1x = 0
	c1y = 0
	for i in range(len(cluster1)):
		c1x += px[cluster1[i]-1]
		c1y += py[cluster1[i]-1]
	c1x = c1x/len(cluster1)
	c1y = c1y/len(cluster1)
	a[0] = c1x;
	a[1] = c1y;
	
	c2x = 0
	c2y = 0
	for i in range(len(cluster2)):
		c2x += px[cluster2[i]-1]
		c2y += py[cluster2[i]-1]
	c2x = c2x/len(cluster2)
	c2y = c2y/len(cluster2)
	b[0] = c2x;
	b[1] = c2y;
	
	c3x = 0
	c3y = 0
	for i in range(len(cluster3)):
		c3x += px[cluster3[i]-1]
		c3y += py[cluster3[i]-1]
	c3x = c3x/len(cluster3)
	c3y = c3y/len(cluster3)
	c[0] = c3x;
	c[1] = c3y;
	
	if comp(temp1,cluster1) and comp(temp2,cluster2) and comp(temp3,cluster3):
		break
print(cluster1, cluster2, cluster3)

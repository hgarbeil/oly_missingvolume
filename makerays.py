import numpy as np
import matplotlib.pyplot as plt
import math

# dem characteristics
nsamps = 2765
nlines = 2910
pixdim = 463

# slope of line
slopedeg = 2.5
tanslope = math.tan (slopedeg * math.pi / 180.)
fd = open ('OlyMons2', 'rb')
dem = np.fromfile(fd, dtype=np.int16).reshape((nlines,nsamps))
# init output array
outarr = np.zeros((nlines,nsamps),dtype=np.float32)+(-99999)

x_cent = 1638
y_cent = 1712
x0=[]
y0=[]

# read in the escarpment file
esfile = open ("Escarp_full.txt", 'r')
for line in esfile :
    line.strip()
    myvals = line.split()
    x0.append(float(myvals[1]))
    y0.append(float(myvals[2]))
esfile.close()

#plt.plot(x0, y0, 'b.')
#plt.show()

npts_on_arc = len(x0)

print "Number of points on arc is : ", len(x0)
for i in range (npts_on_arc) :
    print 'working on point : ', i
    # go from each point to get trajectory
    x = int(x0[i]+.5)
    y = int(y0[i]+.5)
    dx = float(x - x_cent)
    dy = float(y - y_cent)
    tdist = math.sqrt(dx * dx + dy * dy)
    dx = dx / tdist
    dy = dy / tdist
    z_start = dem[y,x]
    print x, y, z_start
    for idist in range (0,1000) :
        xloc = int(dx * idist + x + 0.5)
        yloc = int(dy * idist + y + 0.5 )
        newdist = pixdim * math.sqrt((xloc - x) * (xloc-x) + (yloc-y) * (yloc-y))
        #newz = z_start - tanslope * newdist
        newz =  z_start - tanslope * idist * pixdim
        outarr[yloc,xloc]=newz
        if (newdist < pixdim * 70) :
            continue
        if (xloc <= 0) :
            break
        if (yloc <=0 | yloc==nlines-1) :
            break

        demval = dem[yloc,xloc]
        if (newz <= demval) :
            print "segment done at : ", idist
            break

outarr.tofile ("version2/outrays_2p5deg")
print np.min(outarr)
print np.max(outarr)
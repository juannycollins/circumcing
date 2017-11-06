#!/usr/bin/env python
import numpy
import os
import time
import random
import matplotlib.pyplot as plt

import uber_points
import subroutines



#######################################################################        
def main():
    
    isize = 10
    num_initial_points= 4

# Arrays
    
    points = numpy.ndarray(shape=(isize+1,2), dtype=float, order='F')

    angle_range = numpy.ndarray(shape=(2), dtype=float, order='F')
    points_dists_from_zero = numpy.ndarray(shape=(isize),dtype=float,order='F')
#Setup array for perims
    perims =numpy.ndarray(shape=(isize),dtype=float,order='F')
#Setup array for only perim points.
    perim_points = numpy.ndarray(shape=(isize+2,2), dtype=float, order='F')

    periml = 0
    np = 0
    for i in range(isize+1):
        points[i] = [0.0,0.0]
    for i in range(isize+2):
        perim_points[i] = [0.0,0.0]
    for i in range(isize):
        perims[i] = 0.0
        points_dists_from_zero[i] = 0.0
    
    rangeinput = num_initial_points

    anglesize = 2.0*numpy.pi/float(num_initial_points)
    
    angle_range = [0,anglesize]

    deleteit =  open('pointfile','w')
    
    if(os.path.exists('in_pointfile')):
        Inpointfile = open('in_pointfile','r')
        ichip=0
        for line  in Inpointfile:
            tmplist = line.split()
            xxx = float(tmplist[0])
            yyy = float(tmplist[1])
            points[ichip,0] = xxx
            points[ichip,1] = yyy
            plt.plot(xxx,yyy,"r-")
            ichip = ichip+1
    else:

        for point_num in range(rangeinput):
            simbad = subroutines.random_points(angle_range)
            simbad.openit()
            points[point_num]=simbad.giveit()
            angle_range[0] = angle_range[0] + anglesize
            angle_range[1] = angle_range[1] + anglesize
            simbad.writeit()
        
    points[num_initial_points] =points[0]

    fp = subroutines.distance(points)
    
    points_dist_from_zero = fp.get_distance_to_zero()


# get index of the points array that is the farthest from the middle

    bigest_rad = fp.get_bigest_distance_from_zero()

    print (" farthest value from middle =",bigest_rad)

    findex=fp.get_point_index_thats_farthest_from_middle()

    
    print (" index of point farthest from middle =",findex)

    
# get perimeter length
    
    print(" total perimeter length =",subroutines.perimeter(points).total_length())
    

# initialize graphics
    ax = plt.subplot()
    ax.set_ylim([-1.9,1.9])
    ax.set_xlim([-1.9,1.9])

    pa1 = subroutines.plot_array(points)
    
    pa1.plotit("b.")
    pa1.plotredpoint(findex)



    currentindex = findex

# find bigest angel and plot it

    bigest_angle = 0.0

    big_one = 0.0
    
    currentindex = findex
    originx = points[findex,0]+.001
    originy = points[findex,1]+.001

#FIND THE BIGEST ANGLE WITH THE FINDEX INDEX IN THE MIDDLE
      

    peacan = subroutines.pie_corners(points,findex)
    (peacan_side1,peacan_point,peacan_side2) = peacan.get()

    perim_points[np] =points[findex]
#    np = np +1
#    perim_points[np] =points[peacan_side1]
    np = np +1
    perim_points[np] =points[peacan_side2]

    
    bookmark_side1 = peacan_side1
    bookmark_side2 = peacan_side2
    bookmark_point = peacan_point


#jlc    peacan.seeit()
    peacan_len_1,peacan_len_2 = peacan.lengthit()
    perims[0] = peacan_len_1
    perims[1] = peacan_len_2
    periml = periml + 1
    start_corner = findex
    

    dipe = 0
    while (dipe == 0):
    
#FIND THE BIGEST ANGLE WITH THE second peacan side as MIDDLE INDEX    
        findex=bookmark_side2
        cocanut = subroutines.pie_corners(points,findex)

        (cocanut_side1,cocanut_point,cocanut_side2) = cocanut.get()
    
#Continue the same way around Perimeter Get BIGEST angle.

        if (cocanut_side2 != bookmark_point):
            findex=cocanut_side2
        else:
            findex=cocanut_side1
    
        apple = subroutines.pie_corners(points,findex)
        np=np+1
        perim_points[np] = points[findex]
    
#See if we are threw going around
    
        if(peacan_side1 == findex):

#jlc            plt.plot([points[peacan_side1,0],points[bookmark_side2,0]],
#jlc                     [points[peacan_side1,1],points[bookmark_side2,1]])
            spanx = points[peacan_side1,0]-points[bookmark_side2,0]
            spany = points[peacan_side1,1]-points[bookmark_side2,1]
            length_bookmark_side1_side2 = numpy.sqrt(spanx*spanx+spany*spany)
            periml = periml + 1
            perims[periml]=length_bookmark_side1_side2

            dipe = 1
        else:
            (apple_side1,apple_point,apple_side2) = apple.get()
#jlc            apple.seeit()
            apple_len_1,apple_len_2 = apple.lengthit() 
            perims[periml+1]=apple_len_1
            perims[periml+2]=apple_len_2
            periml = periml+2
            if(apple_side1 == cocanut_point): 
                bookmark_side1 = apple_side1
                bookmark_side2 = apple_side2
                np=np+1
                perim_points[np]=points[apple_side2]
            else:
                bookmark_side1 = apple_side2
                bookmark_side2 = apple_side1
                np=np+1
                perim_points[np]=points[apple_side1]
  
            bookmark_point = apple_point
            if(bookmark_side2 == peacan_side1):
                dipe=1
#   add 1 to periml to get length of perims since it goes from 0 to periml
    periml = periml + 1
    Initial_perimeter = numpy.sum(perims[0:periml])
    
    npprim = np
# set a Temporary Point outside or perim
    npprim = npprim + 2
    perim_points[npprim] = perim_points[0]
    print(" npprim=",npprim)

    findex = npprim - 1
    perim_points[findex] = [0.0,1.0]


    npprim = npprim + 1
    print(perim_points[0:npprim+1])

    print("  npprim=",npprim)


    fp_perim = subroutines.distance(perim_points[0:npprim])
    points_dist_from_zero = fp_perim.get_distance_to_zero()
    smallest_rad = fp_perim.get_smallest_distance_from_zero()
    smallest_rad_index = fp_perim.get_smallest_index()




    degree = numpy.arctan(1.0)/45.0

    target = Initial_perimeter+.07
    
# 360 Loop
    current_was_x =-999
    current_was_y =-999
    start_radius = 1.0



        
    for anng in range(360):
        current_x = numpy.cos(degree*anng)
        current_y = numpy.sin(degree*anng)
        radius = start_radius
        current_length = 999.0
        print ("                               anng=",anng)

        while current_length > target:
            radius = radius - .005
            current_x = radius*numpy.cos(anng*degree)
            current_y = radius*numpy.sin(anng*degree)
            
            perim_points[findex] = [current_x,current_y]
            tingle = uber_points.uber_duber(perim_points[0:npprim],npprim,findex)
            current_length = tingle.uber_duber_length()

        start_radius = radius + .05



        if(current_was_x == -999):
            current_was_x=current_x
            current_was_y=current_y
        
        plt.plot([current_was_x,current_x],[current_was_y,current_y])
        current_was_x=current_x
        current_was_y=current_y
        
    print(" Last Current Length",current_length)
    print(" Initial_perimeter=",Initial_perimeter)


    plt.show()



if __name__ == "__main__":
    main()
           

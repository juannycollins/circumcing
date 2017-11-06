#!/usr/bin/env python
import numpy
import os
import time
import random
import matplotlib.pyplot as plt
import subroutines

class uber_duber:
    def __init__(self,points,isiz,findex):
        self.pts = points
        self.isiz  = isiz
#        print ("@uber points=",points)
#        print("isiz=",self.isiz)
        self.findex = findex
        self.np = 0
        self.periml = 0
        self.quit_flag = 0
        self.prims =numpy.ndarray(shape=(self.isiz+2),dtype=float,order='F')
        self.prim_points = numpy.ndarray(shape=(isiz+2,2),dtype=float, order='F')

    def uber_duber_length(self):
        self.can = subroutines.pie_corners(self.pts,self.findex)
        (self.can_side1,self.can_point,self.can_side2) = self.can.get()

        self.prim_points[self.np] = self.pts[self.findex]

#        self.np = self.np +1
#        self.prim_points[self.np] = self.pts[self.can_side1]
        self.np = self.np +1
        self.prim_points[self.np] = self.pts[self.can_side2]
    
        self.bookmark_side1 = self.can_side1
        self.bookmark_side2 = self.can_side2
        self.bookmark_point = self.can_point
        
#        self.can.seeit()
        self.prims[0],self.prims[1] = self.can.lengthit()
        self.periml = self.periml + 1


        count = 0
        while (self.quit_flag == 0 ):
            count  = count +1
#            print ("%%%%%%%%%%% count =",count," self.np=",self.np," isiz=",self.isiz)
#            print("@@@@@@@@@@@@@@@@@@@")
#            print(self.pts)
#            print("@@@@@@@@@@@@@@@@@@@")
            
#FIND THE BIGEST ANGLE WITH THE second self.can side as MIDDLE INDEX
            self.findex=self.bookmark_side2
            self.coco = subroutines.pie_corners(self.pts,self.findex)
            (self.coco_side1,self.coco_point,self.coco_side2) = self.coco.get()

#            self.np=self.np+1
#            self.prim_points[self.np] = self.pts[self.findex]
    
#Continue the same way around Perimeter Get BIGEST angle.

            if (self.coco_side2 != self.bookmark_point):
                self.findex=self.coco_side2
            else:
                self.findex=self.coco_side1
    
            self.ple = subroutines.pie_corners(self.pts,self.findex)
            self.np=self.np+1
            self.prim_points[self.np] = self.pts[self.findex]
    
#See if we are threw going around
    
            if(self.can_side1 == self.findex):
                plt.plot([self.pts[self.can_side1,0],self.pts[self.bookmark_side2,0]],
                         [self.pts[self.can_side1,1],self.pts[self.bookmark_side2,1]])
                spanx = self.pts[self.can_side1,0]-self.pts[self.bookmark_side2,0]
                spany = self.pts[self.can_side1,1]-self.pts[self.bookmark_side2,1]
                self.length_bookmark_side1_side2 = numpy.sqrt(spanx*spanx+spany*spany)
                self.periml = self.periml + 1
                self.prims[self.periml]=self.length_bookmark_side1_side2
            
                self.quit_flag = 1
            
            else:
                (self.ple_side1,self.ple_point,self.ple_side2) = self.ple.get()
                self.ple.seeit()
                
                length1,length2=self.ple.lengthit()
                self.prims[self.periml+1]=length1
                self.prims[self.periml+2]=length2
#                self.prims[self.periml+1],self.prims[self.periml+2] = self.ple.lengthit() 
                self.periml = self.periml+2
                if(self.ple_side1 == self.coco_point): 
                    self.bookmark_side1 = self.ple_side1
                    self.bookmark_side2 = self.ple_side2
                    self.np=self.np+1
#                    print("self.ple_side1=",self.ple_side1,"np=",self.np,self.bookmark_side2,self.can_side1,self.can_side2,self.coco_point)
#                    print(self.prim_points)
                    self.prim_points[self.np]=self.pts[self.ple_side2]
                else:
                    self.bookmark_side1 = self.ple_side2
                    self.bookmark_side2 = self.ple_side1
                    self.np=self.np+1
                    self.prim_points[self.np]=self.pts[self.ple_side1]
                self.bookmark_point = self.ple_point
                if(self.bookmark_side2 == self.can_side1):
                    self.quit_flag=1

#        print("perims=")
#        print(self.prims[0:self.periml+1])
        self.uber_length=numpy.sum(self.prims[0:self.periml+1])
#        print(" self.np=",self.np)

#        print(self.prim_points[0:self.np+1])
        
#        self.ppg= subroutines.plot_array(self.prim_points[0:self.np+1])    
#        self.ppg.plotit_label("ys")


        
        return self.uber_length
    



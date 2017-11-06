#!/usr/bin/env python
import numpy
import os
import time
import random
import matplotlib.pyplot as plt

import uber_points

class pie_corners:
    def __init__(self,points,findex):
        self.points = points
        self.findex = findex
        self.side1 =0
        self.side2=0
    def get(self):
        big_one = 0.0
        isize  = len(self.points)
        for i in range(isize):
            if(i != self.findex):
                for j in range(isize):
                    if(j != i and j !=self.findex):
                        Z3 = three_points(self.points[self.findex,0],self.points[self.findex,1],
                                          self.points[i,0],self.points[i,1],
                                          self.points[j,0],self.points[j,1])
                        Z3.dot_product()
                        angle_dot = Z3.angdot()
                        if(angle_dot > big_one):
                            self.side1=i
                            self.side2=j
                            big_one = angle_dot
#        print  ("##############",self.side1,self.findex,self.side2)                 
        return (self.side1,self.findex,self.side2)
    def seeit(self):
        plt.plot([self.points[self.side1,0],self.points[self.findex,0]],
                 [self.points[self.side1,1],self.points[self.findex,1]])
        plt.plot([self.points[self.side2,0],self.points[self.findex,0]],
                 [self.points[self.side2,1],self.points[self.findex,1]])
        return
    def lengthit(self):
        delta1x = self.points[self.side1,0] - self.points[self.findex,0]
        delta1y = self.points[self.side1,1] - self.points[self.findex,1]
        length1 = numpy.sqrt(delta1x*delta1x+delta1y*delta1y)
        delta2x = self.points[self.side2,0] - self.points[self.findex,0]
        delta2y = self.points[self.side2,1] - self.points[self.findex,1]
        length2 = numpy.sqrt(delta2x*delta2x+delta2y*delta2y)
        return length1,length2
        
class new_array:
    def __init__(self,points):
        self.points = points
        self.lll = len(points)
        self.new_points = numpy.ndarray(shape=(self.lll,2), dtype=float, order='F')
        self.tmp_point = numpy.ndarray(shape=(2), dtype=float, order='F')
    def rearrange(self,index,newplace):
        self.new_points = numpy.copy(self.points)
        if(newplace == index):
            return self.new_points
        self.tteemmppc = self.new_points[newplace]
        self.tteemmpp =  numpy.copy(self.tteemmppc)
        self.new_points[newplace]=self.new_points[index]
        self.new_points[index]=self.tteemmpp
        self.new_points[self.lll-1]=self.new_points[0]

        return self.new_points

class three_points:
    def __init__(self,x1,y1,x2,y2,x3,y3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        
        self.deltxa = self.x2-self.x1
        self.deltxb = self.x3-self.x1
        self.deltya = self.y2-self.y1
        self.deltyb = self.y3-self.y1
        
        self.maga = numpy.sqrt(self.deltxa*self.deltxa+self.deltya*self.deltya)
#        print(" self.deltxb=",self.deltxb)
#        print(" self.deltyb=",self.deltyb)
        
        self.magb = numpy.sqrt(self.deltxb*self.deltxb+self.deltyb*self.deltyb)
#        print(" self.magb=",self.magb)
    def dot_product(self):
        return self.deltxa*self.deltxb+self.deltya*self.deltyb
    def angdot(self):
        self.denom = self.maga*self.magb
        if self.denom > 0.0:
            self.dp = self.dot_product()
            self.cosiine=self.dp/self.denom
            return numpy.arccos(self.cosiine)
        else:
            return  0.0
    def determinant(self):
        """
        calculate the determinant
        """
        return (self.x2-self.x1)*(self.y3-self.y1)-(self.x3-self.x1)*(self.y2-self.y1)
    def print_input(self):
        print(" x1=",self.x1," y1=",self.y1)
        print(" x2=",self.x2," y2=",self.y2)
        print(" x3=",self.x3," y3=",self.y3)
        print(" maga=",self.maga)
        print(" magb=",self.magb)






class distance:
    def __init__(self,points):
        self.points = points
        self.size = len(self.points) - 1
        self.points_dists_from_zero=numpy.ndarray(shape=(self.size),dtype=float,order='F')
        
    def get_distance_to_zero(self):
        lll=self.size
        
        for i in range(lll):
            ttt = self.points[i,0]*self.points[i,0]+self.points[i,1]*self.points[i,1]
            self.points_dists_from_zero[i] = numpy.sqrt(ttt)
        return self.points_dists_from_zero
    def get_bigest_distance_from_zero(self):
        bigone = numpy.amax(self.points_dists_from_zero)
        return bigone
    def get_smallest_distance_from_zero(self):
        littleone = numpy.amin(self.points_dists_from_zero)
        return littleone
    def get_smallest_index(self):
        littleindex = numpy.argmin(self.points_dists_from_zero)
        return littleindex
    def get_point_index_thats_farthest_from_middle(self):
        bigindex = numpy.argmax(self.points_dists_from_zero)
        return bigindex
    
class perimeter:
    def __init__(self,array):
        self.points = array
        self.numlines = len(self.points)-1
        self.squares = numpy.ndarray(shape=(self.numlines),dtype=float, order='F')
        self.lengths = numpy.ndarray(shape=(self.numlines),dtype=float, order='F')

    def squared(self):
        for i in range(self.numlines):
            self.d1 = self.points[i,0]-self.points[i+1,0]
            self.d2 = self.points[i,1]-self.points[i+1,1]
            self.squares[i] = self.d1*self.d1+self.d2*self.d2
        print (" squares=",self.squares)
        return self.squares       

    def length(self):
        ttt = self.squared()
        self.lengths = numpy.sqrt(self.squares)
        return self.lengths
    
    def total_length(self):
        tttt = self.length()
        return numpy.sum(self.lengths)
            
class plot_array:
    def __init__(self,d2_array):
        self.points = d2_array
    def plotit(self,color):
        for i in range(len(self.points)):
#            print(self.points[i,0])
#            print(self.points[i,1])
            x=self.points[i,0]
            y=self.points[i,1]
            plt.plot(x,y,color)
    def plotit_label(self,color):
        for i in range(len(self.points)):
#            print(self.points[i,0])
#            print(self.points[i,1])
            x=self.points[i,0]
            y=self.points[i,1]
            plt.plot(self.points[i,0],self.points[i,1],color)
            plt.annotate(str(i),xy=(x,y))
    def plotredpoint(self,index):
        plt.plot(self.points[index,0],self.points[index,1],'ro')
        return
    def plotgreenpoint(self,index):
        plt.plot(self.points[index,0],self.points[index,1],'ro')
        return

            

class random_points:
    def __init__(self,angle_range):
        self.angle_range = angle_range
#        self.angle_degree = random.randint(self.angle_range[0],self.angle_range[1])
#        self.degreerange_factor= float(self.angle_degree)/360.00
        self.rdom = random.random()
        self.radius = 1.0 - self.rdom*self.rdom
        self.angle_radians = self.angle_range[0]+(self.angle_range[1]-self.angle_range[0])*random.random()


        self.sin_radians = numpy.sin(self.angle_radians)
        self.cos_radians = numpy.cos(self.angle_radians)
        self.x = self.radius*self.cos_radians
        self.y = self.radius*self.sin_radians

    def giveit(self):
        return self.x,self.y

    
    def openit(self):
        self.rpfile =  open('pointfile','a')
        return
    def writeit(self):
        ymp_string=str(self.x)+' '+str(self.y)+'\n'
        self.rpfile.write(ymp_string)
        return


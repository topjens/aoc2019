# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 06:04:38 2019

@author: Jens
"""

import operator

with open("./input") as file:
    image = file.read().split('\n')[0]
    
image = [int(i) for i in image]

class image:
    
    class layer:
        def __init__(self, pixels):
            self.pixels = pixels
            self.size = len(pixels)
            self.zeros = 0
            self.ones = 0
            self.twos = 0
            for i in pixels:
                if(i == 0):
                    self.zeros += 1
                elif(i == 1):
                    self.ones += 1
                elif(i == 2):
                    self.twos +=1
    
    def __init__(self, path, width, height):
        with open(path) as file:
            self.pixels = file.read().split('\n')[0]
            
        self.pixels = [int(i) for i in self.pixels]
        
        self.width = width
        self.height = height
        self.layer_size = width * height
        
        assert((len(self.pixels) % self.layer_size) == 0)
        
        self.num_layers = int((len(self.pixels) / self.layer_size))
        
        self.layers = []
        
        for i in range(0, self.num_layers):
            self.layers.append(self.layer(self.pixels[i*self.layer_size:(i+1)*self.layer_size]))
            
        self.image = [2] * self.layer_size
        
    def render(self, path = None):
        for layer in self.layers:
            for i in range(layer.size):
                if(self.image[i] == 2):
                    self.image[i] = layer.pixels[i]
                    
        if path == None:
            for i in range(self.height):
                print(self.image[i*self.width:(i+1)*self.width])
        else:
            with open(path, mode='w') as file:
                file.write('P1\n')
                file.write('# Solution to day 8 of AOC 2019\n')
                file.write('%i %i\n' % (self.width, self.height))
                for y in range(self.height):
                    for x in range(self.width):
                        file.write(str(self.image[x + y*self.width]) + ' ')
                    file.write('\n')
                    
        
if __name__ == '__main__':
    img = image("./input", 25, 6)
    
    solution = {}
    
    for i, layer in enumerate(img.layers):
        solution[i] = layer.zeros
        
    # we begin with the maximum possible value of zeros
    min_zeros = img.layer_size
    l = 0
        
    for layer in solution:
        if solution[layer] < min_zeros:
            min_zeros = solution[layer]
            l = layer
            
    print("Layer %i has the least amount of zeros, namely %i" % (l, min_zeros))
    print("Solution of part 1 is %i" % (img.layers[l].ones * img.layers[l].twos))
    
    print("Solution of part 2 is")
    img.render('out.pbm')
#
##remove trailing newline
#image.pop()
#
#image = list(map(int, image))
#
#layer_size = 25*6
#
#layers = []
#
#for i in range(0,100):
#    layers.append(image[i*layer_size : (i+1)*layer_size:])
#    
#solutions = {}
#    
#for i, layer in enumerate(layers):
#    total = 0
#    for j in layer:
#        if(j == 0):
#            total += 1
#    solutions[i] = total
#    
#print(solutions)
#
#print(max(solutions.items(), key=operator.itemgetter(1))[0])
#
#total_one = 0
#total_two = 0
#
#for i in layers[99]:
#    if(i == 1):
#        total_one += 1
#    elif(i == 2):
#        total_two += 1
#        
#print(total_one * total_two)
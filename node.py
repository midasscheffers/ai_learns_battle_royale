import math as mth
import numpy as np



class Node:

    def __init__(self, inputs, weights, output):
        self.bias = 0
        self.inputs = inputs
        self.weights = weights
        self.output = output
        self.change = []
        self.dis_outpt = 0

    def calc_output(self):
        output = 0
        try:
            for i in range(len(self.inputs)):
                output += ((self.inputs[i].output * self.weights[i]))

            output += self.bias
            
            
            output = self.sigmoid(output)
            # output = max(0, output)
            self.output = output
        except:
            print("weights and inputs should be the same lenght")
    

    def avr_change(self):
        avr = 0
        for i in range(len(self.change)):
            for j in range(len(self.change[i])):
                avr += self.change[i][j]
            avr = avr / len(self.change[i])
            self.change[i] = [avr]
    
    def change_weights(self):
        for i in range(len(self.weights)):
            self.weights[i] = self.change[i][0]
    
    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

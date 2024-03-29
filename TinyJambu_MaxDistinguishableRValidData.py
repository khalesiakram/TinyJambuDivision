from gurobipy import *

import time
import os

class TinyJambu:
	def __init__(self, Round, activebits, word, bit):
		self.threads = 8
		self.Round = Round
		self.activebits = activebits
		self.word = word
		self.bit = bit		
		self.blocksize = 128
		self.objectiveBound = self.blocksize - 1		
		self.filename_model = "TinyJambu_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".lp"
		self.filename_modelv2 = "TinyJambu_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + "v2.lp"
		self.filename_modelv3 = "TinyJambu_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + "v3.lp"				
		self.filename_result = "result_" + "_word" + str(self.word) + "_bit" + str(self.bit) + ".txt"
		self.filename_constraint = "constraint_" + str(self.Round) + "_" + str(self.activebits) + "_word" + str(self.word) + "_bit" + str(self.bit) + ".txt"		
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		"""fileobj = open(self.filename_modelv2, "w")
		fileobj.close()		
		fileobj = open(self.filename_modelv3, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()
		fileboj = open(self.filename_constraint, "a")
		fileobj.close()"""
		
	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model
		"""
		fileobj = open(self.filename_model, "w")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,128):
			eqn.append("x" + "_0_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()
	def Createv2(self):
		fileobj = open(self.filename_modelv2, "w")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,128):
			eqn.append("x" + "_0_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

		fileobj = open(self.filename_constraint, "r")
		lines=fileobj.readlines()
		fileobj.close()

		fileobj = open(self.filename_modelv2, "a")
		fileobj.write("Subject To\n")
		for line in lines:
			fileobj.write(line)

		fileobj.write("Binary\n")
		for i in range(0, 1):
			for j in range(0,64):
				fileobj.write("x_" + str(i) + "_" + str(j))
				fileobj.write("\n")
		"""for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("u_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")
		for i in range(0,self.Round):
			for j in range(0,8):
				for k in range(0,4):
					fileobj.write("v_" + str(i) + "_" + str(k) + "_" + str(j))
					fileobj.write("\n")"""
		fileobj.write("END")
		fileobj.close()		
	@staticmethod
	def CreateVariables(n,s):
		"""
		Generate the variables used in the model.
		"""
		array = ["" for i in range(0,129)]
		for i in range(0,129):
			array[i] = s + "_" + str(n) + "_" + str(i)
		return array

	def ConstraintsByCopy(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_model,"a")
		temp = []
		temp.append(variablex)
		temp.append(variableu)
		temp.append(variabley)
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		fileobj.close()
		
	def ConstraintsByCopyv3(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_modelv3,"a")
		temp = []
		temp.append(variablex)
		temp.append(variableu)
		temp.append(variabley)
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		fileobj.close()		

	def ConstraintsByXor(self, variable1, variable2, variable3, variable4, variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_model,"a")
		temp = []
		temp.append(variablex)
		temp.append(variable1)
		temp.append(variable2)
		temp.append(variable3)
		temp.append(variable4)			
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		fileobj.close()      
		
	def ConstraintsByXorv3(self, variable1, variable2, variable3, variable4, variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_modelv3,"a")
		temp = []
		temp.append(variablex)
		temp.append(variable1)
		temp.append(variable2)
		temp.append(variable3)
		temp.append(variable4)			
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		fileobj.close()      		                   
                
	def ConstraintsByAnd(self, variableIn1, variableIn2, variableOut):
		"""
		Generate the constraints by And.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write((variableOut + " - " + variableIn1 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn2 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn1 + " - " + variableIn2 + " <= " + str(0)))
		fileobj.write("\n")
		fileobj.close()	
		
	def ConstraintsByAndv3(self, variableIn1, variableIn2, variableOut):
		"""
		Generate the constraints by And.
		"""
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write((variableOut + " - " + variableIn1 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn2 + " >= " + str(0)))
		fileobj.write("\n")
		fileobj.write((variableOut + " - " + variableIn1 + " - " + variableIn2 + " <= " + str(0)))
		fileobj.write("\n")
		fileobj.close()			

	def Constrain(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")

		eqn = []
		"""for i in range(0,16):
			for j in range(0,8):
				eqn.append("x" + "_0_" + str(8*i+j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")"""
		
		#set the (target) active bit in the final state (output of round R):		
		for i in range(0,16):
			for j in range(0,8):
				if ((i == self.word) and (j == self.bit)):
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(8*i+j) + " = 1\n")
				else:
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(8*i+j) + " = 0\n")
		fileobj.close()
		for i in range(0,self.Round):
			variableIn = TinyJambu.CreateVariables(i,"x")#array of 128 binary variables corresponding to the internal state in the i_th update
			variableOut = TinyJambu.CreateVariables(i+1,"x")#array of 128 binary variables corresponding to the internal state in the (i+1)_th update
			variableBr = TinyJambu.CreateVariables(i,"br")#variables used for modeling the copy operator
			self.ConstraintsByCopy(variableIn[47],variableOut[46],variableBr[47])
			self.ConstraintsByCopy(variableIn[70],variableOut[69],variableBr[70])
			self.ConstraintsByCopy(variableIn[85],variableOut[84],variableBr[85])
			self.ConstraintsByCopy(variableIn[91],variableOut[90],variableBr[91])
			fileobj = open(self.filename_model, "a")
			for j in range(0,127):
				if ((j != 46)&(j != 69)&(j != 84)&(j != 90)):
					fileobj.write(str(variableOut[j]) + " - " +str(variableIn[j+1]) + " = 0 \n")
			fileobj.close()
			self.ConstraintsByAnd(variableBr[70],variableBr[85],variableIn[128])
			self.ConstraintsByXor(variableIn[0],variableBr[47],variableIn[128],variableBr[91],variableOut[127])
	def Constraint2(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		#fileobj.write("Subject To\n")

		eqn = []
		for i in range(0,16):
			for j in range(0,8):
				eqn.append("x" + "_0_" + str(8*i+j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write(" <= ")
		fileobj.write(str(self.objectiveBound))
		fileobj.write("\n")
				
		for i in range(0,16):
			for j in range(0,8):
				if ((i == self.word) and (j == self.bit)):
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(8*i+j) + " = 1\n")
				else:
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(8*i+j) + " = 0\n")
		fileobj.close()
		for i in range(0,self.Round):
			variableIn = TinyJambu.CreateVariables(i,"x")#array of 128 binary variables corresponding to the internal state in the i_th update
			variableOut = TinyJambu.CreateVariables(i+1,"x")#array of 128 binary variables corresponding to the internal state in the (i+1)_th update
			variableBr = TinyJambu.CreateVariables(i,"br")#variables used for modeling the copy operator
			self.ConstraintsByCopy(variableIn[47],variableOut[46],variableBr[47])
			self.ConstraintsByCopy(variableIn[70],variableOut[69],variableBr[70])
			self.ConstraintsByCopy(variableIn[85],variableOut[84],variableBr[85])
			self.ConstraintsByCopy(variableIn[91],variableOut[90],variableBr[91])
			fileobj = open(self.filename_model, "a")
			for j in range(0,127):
				if ((j != 46)&(j != 69)&(j != 84)&(j != 90)):
					fileobj.write(str(variableOut[j]) + " - " +str(variableIn[j+1]) + " = 0 \n")
			fileobj.close()
			self.ConstraintsByAnd(variableBr[70],variableBr[85],variableIn[128])
			self.ConstraintsByXor(variableIn[0],variableBr[47],variableIn[128],variableBr[91],variableOut[127])
			
	def Constraint3(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_modelv3, "a")
		fileobj.write("Maximize\n")
		eqn = []
		for i in range(0,128):
			eqn.append("x" + "_0_" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.write("Subject To\n")			
		for i in range(0,16):
			for j in range(0,8):
				if ((i == self.word) and (j == self.bit)):
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(8*i+j) + " = 1\n")
				else:
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(8*i+j) + " = 0\n")
		fileobj.close()
		for i in range(0,self.Round):
			variableIn = TinyJambu.CreateVariables(i,"x")#array of 128 binary variables corresponding to the internal state in the i_th update
			variableOut = TinyJambu.CreateVariables(i+1,"x")#array of 128 binary variables corresponding to the internal state in the (i+1)_th update
			variableBr = TinyJambu.CreateVariables(i,"br")#variables used for modeling the copy operator
			self.ConstraintsByCopyv3(variableIn[47],variableOut[46],variableBr[47])
			self.ConstraintsByCopyv3(variableIn[70],variableOut[69],variableBr[70])
			self.ConstraintsByCopyv3(variableIn[85],variableOut[84],variableBr[85])
			self.ConstraintsByCopyv3(variableIn[91],variableOut[90],variableBr[91])
			fileobj = open(self.filename_modelv3, "a")
			for j in range(0,127):
				if ((j != 46)&(j != 69)&(j != 84)&(j != 90)):
					fileobj.write(str(variableOut[j]) + " - " +str(variableIn[j+1]) + " = 0 \n")
			fileobj.close()
			self.ConstraintsByAndv3(variableBr[70],variableBr[85],variableIn[128])
			self.ConstraintsByXorv3(variableIn[0],variableBr[47],variableIn[128],variableBr[91],variableOut[127])			

	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round)+1):
                        for j in range(0,129):
                        	fileobj.write("x_" + str(i) + "_" + str(j))
                        	fileobj.write("\n")
                        	"""fileobj.write("x_" + str(i) + "_" + str(0))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(47))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(70))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(85))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(91))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(127))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(128))
                        	fileobj.write("\n")"""
		for i in range(0,self.Round):
			fileobj.write("br_" + str(i) + "_47")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_70")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_85")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_91")
			fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()
	def VariableBinaryv3(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0,(self.Round)+1):
                        for j in range(0,129):
                        	fileobj.write("x_" + str(i) + "_" + str(j))
                        	fileobj.write("\n")
                        	"""fileobj.write("x_" + str(i) + "_" + str(0))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(47))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(70))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(85))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(91))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(127))
                        	fileobj.write("\n")
                        	fileobj.write("x_" + str(i) + "_" + str(128))
                        	fileobj.write("\n")"""
		for i in range(0,self.Round):
			fileobj.write("br_" + str(i) + "_47")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_70")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_85")
			fileobj.write("\n")
			fileobj.write("br_" + str(i) + "_91")
			fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()		

	def Init(self):
		"""
		Generate the constraints introduced by the initial division property.
		"""
		variableout = TinyJambu.CreateVariables(0,"x")#corresponding to the 128 bits of the initial state
		fileobj = open(self.filename_model, "a")
		eqn = []
		for i in range(0, 95):
			temp = variableout[i] + " = 0"
			fileobj.write(temp)
			fileobj.write("\n")
		for i in range(96, 128):
			temp = variableout[i] + " = 1"
			fileobj.write(temp)
			fileobj.write("\n")
		"""for i in range(counterInput+1, 128):
			temp = variableout[i] + " = 0"  #for ex search, should be one
			fileobj.write(temp)
			fileobj.write("\n")"""
		fileobj.close()

	def MakeModel(self):
		"""
		Generate the MILP model of TinyJambu given the round number and activebits.
		"""
		#self.CreateObjectiveFunction()
		self.Constrain()
		self.Init()
		self.VariableBinary()

	def SolveModel(self):
		"""
		Solve the MILP model to search the integral distinguisher of TinyJambu.
		"""
		time_start = time.time()
		m = read(self.filename_model)
		m = read(self.filename_model)
		m.params.threads=self.threads	
		#m.params.TimeLimit=36000
		m.optimize()
		obj = m.getObjective()
		print("**********************************************\n")
		print(m.Status)
		print("\n**********************************************\n")
		if(m.Status == 3):							#2:optimal	3:infeasible	9:time_limit	11:interrupted	
			fileobj = open(self.filename_result, "a")	
			fileobj.write("\n Round")
			fileobj.write(str(self.Round))				
			fileobj.write(" Model is infeasible. Integral Distinguisher Found!\n")
		elif(m.Status == 2):
			fileobj = open(self.filename_result, "a")	
			fileobj.write("\n Round")
			fileobj.write(str(self.Round))				
			fileobj.write(" Model is feasible. No Integral Distinguisher!\n")	
		else:
			fileobj = open(self.filename_result, "a")	
			fileobj.write("\n Round")
			fileobj.write(str(self.Round))				
			fileobj.write(" m.status = ")	
			fileobj.write(m.status)											

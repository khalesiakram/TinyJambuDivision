# Algorithm 3 presented in paper "Applyint MILP Method to Searching Integral 
# Distinguishers based on Division Property for 6 Lightweight Block Ciphers"
# Regarding to the paper, please refer to https://eprint.iacr.org/2016/857
# For more information, feedback or questions, pleast contact at xiangzejun@iie.ac.cn

# Implemented by Xiang Zejun, State Key Laboratory of Information Security, 
# Institute Of Information Engineering, CAS

from TinyJambu import TinyJambu

if __name__ == "__main__":
	for j in range(1):
        	tinyJambu = TinyJambu(897-j, 0, 15, 7)

        	tinyJambu.MakeModel()

        	tinyJambu.SolveModel()                	


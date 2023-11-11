from TinyJambu import TinyJambu

if __name__ == "__main__":
	for j in range(1):
        	tinyJambu = TinyJambu(897-j, 0, 15, 7)

        	tinyJambu.MakeModel()

        	tinyJambu.SolveModel()                	


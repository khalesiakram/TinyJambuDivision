from TinyJambu import TinyJambu

if __name__ == "__main__":
	for j in range(30):
        	tinyJambu = TinyJambu(1160-j, 0, 15, 7)

        	tinyJambu.MakeModel()

        	tinyJambu.SolveModel()                	


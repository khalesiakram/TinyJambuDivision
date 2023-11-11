from TinyJambu import TinyJambu
if __name__ == "__main__":

	for j in range(0,1024):
		print("//////////////////////////////////////////////////////")
		print(j)
		tinyJambu = TinyJambu(1024-j, 0, 15, 7)
		tinyJambu.MakeModel()
		tinyJambu.SolveModel()                	

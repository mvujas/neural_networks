from functions import *
 
def main():
	net = prepare_neural_network("brajeva_azbuka_15_2.nnet", 6, 15, 2, 3)
	loop(net)

if __name__ == "__main__":
	main()


from models import *

def prepare_net(nn_file, *layers):
	net = NeuralNetwork(*layers)
	net.load_net_from_file(nn_file)
	return net

def main():
	window = GUI()
	net = prepare_net("brajeva_azbuka_15_2.nnet", 6, 15, 2, 3)
	print "\n ***** Neuronske mreze sa primenama *****\n\n             Brajeva azbuka\n\n ****************************************"
	while True:
		inn = raw_input(" Da li zelite da napustite program?[d/N] ")
		if inn.strip().upper() in ['D', 'DA']:
			break
		window.start()
		data = window.get_info()
		if data['closed'] == True:
			print " Prekid rada programa..."
			break
		print " Pretpostavka neuronske mreze za unetu kombinaciju je \'%c\'" % (net.run(data['result']))
	print 
	
if __name__ == "__main__":
	main()

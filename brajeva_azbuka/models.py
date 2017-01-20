from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import pickle


def delete_line():
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

signs = ['!', '%', '*', '(', ')', '-', '_', '+', '=', ':',
		 ';', '\"', '.', ',', '?', '/', '\'', '#', '@', '^',
		 '&', '$', '\\', '[', ']', '<', '>', ' ']

def decodeRet(*arrgs):
	lista = arrgs[0]
	maxV = max(lista[0], lista[1], lista[2])
	if maxV == lista[0]:
		return str(unichr(ord('A') - 1 + int(round(lista[0] * 100 / 3))))
	elif maxV == lista[1]:
		return str(int(round(lista[1] * 100 / 3) - 1))
	else:
		return signs[int(round(lista[2] * 100 / 3)) - 1]

class NeuralNetwork:
	def __init__(self, *layers, **options):
		opt = {'momentum': 0.99}
		for key in options:
			if key not in list(opt.keys()):
				raise NetworkError('Brain constructor unknown option: %s' % key)
			opt[key] = options[key]

		self.__net = buildNetwork(*layers, hiddenclass=SigmoidLayer, outclass=SigmoidLayer, bias=True)
		self.__data = SupervisedDataSet(layers[0], layers[-1])
		self.__momentum = opt['momentum']
		self.__trainer = BackpropTrainer(self.__net, self.__data, momentum=self.__momentum)
		self.__layers = layers

	def load_dataset_from_file(self, f):
		infile = open(f, 'r')
		for line in infile.readlines():
		    data = [float(x) for x in line.strip().split(',') if x != '']
		    indata = tuple(data[:self.__layers[0]])
		    outdata = tuple(data[self.__layers[0]:])
		    self.__data.addSample(indata,outdata)
		infile.close()
		self.__trainer = BackpropTrainer(self.__net, self.__data, momentum=self.__momentum)

	def write_dataset(self):
		for inpt, target in self.__data:
			print("(", inpt, " ", target, ")")

	def load_net_from_file(self, f):
		infile = open(f, "r")
		self.__net = pickle.load(infile)
		infile.close()
		self.__trainer = BackpropTrainer(self.__net, self.__data, momentum=self.__momentum)

	def get_acc(self):
		if len(self.__data) != 0:
			acc = 0
			for inpt, target in self.__data:
				res = self.__net.activate(inpt)
				if decodeRet(res) in decodeRet(target):
					acc += 1
			print("Preciznost mreze:" + str(float(acc)/len(self.__data)*100) + "%")
		else:
			print("Dataset je prazan")

	def run(self, sample):
		if isinstance(sample, list) and len(sample) == 6:
			res = self.__net.activate(sample)
			return decodeRet(res)
		else:
			return "Greska!"

	def train(self, maxEpochs=1000, desiredError=0):
		print("")
		for epoch in range(0, maxEpochs):
			error = self.__trainer.train()
			delete_line()
			print "Epoch:", epoch + 1, ", greska:", error
			if error < desiredError:
				return error
				break;
		return error

	def save_net_to_file(self, f):
		outfile = open(f, 'w')
		pickle.dump(self.__net, outfile)
		outfile.close()

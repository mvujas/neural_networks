from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, SoftmaxLayer, LinearLayer
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
import pickle
import gc


def delete_line():
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

class NeuralNetwork:
	def __init__(self, *layers):
		self.__net = buildNetwork(*layers, hiddenclass=SigmoidLayer, outclass=SoftmaxLayer)
		self.__tstdata, self.__trndata = ClassificationDataSet(layers[0], nb_classes=10), ClassificationDataSet(layers[0], nb_classes=10)
		self.__layers = layers
		self.__trainer = BackpropTrainer( self.__net, dataset=self.__trndata, momentum=0.1, verbose=True, weightdecay=0.01)
		
		
	def convert_scikit_to_datasets(self, digits):
		data = ClassificationDataSet(self.__layers[0], nb_classes=10)
		for i in range(0, len(digits.images)):
			data.addSample(digits.images[i].ravel(), [digits.target[i]])
		tstdata_temp, trndata_temp = data.splitWithProportion( 0.25 )
		del data
		gc.collect()
		for n in xrange(0, tstdata_temp.getLength()):
			self.__tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )
		del tstdata_temp
		gc.collect()
		for n in xrange(0, trndata_temp.getLength()):
			self.__trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )
		del trndata_temp
		gc.collect()
		self.__tstdata._convertToOneOfMany()
		self.__trndata._convertToOneOfMany()

	def train(self, maxEpochs=1000, desiredError=0, saveFile=""):
		print ""
		for epoch in range(0, maxEpochs):
			error = self.__trainer.train()
			delete_line()
			delete_line()
			if saveFile != "" and epoch % 500==0:
				self.save_net_to_file(saveFile)
			print "Epoch:", epoch + 1, ", greska:", error
			if error < desiredError:
				return error
		return error
		
	def test(self):
		acc = 0
		for i in range(len(self.__trndata)):
			if self.run(self.__trndata['input'][i]).argmax() == self.__trndata['class'][i]:
				acc += 1
		print "Preciznost na trening setu: %f %%" % (float(acc)/len(self.__trndata)*100)
		acc = 0
		for i in range(len(self.__tstdata)):
			if self.run(self.__tstdata['input'][i]).argmax() == self.__tstdata['class'][i]:
				acc += 1
		print "Preciznost na test setu: %f %%" % (float(acc)/len(self.__tstdata)*100)
		
	def run(self, sample):
		return self.__net.activate(sample)

	def save_net_to_file(self, f):
		outfile = open(f, 'w')
		pickle.dump(self.__net, outfile)
		outfile.close()
	
	def load_net_from_file(self, f):
		infile = open(f, "r")
		self.__net = pickle.load(infile)
		infile.close()

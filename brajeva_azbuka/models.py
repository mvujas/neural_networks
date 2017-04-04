from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import pickle
import Tkinter as tk


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
	def __init__(self, *layers):
		self.__net = buildNetwork(*layers, hiddenclass=SigmoidLayer, outclass=SigmoidLayer, bias=True)
		self.__data = SupervisedDataSet(layers[0], layers[-1])
		self.__trainer = BackpropTrainer(self.__net, self.__data, momentum=0.99)
		self.__layers = layers

	def load_dataset_from_file(self, f):
		infile = open(f, 'r')
		for line in infile.readlines():
		    data = [float(x) for x in line.strip().split(',') if x != '']
		    indata = tuple(data[:self.__layers[0]])
		    outdata = tuple(data[self.__layers[0]:])
		    self.__data.addSample(indata,outdata)
		infile.close()
		self.__trainer = BackpropTrainer(self.__net, self.__data, momentum=0.99)

	def load_net_from_file(self, f):
		infile = open(f, "r")
		self.__net = pickle.load(infile)
		infile.close()
		self.__trainer = BackpropTrainer(self.__net, self.__data, momentum=0.99)

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

class GUI:
	def __init__(self):
		self._closed = True
		self._result = [0] * 6
		self._root = tk.Tk()
		self._root.title('Brajeva azbuka')
		self._root.resizable(0, 0)
		self._root.withdraw()
		self._root.bind('<Return>', self.terminate)
		self._canvas = tk.Canvas(self._root, width=260, height=390)
		self._dot = [[None, None], [None, None], [None, None]]
		for i in range(0, 3):
			for j in range(0, 2):
				r = 50
				space = 15
				starty = 2 * i * (space + r) + space
				startx = 2 * j * (space + r) + space
				self._dot[i][j] = self._canvas.create_oval(startx, starty, startx + 2 * r, starty + 2 * r, fill='white')
				self._canvas.tag_bind(self._dot[i][j], '<Button-1>', self.change_dot)
		self._runButton = tk.Button(self._root, text='Pokreni')
		self._runButton.bind('<Button-1>', self.terminate)

		self._canvas.pack()
		self._runButton.pack()

	def start(self):
		self._result = [0] * 6
		for i in range(0, 3):
			for j in range(0, 2):
				self._canvas.itemconfig(self._dot[i][j], fill='white')
		self._closed = True
		self._root.deiconify()
		self._root.mainloop()

	def change_dot(self, event):
		if self._canvas.itemconfig(event.widget.find_withtag('current'))['fill'][4] == 'white':
			self._canvas.itemconfig(event.widget.find_withtag('current'), fill='black')
		else:
			self._canvas.itemconfig(event.widget.find_withtag('current'), fill='white')

	def terminate(self, event):
		for i in range(0, 3):
			for j in range(0, 2):
				if self._canvas.itemconfig(self._dot[i][j])['fill'][4] == 'black':
					self._result[2 * i + j] = 1
				else:
					self._result[2 * i + j] = 0
		self._closed = False
		self._root.withdraw()
		self._root.quit()

	def get_info(self):
		return { 
			'result' : self._result,
			'closed' : self._closed
		}

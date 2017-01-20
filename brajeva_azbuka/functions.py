'''

	Napravljeno u korist 
	preglednosti koda za pokretanje

'''
from models import NeuralNetwork
import os

def prepare_neural_network(nn_file, *layers):
	net = NeuralNetwork(*layers)
	net.load_net_from_file(nn_file)
	return net

def keyboard_input(text):
	inn = raw_input(text)
	out = inn.split()
	out = [ int(x) for x in out ]
	return out

def keyboard_mode(net):
	os.system("clear")
	print " Nalazite se u modu citanja sa tastature\n Za izlazak iz moda i povratak na pocetni meni unesite prazan unos\n\n"
	while True:
		sample = keyboard_input(" ")
		if len(sample) == 0:
			break
		print('\'' + net.run(sample) + '\'')

def choose_mode():
	inn = raw_input(" Izaberite jednu od sledecih opcija:\n  1) Prelazak u mod citanja sa tastature \n  2) Prelazak u mod za citanje i upis u tekstualnu datoteku \n  3) Pomoc \n  4) Prekid rada programa \n\n ")
	if inn in ('1', '2', '3', '4'):
		return int(inn)
	else:
		return 0

def help():
	while True:
		os.system("clear")
		inn = raw_input(" Pomoc \n\n ")
		if len(inn) == 0:
			break

def file_mode(net):
	os.system("clear")
	print " File mode \n\n"

def loop(net):
	mode = -1
	while mode != 4:
		os.system("clear")
		if mode == 0:
			print " Nepoznat unos\n Otvori pomoc za upustva za koriscenje programa\n"
		mode = choose_mode()
		if mode == 1:
			keyboard_mode(net)
		elif mode == 2:
			file_mode(net)
		elif mode == 3:
			help()



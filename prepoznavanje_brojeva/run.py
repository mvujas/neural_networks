from models import NeuralNetwork
from tkFileDialog import askopenfilename
from skimage.color import rgb2gray
import matplotlib.image as mpimg
from Tkinter import Tk

def prepare_net(nn_file, *layers):
	net = NeuralNetwork(*layers)
	net.load_net_from_file(nn_file)
	return net

def process_image(filename):
	img = mpimg.imread(filename)
	height, width = len(img), len(img[0])
	if not(height == 8 and width == 8):
		return []
	if not('int' in type(img[0][0]).__name__):
		img_gray = rgb2gray(img)
		for i in range(0, height):
			for j in range(0, width):
				img_gray[i][j] *= 255
		return img_gray.ravel()
	return img.ravel()

def main():
	net = prepare_net('digit_recognition.nnet', 64, 100, 10)
	print '\n ***** Neuronske mreze sa primenama *****\n\n          Prepoznavanje cifara\n\n ****************************************\n'
	inn = 'N'
	
	# da tkFileDialog ne bi pravio prazan window
	root = Tk() 
	root.withdraw()
	
	while True:
		if inn.strip().upper() in ['D', 'DA']:
			break
		filename = askopenfilename(filetypes=[('JPG Images', '*.jpg'), ('PNG Images', '*.png')])
		if filename in [(), '']:
			print ' Prekid rada programa...'
			break
		img = process_image(filename)
		if img == []:
			print ' Slika mora biti dimenzija 8x8 piksela!'
			continue
		out = net.run(img)
		print ' Pretpostavka: %d sa sigurnoscu od %.2f %%' % (out.argmax(), out[out.argmax()]*100)
		inn = raw_input(' Da li zelite da napustite program?[d/N] ')

if __name__ == '__main__':
	main()



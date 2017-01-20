from models import Brain

def main():
	net = Brain(6, 15, 2, 3, momentum=0.99)
	net.load_dataset_from_file("trainingData.txt")
	net.train(maxEpochs=30000, desiredError=0.0000001)
	net.save_net_to_file("brajeva_azbuka_15_2.nnet")

if __name__ == "__main__":
	main()

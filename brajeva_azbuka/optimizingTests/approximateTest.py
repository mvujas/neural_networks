f = [None] * 4
a = [None] * 3
for i in range(3):
	f[i] = open("test" + str(i+1) + ".txt", "r")
f[3] = open("test_final.txt", "w")

for i in range(45):
	for k in range(3):
		a[k] = f[k].readline().split()
		a[k] = [ float(x) for x in a[k]]
	s = str(int(a[0][0])) + "  " + str(int(a[0][1])) + "  " + str((a[0][2] + a[1][2] + a[2][2])/3) + "\n"
	f[3].write(s)

for i in range(4):
	f[i].close()
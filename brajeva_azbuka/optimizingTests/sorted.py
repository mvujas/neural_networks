from operator import itemgetter

a = [None] * 45
f = open("test_final.txt")
for i in range(45):
	a[i] = f.readline().split()
	a[i] = [ float(x) for x in a[i] ]

print a
sorted(a, key=itemgetter(2), reverse=True)
print a
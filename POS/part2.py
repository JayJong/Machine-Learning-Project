import numpy as np

def tag(x, e, ycount,xset,yset):
	y = ['' for i in x]
	for i in range(len(x)):
		tmp = -1.
		if x[i] in xset:
			for j in yset:
				if e[yset.index(j)][xset.index(x[i])]>tmp:
					tmp = e[yset.index(j)][xset.index(x[i])]
					y[i] = j
		else:
			for j in yset:
				if e[yset.index(j)][-1]>tmp:
					tmp = e[yset.index(j)][-1]
					y[i] = j
	return y


def emission(x,y,xset,yset):
	e = [[0. for i in range(len(xset)+1)] for j in yset]
	ycount = [sum([1. for j in y if i==j]) for i in yset]

	for i,j in zip(x,y):
		e[yset.index(j)][xset.index(i)] += 1./(ycount[yset.index(j)]+1)

	for j in range(len(yset)):
		e[j][-1] = 1./(ycount[j]+1)

	return e,ycount

def readin():
	xtest = []
	xtest_ori = []
	ytest = []
	f = open('dev.in','r')
	for line in f:
		if line.strip():
			xtest.append(line.strip())
	f.close()

	f = open('dev.out','r')
	for line in f:
		if line.strip():
			line = line.split(' ')
			ytest.append(line[1].strip())
	f.close()
	return xtest,ytest

def init():
	xtrain = []
	ytrain = []
	f = open('train', 'r')
	for line in f:
		if line.strip():
			line = line.split(' ')
			xtrain.append(line[0])
			ytrain.append(line[1].strip())
	f.close()
	return xtrain, ytrain

def writefile(ypred):
	f1 = open('dev.p2.out','w')
	f2 = open('dev.in','r')
	count = 0
	for line in f2:
		if line.strip():
			f1.write(line.strip()+' '+ypred[count]+'\n')
			count += 1
		else:
			f1.write('\n')
	f1.close()
	f2.close()
	return None


if __name__ == "__main__":

	xtrain, ytrain = init()
	xset = sorted(list(set(xtrain)))
	yset = sorted(list(set(ytrain)))

	e, ycount = emission(xtrain,ytrain,xset,yset)

	xtest, ytest = readin()

	ypred = tag(xtest,e,ycount,xset,yset)

	writefile(ypred);

	acuuracy = sum([1. for i,j in zip(ypred,ytest) if i==j])/len(ypred)
	print acuuracy

















































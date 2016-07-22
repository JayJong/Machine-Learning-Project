import numpy as np
import math
import copy

def emission(x,y,xset,yset):
	ycount = {}
	for i in yset:
		ycount[i] = sum([1. for j in y if i==j])

	e = {}
	for i in xset:
		for j in yset:
			e[j,i] = 0.

	for i,j in zip(x,y):
		e[j,i] = e[j,i] + 1./(ycount[j]+1)

	for j in yset:
		e[j,'NA'] = 1./(ycount[j]+1)	

	return e,ycount

def transition(xset,yset):

	a = {}
	for i in yset:
		for j in yset:
			a[i,j] = 0.
	xtrain = ['']
	ytrain = ['START']
	f = open('train', 'r')
	for line in f:
		if line.strip():
			line = line.split(' ')
			xtrain.append(line[0])
			ytrain.append(line[1].strip())
		else:
			xtrain.append('')
			ytrain.append('STOP')
			xtrain.append('')
			ytrain.append('START')			
	f.close()
	del xtrain[-1]
	del ytrain[-1]

	ycount = {}
	for i in yset:
		ycount[i] = sum([1. for j in ytrain if i==j])
	for i in range(len(ytrain)-1):
		a[ytrain[i], ytrain[i+1]] = a[ytrain[i], ytrain[i+1]] + 1.
	
	ycountzero = {}
	for i in yset:
		ycountzero[i] = 0.
		for j in yset:
			if a[i,j] == 0.:
				ycountzero[i] = ycountzero[i]+1
	for i in yset:
		for j in yset:
			if a[i,j]==0.:
				a[i,j] = 1./(ycount[i]+ycountzero[i])
			else:
				a[i,j] = a[i,j]/(ycount[i]+ycountzero[i])

	return a, ycount

def Viterbi(e,a,x,yset):
	pi = [[[(0.,[]) for k in range(10)]for j in range(len(yset)-2)] for i in range(len(x)+2)]
	pi[0][0][0] = (math.log(1.), [yset[0]])

	for j in range(1,len(yset)-1):
		path = copy.deepcopy(pi[0][0][0][1])
		path.append(yset[j])
		score = 0.0
		if x[0] in xset:
			if a['START', yset[j]]!=0. and e[yset[j],x[0]]!=0.:
				score = math.log(a['START', yset[j]])+math.log(e[yset[j],x[0]])
		else:
			if a['START', yset[j]]!=0. and e[yset[j],'NA']!=0.:
				score = math.log(a['START', yset[j]])+math.log(e[yset[j],'NA'])
		pi[1][j-1][0] = (score,path)
		for m in range(1,10):
			pi[1][j-1][m] = (0.0,path)

	for i in range(1,len(x)):
		for j in range(1,len(yset)-1):
			tmp = []
			for k in range(1,len(yset)-1):
				for m in range(10):
					score = 0.0
					if x[i] in xset:
						if a[yset[k],yset[j]]!=0. and e[yset[j],x[i]]!=0. and pi[i][k-1][m][0]!=0.:
							score = pi[i][k-1][m][0]+ math.log(a[yset[k],yset[j]])+ math.log(e[yset[j],x[i]])
					else:
						if a[yset[k],yset[j]]!=0. and e[yset[j],'NA']!=0. and pi[i][k-1][m][0]!=0.:
							score = pi[i][k-1][m][0]+ math.log(a[yset[k],yset[j]])+ math.log(e[yset[j],'NA'])
					path = copy.deepcopy(pi[i][k-1][m][1])
					path.append(yset[j])
					if score!=0.0:
						tmp.append((score,path))
			temp = sorted(tmp, key=lambda tmp: tmp[0], reverse=True)
			for m in range(10):
				if temp:
					try: 
						pi[i+1][j-1][m] = temp[m]
					except:
						pi[i+1][j-1][m] = (0.0,path)
				else:
					if m==0:
						pi[i+1][j-1][m] = (score,path)
					else:
						pi[i+1][j-1][m] = (0.0,path)
			
			# print 'Labels after ',i,x[i],j,yset[j] 
			# for ii in temp:
			# 	print ii
			# 	print 

	tmp = []
	for k in range(1,len(yset)-1):
		for m in range(10):
			score = 0.0
			if a[yset[k],'STOP']!=0. and pi[-2][k-1][m][0]!=0.:
				score = pi[-2][k-1][m][0] + math.log(a[yset[k],'STOP'])
			path = copy.deepcopy(pi[-2][k-1][m][1])
			path.append('STOP')
			if score!= 0.:
				tmp.append((score,path))
	temp = sorted(tmp, key=lambda tmp: tmp[0], reverse=True)
	
	# print 'Labels after STOP!' 
	# for i in temp:
	# 	print i
	# 	print 
	# exit()

	for m in range(10):
		if temp:
			try:
				pi[-1][0][m] = temp[m]
			except:
				pi[-1][0][m] = temp[-1]
		else:
			pi[-1][0][m] = (score,path)
	
	return pi[-1][0]

def tagging(e,a,xtest,yset):
	ypred = [[] for i in range(10)]

	flag = True
	for i in range(len(xtest)):
		if xtest[i]=='':
			if flag:
				sentence = []
				flag = False
			else:
				ans = Viterbi(e,a,sentence,yset)
				for m in range(10):
					(score, sentence_tag) = ans[m]
					for j in range(1,len(sentence_tag)-1):
						ypred[m].append(sentence_tag[j])
				flag = True
		else:
			sentence.append(xtest[i])

	return ypred

def readin():
	xtest = ['']
	ytest = []
	f = open('dev.in','r')
	for line in f:
		if line.strip():
			xtest.append(line.strip())
		else:
			xtest.append('')
			xtest.append('')
	f.close()
	del xtest[-1]

	f = open('dev.out','r')
	for line in f:
		if line.strip():
			line = line.split(' ')
			ytest.append(line[1].strip())
		# else:
		# 	ytest.append('STOP')
		# 	ytest.append('START')
	f.close()
	# del ytest[-1]
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
	f1 = open('dev.p4.out','w')
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

	yset.insert(0, 'START')
	yset.append('STOP')

	a, ycount = transition(xset,yset)

	xtest, ytest = readin()

	ypred = tagging(e, a, xtest, yset)

	writefile(ypred[9])

	accuracy = sum([1. for i,j in zip(ypred[9],ytest) if i==j])/len(ypred[9])
	print accuracy

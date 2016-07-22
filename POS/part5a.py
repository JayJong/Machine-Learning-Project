import numpy as np
import copy
from pprint import pprint
import math


############################################################
## functions for PART 2

def readin():
	xtest = []
	ytest = []
	f = open('dev.in','r')
	for line in f:
		if line.strip():
			word = line.strip()
			xtest.append(word_filter(word)) ## Here is where the word is filtered
			
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
			word = line[0]
			xtrain.append(word_filter(word)) ## Here is where the word is filtered
			ytrain.append(line[1].strip())
	f.close()
	return xtrain, ytrain

############################################################


############################################################
## functions for PART 3

def ViterbiAlgoLog(inputstring, A, B, Possible_States, Possible_Words):
    n = len(inputstring)
    T = len(Possible_States)

    Possible_Words.append('NA')
   
    pi_matrix = []
    prow = []
    for i in range(0,n):
        prow.append([0.0,'nil'])
    for i in range(0,T):
        plist = copy.deepcopy(prow)
        pi_matrix.append(plist)

    k = 0 ## The first and last column have been taken out
    try:
        w1 = Possible_Words.index(inputstring[k])
    except:
        w1 = len(Possible_Words)-1
    for i in range(0,T):
        if A['Start',Possible_States[i]] != 0 and B[Possible_States[i],Possible_Words[w1]] != 0:
            Prob = math.log(A['Start',Possible_States[i]]*B[Possible_States[i],Possible_Words[w1]])
            pi_matrix[i][0][0] = Prob
            pi_matrix[i][0][1] = 'Start'

    for k in range(1,n):
        try:
            wk = Possible_Words.index(inputstring[k])
        except:
            wk = len(Possible_Words)-1
        for i in range(0,T):
            Prob_Hgst = -1e300
            Parent_Hgst = 'NA'
            for v in range(0,T):
                if A[Possible_States[v],Possible_States[i]] != 0 and B[Possible_States[i],Possible_Words[wk]] != 0 and pi_matrix[v][k-1][0] != 0.0:
                    Prob = pi_matrix[v][k-1][0] + math.log(A[Possible_States[v],Possible_States[i]]) + math.log(B[Possible_States[i],Possible_Words[wk]])
                    if Prob > Prob_Hgst:
                        Prob_Hgst = Prob
                        Parent_Hgst = pi_matrix[v][k-1][1] + '&&' + Possible_States[v]
            pi_matrix[i][k][0] = Prob_Hgst
            pi_matrix[i][k][1] = Parent_Hgst

    Prob_Hgst = -1e300
    Parent_Hgst = 'AH'
    for v in range(0,T):
        if pi_matrix[v][n-1][0] != 0.0:
            Prob = pi_matrix[v][n-1][0] + math.log(A[Possible_States[v],'Stop'])
            if Prob > Prob_Hgst:
                Prob_Hgst = Prob
                Parent_Hgst = pi_matrix[v][n-1][1] + '&&' + Possible_States[v]

    optimal_sequence = Parent_Hgst.split('&&')[1::]

    if len(optimal_sequence) == 0:
        optimal_sequence = []
        for i in range(len(inputstring)):
            optimal_sequence.append('_')
    return optimal_sequence, pi_matrix
        

def producetagging(filepath, A, B, Possible_States, Possible_Words):
    f = open(filepath ,'r')
    total_string = []
    optimaltags = []
    input_string = []
    optimal_tags_error = []
    input_string_error = []
    checklen = []
    countphrases = 0
    lines = f.readlines()
    for eachline in lines:
        eachline = eachline.strip()
        split=eachline.split()
        if len(eachline) == 0:
            checklen.append(len(input_string))
            countphrases += 1
            optimal_sequence, pi_matrix = ViterbiAlgoLog(input_string, A, B, Possible_States, Possible_Words)
            optimaltags = optimaltags + optimal_sequence
            optimaltags.append(' ')
            if optimal_sequence[0] == '_':
                    optimal_tags_error.append(optimal_sequence)
                    input_string_error.append(input_string)
            total_string.append(input_string)
            last_input_string = input_string
            input_string = []
        else:
            word = eachline
            input_string.append(word_filter(word)) ## Here is where the word is filtered
    return optimaltags, total_string, countphrases, checklen, last_input_string, optimal_tags_error, input_string_error

def stripalltags(filepath):
    f = open(filepath ,'r')
    answertags = []
    lines = f.readlines()
    for eachline in lines:
        split=eachline.split()
        if len(split) == 2:
            answertags.append(split[1])
        else:
            answertags.append(' ')
    return answertags

def testaccuracy(optimal_tags, answer_tags):
        if len(optimal_tags) != len(answer_tags):
                print "There is an error"
        else:
                score = 0
                length = 0
                wrong = 0
                for i in range(0, len(answer_tags)):
                        if answer_tags[i] == ' ':
                                pass
                        elif optimal_tags[i] == answer_tags[i]:
                                score += 1
                                length += 1
                        else:
                                wrong += 1
                                length += 1
                return score, wrong, length, float(score)/length
        

############################################################


############################################################
## functions for PART 5
        
def word_filter(word):
    if len(word) == 0:
        return ''
    elif word.isdigit():                                # it is a digit
        return '0'
    elif word == '.' or word == '!' or word == '?':     # it is . or ! or ?
        return '.'
    elif word[0:4] == 'http':                           # it is a URL
        return 'http'
    elif word[0] == '@' and len(word) > 1:              # it is a @user
        return '@name'
    elif word[0] == '#' and len(word) > 1:              # it is a Hash Tag
        return '#name'             
    elif len(word) == 4 and word[1] == ':' and  word[0:1].isdigit() and word[2:4].isdigit():
        return '0'                                      # a timing in the format of X:XX	
    elif len(word) == 5 and word[2] == ':' and  word[0:2].isdigit() and word[3:5].isdigit():
        return '0'                                      # a timing in the format of XX:XX 
    else:
        return word.lower()                             # a word

def emission_part5(x,y,xset,yset,de):
	ycount = {}
	for i in yset:
		ycount[i] = sum([1. for j in y if i==j])
			
	e = {}
	for i in xset:
		for j in yset:
			e[j,i] = 0.

	for i,j in zip(x,y):
		if j in yset:
		        e[j,i] += 1.

	ycountzero = {}
	for i in yset:
		ycountzero[i] = sum([1. for j in xset if e[i,j] == 0.0])

	for j in yset:
		e[j,'NA'] = de*( len(xset) - ycountzero[j] )/( len(xset)*ycount[j] )
		for i in xset:
			e[j,i] = max( 0, (e[j,i] - de)/(ycount[j])) + de*( len(xset) - ycountzero[j] )/( len(xset)*ycount[j] )
		
	return e,ycount,ycountzero

def producetransitionmatrix_part5(filepath,dt):

    f = open(filepath,'r')

    list_words = [" "]
    list_tags = ["Start"]

    lines = f.readlines()

    for eachline in lines:
        split=eachline.split()
        if len(split) > 0:
            word = split[0]
            list_words.append(word_filter(word)) ## Here is where the word is filtered
            list_tags.append(split[1])
        if len(split) == 0:
            list_words.append(" ")
            list_words.append(" ")
            list_tags.append("Stop")
            list_tags.append("Start")

    if list_tags[len(list_tags)-1] == 'Start':
            del list_words[-1]
            del list_tags[-1]
    elif list_tags[len(list_tags)-1] == 'Stop' and list_tags[len(list_tags)-2] == 'Start':
            del list_words[-1]
            del list_tags[-1]
            del list_words[-1]
            del list_tags[-1]
    else:
            list_words.append(" ")
            list_tags.append("Stop")

    unique_tags = sorted(list(set(list_tags)))
    unique_tags2 = copy.deepcopy(unique_tags)

    t_ca = {} # dictionary to count the times a tag has appeared
    t_cz = {} # dictionary to count the times a tag cannot transition to another tag
    for tag in unique_tags:
        t_ca[tag] = 0.
        t_cz[tag] = 0.
        
    t_ct = {} # dictionary to count the number of times a tag transitions to another tag
    for tag in unique_tags:
        for tag2 in unique_tags2:
            t_ct[tag,tag2] = 0.
    for i in range(0, len(list_tags)-1):
        j = i + 1
        tagi = list_tags[i]
        tagj = list_tags[j]
        if tagi in unique_tags and tagj in unique_tags:
            t_ca[tagi] += 1.
            t_ct[tagi,tagj] += 1.
        
    for keys in t_ct.keys(): # dictionary to count the times a tag cannot transition to another tag
        if t_ct[keys] == 0:
            t_cz[keys[0]] += 1
            
    t_m = {}  # dictionary to count the probability of a tag transitioning to another tag
    for tag in unique_tags:
        for tag2 in unique_tags2:
            t_m[tag,tag2] = max( 0,(t_ct[tag,tag2] - dt)/(t_ca[tag])) + dt*( len(unique_tags)- t_cz[tag] )/( len(unique_tags)*t_ca[tag] )
        
    return t_m, t_ca, t_ct, t_cz, unique_tags

def writefile1(ypred):
	f1 = open('dev.p5.out','w')
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

def writefile2(ypred):
	f1 = open('test.p5.out','w')
	f2 = open('test.in','r')
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


############################################################


############################################################
            
if __name__ == "__main__":
    de = 0.03
    dt = 0.675

    # training the emission and transmission matrices from 'train'
    xtrain, ytrain = init()
    xset = sorted(list(set(xtrain)))
    yset = sorted(list(set(ytrain)))

    e, ycount, ycountzero = emission_part5(xtrain,ytrain,xset,yset,de)

    xtest, ytest = readin()

    transition_matrix, tags_countappearance, tags_counttransition, tags_countzero, unique_tags = producetransitionmatrix_part5('train',dt)

    optimal_tags, total_string, countphrases, checklen, last_input_string, optimal_tags_error, input_string_error  = producetagging('dev.in', transition_matrix, e, yset, xset)

    answer_tags = stripalltags('dev.out')

   # predicts the tags for data file 'dev.in'
    score, wrong, length, accuracy = testaccuracy(optimal_tags,answer_tags)
    print 'Number of right', score
    print 'Number of wrong', wrong
    print 'Length is', length
    print "The accuracy of Part 5 is", accuracy

    nospaces = []
    for tag in optimal_tags:
        if tag == ' ':
            pass
        else:
            nospaces.append(tag)    
    writefile1(nospaces);
	
############################################################ 



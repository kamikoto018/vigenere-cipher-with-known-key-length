#!/usr/bin/python
# coding: utf-8

def _ord(char):
	if char == '_':
		return 32
	return ord(char) - ord(u'А')

def _chr(idx):
	idx %= 33
	if idx == 32:
		return '_'
	return unichr(ord(u'А') + idx)

#step 1
def group_letters(src, keyLen):
	arr = [[] for i in range(keyLen)] #Create 3d empty array
	i = 0
	for char in src:
		arr[i].append(_ord(char))
		i = (i + 1) % keyLen
	return arr

def decode_src(src, offsets, keyLen):
	res = ''
	i = 0
	for char in src:
		res += _chr(_ord(char) + 1 - offsets[i])
		i = (i + 1) % keyLen
	return res

#step 2
def find_freq(arr):
	return [find_freq_for_col(col) for col in arr]

def find_freq_for_col(vector):
	freq = [0]*33
	for char in vector:
		freq[char] += 1

	return freq


#step 3
def cicle_shift(vector):
	return vector[1:] + vector[:1]

def index_vzaimn_sovpadeniya(freq1, freq2):
	s = 0
	for char in range(33):
		s += freq1[char] * freq2[char]

	return 1.0*s/(sum(freq1)*sum(freq2))



def analysis(src, keyLen, decodeOffset):
	arr = group_letters(src, keyLen);

	freq = find_freq(arr)
	offsets = range(keyLen)
	offsets[0] = 0
	# Calc offsets
	for i in offsets:
		if i == 0:
			continue
		print 'Step ', i + 1
		for o in range(33):
			idx = index_vzaimn_sovpadeniya(freq[0], freq[i])
			if 0.04 < idx and idx < 0.07:
				offsets[i] = o
				print '\tOffset', o, '\tIndex', idx
			freq[i] = cicle_shift(freq[i])

	# Calc keyword
	for i in range(33):
		keyword = ''
		for o in offsets:
			keyword += _chr(i + o)
		print i, '\t', keyword

	# Modify offsets
	for i in range(keyLen):
		offsets[i] = offsets[i] + decodeOffset + 1 # imperical number

	print 'Offsets', offsets
	# Apply offsets
	print 'Decrypted text:', decode_src(src, offsets, keyLen)




if __name__ == '__main__':
	file = open('input.txt', 'r')
	src = file.read().splitlines()[0].decode("utf-8")
	analysis(src, keyLen=3, decodeOffset=17)

	file.close()

import numpy as np
import sys
import json

def readFile(file_ext):
	data = None
	with open(file_ext) as f:
		data = f.readlines()  
	return data

def extract_label(data):
	label = int(data[-2])
	if label == 0:
		label = -1
	
	return label


def data_cleanup(review):
	symbols_to_remove = ['~', '`', '.', '!', '?', '@', '#', '$', '%',\
						'^', '&', ',', '(', ')', '_', '+', '*',\
						'=', '<', '>', ';', ':', '"', '[', ']', '/',\
						'\\', '|', '~', '{', '}']
	symbols_to_remove += ['0','1','2','3','4','5','6','7','8','9']
	# try:
	# 	space_index = review.index(" ")
	# 	review_id = review[:space_index + 1]
	# except:
	# 	print "Error in finding space_index in data_cleanup"
	review = review.lower()
	for char in symbols_to_remove:
		review = review.replace(char, " ")

	return review

def split_into_words(data):
	try:
		words_in_reviews = data.strip().split()
	except:
		print "Exception in split_into_words"
	return words_in_reviews


def remove_stop_words(review):

	stop_words = ['a','about','above','after','again','all','am','an','and','any','are','as','at','be',\
				  'because','been','before','being','below','between','both','but','by','could','did','do','does',\
				  'doing','down','during','few','for','from','further','had','has','have','having','he',\
				  'd','ll','s','her','here','hers','herself','him','himself','his','how','i','m','ve','if','in',\
				  'into','is','it','its','itself','let','me','more','most','my','myself','nor','of','on','once',\
				  'only','or','other','ought','our','ours','ourselves','out','over','own','same','she','should',\
				  'so','some','such','than','that','the','their','theirs','them','themselves','then','there',\
				  'these','they','re','this','those','through','to','too','under','until','up','was','very',
				  'we','were','what','when','where','which','while','who','whom','why','with','would',\
				  'you','your','yours','yourself','yourselves','l','isn','t',\
				  're','aren','seperate']

	review = [word for word in review if word not in stop_words]

	review = [give_stem_word(word) for word in review]

	return review


def give_stem_word(word):
	stem_word = word

	if stem_word.endswith('ing') and len(stem_word) > 6: 
		stem_word = stem_word[:-3]
		if len(stem_word) > 5:
			if stem_word[-1] == stem_word[-2]:
				stem_word = stem_word[:-1]
			elif stem_word[-1] == 'k' and stem_word[-2] == 'c':
				stem_word = stem_word[:-1]
	elif stem_word.endswith('ed') and len(stem_word) > 5:
		stem_word = stem_word[:-2]
		if len(stem_word) > 6:
			if stem_word[-1] == 'i':
				stem_word = stem_word[:-1] + 'y'
	elif stem_word.endswith('ly') and len(stem_word) > 10:
		stem_word = stem_word[:-2]
		if stem_word[-1] == stem_word[-2]:
			stem_word = stem_word[:-1]

	elif stem_word.endswith('er') and len(stem_word) > 12:
		stem_word = stem_word[:-2]
		if stem_word[-1] == stem_word[-2]:
			stem_word = stem_word[:-1]


	return stem_word
	

def get_unique_words(words_in_reviews, unique_words, total_words):

		
	for word in words_in_reviews:
		if word not in unique_words:
			unique_words[word] = total_words
			total_words += 1
				
		
	return unique_words, total_words

def make_one_hot_vector(words_in_reviews, unique_words):
	one_hot_vector = np.zeros((len(words_in_reviews), len(unique_words)))
	for review_index, review in enumerate(words_in_reviews):
		for word in review:
			if word in unique_words:
				one_hot_vector[review_index][unique_words[word]] += 1
	# one_hot_vector = np.array(one_hot_vector)
	return one_hot_vector
				


def train_vanilla_perceptron(maxIter,label, unique_words, one_hot_vector):
	bias = 0
	weights = np.zeros((1,len(unique_words)))
				
	for hyperparam in range(maxIter):
		for index,review in enumerate(one_hot_vector):
			a = np.sum(review * weights) + bias
			if label[index] * a <= 0.0:
				weights += label[index] * review
				bias += label[index]

				
	return weights, bias


def train_averaged_perceptron(maxIter, label, unique_words, one_hot_vector):
	bias = 0
	weights = np.zeros((1,len(unique_words)))
	u = np.zeros((1,len(unique_words)))
	c = 1
	bias_avg = 0

	
	for hyperparam in range(maxIter):
		for index,review in enumerate(one_hot_vector):
			a = np.sum(review * weights) + bias
			
			if label[index] * a <= 0.0:
				weights += label[index] * review
				bias += label[index]
				u += label[index] * c * review
				bias_avg += label[index] * c

			
			c += 1

	weights_avg = weights - (u * 1.0 / c)
	bias = bias - (bias_avg * 1.0 /c)

	return weights_avg, bias
			
		
			
def write_model_parametersVanilla(unique_words, weights, bias, filename = 'vanillamodel.json'):

	
	data = {}
	data['unique_words'] = unique_words
	data['weights'] = weights.tolist()
	data['bias'] = bias



	with open (filename,'w') as f:
		json.dump(data,f)


def write_model_parametersAveraged(unique_words, weights, bias, filename = 'averagedmodel.json'):

	data = {}
	data['unique_words'] = unique_words
	data['weights'] = weights.tolist()
	data['bias'] = bias

	with open (filename,'w') as f:
		json.dump(data, f)

if __name__ == '__main__':
	data = readFile(sys.argv[1])
	label = [0 for x in range(len(data))]
	unique_words = {}
	words_in_reviews = [[] for x in range(len(data))]
	total_words = 0

	for review_index in range(len(data)):
		if len(data[review_index].strip()) == 0:
			continue
		label[review_index] = extract_label(data[review_index])
		data[review_index] = data_cleanup(data[review_index])
		words_in_reviews[review_index] = split_into_words(data[review_index])
		words_in_reviews[review_index] = remove_stop_words(words_in_reviews[review_index])
		unique_words, total_words = get_unique_words(words_in_reviews[review_index], unique_words, total_words)

	one_hot_vector = make_one_hot_vector(words_in_reviews, unique_words)
	weights, bias = train_vanilla_perceptron(40, label, unique_words, one_hot_vector)
	weights_avg, bias_avg = train_averaged_perceptron(40, label, unique_words, one_hot_vector)


	write_model_parametersVanilla(unique_words, weights, bias)
	write_model_parametersAveraged(unique_words, weights_avg, bias_avg)

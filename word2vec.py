#from gensim.models import Word2Vec
#model = Word2Vec.load('GoogleNews-vectors-negative300.bin')
#print  model.similarity('france', 'spain')



################google model###########################

import gensim,json

# with open("output_file.txt", 'wb') as fp:
#     json.dump('yes', fp)

print "hello"
# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
print  model.similarity('block', 'choke')
print model.most_similar(positive=['pipes','blocked'])

#######################################################
'''
#######################retrain#######################
import gensim
from gensim.models import Word2Vec
model = Word2Vec.load('GoogleNews-vectors-negative300.bin')
model.build_vocab(new_sentences, update=True)
model.train(new_sentences)
#########################################################
'''
'''
import gzip
f = gzip.open('GoogleNews-vectors-negative300.bin.gz', 'rb')
#train_set, valid_set, test_set = cPickle.load(f)
model = Word2Vec.load(f)


#model = Word2Vec.load('GoogleNews-vectors-negative300.bin')
print  model.similarity('france', 'spain')
'''


'''
###save links
https://github.com/3Top/word2vec-api
https://radimrehurek.com/gensim/models/word2vec.html
https://quomodocumque.wordpress.com/2016/01/15/messing-around-with-word2vec/
http://ahogrammer.com/2017/01/20/the-list-of-pretrained-word-embeddings/
'''

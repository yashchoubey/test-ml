
# coding: utf-8

# In[1]:


# !wget https://s3.ap-south-1.amazonaws.com/discovery-nlp-data/embd.dat
# !wget https://s3.ap-south-1.amazonaws.com/discovery-nlp-data/dataset.csv


# In[2]:


import pandas as pd
import numpy as np
import re
df = pd.read_csv('dataset.csv',sep=",",header=None ,names=['sentence','type'])

embedding_matrix=np.load("embd.dat")


# In[3]:


Y = df['type']
from sklearn import preprocessing
from keras.utils.np_utils import to_categorical

le = preprocessing.LabelEncoder()
le.fit(Y)
Y=le.transform(Y) 
labels = to_categorical(np.asarray(Y))


# In[4]:


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
# from unidecode import unidecode
# fit_on_texts(textdata))
MAX_NB_WORDS = 16384
MAX_SEQUENCE_LENGTH=128


# In[5]:


tokenizer = Tokenizer(num_words=MAX_NB_WORDS, split=' ')

alist=[str(x) for x in df['sentence'].values ]
tokenizer.fit_on_texts(alist)
X=tokenizer.texts_to_sequences(alist)
X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)


word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, labels, test_size = 0.2)


# In[6]:


# embeddings_index = {}

# f = open('/home/yash/glove.42B.300d.txt')
# for line in f:
#     #print line
#     values = line.split()
#     word = values[0]
#     coefs = np.asarray(values[1:], dtype='float32')
#     embeddings_index[word] = coefs
# f.close()

# print('Found %s word vectors.' % len(embeddings_index))


# word_index = tokenizer.word_index
# print('Found %s unique tokens.' % len(word_index))

# emb_dimension=300
# embedding_matrix = np.zeros((len(word_index) + 1, emb_dimension))
# for word, i in word_index.items():
#     embedding_vector = embeddings_index.get(word)
#     if embedding_vector is not None:
#         # words not found in embedding index will be all-zeros.
#         embedding_matrix[i] = embedding_vector
        
# embedding_matrix.dump('embd.dat')


# In[7]:


from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
from keras.callbacks import History ,ReduceLROnPlateau
from keras import initializers,regularizers,optimizers

history = History()
model = Sequential()
model.add(Embedding(len(word_index)+1,
                            300,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False
                   ))

model.add(LSTM(256,
               return_sequences=True, 
               #dropout=0.4, 
               #recurrent_dropout=0.4, 
               #activation='relu',#Default:tanh
               #recurrent_activation #Default:hard_sigmoid
               #kernel_regularizer=regularizers.l2(0.001)
               # activity_regularizer=regularizers.l1(0.01)))
               #kernel_initializer='lecun_normal',
               #use_bias=True,
               #bias_initializer='random_uniform'#'random_uniform''random_normal','zeros','truncated_normal','variance_scaling','orthogonal','lecun_uniform','glorot_normal','glorot_uniform','he_normal','lecun_normal'             
              ))

model.add(LSTM(128, 
               #dropout=0.4,
               #return_sequences=True,
               #recurrent_dropout=0.4, 
               #activation='relu',
               #kernel_initializer='lecun_normal',
               #kernel_regularizer=regularizers.l2(0.001)
              ))

#model.add(LSTM(256, dropout_U=0.5, dropout_W=0.5, activation='relu', kernel_regularizer=l2_reg))
model.add(Dense(4,activation='softmax'))#,kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01)))
rmsprop = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
model.compile(loss = 'categorical_crossentropy', optimizer=rmsprop,metrics = ['accuracy'])
model.summary()


# In[8]:



reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,patience=5, min_lr=0.0001, cooldown=5)
history=model.fit(x_train, y_train,
          batch_size=790,
          epochs=30,
          verbose=1,
          callbacks=[reduce_lr],
          validation_data=(x_test, y_test))


# In[9]:


example = tokenizer.texts_to_sequences(["food was worse but bed was good"])
example = pad_sequences(example, maxlen=MAX_SEQUENCE_LENGTH)
print model.predict(example),type(model.predict(example))
le.inverse_transform(np.argmax(model.predict(example)))


# In[10]:


# evaluate the model of test data

from sklearn.metrics import classification_report
predictions = model.predict(x_test)
#print(classification_report(predictions,y_test))
print("Accuracy :",model.evaluate(x_test,y_test))


# In[11]:


import matplotlib.pyplot as plt

# get_ipython().magic(u'matplotlib inline')
# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()


# In[23]:


import h5py
h5py.run_tests()
model.save('zero_model.h5')


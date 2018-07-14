from keras.models import load_model
import os

print os.listdir('./Models/')[0]

nos=len( os.listdir('./Models/'))
loaded_model=[]
for model in os.listdir('./Models/'):
    loaded_model.append(load_model('./Models/'+model))

import numpy as np
for i in range(0,len(loaded_model[0].layers)):
    try:
        sum_all=loaded_model[0].layers[i].get_weights()[0]

        for k in range(1,nos):
            sum_all=np.add(sum_all, loaded_model[k].layers[i].get_weights()[0])

        loaded_model[0].layers[i].set_weights([np.divide(sum_all,nos),loaded_model[0].layers[i].get_weights()[1]])
    except:
        pass

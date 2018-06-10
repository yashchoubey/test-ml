import pandas as pd
import numpy as np

# raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'], 
#         'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'], 
#         'age': [42, 52, 36, 24, 73], 
#         'preTestScore': [4, 24, 31, ".", "."],
#         'postTestScore': ["25,000", "94,000", 57, 62, 70]}
# df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])

# df.to_csv('example.csv')

df = pd.read_csv('Combined sheet iiitv.csv')

out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
#json1= df.to_json

#print df.columns

mydict={}
for header in df.columns:
	mydict[header.title()]=[i for i in df[header] if str(i) != 'nan' ]

print mydict
#print type(mydict['accuracy'][1])

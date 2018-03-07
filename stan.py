# from pycorenlp import StanfordCoreNLP
# nlp = StanfordCoreNLP('http://localhost:9000')

# text = 'Pusheen walked along the beach.'
# output = nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse','outputFormat': 'json'})
# #tokenize, ssplit, pos, lemma, ner, parse, dcoref,depparse
# print output
# #print(output['sentences'][0:]['parse'])


import nltk
from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree, Tree
from stop_words import get_stop_words
from pycorenlp import StanfordCoreNLP

en_stop = [x for x in get_stop_words('en') if x not in ["no","off"]]


def remove_words(self,tokens):
    #print "remove_words"
    return [token for token in tokens if token not in en_stop]

def append_no(self,str,lst):
    #print type(str),type(lst)
    strlst=str.split(" ")
    #print strlst
    for idx,item in enumerate(strlst):
        if item=='no':
            #print "success"
            if strlst[idx+1] in lst:
                lst.extend(["no "+strlst[idx+1]])
                if idx<=len(strlst)-3 and (strlst[idx+2]=="and" or strlst[idx+2]=="&") and strlst[idx+3] in lst :
                    #print "success3"   
                    lst.append("no "+strlst[idx+3]) 

    #print lst
    return lst

def getfeedback(self,t,result_dict):
    #print "--------------getfeedback--------------"
    #t.pretty_print()
    for child in t.subtrees(lambda t: t.label() in ['VBD','VBN','VBG','VBP','VBZ']):
        key=''
        value=list()
        #child.pretty_print()
        value.append(child[0])
        child_copy=child
        while not key and child_copy.parent().label()!='ROOT':
            #print "+++++++++++++++++inside loop++++++++++++++++++++"
            child_copy=child_copy.parent()
            #child_copy.pretty_print()
            key=self.find_noun(child_copy)
            #print "------------------dict----------------",key,value
            self.appendResult(key,value,result_dict)
          
    for child in t.subtrees(lambda t: t.label() in ['DT']):
        if child[0]=="no":
            keys=list()
            #child.pretty_print()
            child_copy=child
            while not keys and child_copy.parent().label()!='ROOT':
                #print "+++++++++++++++++inside loop++++++++++++++++++++"
                child_copy=child_copy.parent()
                #child_copy.pretty_print()
                
                for s in child_copy.subtrees(lambda child_copy: child_copy.label() in ["NN", "NNP", "NNPS","NNS","PRP"]):
                    keys.append(s[0])

                for key in keys:
                    self.appendResult(key,["no"],result_dict)

    #print '******************inside search ad*****************************'

    self.search_values(t,result_dict,"verb")
    #print result_dict
    self.search_values(t,result_dict,"adjective")
    #print result_dict

def search_values(self,t,result_dict,term):
    for child in t.subtrees(lambda t: t.label() in ['NN','NNS','NNP','NNPS']):
        value=list()
        #child.pretty_print()
        key=child[0].encode('utf-8')
        #print key,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        child_copy=child
        while not value and child_copy.parent().label()!='ROOT':
            child_copy=child_copy.parent()
            #child_copy.pretty_print()
            #print "___________________________________________________________________________________"
            if term=='verb':
                value=self.find_verb(child_copy)
            elif term=="adjective":
                value=self.find_adjective(child_copy)
            #print "------------------dict----------------",key,value
            self.appendResult(key,value,result_dict)   

def find_noun(self,t):
    #t.pretty_print()
    for s in t.subtrees(lambda t: t.label() in ["NN", "NNP", "NNPS","NNS","PRP"]):
        return s[0].encode('utf-8')
 
def find_adjective(self,t):
    #t.pretty_print()
    temp_list=list()
    for s in t.subtrees(lambda t: t.label() in ["JJS",'JJ','JJR']):
        temp_list.append(s[0])
    return [x.encode('utf-8') for x in temp_list]

def find_verb(self,t):
    #t.pretty_print()
    temp_list=list()
    for s in t.subtrees(lambda t: t.label() in ['VBD','VBN','VBG','VBP','VBZ']):
        temp_list.append(s[0])
    return [x.encode('utf-8') for x in temp_list]

def appendResult(self,key,value,result_dict):
    if key and value:
        if key in result_dict:
            result_dict[key].extend(value)
            result_dict[key]=list(set(result_dict[key]))
        else:
            result_dict[key]=value



if __name__=="__main__":
    result_dict={}
    text="The strongest is rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today.The strongest is rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today.The strongest is rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today.The strongest is rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today.The strongest is rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today.The strongest is rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today.The strongest is rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today."
    try:
        nlp = StanfordCoreNLP('http://localhost:9000')
        output = nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse','outputFormat':'json'})
        print str(output)
        t = output['sentences'][0]['parse']
        t = Tree.fromstring(t)
        t = ParentedTree.convert(t)
        #t.pretty_print()
        self.getfeedback(t,result_dict)
        print result_dict

    except Exception as e:
        print e
        print str(e)
        #return Response(e,status=400 )
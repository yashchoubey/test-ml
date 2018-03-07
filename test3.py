from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree, Tree

def find_triplet(t):
  for i in t.subtrees():
    if i.height()==t.height()-1:
      i.pretty_print()
      find_triplet(i)
      print "______________________&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&_________________________"
      if i.label() in ["S", "SQ", "SBAR", "SBARQ", "SINV", "FRAG"]:
        find_triplet(i)
  #     else:a#if i.label() in ["NP"]:
  #       print "____________________________________________________________________________________"
  #       print i.pretty_print()
  #       print find_subject(i)
  #       #print find_predicate(s)
  #       print find_object(i)
  #       print "____________________________________________________________________________________"
  #     print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII'
  #   print "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"

  #   for i in t.subtrees():
  #     if i.height()==t.height()-1:
  #       i.pretty_print()
  #       print "______________________&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&_________________________"
  #       if i.label() in ["S", "SQ", "SBAR", "SBARQ", "SINV", "FRAG"]:
  #         find_triplet(i)
  # print "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"


# Breadth First Search the tree and take the first noun in the NP subtree.
def find_subject(t):
  #t.pretty_print()
  for s in t.subtrees(lambda t: t.label() in ['NP','NP-TMP']):
    #s.pretty_print()
    for n in s.subtrees(lambda n: n.label() in ["NN", "NNP", "NNPS","NNS","PRP"]):#.startswith('NN')):
      return (n[0])#, find_attrs(n))
 
# Depth First Search the tree and take the last verb in VP subtree.
def find_predicate(t):
  v = None
 
  for s in t.subtrees(lambda t: t.label() in ['VP']):
    for n in s.subtrees(lambda n: n.label() in ['VB']):
      v = n
  return (v[0])#, find_attrs(v))
 
# Breadth First Search the siblings of VP subtree
# and take the first noun or adjective
def find_object(t):
  return_list=list()
  #t.pretty_print()
  for s in t.subtrees(lambda t: t.label() in ['VP']):
    #s.pretty_print()
    for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
      #n.pretty_print()
      if n.label() in ['NP', 'PP']:
        for c in n.subtrees(lambda c: c.label() in ['NN']):
          return_list.append(c[0])#, find_attrs(c))
      else:
        for c in n.subtrees(lambda c: c.label() in ['JJ']):
          return_list.append(c[0])#, find_attrs(c))
  return return_list

def find_attrs(node):
  attrs = []
  p = node.parent()
 
  # Search siblings of adjective for adverbs
  if node.label().startswith('JJ'):
    for s in p:
      if s.label() == 'RB':
        attrs.append(s[0])
 
  elif node.label().startswith('NN'):
    for s in p:
      if s.label() in ['DT','PRP$','POS','JJ','CD','ADJP','QP','NP']:
        attrs.append(s[0])
 
  # Search siblings of verbs for adverb phrase
  elif node.label() in ['VB']:
    for s in p:
      if s.label() in ['ADVP']:
        attrs.append(' '.join(s.flatten()))
 
  # Search uncles
  # if the node is noun or adjective search for prepositional phrase
  if node.label().startswith('JJ') or node.label() in ['NN']:
      for s in p.parent():
        if s != p and s.label() == 'PP':
          attrs.append(' '.join(s.flatten()))
 
  elif node.label() in ['VB']:
    for s in p.parent():
      if s != p and s.label() in ['VB']:
        attrs.append(' '.join(s.flatten()))
 
  return attrs

def getfeedbackvp(t,result_dict):
  t.pretty_print()
  for child in t.subtrees(lambda t: t.label() in ['VBD','VBN','VBG','VBP','VBZ']):
    key=''
    value=list()
    #child.pretty_print()
    value.append(child[0])
    child_copy=child
    while key =='' and child_copy.parent().label()!='ROOT':
      child_copy=child_copy.parent()
      key=find_subject(child_copy)
      appendResult(key,value,result_dict)
      
def getfeedbacknp(t,result_dict):
  t.pretty_print()
  for child in t.subtrees(lambda t: t.label() in ['NN','NNS','NNP','NNPS']):
    key=''
    value=list()
    #child.pretty_print()
    value.append(child[0])
    child_copy=child
    while key =='' and child_copy.parent().label()!='ROOT':
      child_copy=child_copy.parent()
      key=find_subject(child_copy)
      appendResult(key,value,result_dict)     

def appendResult(key,value,result_dict):
  if key in result_dict:
    if type(result_dict[key])=='str':
      temp_list=[]
      temp_list.append(result_dict[key])
      temp_list.append(value)

    else:
      result_dict[key].append(value)
  else:
    result_dict[key]=value




# parser = StanfordCoreNLP('http://localhost:9000')#StanfordParser()
 
# # Parse the example sentence
# sent = 'A rare black squirrel has become a regular visitor to a suburban garden'
# t = list(parser.raw_parse(sent))[0]
# t = ParentedTree.convert(t)
 
# t.pretty_print()
nlp = StanfordCoreNLP('http://localhost:9000')
text= 'A rare black squirrel has become a regular visitor to a suburban garden'
text="The strongest rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today."
#text="the rooms were tidy and overpriced"
#text="""My husband & I are very fussy when we choose our accommodation, we are not the type of people that say "oh it's just a hotel room, we don't care where we sleep" we do care!"""
#text="""But to be honest I do not really know what to say, as the hotel did not really leave any impression on me"""
#text="""the accommodation is also good yet nothing brilliant or amazing"""


output = nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse','outputFormat':'json'})

t = output['sentences'][0]['parse']

t = Tree.fromstring(t)
t = ParentedTree.convert(t)
t.pretty_print()
result_dict={}
getfeedbackvp(t,result_dict)
print result_dict

# for child in t.subtrees(lambda t: t.label() in ["VP"]):
#   child.pretty_print()

#   #print find_subject(child)
#   #print find_predicate(child)
#   print find_object(child)
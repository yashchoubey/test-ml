
day={'0':'Monday','1':"Tuesday",'2':'Wednesday','3':"Thursday",'4':"Friday",'5':"Saturday",'6':"Sunday"}

def getdetails(opening, closing):
	diff=opening-closing
	if diff==0:
		return ' open 24 hours'
	if diff<0:
		return " "+str(opening)+'-'+str(closing)
	if diff>0:
		return ' closed'

opening_hrs = [700 , 1900, 700, 1100, 1500, 1000, 1700]                                                                                                                   
closing_hrs= [1900, 1900, 1900, 1900, 1500, 1000, 1700]

# opening_hrs = [700 , 700, 700, 1100, 1500, 1000, 1700]                                                                                                                  
# closing_hrs = [1900, 1900, 1900, 1900, 1500, 1000, 700]

cache_s='Monday'
cache_e=''
cache_time=''

for i in range(0,7):
	x=getdetails(opening_hrs[i],closing_hrs[i])
	if x==cache_time:
		cache_e=day[str(i)]
	else:
		if i>0:
			if cache_s!=cache_e and cache_e!='' and cache_time!='':
				print cache_s[0:3]+'-'+cache_e[0:3]+'-'+cache_time
			else:
				print cache_s+cache_time

		cache_s=day[str(i)]
		cache_e=''
		cache_time=x

if cache_e=='Sunday' or cache_s=='Sunday':
	if cache_s!=cache_e and cache_time!='':
		print cache_s[0:3]+'-'+cache_e[0:3]+'-'+cache_time
	else:
		print cache_s+cache_time





# opening_hrs = [700 , 1900, 700, 1100, 1500, 1000, 1700]                                                                                                                   
# closing_hrs = [1900, 1900, 1900, 1900, 1500, 1000, 700]
# getdetails(opening_hrs,closing_hrs)



'''
Mon-Wed-700-1900
Thu-1100-1900
Friday -Sat open 24 hours
Sun-closed

Input 2:
opening hrs = [700 , 1900, 700, 1100, 1500, 1000, 1700]                                                                                                                   
closing hrs = [1900, 1900, 1900, 1900, 1500, 1000, 700]
Output-

Mon-700-1900
Tue-24 hours open
Wed-700-1900
Thu-1100-1900
Friday -Sat open 24 hours
Sun-closed

'''
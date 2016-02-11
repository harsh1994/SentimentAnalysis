from nltk.corpus import wordnet as wn
import nltk, re, pprint
from nltk import word_tokenize, pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob
from textblob import Word
import os,glob
from scipy.stats.stats import pearsonr
food=['cuisine','taste','starter','menu','meal','dessert','kitchen','pizza','dish','quantity','spread','chef','ingredient','food','flavour']
service=['service','waiter','staff','delivery','check','reservation','host','counter','serve','table']
price=['cost','price','overpriced','free','money','bargain']
ambience=['ambience','ambiance','decor','design','atmosphere','environment','setting','crowd','interior','music']
x=[]
z=[]
file_path = glob.glob("C:\\Python27\\nlp\\Reviews\\*.txt")

calc_rating=[]
given_rating=[]

review=''' 
 
 
 
This is one of the best restaurants I feel in Ahmedabad. Nice ambience , cool place , very good taste and great service for weekend fun.

Authentic taste is usp of this place for anyone interested in awadhpuri and non veg is too good too. Although I dont eat but my friends have liked it very much

Best part every time there is birthday or deal I get message and phone call about it    '''
 
 

'''
tagged_review = pos_tag(word_tokenize(review))

lmtzr = WordNetLemmatizer()


for i in tagged_review:
    if(i[1]=='NN'):
        x.append(i[0])
    elif(i[1]=='NNS'):
        x.append(i[0])

for i in x:
    y=lmtzr.lemmatize(i)
    z.append(y)

#print z
print review
def detect(tag,z,stat):
    for i in tag:
        if i in z:
            print stat
            break

detect(food,z,"food")
detect(service,z,"service")
detect(price,z,"price")
detect(ambience,z,"ambience")
'''
def polarity(review):
    z = 0
    x=0
    wiki = TextBlob(review)
    siki = wiki.sentences
    a=[]
    for i in siki:
        if(-0.2<i.sentiment.polarity<0.2):
            continue
        a.append(round(i.sentiment.polarity,2))
    if(len(a)==0):
        x = round(sum(a)/5,2)
    else:
        x = round(sum(a)/len(a),2)
    z = scale_rating(x)
    print 'overall rating',z
    calc_rating.append(z)

def scale_rating(x):
    if -1.0 <= x <-0.8:
        return "0.5"
    elif -0.8 <= x <-0.6:
        return "1"
    elif -0.6 <= x <-0.4:
        return "1.5"
    elif -0.4 <= x <-0.2:
        return "2"
    elif -0.2 <= x <0:
        return "2.5"
    elif 0 <= x <0.2:
        return "3"
    elif 0.2 <= x<0.4:
        return "3.5"
    elif 0.4<= x<0.6:
        return "4"
    elif 0.6<= x<0.8:
        return "4.5"
    elif 0.8<= x <1.0:
        return "5"

#polarity(review)

def asprate(review):
    food_selected_sent=[]
    service_selected_sent=[]
    price_selected_sent=[]
    ambience_selected_sent=[]
    category=[]
    
    zen = TextBlob(review)
    sentences=zen.sentences
    for sentence in sentences:
        words = sentence.words
        for i in words:
            w=Word(i)
            i=w.lemmatize()
            if(i in food):
                food_selected_sent.append(sentence)
                
                break
            elif(i in service):
                service_selected_sent.append(sentence)
                
                break
            elif(i in price):
                price_selected_sent.append(sentence)
                
                break
            elif(i in ambience):
                ambience_selected_sent.append(sentence)
                
                break
    #print (food_selected_sent,service_selected_sent,price_selected_sent,ambience_selected_sent)
    food_polarity=[]
    service_polarity=[]
    price_polarity=[]
    ambience_polarity=[]
    for i in food_selected_sent:
        food_polarity.append(i.sentiment.polarity)
    
    for i in service_selected_sent:
        service_polarity.append(i.sentiment.polarity)
    
    for i in price_selected_sent:
        price_polarity.append(i.sentiment.polarity)

    for i in ambience_selected_sent:
        ambience_polarity.append(i.sentiment.polarity)

    #print (food_polarity,service_polarity,price_polarity,ambience_polarity)
    if food_polarity:
        
        sum_food=0       
        for i in food_polarity:
            sum_food+=i
        print 'food',scale_rating(sum_food/len(food_polarity))

    if service_polarity:

        sum_service=0
        for i in service_polarity:
            sum_service+=i
        print 'service',scale_rating(sum_service/len(service_polarity))

    if price_polarity:

        sum_price=0
        for i in price_polarity:
            sum_price+=i
        print 'price',scale_rating(sum_price/len(price_polarity))

    if ambience_polarity:

        sum_ambience=0
        for i in ambience_polarity:
            sum_ambience+=i
        print 'ambience',scale_rating(sum_ambience/len(ambience_polarity))

for files in file_path:
    st_in = files.find('_')+1
    end_in = files.find('.')+2
    rating = files[st_in:end_in]
    given_rating.append(files[st_in:end_in])
    
    with open(files,'r') as myfile:
        raw = myfile.read()
        print files

        polarity(raw)
        asprate(raw)
        
print given_rating
print calc_rating
given_rating = map(float, given_rating)
calc_rating = map(float, calc_rating)
print pearsonr(given_rating,calc_rating)
count = 0
for a,b in zip(given_rating,calc_rating):
    if abs(a-b)<=0.5:
        count+=1
print count

count_rate=0
for rating in given_rating:
    if rating>=4.0:
        count_rate=count_rate+1

print count_rate


#print food_counter,service_counter,ambience_counter,price_counter

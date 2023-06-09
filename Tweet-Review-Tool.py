# -*- coding: utf-8 -*-

from nltk.toolbox import TreeBuilder
import requests, json, textblob, nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

data = None

def get_data():
    global data
    response = requests.get('https://dgoldberg.sdsu.edu/515/customer_service_tweets_full.json')
    if response:
        data = json.loads(response.text)

        
    else:
        print('Sorry, connection error.')

get_data()

def process_data(analysis_type, lower_handle):
    # aggrigate tweets from lower_handle into lower_handle_tweets list
    lower_handle_tweets = [textblob.TextBlob(line['Text'])for line in data if line['Company'].lower() == lower_handle]
    num_tweets = len(lower_handle_tweets)
    if analysis_type == 'polarity':
        return sum([tweet.sentiment.polarity for tweet in lower_handle_tweets])/len(lower_handle_tweets)
    if analysis_type == 'subjectivity':
        return sum([tweet.sentiment.polarity for tweet in lower_handle_tweets])/len(lower_handle_tweets)
    if analysis_type =='formality':
        nouns = {'NN','NNS','NNP','NNPS'}
        adjectives = {'JJ','JJR','JJS'}
        prepositions = {'IN'}
        pronouns = {'DT', 'PDT','WDT'}
        determiners = {'DT', 'PDT', 'WDT'}
        verbs = {'VB', 'VBD','VBG', 'VBN','VBP','VBZ'}
        adverbs = {'RB','RBR', 'RBS', 'WRB'}
        interjections = {'UH'}
        f_set = nouns | adjectives | prepositions | determiners 
        c_set = pronouns | verbs| adverbs | interjections

        total_formality = 0
        for tweet in lower_handle_tweets:
            f = sum(tag in f_set for (word, tag) in tweet.tags)
            c = sum(tag in c_set for (word, tag) in tweet.tags)
            formality = 50 * (((f - c)/(f + c)) + 1)
            total_formality += formality
        return total_formality / num_tweets
    return None


#    for line in data:
#            company_name = line['Company']
#            tweet = line['Text']
#    for line in tweet:
#            blob = textblob.TextBlob(tweet)
#            sentences = blob.sentences

def prompt_analysis():
    while True:
        try:
            analysis = input('Which analysis would you like to perform (polarity/subjectivity/formality)?').lower().strip()
            if analysis not in ['polarity', 'subjectivity', 'formality']:
                raise ValueError
            handle = input('Which Twitter handle would you like to analyze?')
            lower_handle = handle.lower().strip()
            if lower_handle not in [line['Company'].lower() for line in data]:
                raise ValueError
            postprocess_result = process_data(analysis, handle)
            print(f'{handle}: {postprocess_result}')
        except ValueError:
            print('Sorry, that type of analysis is not supported. Please try again.')
        finally:
            repeat = input('Would you like to run another analysis (yes/no)?')
            lower_repeat = repeat.lower().strip()
            if lower_repeat == 'no':
                break
        

print('Welcome to the customer service analyzer!')
repeat = 'yes'

# while repeat.lower().strip() == 'yes':
#     try:
#         analysis = input('Which analysis would you like to perform (polarity/subjectivity/formality)?').lower().strip()
#         print()
#         for analysis in 
#         handle = input('Which Twitter handle would you like to analyze?')
#         print()
#         repeat = input('Would you like to run another analysis (yes/no)?')
#     except ValueError:
#         print('This is not an accepted response. Please enter requested values.')

get_data()
prompt_analysis()

import logging
import pickle
import re
import string

import gensim
import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize
# from crawler.modelling.summarizer import summarize
from crawler.modelling.summerizer_new import summarize
from crawler.models import Article, ArticleTopic, Topic
from nltk.stem import PorterStemmer, WordNetLemmatizer

log = logging.getLogger(__name__)


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def textcleaning(article, stemmer, lemm):
    # Tokenization
    article = re.sub(r'[^\w\s]', '', article).strip()
    words_tokenized = nltk.word_tokenize(article)
    # Stop words removal
    stopwords = nltk.corpus.stopwords.words('english')
    cleaned_words = [
        word.lower() for word in words_tokenized if word.lower() not in stopwords]
    # lemmatization
    lemm_words = [lemm.lemmatize(w) for w in cleaned_words]

    return lemm_words


def preprocess_articles():
    articles = Article.objects.all().values_list('id', 'article')[:500]
    # print(len(articles))
    articles_df = pd.DataFrame.from_records(data=list(articles), columns=['id', 'article'])
    print("Got {} reconds for lda model".format(len(articles_df)))
    stemmer = PorterStemmer()
    lemm = WordNetLemmatizer()
    articles_df['preprocessed'] = articles_df.apply(
        lambda row: textcleaning(row.article, stemmer, lemm), axis=1)
    # articles_df['sentences'] = articles_df.apply(
    #     lambda row: createsentences(row.article), axis=1)
    return articles_df


def run_topic_modelling(articles_df):
    NUMTOPICS = 30
    dictionary = gensim.corpora.Dictionary(articles_df['preprocessed'])
    dictionary.filter_extremes(no_below=15, no_above=0.1)
    bow_corpus = [dictionary.doc2bow(doc)
                  for doc in articles_df['preprocessed']]
    try:
        fileObject = open('lda_model','rb')  
        lda_model4 = pickle.load(fileObject)
        print("model found")
        fileObject.close()
    except FileNotFoundError:
        print("runnign model now")
        lda_model4 = gensim.models.LdaMulticore(bow_corpus,
                                                num_topics=NUMTOPICS,
                                                id2word=dictionary,
                                                passes=100,
                                                workers=2)
        with open('lda_model', 'wb') as fileobj:
            pickle.dump(lda_model4, fileobj)

    topics = lda_model4.show_topics(num_topics=NUMTOPICS)

    topicslist = []
    for idx,t in enumerate(topics):
        x = t[1].split('+')
        for i in x:
            z = i.split('*')
            topicslist.append([idx, float(z[0]), z[1].strip()[1:-1]])
    # print(topicslist)
    return topicslist, dictionary, lda_model4

def save_topics(topicslist):
    print("deleting topics")
    Topic.objects.all().delete()
    for topic in topicslist:
        # print(topic)
        t = Topic(topic=topic[0],keyword=topic[2],probability=topic[1])
        t.save()

def assign_topics_article(dictionary, lda_model):
    articles = Article.objects.all()
    topics = Topic.objects.all()
    print("deleting ArticleTopic mapping")
    ArticleTopic.objects.all().delete()

    stemmer = PorterStemmer()
    lemm = WordNetLemmatizer()
    for article in articles:
        res = lda_model.get_document_topics(dictionary.doc2bow(textcleaning(article.article, stemmer, lemm)))
        for r in res:
            # print("here")
            a = ArticleTopic(articleId=article, topicId=r[0], probability=r[1])
            a.save()
        # print(article.article)
        article.summary=summarize(sent_tokenize(article.article))
        print(article.summary)
        article.save(update_fields=['summary'])
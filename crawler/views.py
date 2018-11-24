from django.shortcuts import render
from crawler.modelling import topicmodelling
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def run_model(request):
    df = topicmodelling.preprocess_articles()
    topics, dictionary, lda_model = topicmodelling.run_topic_modelling(df)
    topicmodelling.save_topics(topics)
    topicmodelling.assign_topics_article(dictionary, lda_model)
    return HttpResponse(status=201)

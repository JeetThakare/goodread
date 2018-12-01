from django.shortcuts import render
from crawler.modelling import topicmodelling
from django.http import HttpResponse
from django.http import JsonResponse
from crawler.models import Article, ArticleTopic, Topic

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

def get_topics(request):
    try:
        topics = Topic.objects.all().order_by('-probability')[:150]
        response = []
        topicset = set()
        for topic in topics:
            originallen = len(topicset)
            topicset.add(topic.keyword)
            if len(topicset) == originallen:
                continue
            response.append({'topic':topic.topic, 'keyword':topic.keyword})
    except:
        return JsonResponse({'data':[], 'status':False})
    del topicset
    return JsonResponse({'data':response, 'status':True})

def get_articles(request):
    topicskeywords = request.GET['q'].split(',')
    # print(topicskeywords)
    topics = set()
    articletopics_set = set()
    res = list()
    for topick in topicskeywords:
        topicobjs = Topic.objects.filter(keyword = topick).order_by('-probability')[:5]
        topics.update([tobj.topic for tobj in topicobjs])
    # print(topics)
    for t in topics:
        articletopics = ArticleTopic.objects.filter(topicId=t).order_by('-probability')[:5]
        articletopics_set.update(articletopics)
    # print(articletopics_set)
    res.append([{'text':article.articleId.article, 'url':article.articleId.url} for article in articletopics_set])
    # print(res)
    return JsonResponse({'data':res})
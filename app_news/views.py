from django.forms import ValidationError
from django.urls import reverse
from django.shortcuts import render
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError, HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.validators import EmailValidator, ValidationError
from django.views import View
from .models import TopPosts, LatestPosts, Business, Sport, EmailList
from newsapi import NewsApiClient
from django.db.models import Count
from django.apps import apps
from .forms import EmailListForm
from django.contrib import messages
import re
from math import ceil
from .topic import TopicModel



class NewsApiMixin:
    api_key = '5e6869c7f6e8463396a829465bff72a7'

    def __init__(self):
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def get_top_articles(self, category):
        return self.newsapi.get_top_headlines(category=category, language='en')
    
    def get_everything(self, sources, language, sort_by):
        return self.newsapi.get_everything(sources=sources, language=language, sort_by=sort_by)
    
    
class ArticleProcessor:
    @staticmethod
    def process_and_save_articles(articles, model):
        topicGetter = TopicModel()
        if 'articles' in articles:
            articles = articles['articles']

            for article in articles:
                title = article['title'] or "No title available"
                description = article['description'] or article['content']
                source = article['source']['name'] or "No source available"
                url_img = article['urlToImage'] or "https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
                url = article['url']
                category = topicGetter.getTopic(description, num_topics=1) or "No category available"
                textContent = str(article['content'])
                timeToRead = ArticleProcessor.calcuate_read_time(textContent, 200)

                # Use get_or_create() to avoid creating duplicate posts
                post, created = model.objects.get_or_create(
                    title=title,
                    defaults={
                        'author': source,
                        'main_image': url_img,
                        'excerpt': description,
                        'urlToPost': url,
                        'category': category,
                        'timeToRead': timeToRead,
                    }
                )

                # If the post is newly created, save it
                if created:
                    try:
                        post.save()
                    except ValidationError as e:
                        print(f"Failed to save post with title '{title}' to {model.__name__} due to validation error: {e}")
        else:
            print(f"No articles found for model {model.__name__}")
    
    @staticmethod
    def calcuate_read_time(text, wpm=200) -> int:
        # Extract the number of additional characters from the text
        additional_chars_match = re.search(r"\+(\d+) chars", text)
        if additional_chars_match:
            additional_chars = int(additional_chars_match.group(1))
        else:
            additional_chars = 0

        cleaned_text = re.sub(r"[^\w\s]|(\+\d+ chars)", "", text)

        partial_word_count = len(cleaned_text.split())

        avg_chars_per_word = 5
        
        total_word_count = partial_word_count + additional_chars / avg_chars_per_word

        minutes = total_word_count / wpm
        
        return ceil(minutes)
    
class AuthorImageProecessor:
    companies = {'BBC News': 'bbc.png',
                'CNN' : 'cnn.png',
                'CBS Sports' : 'cbs.png',
                'Reuters' : 'reuters.png',
                'The Times of India': 'toi.png',
                'YouTube':'youtube.png',
                'Hindustan Times':'ht.png',
                'NDTV News':'ndtv.png',}

    def getLogo(self, name):
        if name in self.companies:
            return self.companies[name]


class IndexView(NewsApiMixin, View):
    template_name = 'app_news/main.html'
    
    def get(self, request):

        # Fetch top headlines
        top_headlines = self.get_top_articles(category='general')
        latest_news = self.get_everything(sources='bbc-news', language='en', sort_by='publishedAt')
        business_news = self.get_top_articles(category='business')
        sport_news = self.get_top_articles(category='sports')

        # Process and save articles
        ArticleProcessor.process_and_save_articles(top_headlines, TopPosts)
        ArticleProcessor.process_and_save_articles(latest_news, LatestPosts)
        ArticleProcessor.process_and_save_articles(business_news, Business)
        ArticleProcessor.process_and_save_articles(sport_news, Sport)

        # Retrieve the author counts
        author_counts = TopPosts.objects.values('author').annotate(count=Count('author'))

        # Sort the author counts by the number of articles in descending order
        sorted_author_counts = sorted(author_counts, key=lambda x: x['count'], reverse=True)

        # Get the sorted list of authors
        sorted_authors = [item['author'] for item in sorted_author_counts][:4]

        all_posts = TopPosts.objects.order_by('pk').last()
        latest_posts = LatestPosts.objects.order_by('-pk')[:4]
        business_posts = Business.objects.order_by('-pk')[:2]
        sport_posts = Sport.objects.order_by('-pk')[:2]

        form = EmailListForm()

        authorImgProcess = AuthorImageProecessor()
        authorImg = [authorImgProcess.getLogo(author) for author in sorted_authors]
        author_and_img = zip(sorted_authors, authorImg)

        context = {'posts': all_posts,
                   'latest': latest_posts, 
                   'business': business_posts, 
                   'sport': sport_posts, 
                   'sorted_authors': sorted_authors, 
                   'authorAndImg': author_and_img,
                   'form' : form,}
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        email = request.POST.get('email')

        emial_validator = EmailValidator()
        try:
            emial_validator(email)
            email_is_valid = True
        except ValidationError:
            email_is_valid = False
        
        if email_is_valid:
            email_list, created = EmailList.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'You have successfully subscribed to our newsletter!')
                email_list.save()
            else:
                messages.warning(request, 'You are already subscribed to our newsletter!')
            
            request.session['subscribed'] = True
            #return HttpResponseRedirect(reverse('success'))
        else:
            messages.error(request, 'Please enter a valid email address!')
            #return HttpResponseRedirect(reverse('index'))
        
        return self.get(request)



#TODO: Finish class
class SpecificCategoryView(View):
    template_name = 'app_news/allPage.html'

    def get(self, request, model):
        try:
            identfyModel = apps.get_model('app_news', model)
            return render(request, self.template_name, {'posts': identfyModel.objects.all()})
        except:
            HttpResponseNotFound('<h1>Page not found</h1>')


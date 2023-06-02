from django.forms import ValidationError
from django.shortcuts import render
from django.views import View
from .models import TopPosts, LatestPosts, Business, Sport
from newsapi import NewsApiClient
from django.db.models import Count
import re
from math import ceil


class IndexView(View):
    template_name = 'app_news/main.html'
    api_key = '5e6869c7f6e8463396a829465bff72a7'

    def get(self, request):
        # Initialize NewsApiClient
        newsapi = NewsApiClient(api_key=self.api_key)

        # Fetch top headlines
        top_headlines = newsapi.get_top_headlines(category='general', language='en')
        latest_news = newsapi.get_everything(sources='bbc-news', language='en', sort_by='publishedAt')
        business_news = newsapi.get_top_headlines(category='business')
        sport_news = newsapi.get_top_headlines(category='sports')

        # Process and save articles
        self.process_and_save_articles(top_headlines, TopPosts)
        self.process_and_save_articles(latest_news, LatestPosts)
        self.process_and_save_articles(business_news, Business)
        self.process_and_save_articles(sport_news, Sport)

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

        return render(request, self.template_name, {'posts': all_posts, 'latest': latest_posts, 'business': business_posts, 'sport': sport_posts, 'sorted_authors': sorted_authors})

    def process_and_save_articles(self, news_articles, model):
        if 'articles' in news_articles:
            articles = news_articles['articles']

            for article in articles:
                title = article['title'] or "No title available"
                description = article['description'] or article['content']
                source = article['source']['name'] or "No source available"
                url_img = article['urlToImage'] or "https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
                url = article['url']
                #category = article['category'] or "No category available"
                textContent = str(article['content'])
                timeToRead = self.calcuate_read_time(textContent, 200)

                # Use get_or_create() to avoid creating duplicate posts
                post, created = model.objects.get_or_create(
                    title=title,
                    defaults={
                        'author': source,
                        'main_image': url_img,
                        'excerpt': description,
                        'urlToPost': url,
                        #'category': category,
                        'timeToRead': timeToRead,
                    }
                )

                # If the post is newly created, save it
                if created:
                    try:
                        post.save()
                        print(f"Saved post with title '{title}' to {model.__name__}")
                    except ValidationError as e:
                        print(f"Failed to save post with title '{title}' to {model.__name__} due to validation error: {e}")
                else:
                    print(f"Post with title '{title}' already exists in {model.__name__}")
        else:
            print(f"No articles found for model {model.__name__}")
    
    def calcuate_read_time(self, text, wpm=200) -> int:
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
    
    def getLogo(self, name):
        pass

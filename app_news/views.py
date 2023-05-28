from django.forms import ValidationError
from django.shortcuts import render
from django.views import View
from .models import TopPosts, LatestPosts
from newsapi import NewsApiClient
from datetime import datetime

class IndexView(View):
    template_name = 'app_news/main.html'
    api_key = '5e6869c7f6e8463396a829465bff72a7'

    def get(self, request):
        # Initialize NewsApiClient
        newsapi = NewsApiClient(api_key=self.api_key)

        # Fetch top headlines
        top_headlines = newsapi.get_top_headlines(country='us')
        latest_news = newsapi.get_everything(sources='bbc-news',language='en',sort_by='publishedAt')

        if 'articles' in top_headlines:
            articles_Top = top_headlines['articles']

            for article in articles_Top:
                title_top = article['title'] or "No title available"
                description_top = article['description'] or article['content']
                source_top = article['source']['name'] or "No source available"
                url_img_top = article['urlToImage'] or "https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
                published_date_str = article['publishedAt']
                published_date = datetime.strptime(published_date_str, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = published_date.strftime("%Y-%m-%d")
                url_Top = article['url']

                # Use get_or_create() to avoid creating duplicate posts
                post, created = TopPosts.objects.get_or_create(
                    title=title_top,
                    defaults={
                        'author': source_top,
                        'main_image': url_img_top,
                        'excerpt': description_top,
                        'urlToPost': url_Top,
                        'date': formatted_date,
                    }
                )

                # If the post is newly created, save it
                if created:
                    try:
                        post.save()
                    except ValidationError:
                        pass

        if 'articles' in latest_news:
            articles_Latest = latest_news['articles']

            for article in articles_Latest:
                title_latest = article['title'] or "No title available"
                description_latest = article['description'] or article['content']
                source_latest = article['source']['name'] or "No source available"
                url_img_latest = article['urlToImage'] or "https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
                published_date_str = article['publishedAt']
                published_date = datetime.strptime(published_date_str, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = published_date.strftime("%Y-%m-%d")
                url_latest = article['url']

                # Use get_or_create() to avoid creating duplicate posts
                post, created = LatestPosts.objects.get_or_create(
                    title=title_latest,
                    defaults={
                        'author': source_latest,
                        'main_image': url_img_latest,
                        'excerpt': description_latest,
                        'urlToPost': url_latest,
                        'date': formatted_date,
                    }
                )

                # If the post is newly created, save it
                if created:
                    try:
                        post.save()
                    except ValidationError:
                        pass

        all_posts = TopPosts.objects.order_by('pk').last()
        latest_posts = LatestPosts.objects.order_by('pk')[:4]
        return render(request, self.template_name, {'posts': all_posts, 'latest': latest_posts})

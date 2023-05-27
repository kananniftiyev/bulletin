from django.forms import ValidationError
from .models import Posts
from django.shortcuts import render
import requests
# Create your views here.

apiKey = '5e6869c7f6e8463396a829465bff72a7'

top_headlines = 'https://newsapi.org/v2/top-headlines?country=pl&apiKey=' + apiKey
business_headlines = requests.get(f'https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={apiKey}').json()
entertainment_headlines = requests.get(f'https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey={apiKey}').json()




def index(request):
    response = requests.get(top_headlines)
    top_data = response.json()
    articles_Top = top_data['articles']
    articles_Business = business_headlines['articles']
    articles_Entertainment = entertainment_headlines['articles']
    all_posts = []
    for article in articles_Top:
        title_top = article['title'] if article['title'] else "No title available"
        description_top = article['description'] if article['description'] else "No description available"
        source_top = article['source']['name'] if article['source']['name'] else "No source available"
        url_img_top = article['urlToImage'] if article['urlToImage'] else "https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
        content_top = article['content'] if article['content'] else "No content available"

        # Use get_or_create() to avoid creating duplicate posts
        post, created = Posts.objects.get_or_create(
            title=title_top,
            defaults={
                'content': content_top,
                'author': source_top,
                'main_image': url_img_top,
                'excerpt': description_top
            }
        )

        # If the post is newly created, save it
        if created:
            try:
                post.save()
            except ValidationError:
                pass

        #post = Posts(title=title_top, content=content_top, author=source_top, main_image=url_img_top, excerpt=description_top)

    

    all_posts = Posts.objects.all().order_by('date').first()
    return render(request, 'app_news/main.html', {'posts' : all_posts})
    



                


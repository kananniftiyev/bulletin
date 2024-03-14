# tasks.py

import logging
from celery import shared_task

from .models import TopPosts, Sport, Business, LatestPosts
from .views import NewsApiMixin, ArticleProcessor

logger = logging.getLogger(__name__)


@shared_task
def fetch_and_save_news():
    try:
        logger.info("Background task 'fetch_and_save_news' started.")

        # Fetch news from the NewsAPI
        news_api = NewsApiMixin()
        top_headlines = news_api.get_top_articles(category='general')
        latest_news = news_api.get_everything(sources='bbc-news', language='en', sort_by='publishedAt')
        business_news = news_api.get_top_articles(category='business')
        sport_news = news_api.get_top_articles(category='sports')

        all_articles = top_headlines['articles'] + latest_news['articles'] + business_news['articles'] + sport_news[
            'articles']

        # Process and save articles in bulk
        ArticleProcessor.process_and_save_articles(all_articles, TopPosts)
        ArticleProcessor.process_and_save_articles(all_articles, LatestPosts)
        ArticleProcessor.process_and_save_articles(all_articles, Business)
        ArticleProcessor.process_and_save_articles(all_articles, Sport)

        logger.info("Background task 'fetch_and_save_news' completed successfully.")
    except Exception as e:
        logger.error(f"Error occurred in background task 'fetch_and_save_news': {str(e)}")

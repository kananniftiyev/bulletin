# Django News Aggregator

This project is a simplified News Aggregator website that helps you stay informed with the latest news from reliable sources. Our platform curates and categorizes articles on various topics, providing succinct summaries for easy browsing.

## Features
- Viewing Specific Category News: Easily browse news articles by specific categories of interest, such as politics, technology, sports, or entertainment. Stay up to date on the topics that matter most to you.

- Email Subscriptions for Latest News: Stay ahead of the curve by subscribing to our email service, which delivers the latest news directly to your inbox. Never miss an important story again.

- Simple Search Functionality: Find the news you're looking for quickly and effortlessly with our user-friendly search function. Simply enter your keywords, and our system will provide you with relevant articles in an instant.


## Installation

The first thing to do is to clone the repository:

```bash
git clone https://github.com/kananniftiyev/django_news_website/
cd django_news_website
```

Create a virtual environment to install dependencies in and activate it:
```bash
virtualenv env
source env/bin/activate
```

Then install the dependencies:
```bash
pip install -r requirements.txt
```

Once pip has finished downloading the dependencies and Setup Database:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## License

[MIT](https://choosealicense.com/licenses/mit/)
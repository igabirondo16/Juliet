from utils.QuerySearcher import QuerySearcher
from exceptions.exceptions import NoFoundArticles
import json

class ArticlesKeeper(object):

    def __init__(self, json_file = {}):

        if json_file == {}:
            self.article = {}
            self.article_list = []

        else:
            json_data = json.loads(json_file)
            self.article = json_data['article']
            self.article_list = json_data['article_list']

    def to_json(self):
         return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def set_article(self, article):
        self.article = article

    def get_article(self):
        return self.article

    def set_article_list(self, article_list):
        self.article_list = article_list

    def get_article_list(self):
        return self.article_list
    
    def get_articles_by_category(self, category):
        qs = QuerySearcher()
        news = qs.get_news_by_category(category)
        
        news_list = []
        idx = 0
        for new in news:
            if idx > 2:
                break

            news_list.append(new)
            idx += 1

        self.set_article_list(news_list)
        return news_list

    def get_article_list_from_category(self, category, user_query):
        qs = QuerySearcher()
        article_list = qs.search_article(category, user_query)
        print("RESULT: " + str(article_list))

        if article_list == None:
            raise NoFoundArticles

        self.set_article_list(article_list)
        return article_list

    def get_article_list_from_all_news(self, user_query):
        article_list = self.get_article_list_from_category('all_articles', user_query)
        return article_list

    def get_article_content(self, article_index):
        article_list = self.get_article_list()
        article = article_list[article_index]
        self.set_article(article)
        return article['content'], article['url']


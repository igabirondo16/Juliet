from utils.QuerySearcher import QuerySearcher
import json

class ArticlesKeeper(object):

    def __init__(self, json_file = {}):

        if json_file == {}:
            self.article = {}

        else:
            json_data = json.loads(json_file)
            self.article = json_data['article']

    def to_json(self):
         return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def set_article(self, article):
        self.article = article

    def get_article(self):
        return self.article
    
    def get_articles_by_category(self, category):
        qs = QuerySearcher()
        news = qs.get_news_by_category(category)
        output_msg = "Kategoria: " + category + "\n\n"
        index = 1
        for new in news:
            header = new['original_header']
            output_msg += str(index) + ") " + header + "\n"
            index += 1

        return output_msg

    def get_article_content_from_category(self, category, user_query):
        qs = QuerySearcher()
        result = qs.search_article(category, user_query)
        print("RESULT: " + str(result))

        if result == None:
            return None

        self.set_article(result)
        return result['content']

    def get_article_content_from_all_news(self, user_query):
        result = self.get_article_content_from_category('all_articles', user_query)
        return result


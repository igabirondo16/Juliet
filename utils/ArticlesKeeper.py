from QuerySearcher import QuerySearcher

class ArticlesKeeper(object):
    
    
    def __init__(self):
        self.article = None
    

    def get_news_by_category(self, category):
        qs = QuerySearcher()
        news = qs.get_news_by_category(category)
        output_msg = "Kategoria: " + category + "\n\n"
        index = 1
        for new in news:
            header = new['original_header']
            output_msg += str(index) + ") " + header + "\n"
            index += 1


        return output_msg

    def get_new_content(self, category, user_query):
        qs = QuerySearcher()
        result = qs.search_article(category, user_query)

        if result == None:
            return "Ez da emaitzarik aurkitu"

        return result['content']


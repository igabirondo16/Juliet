
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import scoring, sorting
from whoosh import qparser

from ixapipes.tok import IxaPipesTokenizer
from ixapipes.pos import IxaPipesPosTagger

from utils.scrapper import filter_user_query

class QuerySearcher:

    def __init__(self):
        self.tokenizer = None
        self.lemmatizer = None 

    def __search(self, category, query):
        # Open the index of the category
        ix = index.open_dir('index', indexname=category)

        qp = QueryParser('header', schema = ix.schema, group=qparser.OrGroup)
        #qp = QueryParser('header', schema=ix.schema)
        q = qp.parse(query)
        print(q)

        with ix.searcher(weighting = scoring.BM25F(B=0)) as searcher:
            
            if not searcher.up_to_date():
                searcher = searcher.refresh()

            results = searcher.search(q, limit=3)

            if not results:
                return None

            else:
                articles = []
                
                for result in results:
                    temp_article = {}
                    temp_article['header'] = result.get('header')
                    temp_article['original_header'] = result.get('original_header')
                    temp_article['url'] = result.get('url')
                    temp_article['content'] = result.get('content')

                    if temp_article not in articles:    
                        articles.append(temp_article)

                
                return articles
    

    def __preprocess_user_query(self, header):
        header = header.replace('"', '')

        if self.tokenizer == None:    
            self.tokenizer = IxaPipesTokenizer('eu')

        if self.lemmatizer == None:
            self.lemmatizer = IxaPipesPosTagger('eu', 'morph-models-2.5.0/eu/eu-pos-perceptron-epec.bin','morph-models-1.5.0/eu/eu-lemma-perceptron-epec.bin')

        tokens = self.tokenizer(header)
        lemmas = self.lemmatizer(tokens)
        final_lemmas = filter_user_query(lemmas)
        return final_lemmas


    def search_article(self, category_name, article_header):
        article_header = self.__preprocess_user_query(article_header)
        article_content = self.__search(category_name, article_header)

        return article_content

    def get_news_by_category(self, category):
        ix = index.open_dir('index', indexname=category)
        all_documents = ix.searcher().documents()
        
        return all_documents


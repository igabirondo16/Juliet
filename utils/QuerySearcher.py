
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import scoring

from ixapipes.tok import IxaPipesTokenizer
from ixapipes.pos import IxaPipesPosTagger

from scrapper import get_lemmatized_text

import os.path

class QuerySearcher:

    def __init__(self):
        self.tokenizer = None
        self.lemmatizer = None 

    def __search(self, category, query):
        # Open the index of the category
        ix = index.open_dir('index', indexname=category)

        qp = QueryParser('header', schema = ix.schema)
        q = qp.parse(query)

        with ix.searcher(weighting = scoring.BM25F(B=0)) as searcher:
            
            if not searcher.up_to_date():
                searcher = searcher.refresh()

            results = searcher.search(q, limit=5)

            if not results:
                return None

            else:
                article = {}
                article['header'] = results[0].get('header')
                article['url'] = results[0].get('url')
                article['content'] = results[0].get('content')

                return article
    

    def __preprocess_user_query(self, header):

        if self.tokenizer == None:    
            self.tokenizer = IxaPipesTokenizer('eu')

        if self.lemmatizer == None:
            self.lemmatizer = IxaPipesPosTagger('eu', 'morph-models-2.5.0/eu/eu-pos-perceptron-epec.bin','morph-models-1.5.0/eu/eu-lemma-perceptron-epec.bin')


        tokens = self.tokenizer(header)
        lemmas = self.lemmatizer(tokens)
        final_lemmas = get_lemmatized_text(lemmas)
        return final_lemmas


    def search_article(self, category_name, article_header):
        article_header = self.__preprocess_user_query(article_header)
        article_content = self.__search(category_name, article_header)

        return article_content

    def get_news_by_category(self, category):
        ix = index.open_dir('index', indexname=category)
        all_documents = ix.searcher().documents()
        
        return all_documents


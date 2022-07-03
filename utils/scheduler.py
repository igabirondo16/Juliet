import schedule
import time
from scrapper import get_all_articles, get_lemmatized_text
from whoosh.fields import Schema, KEYWORD, STORED
from whoosh import index, writing
import os, os.path


# All the articles, apart from being stored in the index its own category, are also stored in all_articles index

def create_schema():
    schema = Schema(header=KEYWORD(stored=True),
                    original_header=STORED,
                    url=STORED,
                    content=STORED)

    return schema

def get_index(topic, schema):
    if not os.path.exists('index'):
        os.mkdir('index')
    
    if not index.exists_in('index', indexname=topic):
        ix = index.create_in('index', schema=schema, indexname=topic)

    else:
        ix = index.open_dir('index', indexname=topic)
    
    return ix

def clear_index(ix):
    writer = ix.writer()
    writer.commit(mergetype=writing.CLEAR)

def print_indexed_documents(ix):
    all_docs = ix.searcher().documents()
    
    for document in all_docs:
        header = document['header']
        print("Lemmatized header: " + header)
        print("Original header: " + document['original_header'])
        print("Content: " + document['content'])
        print("Url: " + document['url'])
        print()

    print()

def update_index_articles(): 
    articles = get_all_articles()
    schema = create_schema()

    for topic in articles.keys():
        ix = get_index(topic, schema)
        clear_index(ix)
        writer = ix.writer()

        article_list = articles[topic]

        for article in article_list:
            header = article['header']
            original_header = article['original_header']
            content = article['content']
            url = article['url']

            #article['header'] = header
            #article['original_header'] = original_header
            
            writer.add_document(header=header, original_header=original_header,content=content, url=url)           

        writer.commit()

    print_indexed_documents(ix)

def main():    
    schedule.every().day.at("13:00").do(update_index_articles)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    #main()
    start = time.time()
    update_index_articles()
    end = time.time()
    print("Time of indexing articles: " + str(end - start))
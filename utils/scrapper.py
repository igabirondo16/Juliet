
from re import sub
import traceback
from bs4 import BeautifulSoup
import requests
import datetime

from ixapipes.tok import IxaPipesTokenizer
from ixapipes.pos import IxaPipesPosTagger

AZKEN_BERRIAK_URL = "https://www.berria.eus"
IRAKURRIENAK_URL = "https://www.berria.eus/irakurriena/"
GIZARTEA_URL = "https://www.berria.eus/gizartea/"
POLITIKA_URL = "https://www.berria.eus/politika/"
EKONOMIA_URL = "https://www.berria.eus/ekonomia/"
MUNDUA_URL = "https://www.berria.eus/mundua/"
IRITZIA_URL = "https://www.berria.eus/iritzia/"
KULTURA_URL = "https://www.berria.eus/kultura/"
KIROLA_URL = "https://www.berria.eus/kirola/"
BIZIGIRO_URL = "https://www.berria.eus/bizigiro/"

topics = ["Azken berriak", "Berri irakurrienak", "Gizartea", "Politika", "Ekonomia", "Mundua", "Iritzia", "Kultura", "Kirola", "Bizigiro"]

forbidden_tokens = ['berri', 'artikulu', 'albiste', 'notizi']

tokenizer = IxaPipesTokenizer('eu')
lemmatizer = IxaPipesPosTagger('eu', 'morph-models-1.5.0/eu/eu-pos-perceptron-epec.bin','morph-models-1.5.0/eu/eu-lemma-perceptron-epec.bin')


def get_file_url(option):

    '''
    Returns the url of the option given by the user.

    Parameters:
        - option (String): Topic chosen by the user.

    Returns:
        Url of the chosen topic. If the option is not a topic, None is returned.
    '''

    if option == "Azken berriak":
        return AZKEN_BERRIAK_URL

    elif option == "Berri irakurrienak":
        return IRAKURRIENAK_URL

    elif option == "Gizartea":
        return GIZARTEA_URL

    elif option == "Politika":
        return POLITIKA_URL

    elif option == "Ekonomia":
        return EKONOMIA_URL

    elif option == "Mundua":
        return MUNDUA_URL

    elif option == "Iritzia":
        return IRITZIA_URL

    elif option == "Kultura":
        return KULTURA_URL

    elif option == "Kirola":
        return KIROLA_URL

    elif option == "Bizigiro":
        return BIZIGIRO_URL

    else:
        return None

def preprocess_header(header):
    tokens = tokenizer(header)
    lemmas = lemmatizer(tokens)
    final_lemmas = get_lemmatized_text(lemmas)
    return final_lemmas

def get_articles(url, main_articles = False):
    '''
    Given an html file, gets all the main headers and the links to the articles by using scrapping. 
    Included classes and id values are selected taking into account the html files' structure.

    Parameters:
        - file (String): Name of the html file

    Returns:
        - A dictionary where:
            Key: Main header of the article
            Value: Url to the article
    '''

    html_file = requests.get(url).text
    soup = BeautifulSoup(html_file, 'html.parser')

    # If chosen topic main_articles, special html structure must be taken into account
    if main_articles:
        links = soup.find(id='nagusiak').find_all(['h2','h3','h4'], class_='article-titu')

    else:
        links = soup.find_all(['h2', 'h3', 'h4'], class_='article-titu')

    articles = []

    for elem in links:
        single_article = {}
        
        l = elem.find('a')
        text = l.text
        url = l.get('href')

        if not url.startswith('https://www.berria.eus'):
            continue

        sub_header, first_paragraph = get_sub_header(url)

        text_to_lemmatize = text + " " +  sub_header + " " + first_paragraph

        print(text_to_lemmatize)

        single_article['header'] = preprocess_header(text_to_lemmatize)
        single_article['original_header'] = text
        single_article['url'] = url

        sub_header = sub_header.replace(u'\xa0',u' ')

        if sub_header and sub_header.strip():
            single_article['content'] = sub_header

        else:
            single_article['content'] = first_paragraph
        
        articles.append(single_article)

    return articles


def get_all_articles():
    '''
    Function to get all the daily articles.

    Returns:
        Dictionary where, the key is the header of the article, and the value is the url of it.
    '''

    global_articles = {}
    all_articles = []
    main_articles = False

    for i in range(len(topics)):
        
        if i < 1:
            main_articles = True

        else:
            main_articles = False

        
        topic = topics[i]
        url = get_file_url(topic)
        articles = get_articles(url, main_articles)
        global_articles[topic] = articles

        if i > 1:
            all_articles += articles

    global_articles['all_articles'] = all_articles

    return global_articles


def get_sub_header(url):
    '''
    Given the session_id of the user and the id of the html file, returns the subheader of the article.
    In case that the selected div label has no contents, first paragraph is returned.

    Parameters:
        - session_id (int): Id of the user session
        - id (int): Id of the html file

    Returns:
        Subheader of the article
    '''
    print("Azken url: " +str(url))
    if url.startswith('/'):
        url = 'https://berria.eus' + url
    

    html_file = requests.get(url).text
    soup = BeautifulSoup(html_file, "html.parser")

    sub_header = soup.find(id = 'albistea_titu').find_all('div', class_="article-sarrera")[0].text
    
    # Extract the first paragraph of the article
    first_paragraph = soup.find('div', class_="article-testua").find('p', recursive=False)
    temp = first_paragraph.find('p', recursive=False)

    if temp != None:
        first_paragraph = temp.text

    else:
        first_paragraph = first_paragraph.text

    return sub_header, first_paragraph

def get_lemmatized_text(naf_text):
    '''
    Given a naf file, gets all the lemmatized words.

    Parameters:
        - naf_text (file in NAF format): File which contains user input, and the lemmatized user input

    Returns:
        String which contains lemmatized user input
    '''
    print(naf_text)
    soup = BeautifulSoup(naf_text, "xml")

    terms = soup.find('terms').find_all('term')

    final_terms = ""
    for term in terms:
        final_terms += " " + term['lemma']

    return final_terms


def filter_user_query(naf_text):
    soup = BeautifulSoup(naf_text, 'xml')

    terms = soup.find('terms').find_all('term')

    final_terms = ""
    for term in terms:
        pos = term['morphofeat']

        if pos.startswith("IZE") and term['lemma'] not in forbidden_tokens:
            final_terms += " " + term['lemma']

    return final_terms


if __name__ == "__main__":
    try:
        url = "https://www.berria.eus/paperekoa/1942/005/001/2022-04-03/genozidioa-berriz-europan.htm"
        sub_header, first_paragraph = get_sub_header(url)
        print(first_paragraph)

    except Exception as e:
        print(traceback.format_exc())

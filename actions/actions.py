from cgitb import text
from email import message
from typing import Any, Text, Dict, List
from urllib import response
from datetime import datetime
import csv
from whoosh import index

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from utils.ArticlesKeeper import ArticlesKeeper
from exceptions.exceptions import NoFoundArticles

MAX_MSG_LENGTH = 3500
MAX_TOKENS = 35

categories = ["Azken berriak", "Berri irakurrienak", "Gizartea", "Politika", "Ekonomia", "Mundua", "Iritzia", "Kultura", "Kirola", "Bizigiro"]

def write_sentence(tracker, text=""):
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    if text == "":
        text = "USER: " + str(tracker.latest_message['text'])

    intent = tracker.latest_message['intent']
    sender_id = tracker.sender_id

    file_path = './conversations/' + str(sender_id) + '.csv'

    with open(file_path, 'a') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([current_time, sender_id, intent, text])


class ActionInitializeArticleKeeper(Action):

    def name(self) -> Text:
        return "action_initialize_article_keeper"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ak_json = ArticlesKeeper().to_json()

        write_sentence(tracker)
        text = "CHATBOT: HASIERA MEZUA"
        write_sentence(tracker, text)

        return [SlotSet('article_keeper', ak_json)]

class ActionDisplayFoundArticles(Action):

    def name(self) -> Text:
        return "action_display_found_articles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try: 
            write_sentence(tracker)
            ak_json = tracker.get_slot('article_keeper')
            ak = ArticlesKeeper(ak_json)
            user_query = tracker.latest_message['text']
            print("Bilatzen ari naiz. User query: " + user_query)

            category = tracker.get_slot('category')
            print('Kategoria: ' + category)

            if not category or not index.exists_in('index', indexname=category):
                article_list = ak.get_article_list_from_all_news(user_query)

            else:
                article_list = ak.get_articles_by_category(category)

            dispatcher.utter_message(response='utter_found_messages')

            idx = 1
            buttons = []

            full_msg = ""

            for article in article_list:
                msg = str(idx) +") " + article['original_header']

                if not full_msg:
                    full_msg = msg

                else:
                    full_msg += "\t" + msg



                btn = {"title":str(idx), "payload":"/choose_article_index{\"article_index\":\"" + str(idx-1) + "\"}"}
                
                buttons.append(btn)

                if idx == len(article_list):
                    dispatcher.utter_message(text=msg, buttons=buttons, button_type="inline")
                else:
                    dispatcher.utter_message(text=msg)

                idx +=1


            ak_json = ak.to_json()

            text = "CHATBOT: " + full_msg
            write_sentence(tracker, text)

            return [SlotSet('article_keeper', ak_json), SlotSet('category', "")]

        except NoFoundArticles:

            text = "CHATBOT: EZ DA MEZURIK AURKITU" 
            write_sentence(tracker, text)

            dispatcher.utter_message(response='utter_error_no_messages')
            return [SlotSet('category', "")]

        
        except Exception:

            text = "CHATBOT: ERRORE OROKORRA" 
            write_sentence(tracker, text)

            dispatcher.utter_message(response='utter_error_general')
            return  [SlotSet('category', "")]
        

class ActionReturnArticleContent(Action):

    def name(self) -> Text:
        return "action_return_article_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:

            write_sentence(tracker)

            ak_json = tracker.get_slot('article_keeper')
            ak = ArticlesKeeper(ak_json)
            article_index = int(tracker.get_slot('article_index'))
            print("Article_index: " + str(article_index))

            content, url = ak.get_article_content(article_index)

            if len(content) > MAX_MSG_LENGTH:
                content_tokens = content.split()
                content = ""

                for i in range(MAX_TOKENS):
                    content += content_tokens[i] + " "

                content += " ..."

            full_msg = content + "\t" + url
            full_msg = full_msg.replace("\n", "")

            if content.endswith('\n'):
                msg = content + url

            else:
                msg = content + "\n" + url
            
            dispatcher.utter_message(text=msg)

            ak_json = ak.to_json()

            text = "CHATBOT: " + full_msg
            write_sentence(tracker, text)

            return [SlotSet('article_keeper', ak_json)]

        except ValueError:

            text = "CHATBOT: > 3 ERROREA" 
            write_sentence(tracker, text)

            dispatcher.utter_message(response='utter_error_article_value')
            return []

        except IndexError:

            text = "CHATBOT: i > len(list) ERROREA" 
            write_sentence(tracker, text)

            dispatcher.utter_message(response='utter_error_article_index')
            return []

        except Exception:

            text = "CHATBOT: ERRORE OROKORRA" 
            write_sentence(tracker, text)

            dispatcher.utter_message(response='utter_error_general')
            return  []


class ActionDisplayHelp(Action):

    def name(self) -> Text:
        return "action_display_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        write_sentence(tracker)

        text = "CHATBOT: LAGUNTZA MEZUA"
        write_sentence(tracker, text)

        dispatcher.utter_message(response='utter_help_msg')
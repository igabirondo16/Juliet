from cgitb import text
from email import message
from typing import Any, Text, Dict, List
from urllib import response

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from utils.ArticlesKeeper import ArticlesKeeper
from exceptions.exceptions import NoFoundArticles


categories = ["Azken berriak", "Berri irakurrienak", "Gizartea", "Politika", "Ekonomia", "Mundua", "Iritzia", "Kultura", "Kirola", "Bizigiro"]


class ActionInitializeArticleKeeper(Action):

    def name(self) -> Text:
        return "action_initialize_article_keeper"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ak_json = ArticlesKeeper().to_json()

        return [SlotSet('article_keeper', ak_json)]

class ActionDisplayFoundArticles(Action):

    def name(self) -> Text:
        return "action_display_found_articles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try: 
            ak_json = tracker.get_slot('article_keeper')
            ak = ArticlesKeeper(ak_json)
            user_query = tracker.latest_message['text']
            print("Bilatzen ari naiz. User query: " + user_query)

            category = tracker.get_slot('category')
            print('Kategoria: ' + category)

            if not category:
                article_list = ak.get_article_list_from_all_news(user_query)

            else:
                article_list = ak.get_articles_by_category(category)

            dispatcher.utter_message(response='utter_found_messages')

            index = 1
            buttons = []

            for article in article_list:
                msg = str(index) +") " + article['original_header']
                btn = {"title":str(index), "payload":"/choose_article_index{\"article_index\":\"" + str(index-1) + "\"}"}
                
                buttons.append(btn)

                if index == len(article_list):
                    dispatcher.utter_message(text=msg, buttons=buttons, button_type="inline")
                else:
                    dispatcher.utter_message(text=msg)

                index +=1


            ak_json = ak.to_json()
            return [SlotSet('article_keeper', ak_json), SlotSet('category', "")]

        except NoFoundArticles:
            dispatcher.utter_message(response='utter_error_no_messages')
            return []

        except Exception:
            dispatcher.utter_message(response='utter_error_general')
            return  []


class ActionReturnArticleContent(Action):

    def name(self) -> Text:
        return "action_return_article_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:

            ak_json = tracker.get_slot('article_keeper')
            ak = ArticlesKeeper(ak_json)
            article_index = int(tracker.get_slot('article_index'))
            print("Article_index: " + str(article_index))

            content, url = ak.get_article_content(article_index)

            if len(content) > 3500:
                content_tokens = content.split()
                num_tokens = 35
                content = ""

                for i in range(num_tokens):
                    content += content_tokens[i] + " "

                content += " ..."

            if content.endswith('\n'):
                msg = content + url

            else:
                msg = content + "\n" + url
            
            dispatcher.utter_message(text=msg)

            ak_json = ak.to_json()
            return [SlotSet('article_keeper', ak_json)]

        except ValueError:
            dispatcher.utter_message(response='utter_error_article_value')
            return []

        except IndexError:
            dispatcher.utter_message(response='utter_error_article_index')
            return []

        except Exception:
            dispatcher.utter_message(response='utter_error_general')
            return  []
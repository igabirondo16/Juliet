# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from utils.ArticlesKeeper import ArticlesKeeper


class ActionInitializeArticleKeeper(Action):

    def name(self) -> Text:
        return "action_initialize_article_keeper"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ak_json = ArticlesKeeper().to_json()

        return [SlotSet('article_keeper', ak_json)]



class ActionReturnArticleContent(Action):

    def name(self) -> Text:
        return "action_return_article_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ak_json = tracker.get_slot('article_keeper')
        ak = ArticlesKeeper(ak_json)
        user_query = tracker.get_slot('article')

        result = ak.get_article_content_from_all_news(user_query)

        if result == None:
            dispatcher.utter_message(response='utter_error_msg')

        else:
            dispatcher.utter_message(text=result)

        ak_json = ak.to_json()
        return [SlotSet('article_keeper', ak_json)]


class ActionReturnArticleUrl(Action):

    def name(self) -> Text:
        return "action_return_article_url"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ak_json = tracker.get_slot('article_keeper')
        ak = ArticlesKeeper(ak_json)

        result = ak.get_article()

        if result == None:
            dispatcher.utter_message(response='utter_error_msg')

        else:
            url = result['url']
            dispatcher.utter_message(text=url)

        ak_json = ak.to_json()
        return [SlotSet('article_keeper', ak_json)]
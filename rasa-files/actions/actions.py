# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset

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


class OrderFishForm(Action):
    def name(self) -> Text:
        return "order_fish_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["fish_type", "fish_menu", "fish_variety", "with_or_without_wine", "confirm_order", "kg", "confirm_price", "payment_type"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ValidateCompareDocumentsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_fish_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:

        additional_slots = []
        if tracker.slots.get("with_or_without_wine") == "yes":
            additional_slots.append("wine_type")

        return additional_slots + slots_mapped_in_domain

    def validate_fish_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate fish_type slot value."""

        return {"fish_type": slot_value}

    def validate_fish_menu(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate fish_menu slot value."""

        return {"fish_menu": slot_value}

    def validate_fish_variety(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate fish_variety slot value."""

        return {"fish_variety": slot_value}

    def validate_with_or_without_wine(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate with_or_without_wine slot value."""

        return {"with_or_without_wine": slot_value}

    def validate_confirm_order(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate confirm_order slot value."""

        return {"confirm_order": slot_value}

    def validate_kg(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate kg slot value."""

        return {"kg": slot_value}

    def validate_confirm_price(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate confirm_price slot value."""

        return {"confirm_price": slot_value}

    def validate_payment_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate payment_type slot value."""

        return {"payment_type": slot_value}


class ActionOrderFish(Action):

    def name(self) -> Text:
        return "action_order_fish"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("coming in compare documents submit",tracker.latest_message['entities'])
        print("fish_type slot", tracker.slots.get("fish_type"))
        print("fish_menu slot", tracker.slots.get("fish_menu"))
        print("fish_variety slot", tracker.slots.get("fish_variety"))
        print("with_or_without_wine slot", tracker.slots.get("with_or_without_wine"))
        print("confirm order slot", tracker.slots.get("confirm_order"))
        print("kg slot", tracker.slots.get("kg"))
        print("confirm price slot", tracker.slots.get("confirm_price"))
        print("payment_type slot", tracker.slots.get("payment_type"))


        # if tracker.slots.get("email") is not None:
        #     dispatcher.utter_message(text=str("Reports sent through email."))
        # else:
        #     dispatcher.utter_message(text=str("Reports can be downloaded from links."))

        # source_document = ""
        # target_document_compare = ""

        # if isinstance(tracker.slots.get("source_document"), list):
        #     source_document = tracker.slots.get("source_document")[0]
        # else:
        #     source_document = tracker.slots.get("source_document")

        # if isinstance(tracker.slots.get("target_document_compare"), list):
        #     target_document_compare = tracker.slots.get("target_document_compare")[0]
        # else:
        #     target_document_compare = tracker.slots.get("target_document_compare")

        # res = "Successfully, the documents <b>{}</b> and <b>{}</b> were compared and reports were generated.".format(source_document, target_document_compare)
        # dispatcher.utter_message(text=res)
        # dispatcher.utter_message(text="Is there anything else, I can help you with?")
        dispatcher.utter_message(text="Your order - 11223344 is confirmed.")
        dispatcher.utter_message(text="Thank you for your support. Enjoy your tasty food.😋")

        return [AllSlotsReset()]
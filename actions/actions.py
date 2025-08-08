


# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.db import guardarUsuario
#
#

# class ActionSetName(Action):
#     def name(self) -> Text:
#         return "action_set_name"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         # 1. Intentar obtener la entidad directamente (ideal)
#         name = next(tracker.get_latest_entity_values("person_name"), None)

#         if name:
#             return [SlotSet("name", name)]

#         # 2. Fallback: intentar inferir el nombre desde el texto libre
#         text = tracker.latest_message.get('text', '').lower()

#         posibles_prefix = ["me llamo", "soy", "mi nombre es", "me dicen", "puedes llamarme"]
#         for prefix in posibles_prefix:
#             if prefix in text:
#                 posible_nombre = text.split(prefix)[-1].strip().title()
#                 if posible_nombre:
#                     return [SlotSet("name", posible_nombre)]

#         # 3. Si no se puede obtener nada
#         dispatcher.utter_message("No pude entender tu nombre. ¿Podrías decirme cómo te llamas?")
#         return []



class ActionGuardarNombre(Action):

    def name(self) -> Text:
        return "action_guardar_nombre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        nombre = tracker.get_slot("name")
        sender_id = tracker.sender_id  # <- este es el ID único del usuario
        
        if not nombre:
            dispatcher.utter_message(text="No entendí tu nombre, ¿puedes repetirlo?")
            return []

        #guardarUsuario(sender_id, nombre)

        dispatcher.utter_message(text=f"Gracias, {nombre}, he guardado tu nombre.")
        return [
            SlotSet("name", nombre),
            SlotSet("usuario_nuevo", False)
        ]



# class ActionPreguntarEmocion(Action):
#     def name(self):
#         return "action_preguntar_emocion"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
#         buttons = [
#             {"title": "😊 Feliz", "payload": '/expresar_emocion{"emocion": "feliz"}'},
#             {"title": " Triste", "payload": '/expresar_emocion{"emocion": "triste"}'},
#             {"title": "😣 Ansioso", "payload": '/expresar_emocion{"emocion": "ansioso"}'},
#             {"title": "😴 Cansado", "payload": '/expresar_emocion{"emocion": "cansado"}'},
#         ]
       
#         dispatcher.utter_message(text="¿Cómo te sientes hoy?\nSelecciona una de las opciones o escribe como te sientes", buttons=buttons,buttons=buttons, button_type="reply")
#         return []
    
class ActionPreguntarEmocion(Action):
    def name(self):
        return "action_preguntar_emocion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Definimos las opciones válidas

        self.valid_choices = {
            "😊 Feliz": "feliz",
            "😌 Tranquilo": "tranquilo",
            "😍 Emocionado": "emocionado",
            "😢 Triste": "triste",
            "😟 Ansioso": "ansioso",
            "😡 Enojado": "enojado",
            "😔 Inseguro": "inseguro",
            "😴 Cansado": "cansado",
            "😐 Neutral": "neutral"
        }

        # Configuración del teclado
        reply_markup = {
            "keyboard": [list(self.valid_choices.keys())[i:i+3] for i in range(0, len(self.valid_choices), 3)],
            "resize_keyboard": True,
            "one_time_keyboard": True,
            "input_field_placeholder": "⚠️ Usa solo los botones ⬇️",
            "is_persistent": True
        }
        # Mensaje inicial
        message = {
            "text": "¿Cómo te sientes hoy?",
            "reply_markup": reply_markup,
            "parse_mode": "Markdown"
        }
        dispatcher.utter_message(json_message=message)
        
        return []
    
class ActionReaccionarEmocion(Action):
    def name(self) -> str:
        return "action_reaccionar_emocion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        emocion_registrada = tracker.get_slot("emocion_registrada")
        emocion = tracker.get_slot("emocion")

        # if emocion_registrada:
        #     dispatcher.utter_message(text="Ya registré cómo te sientes 😊. Gracias.")
        #     return []

        # Reaccionar según la emoción
        if emocion == "feliz":
            dispatcher.utter_message(text="¡Qué alegría saber que estás feliz!")
        elif emocion == "triste":
            dispatcher.utter_message(text="Lamento que estés triste. Estoy aquí para escucharte. 😢")
        elif emocion == "ansioso":
            dispatcher.utter_message(text="Respira profundo. Vamos paso a paso, estoy contigo. 💙")
        elif emocion == "cansado":
            dispatcher.utter_message(text="Descansar es importante. ¿Quieres hablar un poco o prefieres relajarte? 😴")
        else:
            dispatcher.utter_message(text="Gracias por compartir cómo te sientes.")


        dispatcher.utter_message(response="utter_opciones_post_emocion")

        # ✅ Activar la bandera
        return [SlotSet("emocion_registrada", True)]


class ActionSolicitarEmocionLibre(Action):
    def name(self) -> str:
        return "action_solicitar_emocion_libre"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        dispatcher.utter_message(text="Claro, cuéntame con tus propias palabras cómo te sientes.")
        return []




class ActionGetTelegramId(Action):

    def name(self) -> str:
        return "action_get_telegram_id"

    
    def run(self, dispatcher, tracker, domain):
        #Obtener el Id de user telegram del tracker
        user_id = tracker.sender_id

        #Enviar id de tl al user
        dispatcher.utter_message(f"Tu ID de user de telegram es: {user_id}")
        
        #Guardar el id en un slot si es necesario
        return [SlotSet("user_telegram_id", user_id)]


""" class ActionSimularConversacion(Action):
    def name(self) -> Text:
        return "action_simular_conversacion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Usa el slot 'ultimo_tema' para contextualizar
        tema = tracker.get_slot("ultimo_tema") or "una presentación"
        dispatcher.utter_message(f"Vamos a practicar {tema}. Imagina que yo soy un colega. ¿Cómo me saludarías?")
        return []
    

class ActionGuiaRespiracion(Action):  # ¡Antes decía "respiracion" sin "a"!
    def name(self) -> Text:
        return "action_guia_respiracion"  # Nombre exacto como en domain.yml

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("💆‍♂️ Haz esto: Inhala 4 segundos... Aguanta 7... Exhala 8. Repite 3 veces.")
        return []
 """

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




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

#from actions.db import guardarUsuario



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
        print(f"Emoción detectada: {emocion}")
        # if emocion_registrada:
        #     dispatcher.utter_message(text="Ya registré cómo te sientes 😊. Gracias.")
        #     return []
        if not emocion:
            dispatcher.utter_message(text="No he detectado ninguna emoción. Por favor, usa los botones para expresar cómo te sientes.")
            return []
        # Reaccionar según la emoción
        if emocion == "feliz":
            dispatcher.utter_message(text="¡Qué alegría saber que estás feliz! 😄 Me encanta escucharlo.")
        elif emocion == "tranquilo":
            dispatcher.utter_message(text="Qué bueno que te sientas tranquilo. Disfruta de ese momento de calma. 🌿")
        elif emocion == "emocionado":
            dispatcher.utter_message(text="¡Eso suena emocionante! Cuéntame más sobre lo que te tiene así. 🎉")
        elif emocion == "triste":
            dispatcher.utter_message(text="Lamento que estés triste. Si quieres, podemos hablar de lo que te preocupa. 💙")
        elif emocion == "ansioso":
            dispatcher.utter_message(text="Entiendo que te sientas ansioso. Respira profundo, aquí estoy para acompañarte. 🌸")
        elif emocion == "enojado":
            dispatcher.utter_message(text="Entiendo que estés enojado. Si quieres, podemos buscar una forma de canalizarlo. 😡")
        elif emocion == "inseguro":
            dispatcher.utter_message(text="Es normal sentirse inseguro a veces. Recuerda que puedes contar conmigo. 🤝")
        elif emocion == "cansado":
            dispatcher.utter_message(text="Parece que necesitas un descanso. ¿Quieres relajarte un rato? 😴")
        elif emocion == "neutral":
            dispatcher.utter_message(text="Está bien sentirse neutral. Si quieres, podemos charlar para cambiar un poco el ánimo. 🙂")
        else:
            dispatcher.utter_message(text="Gracias por compartir cómo te sientes. Estoy aquí para escucharte. 💬")



        #dispatcher.utter_message(response="utter_opciones_post_emocion")

        # ✅ Activar la bandera
        return [SlotSet("emocion_registrada", True)]






class ActionGuardarContexto(Action):
    def name(self) -> Text:
        return "action_guardar_contexto"

    def run(self, dispatcher, tracker, domain):
        ultimo_tema = tracker.get_slot("ultimo_tema")
        return [
            SlotSet("ultimo_tema_guardado", ultimo_tema),  # Backup
            SlotSet("tema_interrumpido", True)
        ]

class ActionRecuperarContexto(Action):
    def name(self) -> Text:
        return "action_recuperar_contexto"

    def run(self, dispatcher, tracker, domain):
        ultimo_tema = tracker.get_slot("ultimo_tema_guardado")
        return [
            SlotSet("ultimo_tema", ultimo_tema),
            SlotSet("tema_interrumpido", False)
        ]
        
        

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

from telegram import ReplyKeyboardMarkup
from rasa.core.channels.telegram import TelegramOutput
import logging

logger = logging.getLogger(__name__)

class CustomTelegramOutput(TelegramOutput):
    async def send_text_with_buttons(self, recipient_id, text, buttons, **kwargs):
        try:
            # Verificación profunda de estructura
            if (buttons and isinstance(buttons, list) and 
                all(isinstance(row, list) for row in buttons) and
                all(isinstance(btn, dict) for row in buttons for btn in row)):
                
                keyboard = []
                for row in buttons:
                    keyboard_row = []
                    for btn in row:
                        try:
                            keyboard_row.append(btn["title"])
                        except KeyError:
                            logger.warning(f"Botón inválido: {btn}")
                            continue
                    if keyboard_row:  # Solo añadir filas no vacías
                        keyboard.append(keyboard_row)
                
                if keyboard:  # Solo enviar si hay botones válidos
                    await self.bot.send_message(
                        chat_id=recipient_id,
                        text=text,
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard,
                            resize_keyboard=True,
                            one_time_keyboard=True
                        )
                    )
                    return
            
            # Fallback para cualquier caso no manejado
            logger.debug("Usando implementación estándar para botones")
            await super().send_text_with_buttons(recipient_id, text, buttons, **kwargs)
            
        except Exception as e:
            logger.error(f"Error en send_text_with_buttons: {str(e)}")
            raise
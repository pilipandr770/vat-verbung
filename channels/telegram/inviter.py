"""
Акуратне додавання / контакт.
Без масових розсилок.
"""


class TelegramInviter:
    """Запрошує лідів в Telegram."""
    
    def __init__(self):
        """Ініціалізація Telegram inviter."""
        self.platform = "telegram"
    
    def send_invite(self, user_id: str, message: str) -> bool:
        """
        Відправляє запрошення.
        
        Args:
            user_id: ID користувача
            message: Текст запрошення
            
        Returns:
            True якщо успішно
        """
        # TODO: Реалізація відправки запрошення
        print(f"[Telegram] Запрошення користувачу {user_id}")
        return True

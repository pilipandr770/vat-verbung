"""
Follow / акуратний контакт.
Одноразово, без агресивних DM.
"""


class InstagramInviter:
    """Запрошує лідів в Instagram."""
    
    def __init__(self):
        """Ініціалізація Instagram inviter."""
        self.platform = "instagram"
    
    def follow_user(self, user_id: str) -> bool:
        """
        Follow користувача.
        
        Args:
            user_id: ID користувача
            
        Returns:
            True якщо успішно
        """
        # TODO: Реалізація
        print(f"[Instagram] Follow користувачу {user_id}")
        return True
    
    def send_dm(self, user_id: str, message: str) -> bool:
        """
        Відправляє DM (обережно, один раз).
        
        Args:
            user_id: ID користувача
            message: Текст повідомлення
            
        Returns:
            True якщо успішно
        """
        # TODO: Реалізація
        print(f"[Instagram] DM користувачу {user_id}")
        return True

from aiogram.types import User as TelegramUser
from core.models import DatabaseModel


class User(DatabaseModel, TelegramUser):
    """User model."""

    selected_language = "en"
    is_admin = False
    is_superuser = False
    is_active = False

    class Meta(DatabaseModel.Meta):
        collection_name = "user"
        model_name = "user"
        pk_field = "id"
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "language_code",
            "selected_language",
            "is_bot",
            "is_premium",
            "is_admin",
            "is_superuser",
            "is_active",
            "added_to_attachment_menu",
            "can_join_groups",
            "can_read_all_group_messages",
            "supports_inline_queries",
            "created",
        ]

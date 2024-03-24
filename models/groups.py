from core.models import DatabaseModel


class Group(DatabaseModel):
    is_active = True

    class Meta(DatabaseModel.Meta):
        collection_name = "groups"
        model_name = "group"
        pk_field = "chat_id"
        fields = [
            "is_active",
            "chat_id",
        ]

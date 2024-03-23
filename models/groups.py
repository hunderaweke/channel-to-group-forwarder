from core.models import DatabaseModel


class Group(DatabaseModel):
    is_active = True

    class Meta:
        collection_name = "groups"
        model_name = "group"
        pk_field = "id"
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "is_active",
            "created",
        ]

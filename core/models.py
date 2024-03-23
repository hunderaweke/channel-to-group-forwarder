import json

from datetime import datetime


class BaseMode:
    class Meta:
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.meta = cls.Meta()
        cls.meta.model = cls
        cls.meta.model_name = cls.__name__

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

        if self.meta.pk_field not in self.meta.fields:
            self.meta.fields.append(self.meta.pk_field)

        for field in self.meta.fields:
            value = self.kwargs.get(field)
            if value is None:
                default = getattr(self, field, None)
                if callable(default):
                    value = default()
                else:
                    value = default
            setattr(self, field, value)

    def __repr__(self) -> str:
        return f"<{self.meta.model_name} {getattr(self,self.pk_field)}"

    def __str__(self) -> str:
        return f"<{self.meta.model_name.upper()} {getattr(self,self.pk_field)}"

    def to_dict(self):
        return {field: getattr(self, field) for field in self.meta.fields}

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_json(cls, data):
        return cls.from_dict(json.loads(data))
    
    

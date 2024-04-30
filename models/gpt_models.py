from tortoise.models import Model
from tortoise import fields


class History(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=255, null=False, unique=True)
    historyjson = fields.JSONField(null=True)

    class Meta:
        table = 'gpt_history'
        app = 'gpt_history'

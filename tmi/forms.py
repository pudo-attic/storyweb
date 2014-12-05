import colander
from colander import Invalid # noqa


class LoginForm(colander.MappingSchema):
    email = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String())


class CardForm(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    category = colander.SchemaNode(colander.String())
    text = colander.SchemaNode(colander.String())

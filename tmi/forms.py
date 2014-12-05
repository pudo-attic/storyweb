import colander
from colander import Invalid # noqa


class LoginForm(colander.MappingSchema):
    email = colander.SchemaNode(colander.Email())
    password = colander.SchemaNode(colander.String())


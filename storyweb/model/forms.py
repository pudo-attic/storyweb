import colander
from colander import Invalid # noqa


class LoginForm(colander.MappingSchema):
    email = colander.SchemaNode(colander.String(),
                                validator=colander.Email())
    password = colander.SchemaNode(colander.String())


class Ref(object):
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null
        return None

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        value = self.decode(cstruct)
        if value is None:
            raise colander.Invalid(node, 'Missing')
        return value

    def cstruct_children(self, node, cstruct):
        return []

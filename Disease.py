from mongoengine import *

class Disease(Document):
    name = StringField(required=True, unique=True, max_length=30)
    pd = IntField(required=True)
    cli = IntField(required=True)
    loc = IntField(required=True)
    symptoms = ListField(StringField(max_length=30))

    def __init__(self, name, symptoms, pd, loc, cli, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.name = name
        self.symptoms = symptoms
        self.pd = pd
        self.loc = loc
        self.cli = cli

    def set_symptoms(self, symptoms):
        self.symptoms = symptoms
        return

    def set_knowledge_points(self, pd, loc, cli):
        self.pd = pd
        self.loc = loc
        self.cli = cli
        return

    def get_name(self):
        return  self.name

    def get_symp(self):
        return self.symptoms

    def get_pd(self):
        return self.pd

    def get_cli(self):
        return self.cli

    def get_loc(self):
        return self.loc
    #
    # def __str__(self):
    #     return self.name


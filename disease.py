class Disease():
    #pd = population density
    #loc = location of the place
    #cli = climate of the place

    def __init__(self, name, symptoms, pd, loc, cli):
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

    def get_symp(self):
        return self.symptoms

    def get_pd(self):
        return self.pd

    def get_cli(self):
        return self.cli

    def get_loc(self):
        return self.loc

    def get_name(self):
        return self.name

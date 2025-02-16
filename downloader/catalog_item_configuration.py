class CustomizedCatalogItem:

    def __init__(self, id, title="", type=""):
        self.id = id
        self.type = type
        self.title = title

    def __repr__(self):
        return str(self.id) + " " + str(self.type)

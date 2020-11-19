class CatalogItemConfiguration:

    def __init__(self, id, internal_note):
        self.id = id
        self.internal_note = internal_note

    def __repr__(self):
        return str(self.id) + " " + str(self.internal_note)

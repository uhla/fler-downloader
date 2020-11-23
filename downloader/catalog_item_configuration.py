class CustomizedCatalogItem:

    def __init__(self, id, title="", type="", styles="", other_colors=""):
        self.id = id
        self.type = type
        self.styles = styles
        self.other_colors = other_colors
        self.title = title

    def __repr__(self):
        return str(self.id) + " " + str(self.type)

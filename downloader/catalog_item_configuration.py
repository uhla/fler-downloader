class CustomizedCatalogItem:

    def __init__(self, id, type="", styles="", other_colors=""):
        self.id = id
        self.type = type
        self.styles = styles
        self.other_colors = other_colors

    def __repr__(self):
        return str(self.id) + " " + str(self.type)

    def set_image(self, image):
        self.image = image

    def set_title(self, title):
        self.title = title

    def set_image_url(self, image_url):
        self.image_url = image_url

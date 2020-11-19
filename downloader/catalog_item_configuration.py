class CatalogItemConfiguration:

    def __init__(self, id, internal_note=""):
        self.id = id
        self.internal_note = internal_note

    def __repr__(self):
        return str(self.id) + " " + str(self.internal_note)

    def set_image(self, image):
        self.image=image

    def set_title(self, title):
        self.title = title

    def set_image_url(self, image_url):
        self.image_url = image_url

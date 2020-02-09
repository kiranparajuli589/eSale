class Frobulator(object):
    def __init__(self, text=None):
        self.text = None
        self.activated = False

    def activate(self):
        self.activated = True

    def seems_like_language(self):
        """
        Business logic how frobulator should react/oracle on text data.
        """
        assert self.text is not None
        assert self.activated
        if self.text.startswith("Lorem ipsum"):
            return "English"
        else:
            return "UNKNOWN"

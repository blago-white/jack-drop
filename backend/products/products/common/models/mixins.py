class TitleModelMixin:
    title: str

    def __str__(self):
        return self.title

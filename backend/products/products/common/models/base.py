from abc import abstractmethod

from django.utils.html import escape, mark_safe

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(
            self, force_insert=False, force_update=False, using=None,
            update_fields=None
    ):
        self.full_clean()

        super().save(force_insert=force_insert,
                     force_update=force_update,
                     using=using,
                     update_fields=update_fields)

        return self


class BaseImageModel(models.Model):
    class Meta:
        abstract = True

    @abstractmethod
    def _get_image(self) -> models.URLField:
        pass

    def preview(self):
        return mark_safe(f'<img src="{escape(self._get_image())}" '
                         f'style=\"max-width: 500px;\"/>')

    def preview_short(self):
        return mark_safe(
            f"<img src=\"{escape(self._get_image())}\" style=\"width: 50px;\"/>"
        )

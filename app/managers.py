from django.db import models
from django.db.models.functions import Concat


class PersonManager(models.QuerySet):

    def annotate_full_name(self):

        return self.annotate(
            full_name=Concat(
                'first_name', models.Value(" "), 'last_name'
            )
        )

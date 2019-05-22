from import_export import resources
from .models import Item


class ExportExcel(resources.ModelResource):
    class Meta:
        model = Item
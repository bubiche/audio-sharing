from django.db.models import FileField


# Ref: https://stackoverflow.com/questions/32349635/django-migrations-and-filesystemstorage-depending-on-settings
class VariableStorageFileField(FileField):
    """
    Disregard the storage kwarg when creating migrations for this field
    """

    def deconstruct(self):
        name, path, args, kwargs = super(VariableStorageFileField, self).deconstruct()
        kwargs.pop('storage', None)
        return name, path, args, kwargs

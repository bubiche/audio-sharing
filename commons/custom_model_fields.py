from django.db.models import FileField


# Ref: https://stackoverflow.com/questions/32349635/django-migrations-and-filesystemstorage-depending-on-settings
# Don't use this anymore as I use the same thing (s3) to store files on both prod and dev now, just keep it for old migrations
class VariableStorageFileField(FileField):
    """
    Disregard the storage kwarg when creating migrations for this field
    """

    def deconstruct(self):
        name, path, args, kwargs = super(VariableStorageFileField, self).deconstruct()
        kwargs.pop('storage', None)
        return name, path, args, kwargs

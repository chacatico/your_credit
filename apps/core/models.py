from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that provides timestamp fields for all models.
    - created_at: Auto-set when the record is first created
    - updated_at: Auto-updated every time the record is saved
    - deleted_at: Used for soft deletes (null means not deleted)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        """Check if the record has been soft-deleted."""
        return self.deleted_at is not None

    def soft_delete(self):
        """Perform a soft delete by setting deleted_at to current time."""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

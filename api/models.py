from django.db import models


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    portal_response = models.JSONField(null=True, blank=True)  # store API response

    def __str__(self) -> str:
        return f"{self.text[:30]}... ({'delivered' if self.delivered else 'pending'})"

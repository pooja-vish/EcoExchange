from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('question', 'Question'),
        ('css', 'Feedback'),
        ('suggestion', 'Suggestion'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback_type.capitalize()}: {self.title}"

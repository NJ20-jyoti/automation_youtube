from django.db import models
import json

class Cookie(models.Model):
    email = models.EmailField(unique=True)  # Unique email for each account
    cookies = models.TextField()  # Store cookies as a JSON string

    def set_cookies(self, cookie_dict):
        """Set cookies in JSON format."""
        self.cookies = json.dumps(cookie_dict)

    def get_cookies(self):
        """Get cookies as a dictionary."""
        return json.loads(self.cookies)


# class UserKey(models.Model):
#     hardware_id = models.CharField(max_length=255, unique=True)
#     key = models.CharField(max_length=64)
#     expiration_date = models.DateTimeField()

#     def __str__(self):
#         return f"{self.hardware_id} - {self.key} (expires on {self.expiration_date})"

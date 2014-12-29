from django.db import models

class Attendance(models.Model):
    user_token = models.CharField(max_length=30)
    event_id = models.IntegerField()
    def __str__(self):
    	return '%s is attending %u' % (self.user_token, self.event_id)
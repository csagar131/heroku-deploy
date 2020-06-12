from django.db import models
# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length = 255,unique = True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    curr_status = [
        ('new','New'),('inprocess','InProcess'),('resolved','Resolved')
    ]
    priority_list = [
        ('low','Low'),('medium','Medium'),('high','High'),('urgent','Urgent'),
    ]
    subject = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    status = models.CharField(choices = curr_status,max_length=50)
    priority = models.CharField(choices = priority_list,max_length = 50)
    contact = models.EmailField()
    assignto = models.ForeignKey('useraccount.User',on_delete=models.CASCADE)
    createdby = models.ForeignKey('useraccount.User',on_delete= models.CASCADE,related_name = 'creator')
    creationdate = models.DateTimeField(auto_now_add=True)
    updationdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    pdf = models.FileField(blank=True,upload_to='bookapp/pdfs/')
    book_amount = models.IntegerField(default=0)
    publish_date = models.DateField(default=datetime.now())
    number_of_pages = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books", null=True)

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'
    
    # def delete(self, *args, **kwargs):
    #     self.pdf.delete()
    #     self.cover.delete()
    #     super().delete(*args, **kwargs)
    def read_pdf(self):
        with open(self.pdf.path, 'rb') as f:
            pdf_data = f.read()
        return pdf_data
    
    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)
        cover = Image.open(self.cover.path)

        if cover.height > 200 or cover.width > 200:
            output_size = (150, 300)
            cover.thumbnail(output_size)
            cover.save(self.cover.path)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(default='default.png',upload_to="profile_pics", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

def expiry():
    return datetime.today() + timedelta(days=14)
class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True) 
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)

#===========================================================================================================

from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User

class BookRentHistory(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, editable=False, related_name='books')
    rent_date = models.DateField(default=datetime.now().date(), editable=False)
    back_date = models.DateField(
        default=datetime.now().date()-timedelta(days=1))
    fine = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_returned_late = models.BooleanField(default=False)

    @property
    def how_many_days(self):
        return (self.back_date - timezone.now().date()).days

    # def save(self, *args, **kwargs):
    #     if self.how_many_days < 0:
    #         self.fine = abs(self.how_many_days) * 0.5
    #     else:
    #         self.fine = 0
    #     super().save(*args, **kwargs)
 
    @property
    def fine(self):
        return abs(self.how_many_days*0.5)
 
from django.db.models import Sum
from django.shortcuts import render
from .models import BookRentHistory

def student_fines(request):
    student = request.user.student
    rent_history = BookRentHistory.objects.filter(user=student)
    total_fines = rent_history.aggregate(Sum('fine'))['fine__sum']
    context = {'rent_history': rent_history, 'total_fines': total_fines}
    return render(request, 'student_fines.html', context)
       
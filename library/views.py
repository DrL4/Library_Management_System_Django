from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required

def index(request):
    books = Book.objects.all()
    return render(request, "index.html", {'books': books})

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        cover = request.FILES.get('cover')
        pdf = request.FILES.get('pdf')
        book_amount = request.POST['book_amount']
        number_of_pages = request.POST['number_of_pages']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category, pdf=pdf, book_amount=book_amount, number_of_pages=number_of_pages, cover=cover)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    return render(request, "add_book.html")

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form})

@login_required(login_url = '/admin_login')
# def view_issued_book(request):
#     issuedBooks = IssuedBook.objects.all()
#     details = []
#     for i in issuedBooks:
#         days = (date.today()-i.issued_date)
#         d=days.days
#         fine=0
#         if d>14:
#             day=d-14
#             fine=day*5
#         books = list(models.Book.objects.filter(isbn=i.isbn))
#         students = list(models.Student.objects.filter(user=i.student_id))
#         i=0
#         for l in books:
#             t=(students[i].user,students[i].user_id,books[i].name,books[i].isbn,issuedBooks[0].issued_date,issuedBooks[0].expiry_date,fine)
#             i=i+1
#             details.append(t)
#     return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.name,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*5
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request,'student_issued_books.html',{'li1':li1, 'li2':li2})

@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert})
    return render(request, "edit_profile.html")

import os

def delete_book(request, myid):
    book = Book.objects.get(id=myid)
    if book.cover:
        os.remove(book.cover.path)
    if book.pdf:
        os.remove(book.pdf.path)
    book.delete()
    return redirect("/view_books")


def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom,roll_no=roll_no, image=image)
        user.save()
        student.save()
        alert = True
        return render(request, "student_registration.html", {'alert':alert})
    return render(request, "student_registration.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect("/add_book")
            elif request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")


#============================================================

from django.shortcuts import render, get_object_or_404
from .models import Book
from django.contrib import messages
from django.http import Http404
from django.utils import timezone

def book_detail(request, id):
    books = Book.objects.filter(id=id)
    return render(request, 'book_detail.html', {'books': books})

@login_required(login_url='student_login')
def confirm_rent_view(request, id):
    try:
        b = Book.objects.get(id=id)
        if b.book_amount <= 0:
            messages.warning(
                request, f'You cant rent this book')
            return redirect('book_detail', id=b.id)
    except Book.DoesNotExist:
        raise Http404("We ont have this book")
    return render(request, 'confirm_rent_view.html', {'book': b})

@login_required(login_url='student_login')
def rent_book_view(request, id):
    try:
        b = Book.objects.get(id=id)
        if b:
            # Check if the user has rented more than 4 books
            rented_books_count = BookRentHistory.objects.filter(user=request.user).count()
            if rented_books_count >= 4:
                messages.warning(request, 'You have reached the maximum limit of book rentals.')
                return redirect('book_detail', id=b.id)
            
            if b.book_amount > 0:
                b.book_amount -= 1
                b.save()
                log_history = BookRentHistory(user=request.user, book=b)
                log_history.save()
                messages.success(request, f'You rented a book: {b.name}')
            else:
                messages.warning(request, 'You cannot rent this book as it is currently unavailable.')
                return redirect('book_detail', id=b.id)
    except Book.DoesNotExist:
        raise Http404("Book is unavailable")
    return redirect('profile')

@login_required(login_url='student_login')
def return_book_view(request, id):
    if not id:
        raise Http404("ID parameter is empty")
    
    try:
        book = Book.objects.get(id=id)
        book.book_amount += 1
        book.save()
        
        log_history = BookRentHistory.objects.filter(book=book).first()
        
        if log_history.back_date < timezone.now().date():
            messages.warning(request, f'You returned the book late: {book.name}')
        else:
            messages.success(request, f'You successfully returned a book: {book.name}')
        
        log_history.delete()
        
    except Book.DoesNotExist:
        raise Http404("Book is unavailable now")
    
    return redirect('profile')

@login_required(login_url='student_login')
def view_books_student(request):
    books = Book.objects.all()
    return render(request, "student_issued_books.html", {'books':books})


@login_required(login_url='/admin_login')
def view_issued_book(request):
    book_rent_history = BookRentHistory.objects.all()
    return render(request, 'view_issued_book.html', {'book_rent_history': book_rent_history})
  
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        updated_pdf = request.FILES.get('pdf')
        updated_cover = request.FILES.get('cover')
        book_amount = request.POST.get('amount')
        number_of_pages = request.POST.get('pages')
        book.name = name
        book.author = author
        book.isbn = isbn
        book.number_of_pages = number_of_pages
        book.category = category
        book.book_amount = book_amount
        if updated_pdf:
            book.pdf = updated_pdf
        if updated_cover:
            book.cover = updated_cover
        book.save()
        alert = True
        return render(request, "edit_book.html", {'book': book, 'alert': alert})
    return render(request, "edit_book.html", {'book': book})


from django.shortcuts import render, redirect
from .models import Category

def category_view(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        # Handle form submission for adding a new category
        title = request.POST.get('title')
        Category.objects.create(title=title)
        return redirect('category.html')

    return render(request, 'category.html', {'categories': categories})


def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        # Handle form submission for editing the category
        title = request.POST.get('title')
        category.title = title
        category.save()
        return redirect('category_view')

    return render(request, 'edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        # Handle form submission for deleting the category
        category.delete()
        return redirect('category_view')

    return render(request, 'delete_category.html', {'category': category})

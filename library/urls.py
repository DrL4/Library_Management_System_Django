from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
    
    #====================================================================================================
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('book/view_books_student/', views.view_books_student, name='view_books_student'),
    path('book/confirm_rent_view/<int:id>/', views.confirm_rent_view, name='confirm_rent_view'),
    path('book/rent_book_view/<int:id>/', views.rent_book_view, name='rent_book_view'),
    path('book/return_book_view/<int:id>/', views.return_book_view, name='return_book_view'),
    path('book/edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/category/', views.category_view, name='category_view'),
] 
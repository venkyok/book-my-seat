from django.urls import path
from . import views
from . import admin_views

urlpatterns=[
    path('',views.movie_list,name='movie_list'),
    path('<int:movie_id>/',views.movie_detail,name='movie_detail'),
    path('<int:movie_id>/theaters',views.theater_list,name='theater_list'),
    path('theater/<int:theater_id>/seats/book/',views.book_seats,name='book_seats'),
    path('payment/',views.payment_page,name='payment_page'),
    path('payment/process/',views.process_payment,name='process_payment'),
    path('payment/success/',views.payment_success,name='payment_success'),
    path('payment/failed/',views.payment_failed,name='payment_failed'),
    
    # Admin dashboard
    path('admin-dashboard/',admin_views.admin_dashboard,name='admin_dashboard'),
]
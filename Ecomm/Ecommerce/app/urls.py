from django.urls import path

from . import views 
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordChange,MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import user_logout   # <-- added


urlpatterns = [
    path('', views.home,name='home'),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('category/<slug:val>/',views.categoryView.as_view(),name="category"),

    path('category-title/<val>/',views.categoryView.as_view(),name="category-title"),
    path('category/<str:val>/', views.categoryView.as_view(), name='category'),

    path('product/<int:pk>/',views.ProductDetailView.as_view(),name="productdetails"),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
    path('cart/', views.show_cart, name='show_cart'),
    path('remove-cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('increase-cart/<int:id>/', views.increase_cart, name='increase_cart'),
    path('decrease-cart/<int:id>/', views.decrease_cart, name='decrease_cart'),
    path('update-cart/<int:id>/<str:action>/', views.update_cart, name='update_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),

    path('search/', views.search, name='search'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('registration/', views.CustomerRegistrationView.as_view(),name='customerregistration'),

    path('accounts/login/', auth_view.LoginView.as_view(
        template_name='app/login.html',
        authentication_form=LoginForm
    ), name='login'),

    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChange,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('profile/',views.ProfileView.as_view(),name='profile'),

    # ✔ fixed logout
    path('logout/', user_logout, name='logout'),

    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),

    path('placeorder/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),
    
    path('payment/', views.payment_page, name='payment_page'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
]

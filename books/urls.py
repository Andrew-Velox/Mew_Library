from django.urls import path
from .views import BookDetailsView,BuyBookView,BorrowReportView,ReturnBookView



urlpatterns = [
    path('details/<int:id>/', BookDetailsView.as_view(), name = 'details'),
    path('buy/<int:id>/', BuyBookView, name = 'buy'),
    path('borrow_report/', BorrowReportView.as_view(), name = 'borrow_report'),
    # path('review/<int:id>/', BookRatingView.as_view(), name = 'book_review'),
    path('return_book/<int:id>/', ReturnBookView, name = 'return_book'),

]

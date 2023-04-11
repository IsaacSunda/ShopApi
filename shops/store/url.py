from django.urls import path

from store.views import CategoryView, ProductView, CartView, CartItemView, TransactionView, OrderView, \
    CategoryUpdateView, ListCategoryView, ProductUpdateView, ListProductView, UpdateCartView, ListCartView, \
    UpdateCartItemView, ListCartItemView, UpdateTransactionView, ListTransactionView, UpdateOrderView, ListOrderView, \
    ReduceCartView, FetchCategoryProductView, GetItemCart

urlpatterns = [
    # category
    path('category/create', CategoryView.as_view()),
    path('category/update', CategoryUpdateView.as_view()),
    path('category/list', ListCategoryView.as_view()),
    path('category/product/<int:pk>', FetchCategoryProductView.as_view()),
    # product
    path('product/create', ProductView.as_view()),
    path('product/update/<int:pk>', ProductUpdateView.as_view()),
    path('product/list', ListProductView.as_view()),
    # cart
    path('cart/create', CartView.as_view()),
    path('cart/update/<int:pk>', UpdateCartView.as_view()),
    path('cart/list', ListCartView.as_view()),
    path('cart/reduce/<int:pk>', ReduceCartView.as_view()),
    # cart item
    path('cart/item/create', CartItemView.as_view()),
    path('cart/item/update/<int:pk>', UpdateCartItemView.as_view()),
    path('cart/item/list', ListCartItemView.as_view()),
    path('cart/item/fetch/<int:pk>', GetItemCart.as_view()),
    # transaction
    path('transaction/create', TransactionView.as_view()),
    path('transaction/update', UpdateTransactionView.as_view()),
    path('transaction/list', ListTransactionView.as_view()),
    # order
    path('order', OrderView.as_view()),
    path('order/update/<int:pk>', UpdateOrderView.as_view()),
    path('order/list', ListOrderView.as_view()),
]
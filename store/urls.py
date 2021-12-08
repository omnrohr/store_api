from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')
router.register('customers', views.CusermerViewSet, basename='customers')

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-review')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='carts')
carts_router.register('items', views.CartItemViewSet, basename='carts-item')

urlpatterns = router.urls + products_router.urls + carts_router.urls

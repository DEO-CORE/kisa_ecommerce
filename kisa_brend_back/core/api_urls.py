from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.api import views as catalog_views
from about.api import views as about_views
from journal.api import views as journal_views
from orders.api import views as orders_views
from footer.api import views as footer_views

from .views import SubscribeView, HealthView

router = DefaultRouter()

# Catalog
router.register(r'catalog/drops', catalog_views.DropViewSet, basename='drop')
router.register(r'catalog/products', catalog_views.ProductViewSet, basename='product')
router.register(r'catalog/colors', catalog_views.ColorViewSet, basename='color')
router.register(r'catalog/sizes', catalog_views.SizeViewSet, basename='size')
router.register(r'catalog/stocks', catalog_views.ProductSizeStockViewSet, basename='stock')

# About
router.register(r'about/principles', about_views.BrandPrincipleViewSet, basename='principle')
router.register(r'about/history', about_views.BrandHistoryViewSet, basename='history')

# Journal
router.register(r'journal/publications', journal_views.PublicationViewSet, basename='publication')

# Orders
router.register(r'orders', orders_views.OrderViewSet, basename='order')

# Footer
router.register(r'footer/info-pages', footer_views.InfoPageViewSet, basename='info-page')

urlpatterns = [
    path('health/', HealthView.as_view(), name='health'),
    path('newsletter/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('', include(router.urls)),
    # Singleton endpoints
    path('about/main-page/', about_views.MainPageSettingsView.as_view(), name='main-page-settings'),
    path('about/team/', about_views.TeamBlockView.as_view(), name='team-block'),
    path('footer/contacts/', footer_views.ContactsView.as_view(), name='contacts'),
    path('footer/partnership/', footer_views.PartnershipView.as_view(), name='partnership'),
    path('footer/support/', footer_views.SupportView.as_view(), name='support'),
    path('footer/site-settings/', footer_views.SiteSettingsView.as_view(), name='site-settings'),
]
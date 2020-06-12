from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ticket.views import TicketModelViewSet

ticket_router = DefaultRouter(trailing_slash=False)
ticket_router.register('ticket',TicketModelViewSet)


urlpatterns = [
    path('',include(ticket_router.urls)),
]
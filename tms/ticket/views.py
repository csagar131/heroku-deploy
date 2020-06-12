from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.http.response import JsonResponse
from rest_framework.authentication import TokenAuthentication
from ticket.models import Ticket
from ticket.serializer import TicketSerializer


class TicketModelViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
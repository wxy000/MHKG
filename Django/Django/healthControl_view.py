# -*- coding: utf-8 -*-

from django.shortcuts import render


def healthControl(request):
    return render(request, 'doctor/healthControl.html')

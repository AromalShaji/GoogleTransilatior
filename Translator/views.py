from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, date, timedelta
import datetime
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.contrib import messages
from flask import Flask, request, jsonify
from googletrans import Translator, LANGUAGES

#====================================================================================
#----------------------------------------home----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    languages = LANGUAGES
    return render(request,'base.html', {'languages': languages})


#====================================================================================
#----------------------------------------TRANSLATE----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def translate_text(request):
    if request.method == 'POST':
        text = request.POST.get("text")
        dest_lang = request.POST.get("dest_lang")
        
        # Check if text and dest_lang are present
        if text is None or dest_lang is None:
            return JsonResponse({"error": "Missing text or dest_lang parameters"}, status=400)
        
        translator = Translator()
        try:
            translated_text = translator.translate(text, dest=dest_lang).text
            return HttpResponse(translate_text)
            return JsonResponse({"translated_text": translated_text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, date, timedelta
import datetime
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.contrib import messages
import googletrans
from googletrans import Translator, LANGUAGES
import codecs
from django.contrib.auth.decorators import login_required
from .models import user, resultHistory, userFeedback
from datetime import datetime, date, timedelta
import datetime
from gtts import gTTS
import os
import random
import uuid
from django.conf import settings


#====================================================================================
#----------------------------------------home----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if 'id' in request.session:
        languages = LANGUAGES
        if request.method == 'POST':
            return render(request,'home.html', {'languages': languages})
        return render(request,'home.html', {'languages': languages})
    else:
        return redirect('login')

#====================================================================================
#----------------------------------------login----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        if (user.objects.filter(email=useremail, password=password)).exists():
            user_details = user.objects.get(email=useremail, password=password)
            request.session['id'] = user_details.id
            request.session['email'] = user_details.email
            messages.success(request, "Login Successfull")
            return redirect('home')
        else:
            messages.error(request, "Invalid Details!")
            return redirect('login')
    return render(request,'login.html')


#====================================================================================
#----------------------------------------register----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        if (user.objects.filter(email=useremail, password=password)).exists():
            messages.error(request, "Email Already Registred")
            return redirect('login')
        else:
            ob = user()
            ob.name = username
            ob.email = useremail
            ob.password = password
            ob.save()
            messages.success(request, "Registration Successfull")
        return redirect('login')
    return render(request,'register.html')


#=========================================================================================
#----------------------------------------TRANSLATE----------------------------------------
def translate_text(request):
        if 'id' in request.session:
            if request.method == 'POST':
                text = request.POST.get("textInput")
                dest_lang = request.POST.get("dest_lang")
                
                if text is None or dest_lang is None:
                    messages.error(request, "Missing text or dest_lang parameters")
                    return redirect('home')
                
                translator = Translator()
                try:
                    translated_text = translator.translate(text, dest=dest_lang)
                    if translated_text and hasattr(translated_text, 'text'):
                        language_name = LANGUAGES.get(dest_lang, 'Unknown Language')
                        ob = resultHistory()
                        ob.user_id = request.session['id']
                        ob.text = text
                        ob.result = translated_text.text
                        ob.date = datetime.datetime.now().strftime('%Y-%m-%d')
                        ob.language = language_name

                        tts = gTTS(text=translated_text.text, lang=dest_lang, slow=False)
                        audio_filename = f"audio_files/{uuid.uuid4()}.mp3"
                        audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
                        tts.save(audio_path)
                        ob.audio_file = audio_filename
                        ob.save()

                        messages.success(request, "Data Transilated")
                        return render(request,'result.html', {'input' : text, "translated_text": translated_text.text, 'code' : language_name, 'audio_filename' : audio_filename})
                except Exception as e:
                    messages.error(request, str(e))
                    return redirect('home')
            else:
                messages.error(request, "Method not allowed")
                return redirect('home')
        else:
            return redirect('login')
    

#====================================================================================
#----------------------------------------history----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def history(request):
    if 'id' in request.session:
        if request.method == 'POST':
            return redirect('home')
        if (resultHistory.objects.filter(user_id=request.session['id'])).exists():
            history = resultHistory.objects.filter(user_id=request.session['id'])
            return render(request,'history.html', {'histoy' : history})
        return redirect('home')
    else:
        return redirect('login')

#====================================================================================
#----------------------------------------delete----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def history_delete(request,id):
    if 'id' in request.session:
        if request.method == 'POST':
            resultHistory.objects.filter(id =id ,user_id=request.session['id']).delete()
            messages.error(request, "Deleted")
            return redirect('history')
        return redirect('history')
    else:
        return redirect('login')




#====================================================================================
#----------------------------------------feedback----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedback(request):
    if 'id' in request.session:
        if request.method == 'POST':
            textbody = request.POST.get("textbody")
            text = request.POST.get("content")
            ob = userFeedback()
            ob.user_id = request.session['id']
            ob.textbody = textbody
            ob.text = text
            ob.date = datetime.datetime.now().strftime('%Y-%m-%d')
            ob.save()
            messages.success(request, "Feedback Submitted")
            return redirect('home')
        return render(request,'feedback.html')
    else:
        return redirect('login')


#====================================================================================
#----------------------------------------Logout----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session.flush()
    messages.success(request, "Logout Successfull")
    return redirect('login')

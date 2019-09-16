import random
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Geo, movement, events, Profile, user_id, object_name, Push_ID
from django.contrib import auth
from django.contrib.auth.models import User
from pyfcm import FCMNotification
from threading import Thread
from django.core.mail import EmailMessage
from rocketchat.api import RocketChatAPI
from GeoServer.settings import GOOGLE_API_KEY, FROM_EMAIL, RC_USERNAME, RC_PASSWORD, RC_DOMAIN, MAIN_DOMAIN


# Create your views here.

def main(request):
    if request.GET.get('ID'):
        ID_API = request.GET.get('ID')
        if len(ID_API) < 12:
            ID_API = 'UNKNOWN'
        if request.method == 'GET' and Geo.objects.filter(
                ID_obj=ID_API).exists():  # and request.user.is_authenticated: #and request.user.is_authenticated:
            items = []
            lat = request.GET.get('lat')
            long = request.GET.get('long')
            #добавляем событие
            #mov = movement()
            #mov.ID_obj = Geo.objects.get(ID_obj=ID_API)
            # Используем старые события
            mov = movement.objects.get(ID_obj=Geo.objects.get(ID_obj=ID_API))
            mov.Latitude = lat
            mov.Longitude = long
            mov.save()
            #movement.objects.create(items)
            print(lat+' '+long)
            return JsonResponse({'ok': ID_API, 'success':True})
        else:
            return JsonResponse({'error': ID_API, 'success': False})
    else:
        return JsonResponse({'error': 'Unknown ID', 'success': False})

def event(request):
    if request.GET.get('ID'):
        ID_API = request.GET.get('ID')
        if len(ID_API) < 12:
            ID_API = 'UNKNOWN'
        if request.method == 'GET' and Geo.objects.filter(
                ID_obj=ID_API).exists():  # and request.user.is_authenticated: #and request.user.is_authenticated:
            items = []
            ev = request.GET.get('ev')
            dop = request.GET.get('dop')
            logic = (request.GET.get('logic')).capitalize()
            event = events()
            event.ID_obj = Geo.objects.get(ID_obj=ID_API)
            event.event = ev
            if ev == "up": # Добавляем ID устройства в базу, для PUSH уведомлений
                ID_PUSH=Push_ID()
                if Push_ID.objects.filter(ID_Push=dop).exists() == True:
                    print('Этот ID_Push уже имеется в системе')
                    #d = Push_ID.objects.get(ID_Push=dop)
                    #d.delete()
                else:
                    ID_PUSH.ID_Push=dop
                    #ID_PUSH.save()
                    p = Geo.objects.filter(ID_obj=ID_API).values("user")
                #print(str(p[0]['user']))
                    ID_PUSH.User = Profile.objects.get(pk=p[0]['user'])
                    ID_PUSH.save()

            else:
                if ev == "st":       # Отправляем PUSH на ID устройств о событии начало движения автомобиля
                    gcm_key = GOOGLE_API_KEY
                    title = "Авторадар"
                    #message = dop
                    p = Geo.objects.filter(ID_obj=ID_API).values("user", "name")
                    #name = Geo.objects.filter(ID_obj=ID_API).values("name")[:1]
                    print(p[0]['name'])
                    message = p[0]['name'] + ". "+dop

                    ID_PUSH = Push_ID.objects.filter(User = Profile.objects.get(pk=p[0]['user'])).values("ID_Push")
                    if (ID_PUSH.count() > 0) and (ID_PUSH.count() < 2):
                        device_token=ID_PUSH[0]["ID_Push"]
                        data=None
                        sound=None
                        badge=None
                        try:
                            t1 = Thread(target=push_to_fcm, args=(device_token, gcm_key, title, message, data, sound, badge,))
                            t1.start()
                            t1.join()
                        except:
                            print("Ошибка отправки PUSH")
                        print(device_token)
                    if ID_PUSH.count() > 1:
                        s = []
                        for e in ID_PUSH:
                            if e["ID_Push"] != '':
                                s.append(e["ID_Push"])
                                print(e["ID_Push"])
                        data = None
                        sound = None
                        badge = None
                        if len(s) > 1:
                            t1 = Thread(target=push_to_fcm_multy,
                                        args=(s, gcm_key, title, message, data, sound, badge,))
                        else:
                            device_token=ID_PUSH[0]["ID_Push"]
                            t1 = Thread(target=push_to_fcm,
                                        args=(device_token, gcm_key, title, message, data, sound, badge,))
                        try:
                            t1.start()
                            t1.join()
                        except:
                            print("Ошибка отправки PUSH")

                        print(s)
                else:
                    if ev == "dl":  #Удаляем PUSH_ID
                        ID_PUSH = Push_ID()
                        if Push_ID.objects.filter(ID_Push=dop).exists() == True:
                            d = Push_ID.objects.get(ID_Push=dop)
                            d.delete()
                    else:
                        event.dop = dop
                        event.logic = logic
                        event.save()

            return JsonResponse({'ok': ID_API, 'success':True})
        else:
            return JsonResponse({'error': ID_API, 'success': False})
    else:
        return JsonResponse({'error': "Unknown ID", 'success': False})

def monitor(request):
    if request.GET.get('ID'):
        ID_API = request.GET.get('ID')
        if len(ID_API) < 12:
            ID_API = 'UNKNOWN'
        if request.method == 'GET' and Geo.objects.filter(
                ID_obj=ID_API).exists():  # and request.user.is_authenticated: #and request.user.is_authenticated:
            items = []
            if str(request.user) == 'admin':
                APIs = Geo.objects.all()
            else:
                APIs = Geo.objects.filter(user=request.user.id)
            for aaa in APIs:
                #query = list(movement.objects.filter(ID_obj__name=aaa).values("Latitude", "Longitude",).order_by('-datetime')[:0])
                #query = list(Geo.objects.filter(movement__ID_obj=aaa)) #.values("Latitude", "Longitude",))
                query = list(movement.objects.filter(ID_obj=aaa).values("Latitude", "Longitude").order_by('-datetime')[:1])
                query2 = list(events.objects.filter(ID_obj=aaa).values("event", "dop","logic").order_by('-datetime')[:1])
                #print(aaa)
                #print(query)
                myDict = {"ID":str(aaa),"Value":{"movment":query,"events":query2},"Name": aaa.name, "Dop":aaa.dop}
                if aaa.ID_obj == ID_API:
                    center= query

                items.append(myDict)

            #print(items)
            return JsonResponse({'ok': ID_API,"Items":items,'center':center,'success':True})
        else:
            return JsonResponse({'error': ID_API, 'success': False})
    else:
        return JsonResponse({'error': 'Unknown ID', 'success': False})

def mobile(request):
    if request.method == 'GET' and request.user.is_authenticated:
        print('Авторизован')
        Counts = Geo.objects.filter(user=request.user).count()
        if Counts > 0:
            profile = Profile.objects.get(user=user_id(request.user))
            sel = object_name(profile.select)
            zoom = profile.zoom
            if str(request.user) == 'admin':
                APIs = Geo.objects.all()
            else:
                APIs = Geo.objects.filter(user=user_id(request.user))
            list1 = []
            center = []
            for aaa in APIs:
                s = list(
                    movement.objects.filter(ID_obj=aaa).values("ID_obj", "Latitude", "Longitude").order_by('-datetime')[
                    :1])
                list1.append({"Data": s, "Name": aaa.name, "Dop": aaa.dop, "ID": aaa.id, "ID_obj": aaa.ID_obj})
                if aaa.ID_obj == profile.select:
                    center.append({"center": s, "Name": aaa.name, "Dop": aaa.dop, "Phone": aaa.telephone})
                    ID = aaa.ID_obj

            # print(list1)
            # return render(request, "index.html", {movement.objects.filter(ID_obj=0).values("Latitude", "Longitude").order_by('-datetime')[:1]})
            if profile.active == True:
                return render(request, 'index.html',
                          {'list1': list1, 'center': center, 'zoom': zoom, 'user': auth.get_user(request),
                           'user_name': request.user.id, 'zoom': zoom, 'sel': sel, 'ID': ID})
            else:
                return render(request, "balance.html")
        else:
            return redirect("/edit/add/")

    else:
        if request.method == 'POST' and request.user.is_authenticated:
            sel= request.POST.get('select')
            zoom = request.POST.get('zoom')
            profile=Profile.objects.get(user=user_id(request.user))
            profile.zoom = zoom
            profile.select = sel
            profile.save()
            print('Сохранил настройки пользователя')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #остаёмся на той же странице
        else:
            print('Не авторизован')
            #return render(request, 'start.html')
            return redirect('/login/login')

def index(request):
    if request.method == 'GET' and request.user.is_authenticated:
        print('Авторизован')
        profile = Profile.objects.get(user=user_id(request.user))
        sel = object_name(profile.select)
        zoom = profile.zoom
        if str(request.user) == 'admin':
            APIs = Geo.objects.all()
        else:
            APIs = Geo.objects.filter(user = user_id(request.user))
        list1 = []
        center = []
        for aaa in APIs:
            s = list(
                movement.objects.filter(ID_obj=aaa).values("ID_obj", "Latitude", "Longitude").order_by('-datetime')[:1])
            list1.append({"Data": s, "Name": aaa.name, "Dop": aaa.dop, "ID": aaa.id, "ID_obj": aaa.ID_obj})
            if aaa.ID_obj == profile.select:
                center.append({"center": s, "Name": aaa.name, "Dop": aaa.dop, "Phone": aaa.telephone})
                ID=aaa.ID_obj

        print(list1)
        #return render(request, 'index.html', {'list1': list1, 'center':center, 'zoom' : zoom, 'user': auth.get_user(request), 'user_name': request.user.id,'zoom':zoom,'sel':sel, 'ID':ID})
        return redirect("/mobile/mobile", {'list1': list1, 'center':center, 'zoom' : zoom, 'user': auth.get_user(request), 'user_name': request.user.id,'zoom':zoom,'sel':sel, 'ID':ID})
    else:
        if request.method == 'POST' and request.user.is_authenticated:
            sel= request.POST.get('select')
            zoom = request.POST.get('zoom')
            profile=Profile.objects.get(user=user_id(request.user))
            profile.zoom = zoom
            profile.select = sel
            profile.save()
            print('Сохранил настройки пользователя')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #остаёмся на той же странице
        else:
            print('Не авторизован')
            return render(request, 'start.html')
            #return redirect('/login/login')
    #APIs = Geo.objects.all()
    #list1=[]
    #for aaa in APIs:
    #    s=list(movement.objects.filter(ID_obj=aaa).values("ID_obj", "Latitude", "Longitude").order_by('-datetime')[:1])
    #    list1.append({"Data":s,"Name":aaa.name, "Dop":aaa.dop, "ID":aaa.id, "ID_obj":aaa.ID_obj})

    #print(list1)
    #return render(request, "index.html", {movement.objects.filter(ID_obj=0).values("Latitude", "Longitude").order_by('-datetime')[:1]})
    #return render(request, 'index.html', {'list1': list1})


def view(request):
    if request.method == 'GET' and request.user.is_authenticated:
        if request.GET.get('ID'):
            profile = Profile.objects.get(user=user_id(request.user))
            sel = object_name(profile.select)
            zoom = profile.zoom
            ID = request.GET.get('ID')
            if str(request.user) == 'admin':
                APIs = Geo.objects.all()
            else:
                APIs = Geo.objects.filter(user=request.user.id)
            list1=[]
            center=[]
            for aaa in APIs:
                s = list(
                    movement.objects.filter(ID_obj=aaa).values("ID_obj", "Latitude", "Longitude").order_by('-datetime')[:1])
                list1.append({"Data": s, "Name": aaa.name, "Dop": aaa.dop, "ID": aaa.id, "ID_obj": aaa.ID_obj})
                if aaa.ID_obj == ID:
                    center.append({"center":s, "Name": aaa.name, "Dop": aaa.dop, "Phone":aaa.telephone})
                    ID = aaa.ID_obj
                #print(center)
    #print(list1)
    #return render(request, "index.html", {movement.objects.filter(ID_obj=0).values("Latitude", "Longitude").order_by('-datetime')[:1]})
            if profile.active == True:
                return render(request, 'main.html', {'list1': list1, 'center': center, 'zoom' : zoom, 'user': auth.get_user(request), 'user_name': request.user.id,'sel':sel, 'ID':ID})
            else:
                return render(request, "balance.html")

    else:
        print('Не авторизован')
        return redirect('/login/login')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', )
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            Counts=Geo.objects.filter(user=request.user).count()
            if Counts > 0:
                return redirect("/mobile/mobile")
            else:
                return redirect("/edit/add/")
        else:
            args = 'Пользователь с таким логином или паролем не найден'
            return render(request, 'login.html', {"args": args})

def login_mobile(request):
    if request.method == 'GET':
        return render(request, 'login_mobile.html', )
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            Counts=Geo.objects.filter(user=request.user).count()
            if Counts > 0:
                return redirect("/mobile/mobile")
            else:
                return redirect("/edit/add/")
        else:
            args = 'Пользователь с таким логином или паролем не найден'
            return render(request, 'login_mobile.html', {"args": args})

def logout(reguest):
    return_path = reguest.META.get('HTTP_REFERER','login/login') # При выходе с аккаунта остаемся на странице с которой вышли!
    auth.logout(reguest)
    #return redirect(return_path)
    return redirect("/")


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', )
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        #if check_passw(password) == False:
        #    args = 'Пароль должен содержать цифры и буквы на латинице!'
        #    return render(request, 'register.html', {"args": args})
        password2 = request.POST['password2']
        if User.objects.filter(email=email).exists() == True:
            args = 'Этот E-mail уже зарегистрирован в системе'
            return render(request, 'register.html', {"args": args})
        if User.objects.filter(username=username).exists() == True:
            args = 'Этот логин уже занят!'
            return render(request, 'register.html', {"args": args})

        if password == password2:
            userr = list(User.objects.filter(username=username))
            print(userr)
            if str(userr) == '[]':
                #user = User.objects.create_user(username=username, password=password, email=email)
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                if user is not None:
                    #print(request.user.is_authenticated())
                    email_user = EmailMessage(subject='Регистрация в системе Авторадар', body='Поздравляем! Вы зарегистрировались в системе Авторадар. Если Вы используете в авто Android, то введите ID ключ в программу Alarm Service в мультимедийной системе Вашего автомобиля. Ваш логин: '+username+' , пароль: '+ password, from_email=FROM_EMAIL, to=[email])
                    try:
                        email_user.send()
                    except:
                        print("Не удалось послать письмо вновь зарегистрированному пользователю!!!")
                    auth.login(request, user)
                    t2 = Thread(target=send_to_rocketchat, args=(username, email,))
                    try:
                          t2.start()
                          t2.join()

                    except:
                        print('Ошибка соединения с RocketChat')
                    return redirect("/add/add/")
                else:
                    print('Ошибка')
                    args = 'Ошибка'
                    return render(request, 'register.html', {"args": args})
            else:
                print('Пользователь с данным логином уже зарегистрирован')
                args = 'Пользователь с данным логином уже зарегистрирован'
                return render(request, 'register.html', {"args": args})

        else:
            args = 'Пароль не совпадает!'
            return render(request, 'register.html', {"args": args})

def register_mobile(request):
    if request.method == 'GET':
        return render(request, 'register_mobile.html', )
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        #if check_passw(password) == False:
        #    args = 'Пароль должен содержать цифры и буквы на латинице!'
        #    return render(request, 'register_mobile.html', {"args": args})
        password2 = request.POST['password2']
        if User.objects.filter(email=email).exists() == True:
            args = 'Этот E-mail уже зарегистрирован в системе'
            return render(request, 'register_mobile.html', {"args": args})
        if User.objects.filter(username=username).exists() == True:
            args = 'Этот логин уже занят!'
            return render(request, 'register_mobile.html', {"args": args})

        if password == password2:
            userr = list(User.objects.filter(username=username))
            print(userr)
            if str(userr) == '[]':
                #user = User.objects.create_user(username=username, password=password, email=email)
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                if user is not None:
                    #print(request.user.is_authenticated())
                    email_user = EmailMessage(subject='Регистрация в системе Авторадар', body='Поздравляем! Вы зарегистрировались в системе Авторадар. Если Вы используете в авто Android, то введите ID ключ в программу Alarm Service в мультимедийной системе Вашего автомобиля. Ваш логин: '+username+' , пароль: '+ password, from_email=FROM_EMAIL, to=[email])
                    try:
                        email_user.send()
                    except:
                        print("Не удалось послать письмо вновь зарегистрированному пользователю!!!")
                    auth.login(request, user)
                    t2 = Thread(target=send_to_rocketchat, args=(username, email,))
                    try:
                          t2.start()
                          t2.join()

                    except:
                        print('Ошибка соединения с RocketChat')
                    return redirect("/add/add/")
                else:
                    print('Ошибка')
                    args = 'Ошибка'
                    return render(request, 'register_mobile.html', {"args": args})
            else:
                print('Пользователь с данным логином уже зарегистрирован')
                args = 'Пользователь с данным логином уже зарегистрирован'
                return render(request, 'register_mobile.html', {"args": args})

        else:
            args = 'Пароль не совпадает!'
            return render(request, 'register_mobile.html', {"args": args})


def password(request):
    if request.method == 'GET' and request.user.is_authenticated:
        return render(request, 'password.html', {"info": ""})
    else:
        if request.method == 'POST' and request.user.is_authenticated:
            #old_password = request.POST['old_password']
            password = request.POST['password']
            password2 = request.POST['password2']
            user = User.objects.get(username=request.user)
            if (password == password2):
                #User.check_password(old_password, user.password)
                #user = User.objects.get(username=request.user)
                user.set_password(password)
                user.save()
                subject = 'Изменение пароля в личном кабинете системы Авторадар'
                body = 'Уважаемый пользователь системы Авторадар!'+'\n'+'Вы изменили пароль от личного кабинета системы. Ваш новый пароль: ' + password+'.\n'+'Если пароль был изменен не Вами, обратитесь в службу технической поддержки или напишите на почту '+FROM_EMAIL+'\n'+'С уважением, администрация системы Авторадар.'
                email = user.email
                t3 = Thread(target=send_email, args=(subject, body, email))
                try:
                    t3.start()
                    t3.join()

                except:
                    print('Ошибка запуска процесса отправки письма о смене пароля в ЛК')
                return render(request, 'password.html', {"info": "Пароль сохранен!"})
            else:
                return render(request, 'password.html', {"info": "Ошибка сохранения, попробуйте еще раз."})
        else:
            print("Ошибка 404")

def backup(request):
    if request.method == 'GET':
        return render(request, 'backup.html', {"info": ""})
    else:
        if request.method == 'POST':
            #old_password = request.POST['old_password']
            email = request.POST['email']
            if email != '':
                #User.check_password(old_password, user.password)
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    password = generate_pass()
                    user.set_password(password)
                    login = user.username
                    subject = 'Изменение пароля в личном кабинете системы Авторадар'
                    body = 'Уважаемый пользователь системы Авторадар!'+'\n'+'Вы изменили пароль от личного кабинета системы. Ваш логин: '+ login+'. Ваш новый пароль: ' + password+'.\n'+'Если пароль был изменен не Вами, обратитесь в службу технической поддержки или напишите на почту '+FROM_EMAIL+'\n'+'С уважением, администрация системы Авторадар.'\
                       +'\n'+MAIN_DOMAIN
                    email = user.email
                    t3 = Thread(target=send_email, args=(subject, body, email))
                    try:
                        t3.start()
                        t3.join()
                        user.save()

                    except:
                        print('Ошибка запуска процесса отправки письма о смене пароля в ЛК')
                    return render(request, 'backup.html', {"info": "Учетные данные отправлены!"})
                else:
                    print("Email не зарегистрирован!")
                    return render(request, 'backup.html', {"info": "Email не зарегистрирован!"})
            else:
                return render(request, 'backup.html', {"info": "Ошибка сохранения, попробуйте еще раз."})
        else:
            print("Ошибка 404")

def policy(request):
    return render(request, 'policy.html')

def edit(request):
    if request.method == 'GET' and request.user.is_authenticated:
        APIs = Geo.objects.filter(user=request.user.id)
        return render(request, 'edit.html', {"list1": APIs})
    if request.method == 'POST' and request.user.is_authenticated:
        #Obj=Geo.objects.create(ID_obj=request.POST['ID_obj'], name=request.POST['name'], dop=request.POST['opisanie'], admin=True, user=request.user)
        #Mov = movement.objects.create(ID_obj=Obj, Latitude="55.753960", Longitude="037.620393")
        #profile = Profile.objects.get(user=user_id(request.user))
        #profile.select =request.POST['ID_obj']
        #profile.save()
        return redirect("/")

def edit_mobile(request):
    if request.method == 'GET' and request.user.is_authenticated:
        APIs = Geo.objects.filter(user=request.user.id)
        return render(request, 'edit_mobile.html', {"list1": APIs})
    if request.method == 'POST' and request.user.is_authenticated:
        #Obj=Geo.objects.create(ID_obj=request.POST['ID_obj'], name=request.POST['name'], dop=request.POST['opisanie'], admin=True, user=request.user)
        #Mov = movement.objects.create(ID_obj=Obj, Latitude="55.753960", Longitude="037.620393")
        #profile = Profile.objects.get(user=user_id(request.user))
        #profile.select =request.POST['ID_obj']
        #profile.save()
        return redirect("/")



def add(request):
    if request.method == 'GET' and request.user.is_authenticated:
        psw = generate()
        ID_Obj = Geo.objects.filter(ID_obj=psw).exists()
        print(ID_Obj)
        while str(ID_Obj) == True:
            psw = generate()
            ID_Obj = Geo.objects.filter(ID_obj=psw).exists()
            print("ID объекта имеется в базе")

        return render(request, 'add.html',{'ID_obj': psw})
    if request.method == 'POST' and request.user.is_authenticated:
       Counts=Geo.objects.filter(user=request.user).count()
       print("Количество объектов: "+str(Counts))
       profile = Profile.objects.get(user=user_id(request.user))
       print("Макс установленное количество объектов: " + str(profile.maxobject))
       if Counts < profile.maxobject:
           Obj=Geo.objects.create(ID_obj=request.POST['ID_obj'], name=request.POST['name'], dop=request.POST['opisanie'], admin=True, user=request.user)
           Mov = movement.objects.create(ID_obj=Obj, Latitude="55.753960", Longitude="037.620393")
           #profile = Profile.objects.get(user=user_id(request.user))
           profile.select =request.POST['ID_obj']
           profile.save()
           username = request.user.username
           user = User.objects.get_by_natural_key(username=username)
           email_user = EmailMessage(subject='ID ключ дл Вашего Авторадара',
                                     body='ID ключ для Вашего авто: '+profile.select+'. Введите его в программу Авторадар (Alarm Service) в мультимедийной системе автомобиля',
                                     from_email= FROM_EMAIL, to=[user.email])
           try:
               email_user.send()
           except:
               print("Не удалось отправить послание вновь зарегистрированному пользователю!!!")
       return redirect("/mobile/mobile")

def generate():
    psw = ''  # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('1234567890QWERTYUIOPASDFGHJKLZXCVBNM'))
    return(psw)

def generate_pass():
    psw = ''  # предварительно создаем переменную psw
    for x in range(10):
        psw = psw + random.choice(list('1234567890QqWwEeRrTtYyUuIiOoPpAaSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm'))
    return(psw)

def own_clients(request):
    return movement.objects.filter(ID_obj__user=request.user.id).values("ID_obj", "Latitude", "Longitude").order_by('-datetime')[:1]


def check_passw(tested_string):
    pattern = r'^[QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm]+$'
    pattern2 = r'^[1234567890]+$'
    if  re.search(r"[A-Z]", tested_string):
        if re.search(r"[0-9]", tested_string):
            f = True
        else:
            f = False
    else:
        f = False


    #if (re.fullmatch(r'[0-9]*', tested_string)) and (re.fullmatch(r'[A-Z]*', tested_string)):
    #    f = True
    #else:
    #    f = False
    return f


def object(request):
    if request.method == 'GET' and request.user.is_authenticated:
        ID_VK = request.GET.get('ID')
        print(ID_VK)
        APIs = Geo.objects.get(ID_obj=ID_VK)
        profile = Profile.objects.get(user = APIs.user.id)
        return render(request, 'object.html',{"list1": APIs,'profile':profile})
    if request.method == 'POST' and request.user.is_authenticated:

        Obj=Geo.objects.get(ID_obj=request.POST['ID'])

        if "dell" in request.POST:
            #APIs = Geo.objects.get(ID_obj=ID_VK)
            #profile = Profile.objects.get(user=APIs.user.id)
            #profile.select =
            print("Удаляем объект!!!")
            #Obj.delete()
        else:
            Obj.name = request.POST['name']
            Obj.dop = request.POST['Message']
            Obj.telephone = request.POST['Phone']
            Obj.email  = request.POST['Email']
            Obj.save()
        #Mov = movement.objects.create(ID_obj=Obj, Latitude="55.753960", Longitude="037.620393")
        #profile = Profile.objects.get(user=user_id(request.user))
        #profile.select =request.POST['ID_obj']
        #profile.save()
        return redirect("/edit/edit/")

def object_mobile(request):
    if request.method == 'GET' and request.user.is_authenticated:
        ID_VK = request.GET.get('ID')
        print(ID_VK)
        APIs = Geo.objects.get(ID_obj=ID_VK)
        profile = Profile.objects.get(user = APIs.user.id)
        return render(request, 'object_mobile.html',{"list1": APIs,'profile':profile})
    if request.method == 'POST' and request.user.is_authenticated:

        Obj=Geo.objects.get(ID_obj=request.POST['ID'])

        if "dell" in request.POST:
            #APIs = Geo.objects.get(ID_obj=ID_VK)
            #profile = Profile.objects.get(user=APIs.user.id)
            #profile.select =
            print("Удаляем объект!!!")
            #Obj.delete()
        else:
            Obj.name = request.POST['name']
            Obj.dop = request.POST['Message']
            Obj.telephone = request.POST['Phone']
            Obj.email  = request.POST['Email']
            Obj.save()
        #Mov = movement.objects.create(ID_obj=Obj, Latitude="55.753960", Longitude="037.620393")
        #profile = Profile.objects.get(user=user_id(request.user))
        #profile.select =request.POST['ID_obj']
        #profile.save()
        return redirect("/edit_mobile/edit_mobile/")


def push_to_fcm(device_token, gcm_key, title=None, message=None, data=None, sound=None, badge=None):
    fcm_push_service = FCMNotification(api_key=gcm_key)
    fcm_push_service.notify_single_device(
        registration_id=device_token,
        message_title=title,
        message_body=message,
        data_message=data,
        sound=sound,
        badge=badge
    )

def push_to_fcm_multy(device_token, gcm_key, title=None, message=None, data=None, sound=None, badge=None):
    fcm_push_service = FCMNotification(api_key=gcm_key)
    fcm_push_service.notify_multiple_devices(
        registration_ids=device_token,
        message_title=title,
        message_body=message,
        data_message=data,
        sound=sound,
        badge=badge
    )

def send_to_rocketchat(username,email):
    api = RocketChatAPI(settings={'username': RC_USERNAME, 'password': RC_PASSWORD,
                                  'domain': RC_DOMAIN})
    try:
        api.send_message(
            'Зарегистрирован новый пользователь:' + username + ' , e-mail:' + email,
            'users')
    except:
        print('Rocket chat not work!')


def send_email(subject, body, email):
    email_user = EmailMessage(subject=subject,
                              body=body,
                              from_email= FROM_EMAIL, to=[email])
    try:
        email_user.send()
    except:
        print("Не удалось отправить письмо об изменении пароля ЛК!!!")

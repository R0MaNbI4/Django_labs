from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id = article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }

            if form["text"] and form["title"]:
                if not Article.objects.filter(title=form['title']):
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    article = Article.objects.get(title=form['title'])
                    return redirect('get_article', article_id=article.id)
                else:
                    form['errors'] = u"Статья с таким названием уже существует"
                    return render(request, 'create_post.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404

def registration(request):
    if request.method == "POST":
        form = {
            'login': request.POST["login"], 'password': request.POST["password"]
        }

        if form["login"] and form["password"]:
            if not User.objects.filter(username=form["login"]):
                User.objects.create_user(form["login"], "", form["password"])
                form['errors'] = u"Пользователь успешно зарегистрирован"
                return render(request, 'registration.html', {'form': form})
            else:
                form['errors'] = u"Пользователь с таким именем уже есть"
                return render(request, 'registration.html', {'form': form})
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'registration.html', {'form': form})
    else:
        return render(request, 'registration.html', {})

def auth(request):
    if request.method == "POST":
        form = {
            'login': request.POST["login"], 'password': request.POST["password"]
        }

        if form["login"] and form["password"]:
            user = authenticate(username=form["login"], password=form["password"])
            if user != None:
                login(request, user)
                form['info'] = u'Вы успешно авторизовались'
                return render(request, 'auth.html', {'form': form})
            else:
                form['errors'] = u'Пользователь с такими данными не найден'
                return render(request, 'auth.html', {'form': form})
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'auth.html', {'form': form})
    else:
        return render(request, 'auth.html', {})
from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import logging

from .forms import SignInForm, SignUpForm, RecipeForm
from .models import Recipe

logger = logging.getLogger(__name__)


def log_this(f):
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        logger.info(f'Func "{f.__name__}" was called')
        return res

    return wrapper


def get_random_recipe():
    count = Recipe.objects.filter(is_visible=True).count()
    random_index = randint(0, count - 1)
    random_recipe = Recipe.objects.all()[random_index]
    return random_recipe


@log_this
def index(request):
    number_of_cards = 5
    recipes = []
    count = Recipe.objects.filter(is_visible=True).count()
    if count == 0:
        return render(request, "recipebookapp/index.html")
    if count == 1:
        recipes = [Recipe.objects.all()[0]]
        return render(request, "recipebookapp/index.html", {'recipes': recipes})
    if 1 < count < number_of_cards:
        number_of_cards = count
    while len(recipes) < number_of_cards:
        recipe = get_random_recipe()
        if recipe not in recipes:
            recipes.append(recipe)
    return render(request, "recipebookapp/index.html", {'recipes': recipes})


@log_this
def user(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            reg_form = SignUpForm(request.POST)
            if reg_form.is_valid():
                reg_form.save()
                email = reg_form.cleaned_data['email']
                password = reg_form.cleaned_data['password1']
                user = authenticate(request, email=email, password=password)
                login(request, user)
                return redirect('/cooker')
            else:
                messages.error(request, 'Форма регистрации заполнена неверно')
        elif 'login' in request.POST:
            login_form = SignInForm(request.POST)
            if login_form.is_valid():
                if user := authenticate(request, **login_form.cleaned_data):
                    login(request, user)
                    return redirect('/cooker')
                messages.error(request, 'Ошибка авторизации')
            else:
                messages.error(request, 'Форма авторизации заполнена неверно')

    reg_form = SignUpForm()
    login_form = SignInForm()

    context = {
        'reg_form': reg_form,
        'login_form': login_form
    }
    return render(request, 'recipebookapp/user.html', context)


@log_this
@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


@log_this
@login_required
def cooker(request):
    recipes = Recipe.objects.filter(is_visible=True, author=request.user)
    return render(request, "recipebookapp/cooker.html", {'recipes': recipes})


@log_this
@login_required
def recipe_add(request):
    is_completed = False
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            cooking_steps = form.cleaned_data['cooking_steps']
            cooking_time = form.cleaned_data['cooking_time']
            image = form.cleaned_data['image']
            author = request.user
            category = form.cleaned_data['category']
            recipe = Recipe(title=title,
                            description=description,
                            cooking_steps=cooking_steps,
                            cooking_time=cooking_time,
                            image=image,
                            author=author,
                            category=category)
            recipe.save()
            is_completed = True
    else:
        is_completed = False
        form = RecipeForm()
    return render(request, 'recipebookapp/recipe_add.html',
                  {'form': form, 'is_completed': is_completed})


@log_this
@login_required
def recipe_edit(request, recipe_id):
    is_completed = False
    recipe = Recipe.objects.filter(pk=recipe_id).first()
    recipe_img = recipe.image
    if request.user != recipe.author:
        return redirect('/')
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe.title = form.cleaned_data['title']
            recipe.description = form.cleaned_data['description']
            recipe.cooking_steps = form.cleaned_data['cooking_steps']
            recipe.cooking_time = form.cleaned_data['cooking_time']
            recipe.category = form.cleaned_data['category']
            if form.cleaned_data['image'] is not None:
                recipe.image = form.cleaned_data['image']
            recipe.save()
            is_completed = True
    else:
        is_completed = False
        if recipe:
            data = {'title': recipe.title,
                    'description': recipe.description,
                    'cooking_steps': recipe.cooking_steps,
                    'cooking_time': recipe.cooking_time,
                    'category': recipe.category}
            if recipe.image is not None:
                recipe_img = recipe.image
            form = RecipeForm(data)
        else:
            form = RecipeForm()
    return render(request, 'recipebookapp/recipe_edit.html',
                  {'form': form,
                   'is_completed': is_completed,
                   'recipe_img': recipe_img,
                   'recipe': recipe})


@log_this
@login_required
def recipe_delete(request, recipe_id):
    recipe = Recipe.objects.filter(pk=recipe_id).first()
    if request.user != recipe.author:
        return redirect('/')
    if recipe:
        recipe.is_visible = False
        recipe.save()
    return redirect('/cooker')


@log_this
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    context = {
        'recipe': recipe
    }
    return render(request, 'recipebookapp/recipe_detail.html', context)


@log_this
def handler404(request, exception):
    return render(request, '404.html', status=404)


@log_this
def handler500(request):
    return render(request, '500.html', status=500)

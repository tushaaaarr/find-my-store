from django.shortcuts import render,HttpResponse,redirect
from .models import *
import json
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import auth

@login_required(login_url='login')
def home(request):
    if request.GET.get('ordering'):
        ORD = request.GET.get('ordering')
        recipes = Recipe.objects.filter(category =ORD).order_by("price")
        return render(request,'user/index.html',{'recipes':recipes,'ordering':ORD})
    else:
        recipes = Recipe.objects.all().order_by("price")
        return render(request,'user/index.html',{'recipes':recipes})


def login(request): 
    page_data = {}
    next = request.GET.get('next')
    if request.POST:
        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        if User.objects.filter(username=loginusername).exists():
            user = authenticate(username=loginusername, password=loginpassword)
            if user is not None:
                auth.login(request, user)
                if next is not None:
                    return redirect(next)
                else:
                    return redirect('/')
            else:
                page_data['error'] = 'Invalid credentials! Please try again'

        else:
            page_data['error'] = "Account Not Found.."

    return render(request, 'auth/login.html', {'page_data': page_data})

def logout(request):
    django_logout(request)
    return redirect('/login')

@login_required(login_url='login')
def add_recipe(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_merchant == True:
        if request.POST:
            image = request.FILES.get('recipe_image')
            food_name = request.POST.get('name')
            desc = request.POST.get('desc')
            category = request.POST.get('category')
            ingrediants = request.POST.getlist('ingredients')
            prices = request.POST.getlist('price')
            t_price = 50
            ingredient_list = list()
            for idx in range(len(ingrediants)):
                step_dict = {
                'ingredient':ingrediants[idx],
                'price':prices[idx]
                }
                ingredient_list.append(step_dict)

            # Automatically generate price based on ingredients (base price = 50 IR) 
            for price in prices:
                t_price = t_price + int(price)
            store_ob = Store.objects.get(user=request.user)
            new_recipe = Recipe(food_name = food_name, desc =desc,category =category,image = image,
                               ingredients = ingredient_list,price=t_price)   
            new_recipe.save()
        return render(request,'user/add_recipe.html')

    return HttpResponse('Merchant login required.....')
    

@login_required(login_url='login')
def search_recipe(request):  
    if request.is_ajax(): 
        q = request.GET.get('term', '').capitalize()
        search_name = Recipe.objects.filter(food_name__contains=q).order_by("price")
        search_ingredient = Recipe.objects.filter(category__contains=q).order_by("price")
        search_qs = list(search_name) + list(search_ingredient)
        results = []
        for r in search_qs:
            if r.food_name not in results:
                results.append(r.food_name)
        data = json.dumps(results)
        return HttpResponse(data)

    elif request.GET.get('query'):
        q = request.GET.get('query', '').capitalize()
        search_name = Recipe.objects.filter(food_name__startswith=q)
        recipes = []
        searched_recipe = search_name[0]
        item_ingredients = searched_recipe.ingredients
        ingredient_list = [idx['ingredient'] for idx in item_ingredients]    
        stores = DiscountSym.objects.all()

        for store in stores:
            store_ingredient_list = store.ingredients_discount

            # Updating amount with discount amount
            for ingredient in store_ingredient_list:
                try:
                    matched_idx = ingredient_list.index(ingredient['ingredient'])
                    discount_amount = int(item_ingredients[matched_idx]['price'])/100*int(ingredient['price'])
                    item_ingredients[matched_idx]['price'] = float(item_ingredients[matched_idx]['price']) - discount_amount
                except:
                    pass
                
            filtered_price = 0
            for price in item_ingredients:
                filtered_price = filtered_price + float(price['price'])  

            item_ingredients =  Recipe.objects.get(id=16).ingredients

            recipe_dict = {
                'food_name':searched_recipe.food_name,
                'user':store.user,
                'category':searched_recipe.category,
                'desc':searched_recipe.desc,
                'ingredients':searched_recipe.ingredients,
                'pub_date':searched_recipe.pub_date,
                'price':filtered_price,
                'image':searched_recipe.image,
                'id':searched_recipe.id
                }
            recipes.append(recipe_dict)
            
        # sort price low to high
        recipes.sort(key=lambda x: x["price"])
        return render(request,'user/index.html',{'recipes':recipes})
    


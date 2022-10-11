# FIND MY STORE

Live demo --- https://find-stores.herokuapp.com/


After Cloning project Follow below steps

run the following commands (on project base directory) 
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```


Run the following command to start Django Project
```
python manage.py runserver 
```

Login -- as a User
```
username - admin
password - admin
```

```
1) User can see all Recipe list with Orignal Prices. (Login Required).

2) Once user searched any Recipe name then user can see the set of stores that would cost minimum for a recipe (along with Store name). 

(Low to High based on Each store Discount amount for ingredients).

3) User can see  add/edit own recipes (Name, Category, Steps , Images, Ingredients and so on).

4)User can sort recipes with category.

5) Autosuggestion used (for Search bar)

```

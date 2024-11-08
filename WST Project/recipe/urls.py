from django.urls import path
from . import views

app_name = 'recipe'
urlpatterns = [
    path('create/', views.create_recipe, name="create_recipe"),
    #ETO NEED MONG AYUSIN NEIL!!!
    path('update/<int:recipe_primary_key>/', views.update_recipe, name="update_recipe"),
    path('delete/<int:recipe_primary_key>/', views.delete_recipe, name ="delete_recipe"),
    path('<int:recipe_primary_key>/ingredient/create/', views.create_ingredient, name='create_ingredient'),
    path('<int:recipe_primary_key>/ingredient/update/<int:ingredient_primary_key>/', views.update_ingredient, name='update_ingredient')
]
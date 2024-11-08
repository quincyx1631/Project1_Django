from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Category, Recipe, Ingredient, Instruction
from .forms import RecipeForm, IngredientForm, InstuctionForm

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully.')
        else:
            messages.error(request, 'Failed to create recipe.')
    else:
        form = RecipeForm()
    form = RecipeForm()
    return render(request, 'recipe/form.html', {
        'title': 'Create Recipe',
        'form': form, 
    })

@login_required
def update_recipe(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Dish updated successfully.")
        else:
            messages.error(request, "Failed to update the dish.")
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipe/form.html', {
        'title': "Update Recipe",
        'form': form
    })

@login_required
def delete_recipe(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    recipe.delete()
    
    messages.success(request, 'Recipe deleted successfully.')
    return redirect('main:home')

@login_required
def create_ingredient(request, recipe_primary_key):
    if request.method == 'POST':
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe_id = recipe_primary_key
            ingredient.save()

            messages.success(request, 'Ingredient created successfully.')
        else:
            messages.error(request, 'Failed to create ingredient.')
    else:
        form = IngredientForm()
    return render(request, 'recipe/form.html', {
        'title': 'Create Recipe Ingredient',
        'form': form,
    })

@login_required
def update_ingredient(request, recipe_primary_key, ingredient_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_primary_key, recipe=recipe)

    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingredient updated successfully.")
        else:
            messages.error(request, "Failed to update the Ingredient.")
    else:
         form = IngredientForm(instance=ingredient)
    return render(request, 'recipe/form.html', {
        'title': 'Update Recipe Ingredient',
        'form': form,
    })
#views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import Category, Recipe, Ingredient, Instruction
from .forms import RecipeForm, IngredientForm, InstructionForm

@login_required
def view_user_recipes(request):
    recipes = Recipe.objects.filter(created_by=request.user)
    return render(request, 'recipe/view_user_recipes.html', {
        'recipe': 'My Recipes',
        'recipes': recipes,
    })

@login_required
def view_recipes(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    recipes = Recipe.objects.all()

    if category_id:
        recipes = recipes.filter(category_id=category_id)

    if query:
        recipes = recipes.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'recipe/view_recipes.html', {
        'title': 'Recipes',
        'recipes': recipes,
        'categories': categories,
    })

@login_required
def view_recipe_detail(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
    instructions = Instruction.objects.filter(recipe_id=recipe_primary_key)
    return render(request, 'recipe/view_recipe_detail.html', {
        'title': 'Recipe Detail',
        'recipe': recipe,
        'ingredients': ingredients,
        'instructions': instructions,
    })

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
            messages.success(request, "Recipe updated successfully.")
            return redirect('recipe:view_recipe_detail', recipe_primary_key=recipe_primary_key)
        else:
            messages.error(request, "Failed to update the recipe.")
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipe/form.html', {
        'title': "Update Recipe",
        'form': form,
        'recipe': recipe
    })

@login_required
def delete_recipe(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    recipe.delete()
    
    messages.success(request, 'Recipe deleted successfully.')
    return redirect('main:home')

@login_required
def create_ingredient(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    
    if request.method == 'POST':
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe_id = recipe_primary_key
            ingredient.save()

            messages.success(request, 'Ingredient created successfully.')
            return redirect('recipe:view_recipe_detail', recipe_primary_key=recipe_primary_key)
        else:
            messages.error(request, 'Failed to create ingredient.')
    else:
        form = IngredientForm()
    
    return render(request, 'recipe/form.html', {
        'title': 'Create Recipe Ingredient',
        'form': form,
        'recipe': recipe  # Pass recipe to the template for the cancel button
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
            
            # Get fresh data for rendering
            recipe = get_object_or_404(Recipe, pk=recipe_primary_key)
            ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
            instructions = Instruction.objects.filter(recipe_id=recipe_primary_key)
            
            return render(request, 'recipe/view_recipe_detail.html', {
                'title': 'Recipe Detail',
                'recipe': recipe,
                'ingredients': ingredients,
                'instructions': instructions,
            })
        else:
            messages.error(request, "Failed to update the Ingredient.")
    
    # If GET request or form invalid, show the form
    form = IngredientForm(instance=ingredient)
    return render(request, 'recipe/form.html', {
        'title': 'Update Recipe Ingredient',
        'form': form,
    })

def delete_ingredient(request, recipe_primary_key, ingredient_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_primary_key, recipe=recipe)
    ingredient.delete()
    
    messages.success(request, 'Ingredient deleted successfully.')
    
    # Get fresh data for rendering
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
    instructions = Instruction.objects.filter(recipe_id=recipe_primary_key)
    return render(request, 'recipe/view_recipe_detail.html', {
        'title': 'Recipe Detail',
        'recipe': recipe,
        'ingredients': ingredients,
        'instructions': instructions,
    })


@login_required
def create_instruction(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    
    if request.method == 'POST':
        form = InstructionForm(request.POST)
        if form.is_valid():
            instruction = form.save(commit=False)
            instruction.recipe = recipe
            
            # Get the last step number for this recipe
            last_instruction = Instruction.objects.filter(recipe=recipe).order_by('-step_number').first()
            
            # Set step number to 1 if no instructions exist, otherwise increment the last step number
            instruction.step_number = (last_instruction.step_number + 1) if last_instruction else 1
            instruction.save()
            
            messages.success(request, 'Instruction created successfully.')
            
            # Get fresh data for rendering
            recipe = get_object_or_404(Recipe, pk=recipe_primary_key)
            ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
            instructions = Instruction.objects.filter(recipe_id=recipe_primary_key).order_by('step_number')
            
            return render(request, 'recipe/view_recipe_detail.html', {
                'title': 'Recipe Detail',
                'recipe': recipe,
                'ingredients': ingredients,
                'instructions': instructions,
            })
        else:
            messages.error(request, 'Failed to create instruction.')
    else:
        # Get the next available step number
        last_instruction = Instruction.objects.filter(recipe=recipe).order_by('-step_number').first()
        next_step = (last_instruction.step_number + 1) if last_instruction else 1
        form = InstructionForm(initial={'step_number': next_step})
    
    return render(request, 'recipe/form.html', {
        'title': 'Create Recipe Instruction',
        'form': form,
        'recipe': recipe
    })

@login_required
def update_instruction(request, recipe_primary_key, instruction_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    instruction = get_object_or_404(Instruction, pk=instruction_primary_key, recipe=recipe)
    
    if request.method == 'POST':
        form = InstructionForm(request.POST, instance=instruction)
        if form.is_valid():
            new_step_number = form.cleaned_data['step_number']
            
            # Check if the step number exists for any other instruction in this recipe
            existing_step = Instruction.objects.filter(
                recipe=recipe,
                step_number=new_step_number
            ).exclude(pk=instruction_primary_key).first()
            
            if existing_step:
                messages.error(request, f"Step number {new_step_number} already exists. Please choose a different step number.")
                return render(request, 'recipe/form.html', {
                    'title': 'Update Recipe Instruction',
                    'form': form,
                })
            
            form.save()
            messages.success(request, "Instruction updated successfully.")
            
            # Get fresh data for rendering
            recipe = get_object_or_404(Recipe, pk=recipe_primary_key)
            ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
            instructions = Instruction.objects.filter(recipe_id=recipe_primary_key)
            
            return render(request, 'recipe/view_recipe_detail.html', {
                'title': 'Recipe Detail',
                'recipe': recipe,
                'ingredients': ingredients,
                'instructions': instructions,
            })
        else:
            messages.error(request, "Failed to update the instruction.")
    
    # If GET request or form invalid, show the form
    form = InstructionForm(instance=instruction)
    return render(request, 'recipe/form.html', {
        'title': 'Update Recipe Instruction',
        'form': form,
    })

@login_required
def delete_instruction(request, recipe_primary_key, instruction_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    instruction = get_object_or_404(Instruction, pk=instruction_primary_key, recipe=recipe)
    
    # Get the deleted step number
    deleted_step_number = instruction.step_number
    instruction.delete()
    
    # Reorder remaining steps if needed
    remaining_instructions = Instruction.objects.filter(
        recipe=recipe,
        step_number__gt=deleted_step_number
    ).order_by('step_number')
    
    # Decrease step numbers for all steps after the deleted one
    for remaining_instruction in remaining_instructions:
        remaining_instruction.step_number -= 1
        remaining_instruction.save()
    
    messages.success(request, 'Instruction deleted successfully.')
    
    # Get fresh data for rendering
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
    instructions = Instruction.objects.filter(recipe_id=recipe_primary_key)
    
    return render(request, 'recipe/view_recipe_detail.html', {
        'title': 'Recipe Detail',
        'recipe': recipe,
        'ingredients': ingredients,
        'instructions': instructions,
    })

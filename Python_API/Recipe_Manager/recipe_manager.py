'''
Recipe Management System - Sistema di Gestione Ricette Culinarie

Sistema OOP per gestire ricette con calcolo calorie, tempo di preparazione e ingredienti.

Funzionalità:
  • Gestione ricette con ingredienti e calorie
  • Calcolo automatico calorie totali
  • Stima tempo di preparazione
  • Analisi nutrizionale
  • Validazione ingredienti
  • Report dettagliati

Uso:
    from recipe_manager import Dessert, MainDish, recipe_analyzer
    
    tiramisu = Dessert(
        ingredients=['Mascarpone', 'Uova', 'Savoiardi', 'Caffè'],
        calories_per_ingredient=[450, 155, 380, 2]
    )
    print(recipe_analyzer(tiramisu))

API Endpoints (opzionale):
    POST /api/recipes              - Crea nuova ricetta
    GET  /api/recipes/<id>         - Ottieni ricetta
    GET  /api/recipes/<id>/analyze - Analizza ricetta

Autore: Recipe Management Team
License: MIT
'''

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass


# ============================================================================
# Classe Base Astratta: Recipe
# ============================================================================

class Recipe(ABC):
    """
    Classe astratta base per ricette culinarie.
    
    Attributes:
        type (str): Tipo di ricetta (definito nelle sottoclassi)
    """
    type: str
    
    def __init__(self, ingredients: List[str], 
                 calories_per_ingredient: List[float],
                 name: str = "Unnamed Recipe"):
        """
        Inizializza una ricetta.
        
        Args:
            ingredients: Lista nomi ingredienti
            calories_per_ingredient: Lista calorie per ogni ingrediente
            name: Nome della ricetta
        
        Raises:
            TypeError: Se gli argomenti non sono del tipo corretto
            ValueError: Se le liste hanno lunghezze diverse o valori non validi
        """
        # Validazione tipo
        if not isinstance(ingredients, list) or not isinstance(calories_per_ingredient, list):
            raise TypeError("ingredients and calories_per_ingredient must be lists")
        
        # Validazione lunghezza
        if len(ingredients) != len(calories_per_ingredient):
            raise ValueError(
                f"Mismatch: {len(ingredients)} ingredients but "
                f"{len(calories_per_ingredient)} calorie values"
            )
        
        # Validazione ingredienti non vuoti
        if not ingredients:
            raise ValueError("Recipe must have at least one ingredient")
        
        # Validazione calorie positive
        if any(cal < 0 for cal in calories_per_ingredient):
            raise ValueError("Calories cannot be negative")
        
        self.ingredients = ingredients
        self.calories_per_ingredient = calories_per_ingredient
        self.name = name
    
    def __init_subclass__(cls):
        """Validazione attributi obbligatori nelle sottoclassi"""
        if not hasattr(cls, "type"):
            raise AttributeError(
                f"Cannot create '{cls.__name__}' class: missing required attribute 'type'"
            )
    
    def __str__(self):
        """Rappresentazione stringa della ricetta"""
        return f"{self.name} ({self.type})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', ingredients={len(self.ingredients)})"
    
    @abstractmethod
    def total_calories(self) -> float:
        """
        Calcola le calorie totali della ricetta.
        
        Returns:
            float: Calorie totali
        """
        pass
    
    @abstractmethod
    def prep_time(self) -> int:
        """
        Calcola il tempo di preparazione stimato.
        
        Returns:
            int: Tempo in minuti
        """
        pass
    
    def get_ingredient_details(self) -> List[Dict]:
        """
        Ottieni dettagli di tutti gli ingredienti.
        
        Returns:
            list: Lista di dizionari con ingrediente e calorie
        """
        return [
            {
                'ingredient': ing,
                'calories': cal,
                'percentage': (cal / self.total_calories() * 100)
            }
            for ing, cal in zip(self.ingredients, self.calories_per_ingredient)
        ]
    
    def analyze(self) -> Dict:
        """
        Analisi completa della ricetta.
        
        Returns:
            dict: Dizionario con tutte le metriche
        """
        total_cal = self.total_calories()
        
        return {
            'name': self.name,
            'type': self.type,
            'ingredients_count': len(self.ingredients),
            'total_calories': total_cal,
            'prep_time_minutes': self.prep_time(),
            'calories_per_serving': total_cal / 4,  # assume 4 porzioni
            'high_calorie_ingredients': [
                ing for ing, cal in zip(self.ingredients, self.calories_per_ingredient)
                if cal > total_cal * 0.3  # ingredienti >30% del totale
            ]
        }


# ============================================================================
# Ricette Concrete
# ============================================================================

class Dessert(Recipe):
    """
    Ricetta per dolci.
    
    Tempo base: 30 minuti + 10 minuti per ingrediente
    """
    type = "Dessert"
    base_prep_time = 30  # minuti
    
    def total_calories(self) -> float:
        """Somma calorie di tutti gli ingredienti"""
        return sum(self.calories_per_ingredient)
    
    def prep_time(self) -> int:
        """Tempo base + 10 minuti per ingrediente (lavorazione complessa)"""
        return self.base_prep_time + 10 * len(self.ingredients)


class MainDish(Recipe):
    """
    Ricetta per piatti principali.
    
    Tempo base: 45 minuti + 5 minuti per ingrediente
    """
    type = "Main Dish"
    base_prep_time = 45  # minuti
    
    def total_calories(self) -> float:
        """Somma calorie di tutti gli ingredienti"""
        return sum(self.calories_per_ingredient)
    
    def prep_time(self) -> int:
        """Tempo base + 5 minuti per ingrediente"""
        return self.base_prep_time + 5 * len(self.ingredients)


class Appetizer(Recipe):
    """
    Ricetta per antipasti.
    
    Tempo base: 15 minuti + 3 minuti per ingrediente
    """
    type = "Appetizer"
    base_prep_time = 15
    
    def total_calories(self) -> float:
        return sum(self.calories_per_ingredient)
    
    def prep_time(self) -> int:
        """Preparazione più veloce"""
        return self.base_prep_time + 3 * len(self.ingredients)


class Salad(Recipe):
    """
    Ricetta per insalate.
    
    Tempo base: 10 minuti + 2 minuti per ingrediente
    """
    type = "Salad"
    base_prep_time = 10
    
    def total_calories(self) -> float:
        return sum(self.calories_per_ingredient)
    
    def prep_time(self) -> int:
        """Preparazione velocissima"""
        return self.base_prep_time + 2 * len(self.ingredients)


# ============================================================================
# Analizzatore Ricette
# ============================================================================

def recipe_analyzer(recipe: Recipe) -> str:
    """
    Analizza una ricetta e produce un report dettagliato.
    
    Args:
        recipe: Istanza di una ricetta
    
    Returns:
        str: Report formattato
    
    Raises:
        TypeError: Se l'argomento non è una Recipe
    """
    if not isinstance(recipe, Recipe):
        raise TypeError("Argument must be a Recipe object")
    
    # Header
    output = f'\n{recipe.type:-^60}\n'
    output += f'{recipe.name:^60}\n'
    output += f'{"-" * 60}\n\n'
    
    # Informazioni base
    output += f'{"INFORMAZIONI GENERALI":-^60}\n\n'
    output += f'{"Numero ingredienti:":<30} {len(recipe.ingredients):>29}\n'
    
    prep_time = recipe.prep_time()
    hours, mins = divmod(prep_time, 60)
    if hours > 0:
        time_str = f"{hours}h {mins}min"
    else:
        time_str = f"{mins} min"
    output += f'{"Tempo preparazione:":<30} {time_str:>29}\n'
    
    # Calorie
    total_cal = recipe.total_calories()
    output += f'\n{"INFORMAZIONI NUTRIZIONALI":-^60}\n\n'
    output += f'{"Calorie totali:":<30} {total_cal:>24.0f} kcal\n'
    output += f'{"Calorie per porzione (4):":<30} {total_cal/4:>24.0f} kcal\n'
    
    # Classificazione calorica
    output += f'{"Classificazione:":<30}'
    if total_cal < 300:
        output += f'{"⭐ Leggera":>29}\n'
    elif total_cal < 600:
        output += f'{"⭐⭐ Moderata":>29}\n'
    elif total_cal < 900:
        output += f'{"⭐⭐⭐ Sostanziosa":>29}\n'
    else:
        output += f'{"⭐⭐⭐⭐ Molto calorica":>29}\n'
    
    # Dettagli ingredienti
    output += f'\n{"INGREDIENTI":-^60}\n\n'
    output += f'{"Ingrediente":<25} {"Calorie":>15} {"% Totale":>15}\n'
    output += f'{"-" * 60}\n'
    
    for detail in recipe.get_ingredient_details():
        output += f'{detail["ingredient"]:<25} '
        output += f'{detail["calories"]:>15.0f} '
        output += f'{detail["percentage"]:>14.1f}%\n'
    
    # Suggerimenti
    output += f'\n{"SUGGERIMENTI":-^60}\n\n'
    
    analysis = recipe.analyze()
    if analysis['high_calorie_ingredients']:
        output += f'⚠️  Ingredienti ad alto contenuto calorico:\n'
        for ing in analysis['high_calorie_ingredients']:
            output += f'   • {ing}\n'
    
    # Livello difficoltà basato su tempo
    if prep_time < 20:
        difficulty = "Facile 👍"
    elif prep_time < 45:
        difficulty = "Media 👌"
    else:
        difficulty = "Complessa 🔥"
    
    output += f'\n{"Difficoltà stimata:":<30} {difficulty:>29}\n'
    
    output += f'\n{"-" * 60}\n'
    
    return output


def compare_recipes(recipes: List[Recipe]) -> str:
    """
    Confronta multiple ricette.
    
    Args:
        recipes: Lista di ricette da confrontare
    
    Returns:
        str: Tabella comparativa
    """
    if not recipes:
        return "Nessuna ricetta da confrontare"
    
    output = f'\n{"CONFRONTO RICETTE":=^80}\n\n'
    
    # Header tabella
    output += f'{"Nome":<25} {"Tipo":<15} {"Cal":<10} {"Tempo (min)":<15} {"Ingredienti"}\n'
    output += f'{"-" * 80}\n'
    
    # Righe ricette
    for r in recipes:
        output += f'{r.name:<25} {r.type:<15} '
        output += f'{r.total_calories():<10.0f} {r.prep_time():<15} '
        output += f'{len(r.ingredients)}\n'
    
    output += f'{"-" * 80}\n'
    
    # Raccomandazioni
    output += f'\n{"RACCOMANDAZIONI":-^80}\n\n'
    
    lightest = min(recipes, key=lambda r: r.total_calories())
    output += f'🥗 Più leggera: {lightest.name} ({lightest.total_calories():.0f} kcal)\n'
    
    fastest = min(recipes, key=lambda r: r.prep_time())
    output += f'⚡ Più veloce: {fastest.name} ({fastest.prep_time()} min)\n'
    
    simplest = min(recipes, key=lambda r: len(r.ingredients))
    output += f'👍 Più semplice: {simplest.name} ({len(simplest.ingredients)} ingredienti)\n'
    
    output += f'\n{"=" * 80}\n'
    
    return output


# ============================================================================
# Esempi e Demo
# ============================================================================

def run_examples():
    """Esegue esempi dimostrativi"""
    
    print("=" * 70)
    print("RECIPE MANAGEMENT SYSTEM - Gestione Ricette Culinarie")
    print("=" * 70)
    
    # Esempio 1: Tiramisù (Dessert)
    tiramisu = Dessert(
        name="Tiramisù Classico",
        ingredients=['Mascarpone', 'Uova', 'Savoiardi', 'Caffè', 'Cacao'],
        calories_per_ingredient=[450, 155, 380, 2, 12]
    )
    
    print(recipe_analyzer(tiramisu))
    
    # Esempio 2: Carbonara (Main Dish)
    carbonara = MainDish(
        name="Pasta alla Carbonara",
        ingredients=['Pasta', 'Guanciale', 'Uova', 'Pecorino', 'Pepe'],
        calories_per_ingredient=[350, 420, 155, 400, 5]
    )
    
    print(recipe_analyzer(carbonara))
    
    # Esempio 3: Insalata Caprese (Salad)
    caprese = Salad(
        name="Insalata Caprese",
        ingredients=['Pomodori', 'Mozzarella', 'Basilico', 'Olio'],
        calories_per_ingredient=[20, 280, 1, 120]
    )
    
    print(recipe_analyzer(caprese))
    
    # Confronto
    recipes = [tiramisu, carbonara, caprese]
    print(compare_recipes(recipes))


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    run_examples()

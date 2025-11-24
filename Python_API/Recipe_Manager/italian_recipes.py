import sys
sys.path.append('..')

from recipe_manager import Dessert, MainDish, Appetizer, compare_recipes

# Ricette italiane famose
tiramisu = Dessert(
    name="Tiramisù",
    ingredients=['Mascarpone', 'Uova', 'Savoiardi', 'Caffè', 'Cacao'],
    calories_per_ingredient=[450, 155, 380, 2, 12]
)

carbonara = MainDish(
    name="Carbonara",
    ingredients=['Pasta', 'Guanciale', 'Uova', 'Pecorino', 'Pepe'],
    calories_per_ingredient=[350, 420, 155, 400, 5]
)

bruschetta = Appetizer(
    name="Bruschetta",
    ingredients=['Pane', 'Pomodori', 'Aglio', 'Basilico', 'Olio'],
    calories_per_ingredient=[120, 20, 4, 1, 120]
)

# Confronta
print(compare_recipes([tiramisu, carbonara, bruschetta]))

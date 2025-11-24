# 🍳 Recipe Management System

Sistema OOP per gestire ricette culinarie con calcolo automatico di calorie e tempo di preparazione.

## 🎯 Funzionalità

- ✅ Gestione ricette con ingredienti
- ✅ Calcolo automatico calorie totali
- ✅ Stima tempo preparazione
- ✅ Analisi nutrizionale dettagliata
- ✅ Confronto multiplo ricette
- ✅ Validazione robusta input
- ✅ Report formattati

## 📦 Installazione

Nessuna dipendenza esterna richiesta! Solo Python 3.7+
```bash
# Clona il repository
git clone https://github.com/tuo-username/Python_API.git
cd Python_API/Recipe_Manager
```

## 🚀 Uso Rapido
```python
from recipe_manager import Dessert, MainDish, recipe_analyzer

# Crea una ricetta
tiramisu = Dessert(
    name="Tiramisù Classico",
    ingredients=['Mascarpone', 'Uova', 'Savoiardi', 'Caffè'],
    calories_per_ingredient=[450, 155, 380, 2]
)

# Analizza
print(recipe_analyzer(tiramisu))

# Output:
# ---------------------------Dessert---------------------------
#                    Tiramisù Classico                        
# -------------------------------------------------------------
# 
# INFORMAZIONI GENERALI
# Numero ingredienti:                                        4
# Tempo preparazione:                                   70 min
# 
# INFORMAZIONI NUTRIZIONALI
# Calorie totali:                                     987 kcal
# Calorie per porzione (4):                           247 kcal
```

## 📊 Tipi di Ricette

| Classe | Tipo | Tempo Base | Incremento/Ingrediente |
|--------|------|------------|------------------------|
| `Dessert` | Dolci | 30 min | +10 min |
| `MainDish` | Piatti principali | 45 min | +5 min |
| `Appetizer` | Antipasti | 15 min | +3 min |
| `Salad` | Insalate | 10 min | +2 min |

## 🔍 Esempi

### Confronto ricette
```python
from recipe_manager import compare_recipes

recipes = [tiramisu, carbonara, caprese]
print(compare_recipes(recipes))
```

### Analisi nutrizionale
```python
# Ottieni dettagli ingredienti
details = tiramisu.get_ingredient_details()
for d in details:
    print(f"{d['ingredient']}: {d['calories']} kcal ({d['percentage']:.1f}%)")
```

## 🎓 Pattern OOP

Segue il pattern di astrazione/ereditarietà:
- Classe base astratta `Recipe`
- Metodi astratti: `total_calories()`, `prep_time()`
- Sottoclassi concrete con implementazioni specifiche
- Validazione tramite `__init_subclass__`

## 📄 License

MIT License

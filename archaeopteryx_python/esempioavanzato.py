
class GeneratoreMusicale:
    def __init__(self):
        self.scale = {
            'do_maggiore': ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'],
            'la_minore': ['A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4']
        }

    def genera_per_grado_congiunto(self, lunghezza=8):
        """
        Genera una melodia dove le note si muovono principalmente 
        per gradi congiunti (note vicine)
        """
        melodia = stream.Stream()
        scala_corrente = self.scale['do_maggiore']
        nota_precedente_index = 0
        
        for i in range(lunghezza):
            # Movimento limitato a +/- 2 posizioni nella scala
            movimento = random.randint(-2, 2)
            nuovo_index = max(0, min(len(scala_corrente)-1, 
                                   nota_precedente_index + movimento))
            
            n = note.Note(scala_corrente[nuovo_index], quarterLength=1.0)
            melodia.append(n)
            nota_precedente_index = nuovo_index
            
        return melodia

    def genera_per_pattern_ritmico(self, pattern=[1.0, 0.5, 0.5, 1.0]):
        """
        Genera una melodia basata su un pattern ritmico ripetitivo
        """
        melodia = stream.Stream()
        scala_corrente = self.scale['do_maggiore']
        
        # Ripeti il pattern 4 volte
        for _ in range(4):
            for durata in pattern:
                nota_scelta = random.choice(scala_corrente)
                n = note.Note(nota_scelta, quarterLength=durata)
                melodia.append(n)
                
        return melodia

    def genera_domanda_risposta(self):
        """
        Genera una melodia con struttura domanda-risposta
        """
        melodia = stream.Stream()
        
        # Genera la "domanda" (frase ascendente)
        for i in range(4):
            n = note.Note(self.scale['do_maggiore'][i], quarterLength=1.0)
            melodia.append(n)
            
        # Genera la "risposta" (frase discendente)
        for i in range(3, -1, -1):
            n = note.Note(self.scale['do_maggiore'][i], quarterLength=1.0)
            melodia.append(n)
            
        return melodia

# Esempio di utilizzo
generatore = GeneratoreMusicale()

# Genera diversi tipi di melodie
melodia1 = generatore.genera_per_grado_congiunto()
melodia1.write('midi', 'melodia_gradi_congiunti.mid')

melodia2 = generatore.genera_per_pattern_ritmico()
melodia2.write('midi', 'melodia_pattern.mid')

melodia3 = generatore.genera_domanda_risposta()
melodia3.write('midi', 'melodia_domanda_risposta.mid')

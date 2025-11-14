from flask import Flask, request, jsonify, render_template_string
from textblob import TextBlob
from datetime import datetime
from typing import Dict, List, Optional
import logging
from collections import defaultdict
from functools import lru_cache
import json
import csv
import io

# Rate limiting (opzionale, decommentare se installato flask-limiter)
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address


# ============================================================================
# Configurazione App
# ============================================================================

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Supporto caratteri UTF-8

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiter (decommentare per abilitare)
# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,
#     default_limits=["100 per hour"]
# )

# Storage in-memory per statistiche (in produzione usare un database)
sentiment_storage = defaultdict(list)


# ============================================================================
# Sentiment Analyzer
# ============================================================================

class SentimentAnalyzer:
    """Classe per l'analisi del sentiment con TextBlob"""
    
    # Soglie per classificazione sentiment
    POSITIVE_THRESHOLD = 0.1
    NEGATIVE_THRESHOLD = -0.1
    
    # Mappatura emoji per sentiment
    SENTIMENT_EMOJI = {
        'positivo': '😊',
        'negativo': '😞',
        'neutro': '😐'
    }
    
    @staticmethod
    @lru_cache(maxsize=1000)  # Cache per testi già analizzati
    def analyze_text(text: str) -> Dict:
        """
        Analizza il sentiment di un testo.
        
        Args:
            text: Testo da analizzare
        
        Returns:
            dict: {
                'sentiment': str,
                'polarity': float,
                'subjectivity': float,
                'confidence': float
            }
        """
        if not text or not text.strip():
            return {
                'sentiment': 'neutro',
                'polarity': 0.0,
                'subjectivity': 0.0,
                'confidence': 0.0,
                'error': 'Testo vuoto'
            }
        
        try:
            # Analisi con TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classificazione sentiment
            if polarity > SentimentAnalyzer.POSITIVE_THRESHOLD:
                sentiment = 'positivo'
            elif polarity < SentimentAnalyzer.NEGATIVE_THRESHOLD:
                sentiment = 'negativo'
            else:
                sentiment = 'neutro'
            
            # Calcola confidence (basato su quanto è estrema la polarity)
            confidence = abs(polarity)
            
            return {
                'sentiment': sentiment,
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'confidence': round(confidence, 3),
                'emoji': SentimentAnalyzer.SENTIMENT_EMOJI[sentiment]
            }
            
        except Exception as e:
            logger.error(f"Errore analisi sentiment: {e}")
            return {
                'sentiment': 'neutro',
                'polarity': 0.0,
                'subjectivity': 0.0,
                'confidence': 0.0,
                'error': str(e)
            }
    
    @staticmethod
    def get_sentiment_label(polarity: float) -> str:
        """Converte polarity in label testuale"""
        if polarity > SentimentAnalyzer.POSITIVE_THRESHOLD:
            return 'positivo'
        elif polarity < SentimentAnalyzer.NEGATIVE_THRESHOLD:
            return 'negativo'
        return 'neutro'


# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/')
def home():
    """Pagina home con documentazione interattiva"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentiment Analysis API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                border-radius: 10px;
                margin-bottom: 30px;
                text-align: center;
            }
            .section {
                background: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .endpoint {
                background: #f8f9fa;
                padding: 15px;
                border-left: 4px solid #667eea;
                margin: 10px 0;
                border-radius: 5px;
            }
            .method {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
                margin-right: 10px;
            }
            .post { background: #28a745; color: white; }
            .get { background: #007bff; color: white; }
            code {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                display: block;
                border-radius: 5px;
                overflow-x: auto;
                margin: 10px 0;
            }
            .demo-form {
                background: #e7f3ff;
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
            }
            textarea, input {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            button {
                background: #667eea;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover { background: #5568d3; }
            #result {
                margin-top: 20px;
                padding: 15px;
                background: #d4edda;
                border-left: 4px solid #28a745;
                border-radius: 5px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎭 Social Media Sentiment Analysis API</h1>
            <p>Analizza il sentiment di post e commenti sui social media</p>
        </div>
        
        <div class="section">
            <h2>📖 Endpoints Disponibili</h2>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/analyze</strong>
                <p>Analizza il sentiment di un singolo testo</p>
                <code>{
    "text": "Adoro Netflix! È fantastico!",
    "topic": "Netflix"
}</code>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/analyze/batch</strong>
                <p>Analizza multipli post contemporaneamente</p>
                <code>{
    "topic": "Netflix",
    "posts": [
        "Adoro Netflix!",
        "Netflix non mi piace",
        "È ok, niente di speciale"
    ]
}</code>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/stats/&lt;topic&gt;</strong>
                <p>Ottieni statistiche aggregate per un topic</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/health</strong>
                <p>Verifica stato API</p>
            </div>
        </div>
        
        <div class="section">
            <h2>🧪 Prova l'API</h2>
            <div class="demo-form">
                <label>Topic/Marca:</label>
                <input type="text" id="topic" placeholder="es. Netflix, Amazon, Tesla" value="Netflix">
                
                <label>Testo da analizzare:</label>
                <textarea id="text" rows="4" placeholder="Inserisci il testo da analizzare...">Adoro Netflix! È il migliore servizio streaming!</textarea>
                
                <button onclick="analyzeSentiment()">🔍 Analizza Sentiment</button>
                
                <div id="result"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Esempio Risposta</h2>
            <code>{
    "success": true,
    "data": {
        "text": "Adoro Netflix!",
        "topic": "Netflix",
        "sentiment": "positivo",
        "polarity": 0.5,
        "subjectivity": 0.6,
        "confidence": 0.5,
        "emoji": "😊"
    },
    "timestamp": "2025-11-12T10:30:00"
}</code>
        </div>
        
        <script>
            async function analyzeSentiment() {
                const topic = document.getElementById('topic').value;
                const text = document.getElementById('text').value;
                const resultDiv = document.getElementById('result');
                
                try {
                    const response = await fetch('/api/v1/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({topic, text})
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        const result = data.data;
                        resultDiv.innerHTML = `
                            <h3>✅ Risultato Analisi</h3>
                            <p><strong>Sentiment:</strong> ${result.sentiment} ${result.emoji}</p>
                            <p><strong>Polarity:</strong> ${result.polarity}</p>
                            <p><strong>Confidence:</strong> ${result.confidence}</p>
                            <p><strong>Subjectivity:</strong> ${result.subjectivity}</p>
                        `;
                        resultDiv.style.display = 'block';
                    } else {
                        resultDiv.innerHTML = `<h3>❌ Errore</h3><p>${data.error}</p>`;
                        resultDiv.style.display = 'block';
                        resultDiv.style.background = '#f8d7da';
                        resultDiv.style.borderLeft = '4px solid #dc3545';
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<h3>❌ Errore</h3><p>${error.message}</p>`;
                    resultDiv.style.display = 'block';
                }
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/api/v1/analyze', methods=['POST'])
def analyze_single():
    """
    Analizza il sentiment di un singolo testo
    
    Body JSON:
        {
            "text": str (required),
            "topic": str (optional)
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "text" mancante nel body'
            }), 400
        
        text = data['text']
        topic = data.get('topic', 'general')
        
        # Analizza sentiment
        analysis = SentimentAnalyzer.analyze_text(text)
        
        # Prepara risposta
        result = {
            'text': text,
            'topic': topic,
            **analysis
        }
        
        # Salva in storage per statistiche
        sentiment_storage[topic].append({
            'text': text,
            'sentiment': analysis['sentiment'],
            'polarity': analysis['polarity'],
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Analizzato testo per topic '{topic}': {analysis['sentiment']}")
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Errore in /analyze: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/analyze/batch', methods=['POST'])
def analyze_batch():
    """
    Analizza multipli post contemporaneamente
    
    Body JSON:
        {
            "topic": str (required),
            "posts": list[str] (required)
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'posts' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "posts" mancante nel body'
            }), 400
        
        topic = data.get('topic', 'general')
        posts = data['posts']
        
        if not isinstance(posts, list):
            return jsonify({
                'success': False,
                'error': 'Campo "posts" deve essere una lista'
            }), 400
        
        # Analizza tutti i post
        results = []
        for post in posts:
            analysis = SentimentAnalyzer.analyze_text(post)
            results.append({
                'post': post,
                'sentiment': analysis['sentiment'],
                'polarity': analysis['polarity'],
                'subjectivity': analysis['subjectivity'],
                'confidence': analysis['confidence'],
                'emoji': analysis['emoji']
            })
            
            # Salva in storage
            sentiment_storage[topic].append({
                'text': post,
                'sentiment': analysis['sentiment'],
                'polarity': analysis['polarity'],
                'timestamp': datetime.now().isoformat()
            })
        
        # Calcola statistiche aggregate
        sentiments = [r['sentiment'] for r in results]
        polarities = [r['polarity'] for r in results]
        
        stats = {
            'total_posts': len(results),
            'positive': sentiments.count('positivo'),
            'negative': sentiments.count('negativo'),
            'neutral': sentiments.count('neutro'),
            'avg_polarity': round(sum(polarities) / len(polarities), 3) if polarities else 0,
            'sentiment_distribution': {
                'positivo': f"{(sentiments.count('positivo')/len(sentiments)*100):.1f}%",
                'negativo': f"{(sentiments.count('negativo')/len(sentiments)*100):.1f}%",
                'neutro': f"{(sentiments.count('neutro')/len(sentiments)*100):.1f}%"
            }
        }
        
        logger.info(f"Analizzati {len(posts)} post per topic '{topic}'")
        
        return jsonify({
            'success': True,
            'topic': topic,
            'results': results,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Errore in /analyze/batch: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/stats/<topic>', methods=['GET'])
def get_stats(topic):
    """
    Ottieni statistiche aggregate per un topic
    
    Query params:
        format: 'json' | 'csv' (default: json)
    """
    try:
        if topic not in sentiment_storage:
            return jsonify({
                'success': False,
                'error': f'Nessun dato disponibile per topic "{topic}"'
            }), 404
        
        data = sentiment_storage[topic]
        
        # Calcola statistiche
        total = len(data)
        sentiments = [d['sentiment'] for d in data]
        polarities = [d['polarity'] for d in data]
        
        stats = {
            'topic': topic,
            'total_analyzed': total,
     



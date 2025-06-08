from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# Load the enriched wine data
df = pd.read_csv("Enriched_Winedatabase.csv", encoding="ISO-8859-1")

# Basic HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>Joy of Wine AI Sommelier</title>
    <style>
        body { font-family: Georgia, serif; background-color: #fdf6f0; color: #3c2f2f; padding: 2em; }
        h1 { color: #8b0000; }
        select, input[type=submit] { padding: 0.5em; margin-top: 1em; font-size: 1em; }
        .result { border-top: 1px solid #ccc; margin-top: 2em; padding-top: 1em; }
    </style>
</head>
<body>
    <h1>🍷 Joy of Wine: AI Sommelier</h1>
    <form method=\"post\">
        <label for=\"mood\">Select a mood:</label><br>
        <select name=\"mood\">
            <option>Romantic</option>
            <option>Relaxed</option>
            <option>Bold</option>
            <option>Elegant</option>
            <option>Zesty</option>
        </select><br><br>

        <label for=\"season\">Select a season:</label><br>
        <select name=\"season\">
            <option>Spring</option>
            <option>Summer</option>
            <option>Autumn</option>
            <option>Winter</option>
        </select><br><br>

        <input type=\"submit\" value=\"Find My Wine\">
    </form>

    {% if result %}
    <div class=\"result\">
        <h2>Sommelier Recommends:</h2>
        <p><strong>Wine:</strong> {{ result.DISPLAY_NAME }}</p>
        <p><strong>Producer:</strong> {{ result.PRODUCER_NAME }}</p>
        <p><strong>Region:</strong> {{ result.REGION }}, {{ result.COUNTRY }}</p>
        <p><strong>Flavor Notes:</strong> {{ result.FLAVOR_NOTES }}</p>
        <p><strong>Pairing Ritual:</strong> {{ result.PAIRING_RITUALS }}</p>
        <p><strong>Glassware:</strong> {{ result.GLASSWARE }}</p>
        <p><strong>Serving Temp:</strong> {{ result.SERVING_TEMP }}</p>
        <p><strong>Price Level:</strong> {{ result.PRICE_LEVEL }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        mood = request.form.get('mood')
        season = request.form.get('season')
        filtered = df[(df['MOOD'].str.contains(mood, case=False, na=False)) &
                      (df['SEASON'].str.contains(season, case=False, na=False))]
        if not filtered.empty:
            result = filtered.sample(1).iloc[0]
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)

from flask import Flask, render_template, request
from fuzzer import fuzzy_search
from newmodel import identify_place_names
from translator import translator

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    text = ''
    result = []

    if request.method == 'POST':
        message = request.form['message']

        if message:
            text = message
            result = identify_and_search(text)

    return render_template('index.html', text=text, result=result)


def identify_and_search(text):
    translated = translator(text)
    result = identify_place_names(translated)

    formatted_result = []
    for word_to_search in result:
        search_result = fuzzy_search("places.csv", word_to_search)
        formatted_result.append({
            'word': search_result[0],
            'canonical_name': search_result[1],
            'table': search_result[2]
        })

    return formatted_result


if __name__ == '__main__':
    app.run(debug=True)

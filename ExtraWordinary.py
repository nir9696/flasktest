from flask import Flask, request, render_template, redirect, url_for
import requests

NOUN = 'n'
VERB = 'v'
ADJECTIVE = 'adj'
ADVERB = 'adv'


def get_def_api(search_word):
    resp = requests.get(f'https://api.datamuse.com/words?sp={search_word}&md=d')
    resp_json = resp.json()
    placeholders = {}
    nouns_l = []
    verbs_l = []
    adjectives_l = []
    adverbs_l = []
    if 'defs' in resp_json[0]:
        for i in range(len(resp_json[0]['defs'])):
            part_of_speech, defi = resp_json[0]['defs'][i].split('\t')
            if part_of_speech == NOUN:
                placeholders[NOUN] = 'noun'
                nouns_l.append(defi)
            if part_of_speech == VERB:
                placeholders[VERB] = 'verb'
                verbs_l.append(defi)
            if part_of_speech == ADJECTIVE:
                placeholders[ADJECTIVE] = 'adjective'
                adjectives_l.append(defi)
            if part_of_speech == ADVERB:
                placeholders[ADVERB] = 'adverb'
                adverbs_l.append(defi)
    placeholders.update({'nouns': nouns_l, 'verbs': verbs_l, 'adjectives': adjectives_l, 'adverbs': adverbs_l})
    return placeholders


def get_ryme_api(search_word):
    resp = requests.get(f'https://api.datamuse.com/words?rel_rhy={search_word}')
    resp_json = resp.json()
    rhymes_l = []
    for i in range(len(resp_json)):
        rhymes_l.append(resp_json[i]['word'])
    return {'rhymes': rhymes_l}


def get_syn_api(search_word):
    resp = requests.get(f'https://api.datamuse.com/words?rel_syn={search_word}')
    resp_json = resp.json()
    syns_l = []
    for i in range(len(resp_json)):
        syns_l.append(resp_json[i]['word'])
    return {'syns': syns_l}

def get_ant_api(search_word):
    resp = requests.get(f'https://api.datamuse.com/words?rel_ant={search_word}')
    resp_json = resp.json()
    ants_l = []
    for i in range(len(resp_json)):
        ants_l.append(resp_json[i]['word'])
    return {'ants': ants_l}


def get_freq_api(search_word):
    resp = requests.get(f'https://api.datamuse.com/words?sp={search_word}&md=f')
    resp_json = resp.json()
    placeholder = {}
    _, freq_str = resp_json[0]['tags'][0].split(':')
    placeholder['freq'] = round(float(freq_str) / (10 ** 4), 10)
    return placeholder


RESULTS = [get_def_api, get_ryme_api, get_syn_api, get_ant_api, get_freq_api]

app = Flask(__name__)
@app.route('/results/<word>', methods=["POST", "GET"])
def results(word):
    if request.method == "POST":
        search_word = request.form["search"]
        return redirect(url_for("results", word=search_word))
    else:
        search_word = word.lower()
        overall = {"s_word": search_word}
        for func in RESULTS:
            overall.update(func(search_word))
        return render_template("results.html", **overall)


@app.route('/', methods=["POST", "GET"])
@app.route('/home/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        search_word = request.form["search"]
        return redirect(url_for("results", word=search_word))
    else:
        return render_template("index.html")


@app.route('/admin/')
def admin():
    return redirect(url_for("home"))

@app.route('/results/')
def results_example():
    return redirect(url_for("results", word="example"))

if __name__ == "__main__":
    app.run(debug=True)



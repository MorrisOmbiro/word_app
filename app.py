import requests
import itertools
import re

from flask import Flask, request, Response, render_template
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import Regexp, Optional, Required
from flask.json import jsonify
from string import *

class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators=[Optional(), Regexp('^[a-z]*$', 0, "Lower Case Letters Only")])
    pattern = StringField('Pattern', validators=[Optional(), Regexp('^[a-z\.]*$', 0, "Lower Case Letters or . Elements Only")])
    choose_length = SelectField('Length', [Optional()], coerce=int, choices=[(-1, ' '), (1, 3),(2, 4),(3, 5),(4, 6),(5, 7),(6, 8),(7, 9),(8, 10),])
    submit = SubmitField("Go")

    def form_check(self):
        letters = self.avail_letters.data
        length = self.choose_length.data
        patt = self.pattern.data
        print(patt)
        # If a length is specified and a pattern is entered, pattern must match the length
        # example: ..g must be 3
        e=""
        if length != -1:
            length += 2
        print(len(patt))
        print(length)
        if patt != "" and length != -1 and len(patt) != length:
            e = "Need pattern to match length"
        # If no letters are provided, then a pattern must be provided
        if letters == "" and patt == "":
            e = "Need pattern if no letters"
        # ..g for patter ask for letters ... can't match these
        if letters != "" and patt != "":
            for r in patt.replace('.', ''):
                if r not in letters:
                    e="Pattern letter not in letters"
        return e
    # f72e9bac-8434-4aa7-852c-bf16c49917b6er


csrf = CSRFProtect()
app = Flask(__name__) # gunicorn will find you
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

# has to be / ... otherwise goodluck getting heroku to deploy
@app.route('/')
def index():
    form = WordForm()
    return render_template("index.html", form=form, name="Morris Ombiro")

@app.route('/words', methods=['POST','GET'])
def letters_2_words():
    form = WordForm()
    if form.validate_on_submit():
        letters = form.avail_letters.data
        len_ = form.choose_length.data
        pat_ = form.pattern.data

        #check form for es
        err = WordForm.form_check(form);
        print(err)
        if err != "":
            return render_template('index.html', form=form,
                                   name="Morris Ombiro", e=err)
        max_len = len(letters)
        if len_ != -1:
            max_len = len_ + 2
        elif len_ == -1 and pat_:
            max_len = len(pat_)

        if pat_ and not letters:
            letters = "abcdefghijklmnopqrstuvwxyz" + pat_.replace('.', '')
    else:
        return render_template('index.html', form=form,
                               name="Morris Ombiro", e="Lower Case letters only or . on paterns")

    with open('sowpods.txt') as f:
        good_words = set(x.strip().lower() for x in f.readlines())

    word_set = set()

    for l in range(3,max_len+1):
        for word in itertools.permutations(letters,l):
            w = "".join(word)
            if w in good_words:
                if pat_:
                    match = re.match('^' + pat_+'$', w)
                    if match:
                        word_set.add(w)
                else:
                    word_set.add(w)

    if len(word_set) < 1:
        return render_template('index.html', form=form,
                               name="Morris Ombiro", e = "no matching words")
    # first sort
    sort_first = sorted(word_set)
    return render_template('wordlist.html',
        wordlist=sorted(sort_first, key=len),  #secondary sort by length
        name="Morris Ombiro")

@app.route('/proxy/<word>')
def proxy(word):
    return jsonify(requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=f72e9bac-8434-4aa7-852c-bf16c49917b6".format(word=word)).json())

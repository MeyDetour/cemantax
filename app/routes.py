from crypt import methods

from flask import Flask, render_template, request, session ,redirect
from werkzeug.utils import redirect

from app import app

app.secret_key = "super secret key"

import cemantix
cemantix = cemantix.Game()
@app.route('/',methods=['post','get'])
@app.route('/index',methods=['post',"get"])
def index():
    cemantix.start_game()

    word_said = cemantix.get_words_said()
    data = request.form.get('word')

    error = ""
    message = ""
    done = False
    if request.method == 'POST' and not done :
        if data in word_said:
            error = "already said"
        if not data.isalpha():
            error = "data must be alphabetic letter"

        if not data in word_said and data.strip()!="" and data.isalpha() :
           resultat = cemantix.run(data)
           if resultat :
                done = True


    last_word = cemantix.get_last_said()
    words = cemantix.get_words()
    score_to_render = ""
    for word in words:
        if word[1] >= 0:
            score_to_render += f"<div class='word'><span class='{'lastWord' if word[0] == last_word else ''}'>{word[0]}</span><div class='range'><div class='progress' style='width: {word[1]}%; background: linear-gradient(45deg, #3ff905, hsl({100 - word[1]} 100% 43% / 1))'></div></div><span class='{'lastWord' if word[0] == last_word else ''}'>{word[1]}%</span></div>"
        else:
            score_to_render += f"<div class='word'><span class='{'lastWord' if word[0] == last_word else ''}'>{word[0]}</span><div class='range'><div class='progress' style='width: 0%; background: linear-gradient(45deg, #3ff905, hsl({100 - word[1]} 100% 43% / 1))'></div></div><span class='{'lastWord' if word[0] == last_word else ''}'>{word[1]}%</span></div>"

    return render_template('index.html',
                           word = data,
                           done = True,
                           error = error,
                           message = message,
                           words = score_to_render
                           )



@app.route('/reset')
def reset():
    session.clear()
    return  redirect('/')
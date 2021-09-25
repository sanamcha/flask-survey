from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


KEY_RESPONSE = "responses"

app=Flask(__name__)

app.config['SECRET_KEY'] ="secretkey123"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def start_page():
    return render_template('home.html', survey=satisfaction_survey)


@app.route('/start', methods=["POST"])
def start_questions():
    session[KEY_RESPONSE] = []
    return redirect('/questions/0')

@app.route("/questions/<int:id>")
def show_questions(id):
    
    responses = session.get(KEY_RESPONSE)

    if (responses is None):
        return redirect('/')

    if (len(responses) != id):
        flash(f"Invalid question id:{id}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[id]
    return render_template("question.html", question_num=id, question=question)


@app.route("/answer", methods=["POST"])
def list_question():
    choice =request.form['answer']
    responses = session[KEY_RESPONSE]
    responses.append(choice)
    session[KEY_RESPONSE] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/end')

    else:
        return redirect(f'/questions/{len(responses)}')


@app.route("/end")
def end_page():
    return render_template("end.html")





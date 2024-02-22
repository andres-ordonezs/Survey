from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def start_page():
    survey_title = survey.title
    survey_instructions = survey.instructions

    return render_template('survey_start.html',
                           survey_title=survey_title,
                           survey_instructions=survey_instructions
                           )


@app.post('/begin')
def begin_survey():
    responses.clear()

    return redirect('/question/0')


@app.get('/question/0')
def get_first_question():

    question = survey.questions[0]

    return render_template("question.html",
                           question=question)

@app.post("/answer")
def get_answer():
    answer = request.form["answer"]
    responses.append(answer)

    return redirect("/question/1")

@app.get('/question/1')
def get_second_question():

    question = survey.questions[1]
    print("********************responses=",responses)
    return render_template("question.html",
                           question=question)

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

debug = DebugToolbarExtension(app)


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

    return redirect('/question/0')


@app.get('/question/0')
def get_first_question():

    question = survey.questions[0]

    return render_template("question.html",
                           question=question)

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)


@app.get('/')
def choose_page():
    """Root route. It renders survey_start.html template"""

    return render_template('choose_survey.html', surveys = surveys)


@app.get("/start")
def start():

    return render_template("survey_start.html")

@app.post("/get_survey")
def get_survey():

    survey_title = request.form["survey"]
    survey = surveys[survey_title]
    session["cur_survey"] = survey_title

    return render_template('survey_start.html', survey = survey)


@app.post('/begin')
def begin_survey():
    """Redirects to first question in the survey and clears the
    response variable"""

    session['responses'] = []

    return redirect('/question/0')


@app.get('/question/<int:index>')
def get_question(index):
    """Renders the question at current route's index"""

    if len(session['responses']) == len(surveys[str(session["cur_survey"])].questions):
        flash('You have already completed the survey!')
        return redirect("/completion")

    if index != len(session['responses']):
        flash("No time travel allowed!")
        return redirect(f"/question/{len(session['responses'])}")

    question = surveys[str(session["cur_survey"])].questions[index]

    return render_template("question.html", question=question)


@app.post("/answer")
def get_answer():
    """Gets form data and appends it to the resposes variable.
    Checks if the survey is complete and redirects accordingly"""
    answer = request.form["answer"]

    answers = session['responses']
    answers.append(answer)
    session['responses'] = answers

    if len(session['responses']) == len(surveys[str(session["cur_survey"])].questions):
        return redirect("/completion")

    else:
        return redirect(f"/question/{len(session['responses'])}")


@app.get("/completion")
def show_completion():
    """Renders completion template with all answered questions
    with answers"""

    questions = surveys[str(session["cur_survey"])].questions

    return render_template("completion.html",
                           questions=questions,
                           responses=session['responses'])

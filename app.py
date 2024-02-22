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
    """Root route. It renders survey_start.html template"""
    survey_title = survey.title
    survey_instructions = survey.instructions
# TODO: send the whole survey to template
    return render_template('survey_start.html',
                           survey_title=survey_title,
                           survey_instructions=survey_instructions)


@app.post('/begin')
def begin_survey():
    """Redirects to first question in the survey and clears the
    response variable"""
    responses.clear()

    return redirect('/question/0')


@app.get('/question/<int:index>')
# TODO: Change function name
def get_first_question(index):
    """Renders the question at current route's index"""

    question = survey.questions[index]

    return render_template("question.html",
                           question=question,
                           index=index)

# TODO use /answer


@app.post("/answer/<int:index>")
def get_answer(index):
    """Gets form data and appends it to the resposes variable.
    Checks if the survey is complete and redirects accordingly"""

    answer = request.form["answer"]
    responses.append(answer)

    if len(responses) == len(survey.questions):
        return redirect("/completion")

    else:
        return redirect(f"/question/{index+1}")


@app.get("/completion")
def show_completion():
    """Renders completion template with all answered questions
    with answers"""

    questions = survey.questions

    return render_template("completion.html",
                           questions=questions,
                           responses=responses)

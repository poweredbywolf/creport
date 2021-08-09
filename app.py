from flask import Flask, render_template, session, redirect, url_for, flash 

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, form
from werkzeug import datastructures
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import DataRequired

#instantiate application instance
app = Flask(__name__)

#configuration

app.config['SECRET_KEY'] = 'hard password'

#instantiating objects
boostrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CovForm(FlaskForm):
    start_date = DateField('Date of Contraction')
    symptom_date = DateField('Date of Symptoms')
    duration = IntegerField('duration of symptoms')
    severity = SelectField('Severity', choices=[('asy','asymptomatic'), ('mild','mild'), ('heavy','heavy'),
                            ('hospital', 'hospitalised'), ('vent','venilator'), ('death', 'death')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home(): 
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('changing your name huh?')
        name = form.name.data #becomes the request handler - kind of like a delegate in Swift
        flash('submit succesful')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('home'))
    return render_template('home.html', form=form, name=session.get('name'))



@app.route('/covid', methods=['GET', 'POST'])
def covidForm():
    form = CovForm()
    if form.validate_on_submit():
        sdate = form.start_date.data
        duration = form.duration.data
        symptom_date = form.symptom_date.data 
        flash('submit success')
        return render_template('covReport.html', sdate=sdate, duration=duration,symptom_date=symptom_date)
    return render_template('covForm.html', form=form)



@app.route('/test')
def test():
    return render_template('test.html')

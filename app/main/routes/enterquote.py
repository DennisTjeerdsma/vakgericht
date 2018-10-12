from sqlalchemy import func
from flask_login import login_required
from app import db
from flask import render_template, url_for, redirect, flash
from app.main.forms import QuoteForm
from app.models import User, Quote
from app.main import bp

@bp.route('/enterquote', methods=['GET', 'POST'])
@login_required
def enterquote():
    form = QuoteForm()
    if form.validate_on_submit():
        quotedperson = User.query.filter(func.lower(User.username) == func.lower(form.name.data)).first()
        if quotedperson is None:
            flash("Please enter a valid user")
            return redirect(url_for('main.enterquote'))
        quote = Quote(quotedperson=quotedperson, body=form.quote.data)
        db.session.add(quote)
        db.session.commit()
        flash('Your quote has been succesfully added')
        return redirect(url_for('main.index'))
    return render_template('enterquote.html', title='Enter Quote', form=form)
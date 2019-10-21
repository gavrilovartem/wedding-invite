# -*- coding: utf-8 -*- 
from application import application, db
from flask import render_template, redirect, flash, url_for, current_app
from application .forms import LoginForm, AlcoholForm, MusicForm, WishForm, UnitedForm
from flask_login import current_user, login_user, login_required, logout_user
from application .models import User, Alcohol, Music, Wish, UserChoice

from math import pi
import pandas as pd



@application.route('/', methods=['GET', 'POST'])

def cabinet():
	if not current_user.is_authenticated:
		return current_app.login_manager.unauthorized()
	form_uni = UnitedForm(prefix="form_uni")
	if form_uni.validate_on_submit():
		if form_uni.checkbox1.data == True and form_uni.checkbox2.data == True:
 			user_choice = UserChoice(id_user=current_user.id,
 			transfer=dict(form_uni.transfer.choices).get(form_uni.transfer.data),
 			confirmation=dict(form_uni.confirmation.choices).get(form_uni.confirmation.data),
 			bed_flag=dict(form_uni.bed.choices).get(form_uni.bed.data))
 			db.session.add(user_choice)
 			db.session.commit()
 			alcohol = Alcohol(alcohol=dict(form_uni.alcohol.choices).get(form_uni.alcohol.data), id_user=current_user.id)
 			db.session.add(alcohol)
 			db.session.commit()
 			music = Music(text=form_uni.text.data, id_user=current_user.id)
 			db.session.add(music)
 			db.session.commit()
 			wish = Wish(wish=form_uni.wish.data, id_user=current_user.id)
 			db.session.add(wish)
 			db.session.commit()
 			return redirect('/finish')
		else:
			flash('Нужно принять условия соглашения!')
	return render_template('invitation.html', title='Приглашение на свадьбу', form_uni=form_uni, username=current_user.username)
@application.route('/finish') 	
def finish():
	return render_template('finish.html')
@application.route('/visual')
def visual():
	queries_c = db.session.query(User.username, UserChoice.confirmation,UserChoice.transfer, UserChoice.bed_flag).join(UserChoice).all()
	queries_alc = db.session.query(Alcohol.alcohol).all()
	queries_wishes = db.session.query(User.username, Wish.wish).join(Wish).all()
	queries_music = db.session.query(User.username, Music.text).join(Music).all()
	return render_template('visual.html', title='Статистика', queries=queries_c, queries_alc=queries_alc, queries_wishes=queries_wishes, queries_music=queries_music)

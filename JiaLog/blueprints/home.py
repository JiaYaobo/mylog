from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return render_template('home/index.html')


@home_bp.route('/about')
def about():
    return render_template('home/about.html')


@home_bp.route('/contact')
def contact():
    return render_template('home/contact.html')


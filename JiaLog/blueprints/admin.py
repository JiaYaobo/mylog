import os
from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from JiaLog.models import Category, Comment, Note
from JiaLog.forms import SettingForm, NoteForm, CategoryForm, CommentForm
from JiaLog.extensions import db
from JiaLog.utils import allowed_file, redirect_back
from flask_ckeditor import upload_fail, upload_success

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.my_title = form.my_title.data
        current_user.my_sub_title = form.my_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('note.index'))
    form.name.data = current_user.name
    form.my_title.data = current_user.my_title
    form.my_sub_title.data = current_user.my_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/note/manage')
@login_required
def manage_note():
    page = request.args.get('page', 1, type=int)
    pagination = Note.query.order_by(Note.timestamp.desc()).paginate(page,
    per_page=current_app.config['JIALOG_MANAGE_POST_PER_PAGE'])
    notes = pagination.items
    return  render_template('admin/manage_note.html', pagination=pagination, notes=notes)


@admin_bp.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    form = NoteForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        note = Note(title=title, body=body, category=category)
        db.session.add(note)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('note.show_note', note_id=note.id))
    return render_template('admin/new_note.html', form=form)


@admin_bp.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    form = NoteForm()
    note = Note.query.get_or_404(note_id)
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        note.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('note updated', 'success')
        return redirect(url_for('note.show_note', note_id=note.id))
    form.title.data = note.title
    form.body.data = note.body
    form.category.data = note.category_id
    return render_template('admin/edit_note.html', form=form)


@admin_bp.route('/note/<int:note_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('note deleted', 'success')
    return redirect_back()


@admin_bp.route('/set-comment/<int:note_id>', methods=['POST'])
@login_required
def set_comment(note_id):
    note = Note.query.get_or_404(note_id)
    if note.can_comment:
        note.can_comment = False
        flash('Comment disabled', 'info')
    else:
        note.can_comment = True
        flash('Comment enabled', 'info')
    db.session.commit()
    return redirect(url_for('note.show_note', note_id=note.id))


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.', 'success')
    return redirect_back()


@admin_bp.route('/comment/manage', methods=['POST','GET'])
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['JIALOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query
    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Category created.', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('home.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('.manage_category'))

    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('home.index'))
    category.delete()
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_category'))


@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['JIALOG_UPLOAD_PATH'], filename)


@admin_bp.route('/upload', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(current_app.config['JIALOG_UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)


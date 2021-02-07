from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect
from JiaLog.models import Category, Note, Comment
from JiaLog.forms import AdminCommentForm, CommentForm
from JiaLog.extensions import db
from flask_login import current_user


note_bp = Blueprint('note', __name__)


@note_bp.route('/', defaults={'page': 1})
@note_bp.route('/page/<int:page>')
def index(page):
    pagination = Note.query.order_by(Note.timestamp.desc()).paginate(page,
                                                                per_page=current_app.config['JIALOG_POST_PER_PAGE'])
    notes = pagination.items
    return render_template('note/index.html',pagination=pagination, notes=notes)


@note_bp.route('/note/<int:note_id>', methods=['GET', 'POST'])
def show_note(note_id):
    note = Note.query.get(note_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['JIALOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(note).filter_by(reviewed=True).order_by(Comment.timestamp.asc())\
        .paginate(page, per_page)
    comments = pagination.items
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False
    if form.validate_on_submit():
        author = form.author.data
        site = form.site.data
        body = form.body.data
        email = form.email.data
        replied_id = request.args.get('reply')
        comment = Comment(
            author=author, site=site, body=body, from_admin=from_admin, email=email,
            post=note, reviewed=reviewed
        )
        db.session.add(comment)
        db.session.commit()
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
        if current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed', 'info')
        return redirect(url_for('.show_note', note_id=note.id))
    return render_template('note/mynote.html', note=note, pagination=pagination,
                           comments=comments, form=form)


@note_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['JIALOG_POST_PER_PAGE']
    pagination = Note.query.with_parent(category).order_by(Note.timestamp.desc())\
        .paginate(page, per_page=per_page)
    notes = pagination.items
    return render_template('note/category.html', category=category, pagination=pagination, notes=notes)


@note_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('.show_note', note_id=comment.note_id, reply=comment_id, author=comment.author)+
                    '#comment-form')

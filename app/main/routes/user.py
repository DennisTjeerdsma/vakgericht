from app.models import User, Post
from flask_login import login_required
from flask import url_for, render_template, request, current_app
from app.main import bp

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    quotes = user.quotez()
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None                  
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, quotes=quotes)
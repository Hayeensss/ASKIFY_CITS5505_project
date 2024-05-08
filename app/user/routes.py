""" User routes for the user blueprint."""

from flask import current_app, render_template, request
from flask_login import login_required

from app.user import forms, user_bp
from app.user.service import (
    community_data,
    history_data,
    like_data,
    post_data,
    save_data,
    stat_data,
)


@user_bp.route("/")
@login_required
def user():
    """Render the user page."""

    # user data
    post_result = post_data()
    like_result = like_data()
    history_result = history_data()
    save_result = save_data()

    name_list = [
        post_result.get("name"),
        like_result.get("name"),
        history_result.get("name"),
        save_result.get("name"),
    ]
    data_list = [
        post_result.get("data"),
        like_result.get("data"),
        history_result.get("data"),
        save_result.get("data"),
    ]

    user_data = dict(zip(name_list, data_list))
    pagination = post_result.get("pagination")

    # user stat
    user_stat = stat_data()

    # user community
    user_community = community_data()
    print("user_community", user_community)

    return render_template(
        "user.html",
        render_id="users-Posts",
        render_url="/users/lists?name=Posts",
        user_stat=user_stat,
        user_data=user_data,
        user_community=user_community,
        pagination=pagination,
    )


@user_bp.route("/lists", methods=["GET"])
@login_required
def user_lists():
    """Get the user's lists."""

    # name, required
    name = request.args.get("name", type=str)
    if name is None:
        return "Name is required", 400

    # pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # retrieve data
    data_result = {}
    if name == "Posts":
        data_result = post_data(page, per_page)
    elif name == "Likes":
        data_result = like_data(page, per_page)
    elif name == "History":
        data_result = history_data(page, per_page)
    elif name == "Wish":
        data_result = save_data(page, per_page)

    pagination = data_result.get("pagination")

    return render_template(
        "userList.html",
        item=data_result.get("data"),
        pagination=pagination,
    )


@user_bp.route("/profile", methods=["GET", "PUT"])
@login_required
def profile():
    """Render the user profile page."""

    form = forms.ProfileForm(request.form)

    if form.validate_on_submit():
        # update user profile
        pass

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.logger.error(
                    "Forgot password error in field %s: %s",
                    {getattr(form, field).label.text},
                    {error},
                )
        return render_template("editProfile.html", form=form)

    return render_template("editProfile.html", form=form)

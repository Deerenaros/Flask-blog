from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, Regexp


# add checkboxes, dates, admins

class PostForm(Form):
    """
    Object, that could be rendered into html with hidden tag placed in order to CLRF protection.
    Contents post:
        - title (string): post's title, represented by <input type=text />
        - html (string): post's entry, represented by <textarea></textarea>
    """
    title = StringField("title", validators=[InputRequired()])
    html = TextAreaField("html", validators=[InputRequired()])
    tag = StringField("tag")
#    tags = StringField("tags", validators=[Regexp("[\w\s]*", message="Occasion arises while tried parse tag-list...")])
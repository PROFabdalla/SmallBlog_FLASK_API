from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from pprint import pprint
from marshmallow import Schema, fields


app =Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate = Migrate(app, db)
ma = Marshmallow(app)



class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement='auto')
    title = db.Column(db.String(40),unique=True,nullable=False)
    age = db.Column(db.Integer(),nullable=False)

    @property
    def get_method(self):
        return "hollew world"

    def __init__(self,title,age):
        self.title = title
        self.age = age
        



class Posts(db.Model):
    id          = db.Column(db.Integer,primary_key=True)
    title       = db.Column(db.String(255))
    content     = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    comment        = db.relationship('Comments',backref='post')
    
    @property
    def count_commets(self):
        comments = Comments.query.filter(Comments.post_id==self.id).count()
        return comments

    def __init__(self, title, content, date_posted):
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.comment = []




# ----------------------------------- tag_comment model -----------------------------

tags_comments = db.Table('tags_comments',
    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'),primary_key=True),
    db.Column('comment_id',db.Integer,db.ForeignKey('comments.id'),primary_key=True),
)
# ----------------------------------- post model -----------------------------

class Comments(db.Model):
    id          = db.Column(db.Integer,primary_key=True)
    content     = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    post_id     = db.Column(db.Integer,db.ForeignKey('posts.id'))
    tag         = db.relationship('Tags',secondary=tags_comments,lazy='subquery',backref='comment')

    def __init__(self, content, date_posted, post_id):
        self.content = content
        self.date_posted = date_posted
        self.post_id = post_id
        self.tag = []

# ----------------------------------- tag model -----------------------------

class Tags(db.Model):
    id          = db.Column(db.Integer,primary_key=True)
    name     = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)

    def __init__(self, name, date_posted):
        self.name = name
        self.date_posted = date_posted








# ------------------------------------- schemas ----------------------------
class Bookscima(ma.Schema):
    class Meta:
        model = Book
    id      = fields.Integer()
    title = fields.String()
    age = fields.Integer()
    get_method = fields.String()


class Commentsscima(ma.Schema):
    class Meta:
        model = Comments
        # fields = ("id", "content", "date_posted",'post_id',"post.title")
        # include_fk = True
    id      = fields.Integer()
    content = fields.String()
    date_posted = fields.DateTime()
    post = fields.Nested("Postsscima", only=("id", "title","content"))
    tag = fields.List(fields.Nested("Tagscima",only=("id","name")))
    # post = fields.Nested(lambda: Postsscima(only=("id", "title","content")))




class Postsscima(ma.Schema):
    class Meta:
        model = Posts
        # fields = ("id", "title", "content",'date_posted',"comment")
    id      = fields.Integer()
    title = fields.String()
    content = fields.String()
    date_posted = fields.DateTime()
    count_commets =fields.Integer()
    comment = fields.List(fields.Nested(Commentsscima(only=("id", "content","date_posted"))))
    
        

class Tagscima(ma.Schema):
    class Meta:
        model = Tags
    
    id      = fields.Integer()
    name = fields.String()
    date_posted = fields.DateTime()
    comment = fields.List(fields.Nested(Commentsscima(only=("id", "content","date_posted"))))








@app.route('/books',methods=['GET','POST'])
def get_books():
    if request.method == 'POST':
        book_title = request.json['title']
        book_age = request.json['age']
        db.create_all()
        new_book=Book(title=book_title,age=book_age)
        db.session.add(new_book)
        db.session.commit()
        return '{msg: "created"}',201
    else:
        book_list = Book.query.all()
        book_schema = Bookscima(many=True)
        outpot = book_schema.dump(book_list)
        return jsonify({'books':outpot})
        
@app.route('/books/<int:id>',methods=['GET','POST'])
def get_book(id):
    book_list = Book.query.get_or_404(id)
    book_schema = Bookscima()
    outpot = book_schema.dump(book_list)
    return jsonify({'books':outpot})



@app.route('/posts',methods=['GET','POST'])
def get_posts():
    if request.method == 'POST':
        post_title = request.json['title']
        post_content = request.json['content']
        post_date_posted = request.json['date_posted']
        # post_comments = request.json['comments']
        db.create_all()
        new_post=Book(title=post_title,content=post_content,date_posted=post_date_posted)
        db.session.add(new_post)
        db.session.commit()
        return '{msg: "created"}',201
    else:
        post_list = Posts.query.all()
        post_schema = Postsscima(many=True)
        outpot = post_schema.dump(post_list)
        return jsonify({'posts':outpot})


@app.route('/posts/<int:id>',methods=['GET','POST'])
def get_post(id):
    post_list = Posts.query.get_or_404(id)
    post_schema = Postsscima()
    outpot = post_schema.dump(post_list)
    return jsonify({'post':outpot})



@app.route('/comments',methods=['GET','POST'])
def get_comments():
    if request.method == 'POST':
        comment_content = request.json['content']
        comment_date_posted = request.json['date_posted']
        post_post = request.json['post_id']
        db.create_all()
        new_comment=Comments(content=comment_content,date_posted=comment_date_posted,post_id=post_post)
        db.session.add(new_comment)
        db.session.commit()
        return '{msg: "created"}',201
    else:
        comment_list = Comments.query.all()
        comment_schema = Commentsscima(many=True)
        outpot = comment_schema.dump(comment_list)
        return jsonify({'comments':outpot})



@app.route('/comments/<int:id>',methods=['GET','POST'])
def get_comment(id):
    comment_list = Comments.query.get_or_404(id)
    comment_schema = Commentsscima()
    outpot = comment_schema.dump(comment_list)
    return jsonify({'comment':outpot})


@app.route('/tags',methods=['GET','POST'])
def get_tag():
    if request.method == "POST":
        name = request.json['name']
        date_posted = request.json['date_posted']
        new_tag=Tags(name=name,date_posted=date_posted)
        db.session.add(new_tag)
        db.session.commit()
        return '{msg:"created"}',201
    else:
        tags_list = Tags.query.all()
        tag_schema = Tagscima(many=True)
        outpot = tag_schema.dump(tags_list)
        return jsonify({'tags':outpot})


@app.route('/tags/<int:id>',methods=['GET','POST'])
def get_one_post(id):
    get_tag = Tags.query.get_or_404(id)
    get_schema = Tagscima()
    outpot = get_schema.dump(get_tag)
    return jsonify({'tag':outpot})


if __name__ == "__main__":
    app.run(debug=True)








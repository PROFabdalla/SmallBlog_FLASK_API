from app import db



class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement='auto')
    title = db.Column(db.String(40),unique=True,nullable=False)
    age = db.Column(db.Integer(),nullable=False)

    def __init__(self,title,age):
        self.title = title
        self.age = age



class Posts(db.Model):
    id          = db.Column(db.Integer,primary_key=True)
    title       = db.Column(db.String(255))
    content     = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    comment        = db.relationship('Comments',backref='post')

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





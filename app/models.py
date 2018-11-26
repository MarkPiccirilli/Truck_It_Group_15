from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id  = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rating = db.Column(db.Integer)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)
        
    # Set up user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
class JobPost(UserMixin, db.Model):
    __tablename__ = 'job_posts'
    
    id  = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60), index=True, unique=True)
    description = db.Column(db.String(255), index=True, unique=True)
    postedDate = db.Column(db.Date)
    pickupDate = db.Column(db.Date)
    dropoffDate = db.Column(db.Date)
    deliveryInstuctions = db.Column(db.String(255), index=True, unique=True)
    claimed = db.Column(db.Boolean, default=False)
    paid = db.Column(db.Boolean, default=False)
    taker = db.Column(db.Integer, db.ForeignKey('users.id'))
    poster = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return '<User: {}>'.format(self.username)
        
        
class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
        
class SpecialCategory(db.Model):
    """
    Create a Special Categpry table
    """

    __tablename__ = 'special_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    def __repr__(self):
        return '<Category: {}>'.format(self.name)
        
class Job_Category(db.Model):
    """
    Create a join table for jobs and categories
    """

    __tablename__ = 'job_categories'

    job = db.Column(db.Integer, db.ForeignKey('job_posts.id'))
    category = db.Column(db.Integer, db.ForeignKey('special_categories.id'))

    def __repr__(self):
        return '<Category: {}>'.format(self.name)
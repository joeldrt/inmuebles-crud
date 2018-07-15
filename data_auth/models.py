from run import db
from passlib.hash import pbkdf2_sha256 as sha256


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


class RoleModel(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_role_name(cls, role_name):
        return cls.query.filter_by(role_name=role_name).first()

    @classmethod
    def return_all(cls):
        return [role.role_name for role in RoleModel.query.all()]


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())

    roles = db.relationship('RoleModel', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_me(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
                'firstName': x.firstName,
                'lastName': x.lastName,
                'roles': [role.role_name for role in x.roles]
            }
        return list(map(lambda x: to_json(x), UserModel.query.all()))

    # @classmethod
    # def delete_all(cls):
    #     try:
    #         num_rows_deleted = db.session.query(cls).delete()
    #         db.session.commit()
    #         return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
    #     except:
    #         return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        return sha256.verify(password, hashed_password)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

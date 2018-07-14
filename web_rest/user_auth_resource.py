from flask_restful import Resource, reqparse
from data_auth.models import UserModel, RevokedTokenModel, RoleModel
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity, get_jwt_claims, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('firstName')
parser.add_argument('lastName')
parser.add_argument('roles', action='append')
parser.add_argument('old_password')


class UserRegistration(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if 'admin' not in claims['roles']:
            return {'message': 'You dont have persmision to perform this operation'}, 401

        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            firstName=data['firstName'],
            lastName=data['lastName']
        )

        for role in data['roles']:
            new_user_role = RoleModel.find_by_role_name(role)
            if new_user_role:
                new_user.roles.append(new_user_role)

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=new_user)
            refresh_token = create_refresh_token(identity=new_user)
            return {
                'message': 'User {} was created'.format(new_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exists'.format(data['username'])}, 401

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=current_user)
            refresh_token = create_refresh_token(identity=current_user)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}, 401


class UserAccount(Resource):
    @jwt_required
    def get(self):
        current_username = get_jwt_identity()
        user = UserModel.find_by_username(current_username)
        ret_user = {
            'username': user.username,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'roles': [role.role_name for role in user.roles]
        }
        return ret_user


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        username = get_jwt_identity()
        user = UserModel.find_by_username(username)
        access_token = create_access_token(identity=user)
        return {'access_token': access_token}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()

        if 'admin' not in claims['roles']:
            return {'message': 'You dont have persmision to perform this operation'}, 401

        return UserModel.return_all()


class DeleteUser(Resource):
    @jwt_required
    def delete(self, username):
        current_username = get_jwt_identity()

        if username == current_username:
            return {'message': 'Request user cant ask for deleting himself'}, 403

        claims = get_jwt_claims()

        if 'admin' not in claims['roles']:
            return {'message': 'You dont have persmision to perform this operation'}, 401

        user_to_delete = UserModel.find_by_username(username)

        if not user_to_delete:
            return {'message': 'User {} doesn\'t exists'.format(username)}, 401

        try:
            user_to_delete.delete_me()
            return {'messages': 'User {} deleted'.format(username)}
        except:
            return {'message': 'Something went wrong width delete process'}, 500


class ChangePassword(Resource):
    @jwt_required
    def post(self):

        data = parser.parse_args()

        if not data['username'] or not data['password'] or not data['old_password']:
            return {'message': 'Imposible to perform operation... missing parameters'}, 400

        current_username = get_jwt_identity()

        if current_username != data['username']:
            return {'message': 'Not matching username'}, 400

        user = UserModel.find_by_username(current_username)

        if not user:
            return {'message': 'User {} doesn\'t exists'.format(current_username)}, 401

        if not UserModel.verify_hash(data['old_password'], user.password):
            return {'message': 'Current password doesn\'t match'}, 403

        user.password = UserModel.generate_hash(data['password'])

        try:
            user.save_to_db()
            return {'message': 'Password for user {} successfully changed'.format(user.username)}
        except:
            return {'message': 'Something went wrong'}, 500

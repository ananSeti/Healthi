 ## resources/auth.py

import datetime
import json
from flask import request
from flask_jwt_extended import create_access_token
from database.models import User
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.apis.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError
import numpy as np
import pickle


class SignupApi(Resource):
    def post(self):
        try:
            user_dict = dict()
            body = request.get_json()
            user = User(**body)
            user.representation = []
            user.hash_password()
            user.save()
            id = user.id

            return { 'id': str(id)}, 200

        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError
 
            access_token = create_access_token(identity=str(user.id), expires_delta=False)
            
            return {'token': access_token}, 200
        
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError

## resources/tuning.py

import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User, Recipe
from flask_restful import Resource
from resources.apis.errors import SchemaValidationError, UnauthorizedError, InternalServerError
from collections import deque

class FeedTunerApi(Resource):

    @jwt_required
    def post(self, uri):
        try:
            body = request.get_json()
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)

            q = deque(user.recently_liked)
            q.append(uri)
            if len(q) > 10:
                q.popleft()

            user.recently_liked = list(q)

            return {}, 200
            
        except Exception as e:
            raise InternalServerError

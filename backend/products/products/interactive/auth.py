import random

from channels.exceptions import RequestAborted

from games.repositories.api.users import UsersApiRepository


class JWTTokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    users_repository: UsersApiRepository = UsersApiRepository()

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, receive=None, send=None):
        header = scope['query_string']

        token_name, token_key = "Bearer", header.decode()

        if token_name == 'Bearer':
            user_data: dict = self.users_repository.get_by_jwt(
                jwt_token=f"Bearer {token_key}"
            )

            scope['user'] = user_data
        else:
            raise RequestAborted()

        return self.inner(scope, receive, send)


JWTTokenAuthMiddlewareStack = lambda inner: JWTTokenAuthMiddleware(inner)

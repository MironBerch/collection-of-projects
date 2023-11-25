from rest_framework.authentication import TokenAuthentication


class TokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

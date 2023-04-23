from rest_framework_simplejwt.tokens import RefreshToken


def generateToken(tokenType,user):
    data = {}
    refresh = RefreshToken.for_user(user)
    if tokenType == 'ACCESS_TOKEN':
        data['access_token'] = str(refresh.access_token)
    else:
        data['refresh_token'] = str(refresh)
    return data




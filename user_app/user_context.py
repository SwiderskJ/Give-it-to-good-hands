def user(request):
    if not request.user:
        return {}

    return {
        'user': request.user,
    }

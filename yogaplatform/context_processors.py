from yoga.models import *

def studio(request):

    studio_list = []
    if request.user.is_authenticated:
        owned_studios = request.user.profile.owned_studios.all()
        invited_studios = request.user.profile.studio_invites.all()
        studio_list= owned_studios.union(invited_studios)
    print(studio_list)
    return {
        'all_studios': studio_list,
    }


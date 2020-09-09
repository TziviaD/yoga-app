from yoga.models import Studio

def studio(request):
    studio_list = []
    return {
        'all_studios': Studio.objects.all(),
    }


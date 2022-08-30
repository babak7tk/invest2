from ContractRecord.models import ContactRequest


def sidebar_items_count(request):
    all_requests_count_int = ContactRequest.objects.count()

    context = {
        'all_requests_count': all_requests_count_int
    }
    return context

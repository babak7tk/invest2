import datetime
from ContractRecord.models import ContactRequest
from Token.models import Service
from config.celery import app


@app.task()
def get_contract_requests_ime_result():
    now = datetime.datetime.now()
    today_name = now.strftime("%A")
    hour = now.hour

    if today_name in ['Thursday', 'Friday'] or hour < 8 or hour > 18:
        return

    service = Service.objects.filter(url='https://api.ime.co.ir/v2').first()

    print('--------------- ime requests response cron job ----------------')

    if service:
        approved_requests = ContactRequest.objects.filter(req_status='30')
        for item in approved_requests:
            if service.token:
                item.user_code = '123'
                item.ime_code_date = '2012-10-15'
                item.req_status = '40'
                item.save()

        print('Done.........')

    # if service:
    #     approved_requests = ContactRequest.objects.filter(req_status='30')
    #     headers = {
    #         'Authorization': f'Bearer {service.token}',
    #         'Content-Type': 'application/json'
    #     }
    #
    #     for item in approved_requests:
    #         response = requests.get(url=service.url + f'/spot/CustomerRequests/{item.request_id}', headers=headers)
    #         if response.status_code == 200:
    #             response = response.json()
    #             if response.get('response').get('responseStatusId'):
    #                 item.user_code = response.get('response').get('responseStatusId')
    #                 item.ime_code_date = response.get('response').get('createDate')
    #                 item.req_status = '40'
    #                 item.save()

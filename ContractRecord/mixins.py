from Sms.helpers import send_sms
from crum import get_current_request


class ContactRequestLoggerMixin:
    def create_new_log(self, process_step, action_type, action, functor, req_ob):
        from ContractRecord.models import ContactRequestLogs
        ContactRequestLogs.objects.create(
            user=get_current_request().user, process_step=process_step,
            request=req_ob,
            action_type=action_type, action=action,
            functor=functor
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_req_status = self.req_status

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_complete and self.last_req_status != self.req_status:
            if self.req_status in ['10', '21']:
                self.create_new_log('request_pending', 'sms', 'request_pending_sms', 'system', self)
                self.create_new_log('request_pending', 'review_admin', 'request_pending', 'admin', self)

                msg = f'اطلاعات شما با موفقیت ثبت شد و مدیران پس از بررسی وضعیت آن را تعیین میکنند.'
                send_sms(self.user.phone, msg)

            elif self.req_status == '20':
                self.create_new_log('request_reject', 'sms', 'request_reject_sms', 'system', self)
                self.create_new_log('request_reject', 'review_user', 'request_reject', 'user', self)

                msg = f'{self.reason_of_reject}'
                send_sms(self.user.phone, msg)

            elif self.req_status == '30':
                self.create_new_log('request_approved', 'review_admin', 'request_approved', 'admin', self)

            elif self.req_status == '40':
                send_sms(self.user.phone, self.reason_of_approved)
                self.create_new_log('request_full_approved', 'review_admin', 'request_full_approved', 'system', self)
                self.create_new_log('request_full_approved', 'review_admin', 'request_full_approved_code', 'admin', self)
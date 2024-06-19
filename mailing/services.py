import smtplib
from datetime import datetime, timezone, timedelta
from django.core.mail import send_mail
from mailing.models import Mailing, Logs
from config.settings import EMAIL_HOST_USER


def change_mailing_status(mailing):
    dict_periodicity = {
        'Один раз': 0,
        'Ежедневно': 1,
        'Еженедельно': 7,
        'Ежемесячно': 30
    }
    periodicity = dict_periodicity[mailing.periodicity]
    if periodicity == 0:
        mailing.status = mailing.StatusOfMailing.FINISHED
    else:
        mailing_last = mailing.sent_time + timedelta(days=periodicity)
        if mailing_last > mailing.data_mailing_finish:
            mailing.status = mailing.StatusOfMailing.FINISHED
        else:
            mailing.sent_time = mailing_last
            mailing.status = mailing.StatusOfMailing.LAUNCHED
    mailing.save()


def start_mailing():
    now = datetime.now(timezone.utc)
    mailing_list = Mailing.objects.filter(sent_time__lte=now, status__in=[Mailing.StatusOfMailing.CREATED,
                                                                          Mailing.StatusOfMailing.LAUNCHED])
    for mailing in mailing_list:
        title = mailing.message.letter_subject
        message = mailing.message.letter_body
        client_list = mailing.client_mailing.all()
        for client in client_list:
            data_send = datetime.now(timezone.utc)
            try:
                send_mail(
                    subject=title,
                    message=message,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False)
                answer_server = 'Отправлено'
                status = Logs.StatusOfLogs.SUCCESS
            except smtplib.SMTPResponseException as error:
                answer_server = str(error)
                status = Logs.StatusOfLogs.FAILED
            finally:
                add_log_mailing(mailing, data_send, status, answer_server)
        change_mailing_status(mailing)


def add_log_mailing(mailing, data_send, status, answer_server):
    Logs.objects.create(
        mailing=mailing,
        datatime=data_send,
        status=status,
        answer_server=answer_server,
    )

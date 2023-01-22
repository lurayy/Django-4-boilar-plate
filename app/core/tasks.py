from os import path, makedirs
from core.celery import celery_app
from django.utils.timezone import now
from django.core.mail import send_mail

from django.conf import settings
from django.core import management
from django.utils.text import slugify


def get_path(e_path):
    file_path = f"{e_path}/{str(now().date())}/"
    if path.exists(file_path):
        return file_path
    makedirs(file_path)
    return file_path


@celery_app.task
def write_log_file(log_type, msg, is_error=False):
    file_name = 'yield'
    if is_error:
        file_name = 'error'
    file = f"{get_path('logs/'+log_type)}/{file_name}.log"

    with open(file, 'a', encoding='utf-8') as file_:
        file_.write(f"{now()} : {msg}\n")


@celery_app.task
def push_email(email_to, subject, message=None, html=None, obj=None):
    res = send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER, [email_to],
                    html_message=html)
    if res:
        if obj:
            obj.email_sent = True
            obj.email_timestamp = now()
            obj.save()
    else:
        write_log_file.delay('app/email', f"Failed To Send Email, {obj}", True)


@celery_app.task
def dump_database():
    path_to = f'{get_path("backups")}/{slugify(str(now()))}.json'
    with open(path_to, 'w', encoding='utf-8') as file_:
        write_log_file('app/backup',
                       f'Starting data load process . . . : {str(now())}')
        management.call_command('dumpdata',
                                exclude=[
                                    'auth.permission', 'contenttypes',
                                    'admin.LogEntry', 'sessions'
                                ],
                                indent=2,
                                stdout=file_)
        write_log_file('app/backup',
                       f'Completed dumping process . . . : {str(now())}')


@celery_app.task
def restore_database(file_path):
    write_log_file('app/restore',
                   f'Starting data load process . . . : {str(now())}')
    management.call_command('flush', '--no-input')
    management.call_command('loaddata', f'{file_path}')
    write_log_file('app/restore',
                   f'Data load process completed. : {str(now())}')

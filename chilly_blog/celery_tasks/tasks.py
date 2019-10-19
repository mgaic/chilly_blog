from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

# 创建celery应用对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/4')


@app.task
def send_register_success_email(receiver, user_name):
    print("发送邮件")
    subject = "亲爱的用户{}, 恭喜您注册chilly博客成功".format(user_name) #title
    message = "亲爱的用户{}, 恭喜您注册chilly博客成功".format(user_name)  #content
    from_email = settings.EMAIL_HOST_USER
    rec = ["1978912861@qq.com"]  #测试, 应为 receiver
    send_mail(subject, message, from_email,  rec )


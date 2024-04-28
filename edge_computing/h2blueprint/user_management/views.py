from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import user_management
from .forms import LoginForm
import re
import os
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


# Create your views here.
def send_mail(request):
    if request.method == 'GET':
        id = os.environ.get('PROJECT_EMAIL_ID')
        pw = os.environ.get('PROJECT_EMAIL_PW')
        email = os.environ.get('PROJECT_EMAIL_LINK')
        processing_mail(send_from=email, send_to=['kxc929@naver.com', 'kxc929@naver.com'],
                subject='h2blueprint 이메일 인증', message=f'<h1>안녕하세요</h1>{id}입니다', files=[os.path.join('static/','등수.png')],
                mtype='html', server='smtp.naver.com', userid=id, userpassword=pw)
        
        return redirect('https://mail.naver.com')


def processing_mail(send_from, send_to, subject, message, mtype='plain', files=[],
              server="localhost", port=587, userid='', userpassword='',
              use_tls=True):
    
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, mtype))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment', filename=Path(path).name)
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(userid, userpassword)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


def home(request):
    return render(request, 'home.html')


def passwordchange(request):
    if request.session.get('user'):
        if request.method == 'POST':
            userpassword = request.POST.get('userpassword', None)
            re_userpassword = request.POST.get('re-userpassword', None)
            userpassword = str(userpassword)
            re_userpassword = str(re_userpassword)

            res_data = {}

            if not (userpassword and re_userpassword):
                res_data['error'] = '모든 값을 입력해야합니다.'
            elif userpassword != re_userpassword:
                res_data['error'] = '비밀번호가 다릅니다.'
            else:
                userpassword_valid = check(userpassword)
                temp = user_management.objects.filter(id=request.session['user']).last()
                if userpassword_valid == True:
                    if not check_password(userpassword, temp.userpassword):
                        temp.userpassword = make_password(userpassword)
                        temp.save()

                        return redirect('/')
                    else:
                        res_data['error'] = '이전 비밀번호와 같습니다.'
                elif userpassword_valid == False:
                    if userpassword == temp.userid:
                        res_data['error'] = '비밀번호가 사용자 이름과 같습니다.'
                    else:
                        res_data['error'] = '9자리 이상 숫자, 특수문자, 소문자, 대문자로 해주세요.'

            return render(request, 'passwordchange.html', res_data)
        else:
            return render(request, 'passwordchange.html')
    else:
        return render(request, 'passwordchange.html')


def logout(request):
    if request.session.get('user'):
        del (request.session['user'])
        
    return redirect('/')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = user_management.objects.get(pk=form.user_id)

            if user.login_judge == "success":
                request.session['user'] = form.user_id

                return redirect('/')
            elif user.login_judge == "fail":
                form = LoginForm(request.POST)
                
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def check(userpassword):
    PT = []
    PT.append(re.compile('^(?=.*[A-Z])(?=.*[a-z])[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile('^(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile(
        '^(?=.*[A-Z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{9,}$'))

    PT.append(re.compile('^(?=.*[a-z])(?=.*[A-Z])[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile('^(?=.*[a-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile(
        '^(?=.*[a-z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{9,}$'))

    PT.append(re.compile('^(?=.*\d)(?=.*[A-Z])[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile('^(?=.*\d)(?=.*[a-z])[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile('^(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{9,}$'))

    PT.append(re.compile('^(?=.*[!@#$%^&*])(?=.*\d)[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile(
        '^(?=.*[!@#$%^&*])(?=.*[a-z])[A-Za-z\d!@#$%^&*]{9,}$'))
    PT.append(re.compile(
        '^(?=.*[!@#$%^&*])(?=.*[A-Z])[A-Za-z\d!@#$%^&*]{9,}$'))

    for num in range(len(PT)):
        if re.match(PT[num], userpassword):
            return True
    return False


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        userid = request.POST.get('userid', None)
        useremail = request.POST.get('useremail', None)
        userpassword = request.POST.get('userpassword', None)
        re_userpassword = request.POST.get('re-userpassword', None)

        res_data = {}

        if not (userid and useremail and userpassword and re_userpassword):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif userpassword != re_userpassword:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            userpassword_valid = check(userpassword)
            if userpassword_valid == True:
                if userpassword != userid:
                    userid = str(userid)
                    userpassword = str(userpassword)

                    temp = user_management.objects.filter(userid=userid)
                    if temp:
                        res_data['error'] = '다시 생성해주세요.'
                        return render(request, 'register.html', res_data)

                    temp = user_management.objects.filter(useremail=useremail)
                    if temp:
                        res_data['error'] = '다시 생성해주세요.'
                        return render(request, 'register.html', res_data)

                    for word in ['|', ';', '&', ':', '>', '<', '`', '\\', '!', '/']:
                        if word in userid:
                            res_data['error'] = '|, ;, &, :, >, <, `, \, !, / 을 제외한 문자로 아이디를 만들어주세요.'

                            return render(request, 'register.html', res_data)

                    user = user_management(
                        userid=userid,
                        useremail=useremail,
                        userpassword=make_password(userpassword),
                    )
                    user.save()
                    return redirect('/')

                elif userpassword == userid:
                    res_data['error'] = '비밀번호가 사용자 이름과 같습니다.'
            elif userpassword_valid == False:
                if userpassword == userid:
                    res_data['error'] = '비밀번호가 사용자 이름과 같습니다.'
                else:
                    res_data['error'] = '9자리 이상 숫자, 특수문자, 소문자, 대문자로 해주세요.'

        return render(request, 'register.html', res_data)

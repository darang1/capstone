from django import forms
from .models import user_management
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    userid = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        },
        max_length=128, label="사용자 이름")
    userpassword = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, max_length=128, label="비밀번호")

    def clean(self):
        cleaned_data = super().clean()
        userid = cleaned_data.get('userid')
        userpassword = cleaned_data.get('userpassword')

        if userid and userpassword:
            userid = str(userid)
            userpassword = str(userpassword)

            try:
                user = user_management.objects.get(userid=userid)
            except user_management.DoesNotExist:
                self.add_error('userid', '다시 입력해주세요.')
                return

            fail = user_management.objects.get(userid=userid)
            if not check_password(userpassword, user.userpassword):
                fail.fail_account_count += 1
                fail.save()

                if fail.login_judge == 'success':
                    if fail.fail_account_count >= 3:
                        fail.login_judge = 'fail'
                        self.user_login_judge = fail.login_judge
                        self.user_id = user.id
                        fail.save()
                    else:
                        self.add_error('userpassword', '다시 입력해주세요.')
                elif fail.login_judge == 'fail':
                    self.user_login_judge = fail.login_judge
                    self.user_id = user.id
                    self.add_error('userpassword', '계정이 잠겼습니다. 관리자한테 연락바랍니다.')

            elif fail.login_judge == 'fail':
                self.user_login_judge = fail.login_judge
                self.user_id = user.id
                self.add_error('userpassword', '계정이 잠겼습니다. 관리자한테 연락바랍니다.')

            elif fail.login_judge == 'success':
                fail.fail_account_count = 0
                fail.save()
                self.user_id = user.id

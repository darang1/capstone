from django.db import models

# Create your models here.
class server_connection(models.Model):
    server_ip = models.GenericIPAddressField(protocol='IPv4', unpack_ipv4=False, 
                                            max_length=32, verbose_name='서버 IP')
    server_port = models.CharField(max_length=32,
                                  verbose_name='서버 PORT')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')
    fail_account_count = models.IntegerField(default = 0, verbose_name='서버 연결 실패 횟수')
    server_judge = models.CharField(max_length=16,
                                default='success', verbose_name='잠금 상태')
    
    def __str__(self):
        return self.server_ip

    class Meta:
        db_table = 'server_connection'
        verbose_name = '서버 연결'
        verbose_name_plural = '서버 연결'

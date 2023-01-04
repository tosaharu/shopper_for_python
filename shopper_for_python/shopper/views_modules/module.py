from ..models import *
import datetime
from random import randint


# エリア情報をコンテキストに入力


def get_area_contexts(context):
    context['regions'] = Region.objects.all()
    context['prefectures'] = Prefecture.objects.all()
    # djangoの全件取得は件数が多いとかなり重いので避ける
    # context['areas'] = Area.objects.all()

# 年月日をDate型に変換する


def convert_YMD_to_DATE(year, month, day):
    birthdaySTR = year + '-' + month + '-' + day + ' 00:00:00'
    birthdayDATETIME = datetime.datetime.strptime(
        birthdaySTR, '%Y-%m-%d %H:%M:%S')
    birthdayDATE = datetime.date(
        birthdayDATETIME.year, birthdayDATETIME.month, birthdayDATETIME.day)
    return birthdayDATE

# 6桁数字のワンタイムパスワードを発行する


def create_onetime_password():
    dig1 = str(randint(0, 9))
    dig2 = str(randint(0, 9))
    dig3 = str(randint(0, 9))
    dig4 = str(randint(0, 9))
    dig5 = str(randint(0, 9))
    dig6 = str(randint(0, 9))
    return dig1 + dig2 + dig3 + dig4 + dig5 + dig6

import bs4
import requests
from bs4 import BeautifulSoup
import time
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.views.generic import TemplateView

from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .forms import U_RegisterUserForm
from .views_modules.module import *
from django.core.mail import send_mail
import datetime
import json

# from selenium import webdriver
# import chromedriver_binary
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.add_argument('--headless')
# options.add_argument("--no-sandbox")
# Create your views here.

# トップページ


class IndexView(TemplateView):
    print('トップページ')
    template_name = "shopper/index.html"


# 選択された都道府県に応じたエリア選択肢を返すajax


class Ajax_GetArea(View):
    def get(self, request):
        print('選択された都道府県に応じたエリア選択肢を返すajax')

        html = '<option value="" selected="selected">エリアを選択してください</option>'
        # リクエストパラメーター取得

        try:
            prefecture = int(request.GET['prefecture'])
        except ValueError:
            return HttpResponse(html)

        print(prefecture)

        # エリア取得用セッションの更新
        selected_prefecture_areas = Area.objects.filter(
            prefecture=Prefecture.objects.get(id=prefecture))
        print(selected_prefecture_areas)

        for selected_prefecture_area in selected_prefecture_areas:
            html += '<option value="'
            html += str(selected_prefecture_area.id)
            html += '">'
            html += selected_prefecture_area.name
            html += '</option>'
        print(html)

        return HttpResponse(html)

# 選択されたエリアに応じた店舗選択肢を返すajax


class Ajax_GetStore(View):
    def get(self, request):
        print('選択されたエリアに応じた店舗選択肢を返すajax')

        html = '<option value="" selected="selected">店舗を選択してください</option>'
        # リクエストパラメーター取得

        try:
            area = int(request.GET['area'])
        except ValueError:
            return HttpResponse(html)

        print(area)

        # エリア取得用セッションの更新
        selected_area_stores = Store.objects.filter(
            area=Area.objects.get(id=area))
        print(selected_area_stores)

        for selected_area_store in selected_area_stores:
            html += '<option value="'
            html += str(selected_area_store.id)
            html += '">'
            html += selected_area_store.name
            html += '</option>'
        print(html)

        return HttpResponse(html)


# 新規会員登録処理


class U_RegisterUserView(View):
    def get(self, request):
        print('新規会員登録画面')
        context = {}
        get_area_contexts(context)

        # セッションの中身を確認
        if 'user' in request.session:
            return redirect('u_Main')

        return render(request, 'shopper/u_RegisterUser.html', context)

    def post(self, request):
        print('新規会員登録実行')
        context = {}
        get_area_contexts(context)

        # リクエストパラメーター取得
        email = request.POST['email']
        name = request.POST['name']

        gender = int(request.POST['gender'])

        # modelの外部キーはオブジェクトで扱われているので下記のように記載する必要あり
        area = Area.objects.get(id=int(request.POST['area']))

        # 入力されたパスワードを取得し、ハッシュ化
        originalPass = request.POST['password']
        password = make_password(originalPass)

        # 入力された誕生日を取得
        year = request.POST['year']
        month = request.POST['month']
        day = request.POST['day']

        # 年月日をDate型に変換する
        birthdayDATE = convert_YMD_to_DATE(year, month, day)

        print(email)
        print(password)
        print(name)
        print(gender)
        print(area)
        print(birthdayDATE)

        user = User.objects.create(email=email, password=password, name=name,
                                   birthday=birthdayDATE, gender=gender, area=area, active_flag=1)

        # ログインユーザーをセッションに保存
        request.session['user'] = user

        # エリア選択はリストなので、リスト化
        area_list = []
        area_list.append(user.area)
        print(area_list)
        print(area_list[0])

        # エリア選択の初期情報をセッションに保存
        request.session['tmp_areas'] = area_list

        return redirect('u_Main')


# メールアドレスがDBに登録済か確認するajax


class Ajax_CheckUserMail(View):
    def get(self, request):
        print('メールアドレスがDBに登録済か確認するajax')

        # 入力された情報を取得
        email = request.GET['email']

        # アドレスを使用しているユーザーデータを照会
        checked_users = User.objects.filter(email=email)
        result = len(checked_users)

        #  アドレスを使用しているユーザーが存在する場合
        if result == 1:

            # セッションの中身を確認
            if 'user' in request.session:
                user = request.session['user']

                # 照会結果のユーザーとセッションユーザーが同じ場合
                if user.id == checked_users[0].id:
                    result = 0

        # 登録済のメールアドレス有り:result=1
        # 登録済のメールアドレス無し、または自分のメールアドレスの場合:result=0
        return HttpResponse(result)


# ログイン


class U_LoginView(View):
    def get(self, request):
        print('ログイン画面')

        # セッションの中身を確認
        if 'user' in request.session:
            return redirect('u_Main')

        return render(request, 'shopper/u_Login.html')

    def post(self, request):
        print('ログイン実行')
        context = {}

        # 入力されたメールアドレスとパスワードを取得
        email = request.POST['email']
        password = request.POST['password']
        users = User.objects

        if users.filter(email=email, active_flag=1).exists():
            user = users.get(email=email)

            if check_password(password, user.password):
                # ログインユーザーをセッションに保存
                request.session['user'] = user

                # エリア選択はリストなので、リスト化
                area_list = []
                area_list.append(user.area)
                print(area_list)
                print(area_list[0])

                # エリア選択の初期情報をセッションに保存
                request.session['tmp_areas'] = area_list

                return redirect('u_Main')

        context['errorMessage'] = "メールアドレスもしくはパスワードが正しくありません"
        return render(request, 'shopper/u_Login.html', context)


# メイン画面


class U_MainView(View):
    def get(self, request):
        print('メイン画面')
        context = {}
        get_area_contexts(context)

        # セッションの中身を確認
        if 'user' in request.session:

            # ログインセッションを取得
            user = request.session['user']
            areas = request.session['tmp_areas']

            # 投稿リスト取得
            lists = get_categorized_product_lists(request, user, areas)
            context['user_categorized_product_lists'] = lists['user']
            context['other_categorized_product_lists'] = lists['other']

            # ユーザーの投稿履歴を新しい順に取得
            user_product_list = Product.objects.filter(
                user=user.id).order_by('date').reverse()
            context['user_product_list'] = user_product_list

            # 重いのを解消するために追加
            request.session['selected_prefecture_areas'] = Area.objects.filter(
                prefecture=request.session['tmp_areas'][0].prefecture)

            # 選択済エリアを表示するための選択済エリアリスト（int）
            area_ids = []
            for tmp_area in request.session['tmp_areas']:
                print(tmp_area.id)
                area_ids.append(tmp_area.id)
            request.session['area_ids'] = area_ids
            print(request.session['area_ids'])

            return render(request, 'shopper/u_Main.html', context)

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html', context)


# 選択された都道府県に応じたエリア選択肢（複数選択対応）を返すajax


class Ajax_GetMultiSelectArea(View):
    def get(self, request):
        print('選択された都道府県に応じたエリア選択肢を返すajax')

        html = ''
        # リクエストパラメーター取得

        try:
            prefecture = int(request.GET['header_prefecture'])
        except ValueError:
            return HttpResponse(html)

        print(prefecture)

        # エリア取得用セッションの更新
        selected_prefecture_areas = Area.objects.filter(
            prefecture=Prefecture.objects.get(id=prefecture))
        request.session['selected_prefecture_areas'] = selected_prefecture_areas
        print(request.session['selected_prefecture_areas'][0].prefecture.name)

        for selected_prefecture_area in selected_prefecture_areas:
            html += '<li class="col-sm-6 col-xl-4 area_selection" onclick="ShowSelectedArea() "><label><input name="header_area" type="checkbox" value="'
            html += str(selected_prefecture_area.id)
            html += '"'
            if selected_prefecture_area.id in request.session['area_ids']:
                html += ' checked="checked" '
            html += '><span>'
            html += selected_prefecture_area.name
            html += '</span></label></li>'
        print(html)

        return HttpResponse(html)


# 選択されたエリアに応じた商品リストを返すajax


class Ajax_GetAreaProduct(View):
    def get(self, request):
        print('選択されたエリアに応じた商品リストを返すajax')

        # セッションの中身を確認
        if 'user' in request.session:

            user = request.session['user']

            # リクエストパラメーター取得
            header_areas = request.GET.getlist('header_areas[]')
            print(header_areas)

            # セッションの選択済エリアリスト
            request.session['tmp_areas'] = Area.objects.filter(
                id__in=header_areas)

            print(request.session['tmp_areas'])
            print(request.session['tmp_areas'][0])

            # 投稿リスト取得
            lists = get_categorized_product_lists(request, user, header_areas)
            user_categorized_product_lists = lists['user']
            other_categorized_product_lists = lists['other']

            html = display_categorized_product_lists(
                request, user_categorized_product_lists, other_categorized_product_lists)

            return HttpResponse(html)


# 選択されたソートに応じた商品リストを返すajax


class Ajax_GetSortedProduct(View):
    def get(self, request):
        print('選択されたソートに応じた商品リストを返すajax')

        # セッションの中身を確認
        if 'user' in request.session:

            # ログインセッションを取得
            user = request.session['user']
            areas = request.session['tmp_areas']

            # リクエストパラメーター取得
            sort = int(request.GET['sort'])
            print(sort)

            # セッションの選択済エリアリスト
            request.session['sort'] = sort
            print(request.session['sort'])

            # 投稿リスト取得
            lists = get_categorized_product_lists(request, user, areas)
            user_categorized_product_lists = lists['user']
            other_categorized_product_lists = lists['other']

            html = display_categorized_product_lists(
                request, user_categorized_product_lists, other_categorized_product_lists)

            return HttpResponse(html)


# 商品情報投稿


class U_RegisterProductView(View):
    def get(self, request):
        print('商品情報投稿画面')

        # セッションの中身を確認
        if 'user' in request.session:
            context = {}

            get_area_contexts(context)

            # 重いのを解消するために追加（メイン画面とは違い、登録されている都道府県のエリアで固定）
            context['selected_prefecture_areas'] = Area.objects.filter(
                prefecture=request.session['user'].area.prefecture)
            print(context['selected_prefecture_areas'])

            # 登録エリアに絞った店舗一覧の取得
            selected_area_stores = Store.objects.filter(
                area=request.session['user'].area)
            context['selected_area_stores'] = selected_area_stores

            # 大・中品目は廃止したので不要
            # main_item_list = MainItem.objects.all()
            # context['main_item_list'] = main_item_list
            # sub_item_list = SubItem.objects.all()
            # context['sub_item_list'] = sub_item_list

            # 品目一覧の取得
            item_list = Item.objects.all()
            context['item_list'] = item_list
            # 単位一覧の取得
            unit_list = Unit.objects.all()
            context['unit_list'] = unit_list

            return render(request, 'shopper/u_RegisterProduct.html', context)

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')

    def post(self, request):
        print('商品情報投稿')

        # セッションの中身を確認
        if 'user' in request.session:
            user = request.session['user']

            # 入力された各種データを取得
            date = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d')
            store = Store.objects.get(id=request.POST['store'])
            item = Item.objects.get(id=request.POST['item'])
            detail = request.POST['detail']
            price = int(request.POST['price'])
            amount = int(request.POST['amount'])
            discount = int(request.POST['discount'])
            comment = request.POST['comment']

            print(type(date))
            print(type(store))
            print(type(item))
            print(type(detail))
            print(type(price))
            print(type(amount))
            print(type(discount))
            print(type(comment))

            Product.objects.create(user=user, item=item, detail=detail, store=store,
                                   amount=amount, price=price, date=date, discount=discount, comment=comment)
            return redirect('u_Main')

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')


# 入力された店舗名をもとに店舗名をサジェストするajax


class Ajax_SearchStoreName(View):
    def get(self, request):
        print('入力された店舗名をもとに店舗名をサジェストするajax')

        suggestion_list = ""
        # 入力された各種データを取得
        store_area = request.GET['store_area']
        store_name = request.GET['store_name']

        url = "https://tokubai.co.jp/search?utf8=%E2%9C%93&latitude=&longitude=&from=&bargain_keyword="
        url += store_area
        url += "%E3%80%80"
        url += store_name
        print(url)

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        res = requests.get(url=url, headers=headers)

        print(res.status_code)

        if not res.ok:
            print("ページ取得失敗")
            return HttpResponse(suggestion_list)

        soup = BeautifulSoup(res.content, "html.parser")
        print(type(soup))
        element_list = soup.select('span.shop_name')
        print(type(element_list))
        print(element_list)

        for element in element_list:
            print(type(element))
            print(element)
            sp = element.span
            print(type(sp))
            print(sp)
            sp.extract()

            suggestion_list += '<option value="'
            suggestion_list += element.get_text()
            suggestion_list += '"></option>'

            print(element.get_text())

        print(suggestion_list)
        if not suggestion_list:
            element_list += '<option value="候補はありません"></option>'

        return HttpResponse(suggestion_list)


# 入力された店舗名をもとに店舗住所をサジェストするajax


class Ajax_SearchStoreAddress(View):
    def get(self, request):
        print('入力された店舗名をもとに店舗住所をサジェストするajax')

        suggestion_list = ""
        # 入力された各種データを取得
        store_area = request.GET['store_area']
        store_name = request.GET['store_name']

        url = "https://tokubai.co.jp/search?utf8=%E2%9C%93&latitude=&longitude=&from=&bargain_keyword="
        url += store_area
        url += "%E3%80%80"
        url += store_name
        print(url)

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        res = requests.get(url=url, headers=headers)

        print(res.status_code)

        if not res.ok:
            print("ページ取得失敗")
            return HttpResponse(suggestion_list)

        soup = BeautifulSoup(res.content, "html.parser")

        element_list = soup.select('.shop_address')
        for element in element_list:
            suggestion_list += '<option value="'
            suggestion_list += element.string
            suggestion_list += '"></option>'

            print(element.string)

        print(suggestion_list)
        if not suggestion_list:
            suggestion_list += '<option value="候補はありません"></option>'

        return HttpResponse(suggestion_list)


# 店舗がDBに登録済か確認するajax


class Ajax_CheckStore(View):
    def get(self, request):
        print('店舗がDBに登録済か確認するajax')

        # 入力された情報を取得
        store_name = request.GET['store_name']

        # 店舗名からスペースを除去
        removed_store_name = store_name.replace(" ", "").replace("　", "")
        print(removed_store_name)

        # 店舗データを照会
        checked_stores = Store.objects.filter(name=removed_store_name)

        # store_idが送られてきている（店舗情報編集からの送信）場合は、編集中の店舗を類似リストから除外
        store_id = int(request.GET['store_id'])
        if store_id > 0:
            print('現在の店舗情報を除外！')
            checked_stores = checked_stores.exclude(id=store_id)

        print(checked_stores)

        result = len(checked_stores)

        # 登録済の品目有り:result>=1
        # 登録済の品目無し:result=0
        return HttpResponse(result)

# 類似店舗をチェックして返すajax


class Ajax_CheckSimilarStoreInfo(View):
    def get(self, request):
        print('類似店舗をチェックして返すajax')

        # 送られてきたデータを取得
        store_name = request.GET['store_name']
        # スペースで区切られているはずの会社名・店舗名をそれぞれ取得
        store_keywords = store_name.split()
        print(store_keywords)

        # キーワードを全て含む店名リストを取得する
        similar_store_list = Store.objects.all()
        for store_keyword in store_keywords:
            similar_store_list = similar_store_list.filter(
                name__contains=store_keyword)

        # store_idが送られてきている（店舗情報編集からの送信）場合は、編集中の店舗を類似リストから除外
        store_id = int(request.GET['store_id'])
        if store_id > 0:
            print('現在の店舗情報を除外！')
            similar_store_list = similar_store_list.exclude(id=store_id)

        print(similar_store_list)

        json_encode = []
        for similar_store in similar_store_list:
            json_encode.append(similar_store.name)

        print(json_encode)

        return JsonResponse(json_encode, safe=False)


# 店舗情報を新規登録するajax


class Ajax_RegisterStoreInfo(View):
    def post(self, request):
        print('店舗情報を新規登録するajax')

        user = request.session['user']

        # 入力された各種データを取得
        store_name = request.POST['store_name']
        store_area = Area.objects.get(id=request.POST['store_area'])
        store_address = request.POST['store_address']
        store_start_hour = request.POST['store_start_hour']
        print(store_start_hour)
        store_end_hour = request.POST['store_end_hour']
        store_URL = request.POST['store_URL']
        store_tel = request.POST['store_tel']
        store_payment = request.POST['store_payment']
        store_facility = request.POST['store_facility']
        store_service = request.POST['store_service']

        # DB側でnullが許されず、ユーザーが入力しない値
        store_corporation_flag = 0
        store_open_flag = 0

        # 店舗名からスペースを除去
        # removed_store_name = store_name.replace(" ", "").replace("　", "")
        # print(removed_store_name)

        store = Store.objects.create(name=store_name, area=store_area, address=store_address, start_hour=store_start_hour, end_hour=store_end_hour,
                                     url=store_URL, tel=store_tel, payment=store_payment, facility=store_facility, service=store_service, administrated_flag=store_corporation_flag, open_flag=store_open_flag)
        return HttpResponse(store.id)


# 品目がDBに登録済か確認するajax


class Ajax_CheckItem(View):
    def get(self, request):
        print('品目がDBに登録済か確認するajax')

        # 入力された情報を取得
        item_name = request.GET['item_name']

        try:
            item_unit = int(request.GET['item_unit'])
        except ValueError:
            return HttpResponse(999)

        # 品目データを照会
        checked_items = Item.objects.filter(name=item_name, unit=item_unit)
        result = len(checked_items)

        # 登録済の品目有り:result>=1
        # 登録済の品目無し:result=0
        return HttpResponse(result)

# 類似品目をチェックして返すajax


class Ajax_CheckSimilarItemInfo(View):
    def get(self, request):
        print('類似品目をチェックして返すajax')

        item_name = request.GET['item_name']

        similar_item_list = Item.objects.filter(name__contains=item_name)
        print(similar_item_list)

        json_encode = []
        for similar_item in similar_item_list:
            json_encode.append(similar_item.name+" /"+similar_item.unit.name)

        print(json_encode)

        return JsonResponse(json_encode, safe=False)


# 品目情報を新規登録するajax


class Ajax_RegisterItemInfo(View):
    def post(self, request):
        print('品目情報を新規登録するajax')

        # 入力された各種データを取得
        item_name = request.POST['item_name']
        print(item_name)

        # filterはインスタンスでなくてもいけたが、createはさすがに無理か・・・？　⇒やっぱり無理
        item_unit = Unit.objects.get(id=request.POST['item_unit'])
        # item_unit = int(request.POST['item_unit'])
        print(item_unit)

        item = Item.objects.create(name=item_name, unit=item_unit)
        print(item)
        return HttpResponse(item.id)

# 店舗情報


class U_StoreInfoView(View):
    def get(self, request, store_id):
        print('店舗情報画面')
        context = {}
        get_area_contexts(context)

        store = Store.objects.get(id=store_id)
        context['store'] = store
        context['coupon_list'] = Coupon.objects.filter(store=store)
        context['flyer_list'] = Flyer.objects.filter(store=store)
        context['recipe_list'] = Recipe.objects.filter(store=store)

        # 店舗が存在する都道府県のエリアリストを取得する
        context['stores_prefecture_areas'] = Area.objects.filter(
            prefecture=store.area.prefecture)
        print(context['stores_prefecture_areas'])

        return render(request, 'shopper/u_StoreInfo.html', context)

    def post(self, request, store_id):
        # 入力された各種データを取得
        store_name = request.POST['store_name']
        store_area = Area.objects.get(id=request.POST['store_area'])
        store_address = request.POST['store_address']
        store_start_hour = request.POST['store_start_hour']
        print(store_start_hour)
        store_end_hour = request.POST['store_end_hour']
        store_URL = request.POST['store_URL']
        store_tel = request.POST['store_tel']
        store_payment = request.POST['store_payment']
        store_facility = request.POST['store_facility']
        store_service = request.POST['store_service']

        # 店舗名からスペースを除去
        removed_store_name = store_name.replace(" ", "").replace("　", "")
        print(removed_store_name)

        result = Store.objects.filter(id=store_id).update(name=removed_store_name, area=store_area, address=store_address, start_hour=store_start_hour, end_hour=store_end_hour,
                                                          url=store_URL, tel=store_tel, payment=store_payment, facility=store_facility, service=store_service)
        # result=0の失敗が発生するようであれば、失敗したとき用の処理も用意する

        context = {}
        get_area_contexts(context)

        store = Store.objects.get(id=store_id)
        context['store'] = store
        context['coupon_list'] = Coupon.objects.filter(store=store)
        context['flyer_list'] = Flyer.objects.filter(store=store)
        context['recipe_list'] = Recipe.objects.filter(store=store)

        # 店舗が存在する都道府県のエリアリストを取得する
        context['stores_prefecture_areas'] = Area.objects.filter(
            prefecture=store.area.prefecture)
        print(context['stores_prefecture_areas'])
        return render(request, 'shopper/u_StoreInfo.html', context)

# 店舗情報編集


class U_EditStoreInfoView(View):
    def get(self, request, id):
        print('店舗情報編集画面')
        context = {}

        store_id = id
        store = Store.objects.get(id=store_id)
        context['store'] = store
        # context['coupon_list'] = Coupon.objects.filter(store=store)
        # context['flyer_list'] = Flyer.objects.filter(store=store)
        # context['recipe_list'] = Recipe.objects.filter(store=store)

        return render(request, 'shopper/u_EditStoreInfo.html', context)

    def post(self, request):
        print('商品情報投稿')
        context = {}
        get_area_contexts(context)


# ユーザー情報変更画面表示


class U_ChangeInfoView(View):
    def get(self, request):
        print('ユーザー情報変更画面')

        # セッションの中身を確認
        if 'user' in request.session:
            user = request.session['user']

            context = {}
            get_area_contexts(context)

            # 重いのを解消するために追加（メイン画面とは違い、登録されている都道府県のエリアで固定）
            context['selected_prefecture_areas'] = Area.objects.filter(
                prefecture=request.session['user'].area.prefecture)
            print(context['selected_prefecture_areas'])

            return render(request, 'shopper/u_ChangeInfo.html', context)

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')


# ユーザーの誕生日を取得するajax


class Ajax_GetUserBirthday(View):
    def get(self, request):
        print('ユーザーの誕生日を取得するajax')

        data = {}

        if 'user' in request.session:
            user = request.session['user']
            data = {
                'year': user.birthday.year,
                'month': user.birthday.month,
                'day': user.birthday.day
            }

        return JsonResponse(data)


# ユーザーの情報を変更するajax


class Ajax_ChangeUserInfo(View):
    def post(self, request):
        print('ユーザーの情報を変更するajax')

        # 入力された情報を取得
        email = request.POST['email']
        name = request.POST['name']
        gender = int(request.POST['gender'])
        area = Area.objects.get(id=int(request.POST['area']))

        # セッションを取得
        user = request.session['user']

        # ユーザーデータを更新
        result = User.objects.filter(id=user.id).update(
            email=email, name=name, gender=gender, area=area)

        print(result)

        # 正常にアップデートできた場合は result = 1
        if result == 1:
            # userインスタンス更新
            user.email = email
            user.name = name
            user.gender = gender
            user.area = area

            # ユーザーセッションを更新
            request.session['user'] = user

            print(request.session['user'])
            print(request.session['user'].gender)

            # エリア選択セッションを更新
            # エリア選択はリストなので、リスト化
            area_list = []
            area_list.append(user.area)
            print(area_list)
            print(area_list[0])

            # エリア選択の初期情報をセッションに保存
            request.session['tmp_areas'] = area_list

        return HttpResponse(result)


# ユーザーのパスワードを変更するajax


class Ajax_ChangeUserPassword(View):
    def post(self, request):
        print('ユーザーのパスワードを変更するajax')

        # 入力された旧パスワードを取得
        password = request.POST['password']

        result = 0

        # セッションの確認
        if 'user' in request.session:

            # セッションを取得
            user = request.session['user']
            if check_password(password, user.password):

                # 入力された新パスワードを取得し、ハッシュ化
                originalPass = request.POST['newpassword']
                newpassword = make_password(originalPass)

                # ユーザーデータを更新
                result = User.objects.filter(
                    id=user.id).update(password=newpassword)

                # 正常にアップデートできた場合は result = 1
                if result == 1:

                    # セッションを更新
                    user.password = newpassword
                    request.session['user'] = user

            else:
                # パスワードが一致しない場合
                result = 9

        # セッション切れの場合

        return HttpResponse(result)

# ログアウト処理


class U_LogoutView(View):
    def get(self, request):
        print('ログアウト画面')

        # セッション破棄
        request.session.flush()

        return render(request, 'shopper/u_Logout.html')

# パスワード紛失時の再設定認証処理


class U_ResetPasswordAuthView(View):
    def get(self, request):
        print('パスワード再設定認証画面1')
        return render(request, 'shopper/u_ResetPasswordAuth1.html')

    def post(self, request):
        print('パスワード再設定認証画面2')
        # ワンタイムパスワードの生成
        onetime_password = create_onetime_password()

        # 入力されたメールアドレスを取得
        email = request.POST['email']

        # パスワードをメールで送信
        subject = "ワンタイムパスワード送信"
        message = onetime_password
        from_email = "shopper.webmaster2271@gmail.com"
        to = [email, ]
        send_mail(subject, message, from_email, to)

        # パスワードをセッションに保存
        request.session['onetime_password'] = onetime_password
        return render(request, 'shopper/u_ResetPasswordAuth2.html')


# 入力されたメールアドレスが存在し、誕生日が登録情報と合致するかをチェックするajax


class Ajax_CheckUserMailAndBirthday(View):
    def post(self, request):
        print('メールアドレスと誕生日を確認するajax')

        # リクエストパラメーター取得
        email = request.POST['email']

        # 入力された誕生日を取得
        year = request.POST['year']
        month = request.POST['month']
        day = request.POST['day']

        # 年月日をDate型に変換する
        birthdayDATE = convert_YMD_to_DATE(year, month, day)

        # 該当ユーザーの存在をチェック
        result = len(User.objects.filter(
            email=email, birthday=birthdayDATE, active_flag=1))

        if result == 1:
            print('一致するデータを1件確認')

            # ユーザー情報をセッションに保存
            request.session['change_password_user'] = User.objects.get(
                email=email, birthday=birthdayDATE)

        print(result)
        return HttpResponse(result)


# ワンタイムパスワードをチェックするajax


class Ajax_CheckOneTimePass(View):
    def post(self, request):
        print('ワンタイムパスワードをチェックするajax')

        # リクエストパラメーター取得
        input_onetime_password = request.POST['onetime_password']

        # セッションにパスワード保存されているか確認
        if 'onetime_password' in request.session:
            # パスワードをセッションから取得
            correct_onetime_password = request.session['onetime_password']

            if input_onetime_password == correct_onetime_password:
                # パスワード一致の場合
                return HttpResponse(2)

            # パスワード不一致の場合
            return HttpResponse(1)

        # セッション切れの場合
        return HttpResponse(0)

# パスワード紛失時のパスワードリセット処理


class U_ResetPasswordView(View):
    def get(self, request):
        print('パスワード再設定画面')
        return render(request, 'shopper/u_ResetPassword.html')

    def post(self, request):
        # セッションの確認
        if 'change_password_user' in request.session:
            # ユーザー情報をセッションから取得
            change_password_user = request.session['change_password_user']

            originalPass = request.POST['newpassword']
            password = make_password(originalPass)

            # ユーザーデータを更新
            result = User.objects.filter(
                id=change_password_user.id).update(password=password)

            if result == 1:
                # 対象の1件が正常にアップデートされた場合
                return render(request, 'shopper/u_ResetPasswordComplete.html')

            # アップデートが何かしらの理由でできなかった場合
            # あまりなさそうなので一旦保留

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')


# セッション切れの際に飛ぶページ


class U_SessionExpiredView(View):
    def get(self, request):
        return render(request, 'shopper/u_SessionExpired.html')


# 退会処理


class U_QuitView(View):
    def get(self, request):
        print('退会確認画面')

        # セッションの確認
        if 'user' in request.session:
            return render(request, 'shopper/u_QuitConfirm.html')

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')

    def post(self, request):
        # セッションの確認
        if 'user' in request.session:

            # ユーザー情報をセッションから取得
            user = request.session['user']

            # ユーザーデータを更新
            result = User.objects.filter(
                id=user.id).update(active_flag=0)

            if result == 1:
                # 対象の1件が正常にアップデートされた場合
                request.session.flush()

                return render(request, 'shopper/u_QuitComplete.html')

            # アップデートが何かしらの理由でできなかった場合
            # あまりなさそうなので一旦保留

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')


# お問い合わせ


class U_InquiryView(View):
    def get(self, request):
        print('お問い合わせ画面')

        return render(request, 'shopper/u_Inquiry.html')

    def post(self, request):
        print('お問い合わせ投稿')

        # セッションの確認
        if 'user' in request.session:

            # 送られてきたデータを取得
            type = int(request.POST['type'])
            text = request.POST['text']
            email = request.POST['email']

            # セッションからユーザーインスタンスを取得
            user = request.session['user']

            Inquiry.objects.create(user=user, type=type,
                                   text=text, email=email)

            return render(request, 'shopper/u_InquiryComplete.html')

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')

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

        User.objects.create(email=email, password=password, name=name,
                            birthday=birthdayDATE, gender=gender, area=area, active_flag=1)
        return render(request, 'shopper/u_Main.html', context)


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

            user = request.session['user']

            # ユーザーが投稿したことのある品目をリスト化(queryset)
            posted_item_list = Product.objects.filter(
                user=user.id).values_list('item').distinct()
            print(posted_item_list)

            # 選択中のエリアにある店舗をリスト化(queryset)
            area_store_list = Store.objects.filter(
                area__in=request.session['tmp_areas']).values_list('id')
            print(area_store_list)

            # queryset ではなくlistにする場合はこちら
            # product_list = [data.id for data in product_queryset]

            user_categorized_product_lists = []
            other_categorized_product_lists = []

            # リストの品目ごとに、
            for posted_item in posted_item_list:
                print(posted_item)
                # ユーザー自身の投稿を安い順に5件取得する
                user_categorized_product_list = Product.objects.filter(
                    item=posted_item, user=user.id).order_by('price')[:5]

                user_categorized_product_lists.append(
                    user_categorized_product_list)

                # 選択中のエリア内の他ユーザーの投稿を安い順に5件取得する
                other_categorized_product_list = Product.objects.filter(
                    item=posted_item, store__in=area_store_list).exclude(user=user.id).order_by('price')[:5]

                other_categorized_product_lists.append(
                    other_categorized_product_list)

            print(user_categorized_product_lists)
            print(other_categorized_product_lists)

            # 表示テスト
            # for user_categorized_product_list in user_categorized_product_lists:
            #     print(user_categorized_product_list[0].item.name)

            #     for user_categorized_product in user_categorized_product_list:
            #         print(user_categorized_product.detail)
            #         print(user_categorized_product.price)
            #         print(user_categorized_product.store.name)

            context['user_categorized_product_lists'] = user_categorized_product_lists
            context['other_categorized_product_lists'] = other_categorized_product_lists

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

            # ユーザーが投稿したことのある品目をリスト化(queryset)
            posted_item_list = Product.objects.filter(
                user=user.id).values_list('item').distinct()
            print(posted_item_list)

            # 選択中のエリアにある店舗をリスト化(queryset)　※22/12/27複数選択可能化に伴い修正
            area_store_list = Store.objects.filter(
                area__in=header_areas).values_list('id')
            print(area_store_list)

            user_categorized_product_lists = []
            other_categorized_product_lists = []
            categorized_product_dicts = []

            # リストの品目ごとに、
            for posted_item in posted_item_list:
                print(posted_item)
                # ユーザー自身の投稿を安い順に5件取得する
                user_categorized_product_list = Product.objects.filter(
                    item=posted_item, user=user.id).order_by('price')[:5]

                user_categorized_product_lists.append(
                    user_categorized_product_list)

                # 選択中のエリア内の他ユーザーの投稿を安い順に5件取得する
                other_categorized_product_list = Product.objects.filter(
                    item=posted_item, store__in=area_store_list).exclude(user=user.id).order_by('price')[:5]

                other_categorized_product_lists.append(
                    other_categorized_product_list)

            print(user_categorized_product_lists)
            print(other_categorized_product_lists)

            html = ''

            # 自分の投稿情報の存在確認
            if user_categorized_product_lists is not None and len(user_categorized_product_lists) != 0:
                html += '<ul>'
                # 品目ごとのブロック
                for user_categorized_product_list in user_categorized_product_lists:
                    html += '<li class="card mb-1"><div class="card-body overflow-auto"><h5 class="card-title">'
                    html += user_categorized_product_list[0].item.name
                    html += '</h5><div class="row mb-1 flex-nowrap"><div class="list-header col-2 col-lg-1">価格</div><div class="list-header col-2 col-lg-1">数量</div><div class="list-header col-3 col-lg-2">商品詳細</div><div class="list-header col-2 col-lg-1">ユーザー</div><div class="list-header col-3 col-lg-2">店舗</div><div class="list-header col-3 col-lg-1">日付</div><div class="list-header col-2 col-lg-1">割引</div><div class="list-header col-4 col-lg-3">コメント</div></div>'
                    # 自分の投稿情報のブロック
                    for user_categorized_product in user_categorized_product_list:
                        html += '<div class="self row mb-1 flex-nowrap"><div class="col-2 col-lg-1 price card-text p-2"><span>'
                        html += str(user_categorized_product.price)
                        html += '</span>円</div><div class="col-2 col-lg-1 card-text p-2">'
                        html += str(user_categorized_product.amount)
                        html += '</div><div class="col-3 col-lg-2 card-text p-2">'
                        html += user_categorized_product.detail
                        html += '</div><div class="col-2 col-lg-1 card-text p-2">あなた</div><div class="col-3 col-lg-2 store card-text p-2"><a href="/shopper/u_StoreInfo/'
                        html += str(user_categorized_product.store.id)
                        html += '">'
                        html += user_categorized_product.store.name
                        html += '</a></div><div class="col-3 col-lg-1 date card-text p-2">'
                        html += str(user_categorized_product.date)
                        html += '</div><div class="col-2 col-lg-1 card-text p-2">'
                        if user_categorized_product.discount == 0:
                            html += '-'
                        else:
                            html += '○'
                        html += '</div><div class="col-4 col-lg-3 card-text p-2">'
                        html += user_categorized_product.comment
                        html += '</div></div>'
                    # 他ユーザーの投稿情報の存在確認
                    if other_categorized_product_lists is not None and len(other_categorized_product_lists) != 0:
                        for other_categorized_product_list in other_categorized_product_lists:
                            # 他ユーザー投稿がその品目に対して存在するか
                            if other_categorized_product_list.exists():
                                # 品目が合致するリストを抽出
                                if other_categorized_product_list[0].item == user_categorized_product_list[0].item:
                                    # 他ユーザーの投稿情報のブロック
                                    for other_categorized_product in other_categorized_product_list:
                                        html += '<div class="other row mb-1 flex-nowrap"><div class="col-2 col-lg-1 price card-text p-2"><span>'
                                        html += str(other_categorized_product.price)
                                        html += '</span>円</div><div class="col-2 col-lg-1 card-text p-2">'
                                        html += str(other_categorized_product.amount)
                                        html += '</div><div class="col-3 col-lg-2 card-text p-2">'
                                        html += other_categorized_product.detail
                                        html += '</div><div class="col-2 col-lg-1 card-text p-2">'
                                        html += other_categorized_product.user.name
                                        html += '</div><div class="col-3 col-lg-2 store card-text p-2"><a href="/shopper/u_StoreInfo/'
                                        html += str(other_categorized_product.store.id)
                                        html += '">'
                                        html += other_categorized_product.store.name
                                        html += '</a></div><div class="col-3 col-lg-1 date card-text p-2">'
                                        html += str(user_categorized_product.date)
                                        html += '</div><div class="col-2 col-lg-1 card-text p-2">'
                                        if user_categorized_product.discount == 0:
                                            html += '-'
                                        else:
                                            html += '○'
                                        html += '</div><div class="col-4 col-lg-3 card-text p-2">'
                                        html += user_categorized_product.comment
                                        html += '</div></div>'
                        else:
                            html += '<div id="no_data">他ユーザーの投稿情報がありません</div>'
                html += '</ul>'
            else:
                html += '<div class="my-5"><p>まだ商品の投稿がありません</p><p>購入した商品の情報を登録しましょう</p></div>'
            return HttpResponse(html)

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html')


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

            main_item_list = MainItem.objects.all()
            context['main_item_list'] = main_item_list
            sub_item_list = SubItem.objects.all()
            context['sub_item_list'] = sub_item_list
            item_list = Item.objects.all()
            context['item_list'] = item_list

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
        store_end_hour = request.POST['store_end_hour']
        store_URL = request.POST['store_URL']
        store_tel = request.POST['store_tel']
        store_payment = request.POST['store_payment']
        store_facility = request.POST['store_facility']
        store_service = request.POST['store_service']

        # DB側でnullが許されず、ユーザーが入力しない値
        store_corporation_flag = 0
        store_open_flag = 0

        store = Store.objects.create(name=store_name, area=store_area, address=store_address, start_hour=store_start_hour, end_hour=store_end_hour,
                                     url=store_URL, tel=store_tel, payment=store_payment, facility=store_facility, service=store_service, administrated_flag=store_corporation_flag, open_flag=store_open_flag)
        return HttpResponse(store.id)


# 店舗情報


class U_StoreInfoView(View):
    def get(self, request, id):
        print('店舗情報画面')
        context = {}

        store_id = id
        store = Store.objects.get(id=store_id)
        context['store'] = store
        context['coupon_list'] = Coupon.objects.filter(store=store)
        context['flyer_list'] = Flyer.objects.filter(store=store)
        context['recipe_list'] = Recipe.objects.filter(store=store)

        return render(request, 'shopper/u_StoreInfo.html', context)

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
        gender = request.POST['gender']
        area = request.POST['area']

        # セッションを取得
        user = request.session['user']

        # ユーザーデータを更新
        result = User.objects.filter(id=user.id).update(
            email=email, name=name, gender=gender, area=area)

        # 正常にアップデートできた場合は result = 1
        if result == 1:
            # userインスタンス更新
            user.email = email
            user.name = name
            user.gender = gender

            # 外部キー設定のフィールドは対応するモデルのインスタンスで保存する
            user.area = User.objects.get(id=user.id).area

            # ユーザーセッションを更新
            request.session['user'] = user

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

            # パスワードが一致しない場合

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

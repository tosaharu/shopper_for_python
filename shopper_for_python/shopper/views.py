from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .forms import U_RegisterUserForm
from .views_modules.module import *
from django.core.mail import send_mail
import datetime

# Create your views here.


# 新規会員登録処理


class U_RegisterUserView(View):
    def get(self, request):
        print('新規会員登録画面')
        context = {}
        get_area_contexts(context)

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

# ログイン


class U_LoginView(View):
    def get(self, request):
        print('ログイン画面')
        context = {}
        get_area_contexts(context)
        return render(request, 'shopper/u_Login.html', context)

    def post(self, request):
        print('ログイン実行')
        context = {}
        get_area_contexts(context)

        # 入力されたメールアドレスとパスワードを取得
        email = request.POST['email']
        password = request.POST['password']
        users = User.objects

        if users.filter(email=email, active_flag=1).exists():
            user = users.get(email=email)

            if check_password(password, user.password):
                # セッションに保存
                request.session['user'] = user
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
                area=user.area.id).values_list('id')
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
                user=user.id).order_by('date')
            context['user_product_list'] = user_product_list

            return render(request, 'shopper/u_Main.html', context)

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html', context)


# 商品情報投稿


class U_RegisterProductView(View):
    def get(self, request):
        print('商品情報投稿画面')
        context = {}

        get_area_contexts(context)

        store_list = Store.objects.all()
        context['store_list'] = store_list
        main_item_list = MainItem.objects.all()
        context['main_item_list'] = main_item_list
        sub_item_list = SubItem.objects.all()
        context['sub_item_list'] = sub_item_list
        item_list = Item.objects.all()
        context['item_list'] = item_list

        return render(request, 'shopper/u_RegisterProduct.html', context)

    def post(self, request):
        print('商品情報投稿')
        context = {}
        get_area_contexts(context)

        # セッションの存在確認が必要

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
        get_area_contexts(context)

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
        context = {}
        get_area_contexts(context)

        # セッションの中身を確認
        if 'user' in request.session:
            user = request.session['user']
            print(user)
            print(user.gender)

            return render(request, 'shopper/u_ChangeInfo.html', context)

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html', context)


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

            # セッションを更新
            request.session['user'] = user

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
        context = {}
        get_area_contexts(context)

        # セッション破棄
        request.session.flush()

        return render(request, 'shopper/u_Logout.html', context)

# パスワード紛失時の再設定認証処理


class U_ResetPasswordAuthView(View):
    def get(self, request):
        print('パスワード再設定認証画面1')
        context = {}
        get_area_contexts(context)
        return render(request, 'shopper/u_ResetPasswordAuth1.html', context)

    def post(self, request):
        context = {}
        get_area_contexts(context)

        # ワンタイムパスワードの生成
        onetime_password = create_onetime_password()

        # 入力されたメールアドレスを取得
        email = request.POST['email']

        # パスワードをメールで送信
        subject = "ワンタイムパスワード送信"
        message = onetime_password
        from_email = "shopper.webmaster2271@gmail.com"
        to = [email,]
        send_mail(subject, message, from_email, to)

        # パスワードをセッションに保存
        request.session['onetime_password'] = onetime_password
        return render(request, 'shopper/u_ResetPasswordAuth2.html', context)


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
        context = {}
        get_area_contexts(context)
        return render(request, 'shopper/u_ResetPassword.html', context)

    def post(self, request):
        context = {}
        get_area_contexts(context)

        originalPass = request.POST['newpassword']
        password = make_password(originalPass)

        # セッションの確認
        if 'change_password_user' in request.session:

            # ユーザー情報をセッションから取得
            change_password_user = request.session['change_password_user']

            # ユーザーデータを更新
            result = User.objects.filter(
                id=change_password_user.id).update(password=password)

            if result == 1:
                # 対象の1件が正常にアップデートされた場合
                return render(request, 'shopper/u_ResetPasswordComplete.html', context)

            # アップデートが何かしらの理由でできなかった場合
            # あまりなさそうなので一旦保留

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html', context)


# セッション切れの際に飛ぶページ


class U_SessionExpiredView(View):
    def get(self, request):
        context = {}
        get_area_contexts(context)
        return render(request, 'shopper/u_SessionExpired.html', context)


# 退会処理


class U_QuitView(View):
    def get(self, request):
        print('退会確認画面')
        context = {}
        get_area_contexts(context)
        return render(request, 'shopper/u_QuitConfirm.html', context)

    def post(self, request):
        context = {}
        get_area_contexts(context)

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

                return render(request, 'shopper/u_QuitComplete.html', context)

            # アップデートが何かしらの理由でできなかった場合
            # あまりなさそうなので一旦保留

        # セッション切れの場合
        return render(request, 'shopper/u_SessionExpired.html', context)

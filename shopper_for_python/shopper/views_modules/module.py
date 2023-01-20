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

# ユーザーが投稿したことのある商品品目について、
# そのユーザーの投稿リストと他ユーザーの投稿リストをそれぞれ取得する
# request：djangoのリクエスト型
# user：modelのユーザー型
# areas：modelのエリア型のリスト


def get_categorized_product_lists(request, user, areas):
    categorized_product_lists = {}

    # 値段ソートの基準を設定（デフォルトは単純価格）
    price_sort = 'price'

    if 'sort' in request.session:
        if request.session['sort'] == 1:
            # 値段ソートの基準をを数量当たり価格に
            price_sort = 'price_per_amount'

    print(price_sort)

    # ユーザーが投稿したことのある品目をリスト化(リスト型)
    raw_posted_item_list = Product.objects.filter(
        user=user.id).order_by('date').reverse().values_list('item')
    print(raw_posted_item_list)

    # 重複削除リストに変換（queryset内のオブジェクトはタプルでありハッシュ化可なため、リストの場合はハッシュ化不可なので以下の方法は使えない）
    posted_item_list = list(dict.fromkeys(raw_posted_item_list))
    print(posted_item_list)

    # 選択中のエリアにある店舗をリスト化(queryset)　※22/12/27複数選択可能化に伴い修正
    area_store_list = Store.objects.filter(
        area__in=areas).values_list('id')
    print(area_store_list)

    user_categorized_product_lists = []
    other_categorized_product_lists = []

    # リストの品目ごとに、
    for posted_item in posted_item_list:
        print(posted_item)
        # ユーザー自身の投稿を安い順に5件取得する
        user_categorized_product_list = Product.objects.filter(
            item=posted_item, user=user.id).order_by(price_sort)[:5]

        user_categorized_product_lists.append(
            user_categorized_product_list)

        # 選択中のエリア内の他ユーザーの投稿を安い順に5件取得する
        other_categorized_product_list = Product.objects.filter(
            item=posted_item, store__in=area_store_list).exclude(user=user.id).order_by(price_sort)[:5]

        other_categorized_product_lists.append(
            other_categorized_product_list)

    print(user_categorized_product_lists)
    print(other_categorized_product_lists)

    categorized_product_lists['user'] = user_categorized_product_lists
    categorized_product_lists['other'] = other_categorized_product_lists

    return categorized_product_lists

# ajax通信でメイン画面の投稿リストを描画する


def display_categorized_product_lists(request, user_categorized_product_lists, other_categorized_product_lists):
    html = ''
    # 品目ごとのブロック
    for user_categorized_product_list in user_categorized_product_lists:
        html += '<li class="card mb-1"><div class="card-body overflow-auto"><h5 class="card-title">'
        html += user_categorized_product_list[0].item.name + \
            "/" + user_categorized_product_list[0].item.unit.name
        html += '</h5><div class="row mb-1 flex-nowrap">'

        html += '<div class="list-header col-2 col-lg-1">'
        # 選択されているソート方法に応じて1列目の項目名を出し分け
        if 'sort' in request.session:
            if request.session['sort'] == 1:
                html += '価格/' + \
                    user_categorized_product_list[0].item.unit.name
            else:
                html += '価格'
        else:
            html += '価格'
        html += '</div>'

        html += '<div class="list-header col-2 col-md-1">数量</div>'

        html += '<div class="list-header col-2 col-lg-1">'
        # 選択されているソート方法に応じて3列目の項目名を出し分け
        if 'sort' in request.session:
            if request.session['sort'] == 1:
                html += '価格'
            else:
                html += '価格/' + \
                    user_categorized_product_list[0].item.unit.name
        else:
            html += '価格/' + \
                user_categorized_product_list[0].item.unit.name
        html += '</div>'

        html += '<div class="list-header col-3 col-lg-2">商品詳細</div>'
        html += '<div class="list-header col-3 col-lg-2">店舗</div>'
        html += '<div class="list-header col-3 col-md-1">日付</div>'
        html += '<div class="list-header col-2 col-md-1">割引</div>'
        html += '<div class="list-header col-4 col-lg-2">コメント</div>'
        html += '<div class="list-header col-2 col-lg-1">ユーザー</div></div>'
        # 自分の投稿情報のブロック
        for user_categorized_product in user_categorized_product_list:
            html += '<div class="self row mb-1 flex-nowrap"><div class="col-2 col-lg-1 price card-text p-2"><span>'

            # 選択されているソート方法に応じて1列目の値を出し分け
            if 'sort' in request.session:
                if request.session['sort'] == 1:
                    html += str(user_categorized_product.price_per_amount)+" "
                else:
                    html += str(user_categorized_product.price)+" "
            else:
                html += str(user_categorized_product.price)+" "

            html += '</span>円</div><div class="col-2 col-md-1 card-text p-2">'
            html += str(user_categorized_product.amount)
            html += '</div><div class="col-2 col-lg-1 card-text p-2">'

            # 選択されているソート方法に応じて3列目の値を出し分け
            if 'sort' in request.session:
                if request.session['sort'] == 1:
                    html += str(user_categorized_product.price)
                else:
                    html += str(user_categorized_product.price_per_amount)
            else:
                html += str(user_categorized_product.price_per_amount)

            html += '</div><div class="col-3 col-lg-2 card-text p-2">'
            html += user_categorized_product.detail
            html += '</div><div class="col-3 col-lg-2 store card-text p-2"><a href="/shopper/u_StoreInfo/'
            html += str(user_categorized_product.store.id)
            html += '">'
            html += user_categorized_product.store.name
            html += '</a></div><div class="col-3 col-md-1 date card-text p-2">'
            html += str(user_categorized_product.date)
            html += '</div><div class="col-2 col-md-1 card-text p-2">'
            if user_categorized_product.discount == 0:
                html += '-'
            else:
                html += '○'
            html += '</div><div class="col-4 col-lg-2 card-text p-2">'
            html += user_categorized_product.comment
            html += '</div><div class="col-2 col-lg-1 card-text p-2">あなた</div></div>'
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

                            # 選択されているソート方法に応じて1列目の値を出し分け
                            if 'sort' in request.session:
                                if request.session['sort'] == 1:
                                    html += str(other_categorized_product.price_per_amount)+" "
                                else:
                                    html += str(other_categorized_product.price)+" "
                            else:
                                html += str(other_categorized_product.price)+" "

                            html += '</span>円</div><div class="col-2 col-md-1 card-text p-2">'
                            html += str(other_categorized_product.amount)
                            html += '</div><div class="col-2 col-lg-1 card-text p-2">'

                            # 選択されているソート方法に応じて3列目の値を出し分け
                            if 'sort' in request.session:
                                if request.session['sort'] == 1:
                                    html += str(other_categorized_product.price)
                                else:
                                    html += str(other_categorized_product.price_per_amount)
                            else:
                                html += str(other_categorized_product.price_per_amount)

                            html += '</div><div class="col-3 col-lg-2 card-text p-2">'
                            html += other_categorized_product.detail
                            html += '</div><div class="col-3 col-lg-2 store card-text p-2"><a href="/shopper/u_StoreInfo/'
                            html += str(other_categorized_product.store.id)
                            html += '">'
                            html += other_categorized_product.store.name
                            html += '</a></div><div class="col-3 col-md-1 date card-text p-2">'
                            html += str(other_categorized_product.date)
                            html += '</div><div class="col-2 col-md-1 card-text p-2">'
                            if other_categorized_product.discount == 0:
                                html += '-'
                            else:
                                html += '○'
                            html += '</div><div class="col-4 col-lg-2 card-text p-2">'
                            html += other_categorized_product.comment
                            html += '</div><div class="col-2 col-lg-1 card-text p-2">'
                            html += other_categorized_product.user.name
                            html += '</div></div>'
        html += '<div id="no_data">他ユーザーの投稿情報がありません</div></div></li>'
    return html

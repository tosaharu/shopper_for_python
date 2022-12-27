/**
 *
*/
// 最初に必要な処理
window.addEventListener('load', () => {
  ShowSelectedRegionPrefectureSelection();
  ShowSelectedPrefectureAreaSelection();
  ShowSelectedArea();
})


// 地域選択に関する処理
let region_select_button = document.getElementById('header_region');
region_select_button.addEventListener('blur', () => {
  ShowSelectedRegionPrefectureSelection();
  // ShowSelectedArea();
})

// 都道府県選択に関する処理
let prefecture_select_button = document.getElementById('header_prefecture');
prefecture_select_button.addEventListener('blur', () => {
  ShowSelectedPrefectureAreaSelection();
  // ShowSelectedArea();
});


function ShowSelectedRegionPrefectureSelection() {
  // 地域が選択された際に、都道府県を選択可能にする
  let region = document.getElementById('header_region').value;
  let prefecture_selector = document.getElementById('header_prefecture');
  if (region >= 1) {
    prefecture_selector.removeAttribute("disabled");
  } else {
    prefecture_selector.setAttribute("disabled", "disabled");
  }
  // 選択地域の変更に応じて、選択可能な都道府県を表示する
  hidden_list = document.querySelectorAll('[data-header_region_id]');
  for (let i = 0; i < hidden_list.length; i++) {
    hidden_list[i].setAttribute("hidden", "");
    hidden_list[i].setAttribute("disabled", "");
  }

  display_list = document.querySelectorAll('[data-header_region_id="' + region + '"]')
  for (let i = 0; i < display_list.length; i++) {
    display_list[i].removeAttribute("hidden");
    display_list[i].removeAttribute("disabled");
  }

  // 選択地域を変更した際に、対象外の都道府県の選択をリセットする
  let index = prefecture_selector.selectedIndex;
  let p_region = document.querySelectorAll('[data-header_region_id]')[index].dataset.header_region_id;
  console.log(region);
  console.log(p_region);

  if (p_region != region) {
    prefecture_selector.options[0].selected = true;
  }
  ShowSelectedPrefectureAreaSelection();

}


// 選択していている都道府県に合わせたエリアを表示する
function ShowSelectedPrefectureAreaSelection() {
  $.ajax({
    url: "Ajax_GetArea/",
    type: "GET",
    data: { header_prefecture: $('#header_prefecture').val() }
  }).done(function (result) {
    //通信成功時のコールバック
    console.log(result);
    console.log($('div.ms-drop>ul'));

    // djangohtmlを活用するパターン（ページを更新しないとソースも更新されないようなのでボツ）
    //html = '{% for selected_prefecture_area in request.session.selected_prefecture_areas %}<li class="col-sm-6 col-xl-4 area_selection" onclick="ShowSelectedArea() "><label><input name="header_area" type="checkbox" value="{{selected_prefecture_area.id}}" {%if selected_prefecture_area.id == request.session.tmp_area.id%} checked="checked" {% endif %}><span>{{selected_prefecture_area.name}}</span></label></li>{% endfor %}';
    //console.log(html);

    // 既存リストの削除
    $('div.ms-drop>ul>li').remove();
    // 選択都道府県のリストを挿入
    $('div.ms-drop>ul').append(result);


  }).fail(function () {
    //通信失敗時のコールバック
    console.log("通信失敗");
    $('div.ms-drop>ul>li').remove();

  }).always(function () {
    //常に実行する処理
    ShowSelectedArea();
  })
};

// 選択されているエリアをボタン上に表示する
function ShowSelectedArea() {
  let selected_area_text = "";

  let selected_area_list = document.querySelectorAll('.area_selection>label>input');
  console.log(selected_area_list);
  let cnt = 0;
  for (selected_area of selected_area_list) {
    console.log(selected_area);
    if (selected_area.checked) {
      if (cnt > 0) {
        selected_area_text = selected_area_text + ",";
      }
      selected_area_text = selected_area_text + selected_area.nextElementSibling.textContent;
      cnt++;
    }
  }
  console.log(selected_area_text);
  if (selected_area_text != null && selected_area_text != "") {
    $('#msbtn>span').text(selected_area_text);
  } else {
    $('#msbtn>span').text("");
  }
}
// エリア選択ボタン押下時の最安情報リスト更新
let reload_selection = document.getElementById('reload_selection');
reload_selection.addEventListener('click', GetAreaProduct());


// 最安商品リストの取得
function GetAreaProduct() {
  let header_areas = $('input[name="header_area"]').filter(":checked").map(function () {
    return $(this).val();
  }).get();
  console.log(header_areas);

  $.ajax({
    url: "Ajax_GetAreaProduct/",
    type: "GET",
    data: { header_areas: header_areas, },
  }).done(function (result) {
    //通信成功時のコールバック
    console.log(result);
    console.log($('div.ms-drop>ul'));

    // djangohtmlを活用するパターン（ページを更新しないとソースも更新されないようなのでボツ）
    //html = '{% for selected_prefecture_area in request.session.selected_prefecture_areas %}<li class="col-sm-6 col-xl-4 area_selection" onclick="ShowSelectedArea() "><label><input name="header_area" type="checkbox" value="{{selected_prefecture_area.id}}" {%if selected_prefecture_area.id == request.session.tmp_area.id%} checked="checked" {% endif %}><span>{{selected_prefecture_area.name}}</span></label></li>{% endfor %}';
    //console.log(html);

    // // 既存リストの削除
    // $('div.ms-drop>ul>li').remove();
    // // 選択都道府県のリストを挿入
    // $('div.ms-drop>ul').append(result);


  }).fail(function () {
    //通信失敗時のコールバック
    console.log("通信失敗");
    $('div.ms-drop>ul>li').remove();

  }).always(function () {
    //常に実行する処理
    ShowSelectedArea();
  })
};
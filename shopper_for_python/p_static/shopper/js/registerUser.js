/**
 * 新規登録画面
 * 
 * ・登録ボタンを押下した際にモーダルにデータを送る処理
 */

// 対象のボタンを取得
let btn = document.getElementById('subm1');

// ボタン押下時の処理
btn.addEventListener('click', () => {
	selectAndInsertData("email", "modal_email");
	selectAndInsertData("password2", "modal_password");
	selectAndInsertData("name", "modal_name");
	selectAndInsertGender("gender", "modal_gender");
	selectAndInsertBirthday("year-select", "month-select", "day-select", "modal_birthday");
	selectAndInsertArea("region", "prefecture", "area", "modal_area");
})

// 第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
function selectAndInsertData(getFrom, insertInto) {
	let val = document.getElementById(getFrom).value;
	document.getElementById(insertInto).innerHTML = val;
}

// （性別チェックボックス用）第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
function selectAndInsertGender(getFrom, insertInto) {
	let val;
	let elements = document.getElementsByName(getFrom);
	for (let i = 0; i <= elements.length; i++) {
		if (elements[i].checked) {
			val = elements[i].value;
			break;
		}
	}
	console.log(val)
	switch (val) {
		case "1":
			val = "男性";
			break;
		case "2":
			val = "女性";
			break;
		case "3":
			val = "回答しない";
			break;
	}
	document.getElementById(insertInto).innerHTML = val;
}

// （誕生日セレクトボックス用）第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
function selectAndInsertBirthday(getFrom1, getFrom2, getFrom3, insertInto) {
	let year = document.getElementById(getFrom1).value;
	let month = document.getElementById(getFrom2).value;
	let day = document.getElementById(getFrom3).value;
	document.getElementById(insertInto).innerHTML = year + " 年 " + month + " 月 " + day + " 日 ";
}

// （エリアセレクトボックス用）第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
function selectAndInsertArea(getFrom1, getFrom2, getFrom3, insertInto) {
	let r_index = document.getElementById(getFrom1).selectedIndex
	let region = document.getElementById(getFrom1).children[r_index].innerHTML;
	let p_index = document.getElementById(getFrom2).selectedIndex
	let prefecture = document.getElementById(getFrom2).children[p_index].innerHTML;
	let a_index = document.getElementById(getFrom3).selectedIndex
	let area = document.getElementById(getFrom3).children[a_index].innerHTML;

	document.getElementById(insertInto).innerHTML = region + " - " + prefecture + " - " + area;
}

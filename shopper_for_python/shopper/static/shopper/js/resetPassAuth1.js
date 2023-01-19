/**
 * パスワード再設定認証（メールアドレス・生年月日要求）画面
 * 
 * ・入力データを照合し、問題なければ確認モーダルを表示する処理
 */

// bsのモーダル用functionを使用できるように（参考元ではmodule化=>impotして使用していたが、bootstrap.クラス名でも呼び出し可なのでそちらで）
let modal = document.getElementById('modal');
let modalObj = new bootstrap.Modal(modal);
let btn = document.getElementById('subm1');

// toastクラスがついている要素にBootStrapのトーストを適用する
let toastElList = [].slice.call(document.querySelectorAll(".toast"));
let toastList = toastElList.map(function (toastEl) {
	return new bootstrap.Toast(toastEl, {
		// オプション
	});
});

// ボタンをクリックしたときに実行される関数
function showToast() {
	// トーストを表示する
	toastList[0].show();
}

btn.addEventListener('click', () => {
	$.ajax({
		url: "Ajax_CheckUserMailAndBirthday/",
		type: "POST",
		data: {
			email: $('input[name="email"]').val(),
			year: $('select[name="year"]').val(),
			month: $('select[name="month"]').val(),
			day: $('select[name="day"]').val(),
		},
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	}).done(function (result) {
		//通信成功時のコールバック
		let collation = Number(result);
		console.log(collation);
		if (collation == 1) {
			console.log("通信成功");
			let address = $('input[name="email"]').val()
			console.log(address);
			$('#modal_email').text(address);
			modalObj.show()
		} else {
			console.log("通信失敗");
			let src = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e";
			let text = "合致するデータがありません";
			$('#errorToast > div > img').attr('src', src);
			$('#errorToast > div > strong').text(text);
			showToast()
		}
	}).fail(function (result) {
		//通信失敗時のコールバック
		console.log("通信失敗");
		let src = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e";
		let text = "通信エラーが発生しました";
		$('#errorToast > div > img').attr('src', src);
		$('#errorToast > div > strong').text(text);
		showToast()
	}).always(function (result) {
		//常に実行する処理
		console.log("通信完了");
	})
})
/**
 * アプリで使用するバリデーション機能
 */

// バリデーションの警告文がチェック対象の直後にある場合（通常の配置）に、バリデーションの種類に合った警告文に更新する
function updateValidationMessage(input) {
	let validationMessage = input.validationMessage;
	console.log(validationMessage);
	let insertAt = input.nextElementSibling;
	console.log(insertAt);
	insertAt.innerHTML = validationMessage;
}

// フォームをチェックし、問題があればボタンは無効に、なければ有効に切り替える
function toggleFormButton(form_id, button_id) {
	let subm_form = document.getElementById(form_id);
	let subm = document.getElementById(button_id);
	if (subm_form.checkValidity()) {
		subm.removeAttribute('disabled');
	} else {
		subm.setAttribute('disabled', 'disabled');
	}
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// ラジオボタン以外の選択肢HTML構造用
function activateValidation(outline_id, input_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.getElementById(input_id);
	console.log(input)

	input.addEventListener('focus', function () {
		outline.classList.remove('was-validated');
	}, false)

	input.addEventListener('blur', function () {
		outline.classList.add('was-validated');
		toggleFormButton(form_id, button_id);
		updateValidationMessage(input)
	}, false)
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// ラジオボタンの選択肢HTML構造用
function activateRadioValidation(outline_id, input_name, invalid_feedback_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let forms = document.getElementsByName(input_name);
	console.log(forms)
	let insertAt = document.getElementById(invalid_feedback_id);
	console.log(insertAt)

	for (let input of forms) {
		input.addEventListener('focus', function () {
			outline.classList.remove('was-validated');
		}, false)

		input.addEventListener('blur', function () {
			outline.classList.add('was-validated');
			toggleFormButton(form_id, button_id);

			let validationMessage = input.validationMessage;
			console.log(validationMessage);
			insertAt.innerHTML = validationMessage;
		}, false)
	}
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// 2か所のパスワードの入力が一致していることをバリデートする
function activateDoublePassValidation(outline_id, input_id, reference_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.getElementById(input_id);
	console.log(input)
	let reference = document.getElementById(reference_id);
	console.log(reference)

	input.addEventListener('focus', function () {
		input.classList.remove('is-valid');
		input.classList.remove('is-invalid');
		outline.classList.remove('was-validated');
	}, false)

	input.addEventListener('blur', function () {
		console.log(input.value);
		console.log(reference.value);
		if (input.value == reference.value) {
			console.log("パス合致");
			input.classList.remove('is-invalid');
			input.classList.add('is-valid');
			input.setCustomValidity("")

		} else {
			console.log("パス不一致");
			input.classList.remove('is-valid');
			input.classList.add('is-invalid');
			input.setCustomValidity("パスワードが一致しません")

		}
		outline.classList.add('was-validated');
		toggleFormButton(form_id, button_id);
		updateValidationMessage(input)
	}, false)
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// メールアドレスがDBに存在しないことをバリデートする
function activateExistingMailValidation(outline_id, input_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.getElementById(input_id);
	console.log(input)

	input.addEventListener('focus', function () {
		input.classList.remove('is-valid');
		input.classList.remove('is-invalid');
		outline.classList.remove('was-validated');
	}, false)


	input.addEventListener('blur', function () {
		$.ajax({
			url: "Ajax_CheckUserMail/",
			type: "GET",
			data: { email: $('#email').val() }
		}).done(function (result) {
			//通信成功時のコールバック
			let checkMail = Number(result);
			if (checkMail == 1) {
				console.log("登録済のメールアドレス有り");
				input.classList.remove('is-valid');
				input.classList.add('is-invalid');
				input.setCustomValidity("そのメールアドレスは既に使用されています")
			} else {
				console.log("登録済のメールアドレス無し、または自分のメールアドレスの場合");
				input.classList.remove('is-invalid');
				input.classList.add('is-valid');
				input.setCustomValidity("")
			}
			outline.classList.add('was-validated');
			toggleFormButton(form_id, button_id);
			updateValidationMessage(input)
		}).fail(function () {
			//通信失敗時のコールバック
			console.log("通信失敗");
		}).always(function () {
			//常に実行する処理
		});

	}, false)
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// 店舗名がDBに存在しないことをバリデートする
function activateExistingStoreValidation(outline_id, input_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.getElementById(input_id);
	console.log(input)

	input.addEventListener('focus', function () {
		input.classList.remove('is-valid');
		input.classList.remove('is-invalid');
		outline.classList.remove('was-validated');
	}, false)


	input.addEventListener('blur', function () {
		// store_idが存在する場合に設定（店舗情報画面でも使用するため）
		let store_id = 0;
		if ($('#store_id').length) {
			store_id = $('#store_id').val();
		}
		console.log(store_id);
		$.ajax({
			url: "Ajax_CheckStore/",
			type: "GET",
			data: {
				store_name: $('#store_name').val(),
				store_id: store_id,
			},
		}).done(function (result) {
			//通信成功時のコールバック
			let checkStore = Number(result);
			if (checkStore > 0) {
				console.log("登録済の店舗有り");
				input.classList.remove('is-valid');
				input.classList.add('is-invalid');
				input.setCustomValidity("その店舗は登録されています")
			} else {
				console.log("登録済の店舗無し");
				input.classList.remove('is-invalid');
				input.classList.add('is-valid');
				input.setCustomValidity("")
			}
			outline.classList.add('was-validated');
			toggleFormButton(form_id, button_id);
			updateValidationMessage(input)
		}).fail(function () {
			//通信失敗時のコールバック
			console.log("通信失敗");
		}).always(function () {
			//常に実行する処理
		});

	}, false)
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// 品目×単位の組み合わせがDBに存在しないことをバリデートする
function activateExistingItemValidation(outline_id1, outline_id2, input_id1, input_id2, form_id, button_id) {
	let outline1 = document.getElementById(outline_id1);
	console.log(outline1)
	let outline2 = document.getElementById(outline_id2);
	console.log(outline2)
	let input1 = document.getElementById(input_id1);
	console.log(input1)
	let input2 = document.getElementById(input_id2);
	console.log(input2)

	// 入力欄がフォーカスされた際の処理
	input1.addEventListener('focus', () => {
		FormFocus(input1, outline1)
	}, false)
	input2.addEventListener('focus', () => {
		FormFocus(input2, outline2)
	}, false)

	function FormFocus(input, outline) {
		console.log("品目×単位、フォーカス時")
		input.classList.remove('is-valid');
		input.classList.remove('is-invalid');

		outline.classList.remove('was-validated');
	}

	// 入力欄のフォーカスが外れた際の処理
	input1.addEventListener('blur', () => {
		AjaxCheckItem(input1, outline1, input2, outline2)
	}, false)
	input2.addEventListener('blur', () => {
		AjaxCheckItem(input2, outline2, input1, outline1)
	}, false)

	// 下記のように直接addeventlistnerに関数をぶち込むと、ロード時にも実行されてしまう模様
	// input1.addEventListener('blur', AjaxCheckItem(), false)

	// ※第4引数は不要なことが分かったが、処理追加するかもしれないので一応残しておく
	function AjaxCheckItem(input, outline, othersInput, othersOutline) {
		console.log("品目×単位、フォーカス外れ時")
		$.ajax({
			url: "Ajax_CheckItem/",
			type: "GET",
			data: {
				item_name: $('#item_name').val(),
				item_unit: $('#item_unit').val()
			}
		}).done(function (result) {
			//通信成功時のコールバック
			let checkItem = Number(result);
			if (checkItem > 0) {
				if (checkItem != 999) {
					console.log("登録済の品目有り");

					input.classList.remove('is-valid');
					input.classList.add('is-invalid');
					input.setCustomValidity("その品目と単位の組み合わせは既に登録されています")

					// 存在しないものを.valueで取ってきた場合、空のstringが返ってくる模様・・・（nullなどで判定不可）
					if (othersInput.value != "") {
						console.log(othersInput.value)
						console.log(typeof (othersInput.value))
						othersInput.classList.remove('is-valid');
						othersInput.classList.add('is-invalid');
						othersInput.setCustomValidity("その品目と単位の組み合わせは既に登録されています")
					}
				}
				// 999は単位が空（未選択）で送られた際のエラーレスポンスなので何もしない
			} else {
				console.log("登録済の品目無し");

				input.classList.remove('is-invalid');
				input.classList.add('is-valid');
				input.setCustomValidity("")

				if (othersInput.value != "") {
					console.log(othersInput.value)
					console.log(typeof (othersInput.value))
					othersInput.classList.remove('is-invalid');
					othersInput.classList.add('is-valid');
					othersInput.setCustomValidity("")
				}
			}
			outline.classList.add('was-validated');
			updateValidationMessage(input)

			toggleFormButton(form_id, button_id);
		}).fail(function () {
			//通信失敗時のコールバック
			console.log("通信失敗");
		}).always(function () {
			//常に実行する処理
		});
	}
}


// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// select2プラグインを使用した検索機能付きselect用
function activateSelect2Validation(outline_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.querySelector('#' + outline_id + ' > span > span > span');
	console.log(input)

	input.addEventListener('focus', function () {
		console.log('focus');
		outline.classList.remove('was-validated');
	}, false)

	input.addEventListener('blur', function () {
		console.log('blur');
		outline.classList.add('was-validated');
		toggleFormButton(form_id, button_id);
	}, false)
}
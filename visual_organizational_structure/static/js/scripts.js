

const langButtons = document.querySelectorAll("[data-btn]");
const allLangs = ["ru", "en"];
const currentPathName = window.location.pathname;
let currentLang =
	localStorage.getItem("language") || checkBrowserLang() || "ru";
let currentTexts = {};

const homeTexts = {
    "header_settings": {
        ru: "настройки",
        en: "settings"
    },
    "header_help": {
        ru: "поддержка",
        en: "help"
    },
    "footer_contacts": {
        ru: "Контакты",
        en: "Contacts"
    },
    "footer_settings": {
        ru: "Настройки",
        en: "Settings"
    },
    "footer_help": {
        ru: "Поддержка",
        en: "Help"
    },
    "pass_change": {
        ru: "Сменить пароль",
        en: "Switch password"
    },
    "lang_change": {
        ru: "Смена языка",
        en: "Switch language"
    },
    "theme_change_dark": {
        ru: "Темная",
        en: "Dark"
    },
    "theme_change_ligth": {
        ru: "Светлая",
        en: "Ligth"
    },
    "theme_change": {
        ru: "Смена темы",
        en: "Switch theme"
    },
    "login": {
        ru: "Войти",
        en: "Login"
    },
    "logout": {
        ru: "Выйти",
        en: "Logout"
    },
    "create_dash": {
        ru: "Создать доску",
        en: "Create dashboard"
    },
    "delete_dash": {
        ru: "Вы уверены?",
        en: "Are you sure?"
    },
    "Yes": {
        ru: "Да",
        en: "Yes"
    },
    "No": {
        ru: "Отмена",
        en: "Cancel"
    },


    
}

function checkPagePathName() {
	switch (currentPathName) {
		case "/layout.html":
			currentTexts = homeTexts;
			break;
		

		default:
			currentTexts = homeTexts;
			break;
	}
}
checkPagePathName();

// Изменение языка у текстов
function changeLang() {
	for (const key in currentTexts) {
		let elem = document.querySelector(`[data-lang=${key}]`);
		if (elem) {
			elem.textContent = currentTexts[key][currentLang];
		}
	}
}
changeLang();

// Вешаем обработчики на каждую кнопку
langButtons.forEach((btn) => {
	btn.addEventListener("click", (event) => {
		if (!event.target.classList.contains("_btn_active")) {
			currentLang = event.target.dataset.btn;
			localStorage.setItem("language", event.target.dataset.btn);
			resetActiveClass(langButtons, "_btn_active");
			btn.classList.add("_btn_active");
			changeLang();
		}
	});
});

// Сброс активного класса у переданного массива элементов
function resetActiveClass(arr, activeClass) {
	arr.forEach((elem) => {
		elem.classList.remove(activeClass);
	});
}

// Проверка активной кнопки
function checkActiveLangButton() {
	switch (currentLang) {
		case "ru":
			document
				.querySelector('[data-btn="ru"]')
				.classList.add("_btn_active");
			break;
		case "en":
			document
				.querySelector('[data-btn="en"]')
				.classList.add("_btn_active");
			break;

		default:
			document
				.querySelector('[data-btn="ru"]')
				.classList.add("_btn_active");
			break;
	}
}
checkActiveLangButton();

// Проверка языка браузера
function checkBrowserLang() {
	const navLang = navigator.language.slice(0, 2).toLowerCase();
	const result = allLangs.some((elem) => {
		return elem === navLang;
	});
	if (result) {
		return navLang;
	}
}
console.log("navigator.language", checkBrowserLang());


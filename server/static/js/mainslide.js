let date = new Date();
const thisYear = date.getFullYear();
const thisMonth = date.getMonth();
const thisDate = date.getDate();
const thisDay = date.getDay();
const lastDate = new Date(thisYear, thisMonth + 1, 0).getDate();
daysKorean = ["일", "월", "화", "수", "목", "금", "토"];
days = [];
dates = [];
//지금부터 이번 달 말일
for (let i = thisDate; i <= lastDate; i++) {
	dates.push(i);
}
// 다음 달 날짜껒
thisDateLength = dates.length;
for (let i = 1; i <= 31 - thisDateLength; i++) {
	dates.push(i);
}

let dayIndex = thisDay;
let prev_day = 0;
let now_month = thisMonth + 1;
let now_year = thisYear;


dates.forEach((date, i) => {
	let condition =
		dayIndex % 7 == 0 ? "sun" : dayIndex % 7 == 6 ? "sat" : "rest_day";
	// i가 0이 아닌데 date가 1이면 달이 넘어갔다는 의미
	if (prev_day > date) {
		now_month++;
		if (now_year == 13) {
			now_year++;
			now_month = 1;
		}
	}
	prev_day = i;

	// 현재 날짜의 curSlideIndex 계산
	days[
		i
	] = `<input class = "slide-list" id = "date-${i}" type = "radio" name = "date" value = "${now_year}-${now_month}-${date}">
  <label class = "date-select" for="date-${i}">
  <li class='date ${condition}' name = "date"><div><strong>${
		daysKorean[dayIndex++ % 7]
	}요일</strong></div><div><strong>${date}일</strong></div></li>
  </label>
  `;
});

const week = document.querySelector(".week");
week.innerHTML = days.join("");

// 상세 설정 필터 이후에도 현재 선택된 슬라이드의 checked 상태 변환
window.addEventListener("load", () => {
	// 아직 날짜 필터를 걸지 않았을 경우

	const slide = document.querySelector(".week");
	slide.classList.add("week-transition");
});

//https://eunhee-programming.tistory.com/106
const slides = document.querySelector(".week"); //전체 슬라이드 컨테이너
const slideDate = document.querySelectorAll("week_slideshow .date"); //모든 슬라이드들
let currentIdx = 0; //현재 슬라이드 index
const slideDateCount = slideDate.length; // 슬라이드 개수
const prev = document.querySelector(".prev"); //이전 버튼
const next = document.querySelector(".next"); //다음 버튼
const slideWidth = 50; //한개의 슬라이드 넓이
const slideMargin = 50; //슬라이드간의 margin 값

//전체 슬라이드 컨테이너 넓이 설정
//slides.style.width = (slideWidth + slideMargin) * slideDateCount + "px";

function moveSlide(num) {
	viewWidth = window.innerWidth;
	if (viewWidth >= 700) {
		slides.style.left = -num * 700 + "px";
	} else {
		slides.style.left = -num * viewWidth + "px";
	}
	currentIdx = num;
}

prev.addEventListener("click", function () {
	/*첫 번째 슬라이드로 표시 됐을때는 
이전 버튼 눌러도 아무런 반응 없게 하기 위해 
currentIdx !==0일때만 moveSlide 함수 불러옴 */
	if (currentIdx !== 0) moveSlide(currentIdx - 1);
});

next.addEventListener("click", function () {
	/* 마지막 슬라이드로 표시 됐을때는 
다음 버튼 눌러도 아무런 반응 없게 하기 위해
currentIdx !==slideCount - 1 일때만 
moveSlide 함수 불러옴 */
	if (currentIdx !== 4) {
		moveSlide(currentIdx + 1);
	}
});

const date_form = document.getElementById("date-form");

	function form_submit() {
	const xhr = new XMLHttpRequest();
	const formData = new FormData(date_form);
	const entries = formData.entries();

	let url = "/?";
	for (const pair of entries) {
		console.log(pair[1]);
		url += `${pair[0]}=${pair[1]}&`;
	}
	xhr.open("GET", url, true);
	xhr.setRequestHeader("x-requested-with", "XMLHttpRequest");

	xhr.onreadystatechange = function () {
		if (xhr.readyState == xhr.DONE) {
			if (xhr.status == 200 || xhr.status == 201) {

				const { matches } = JSON.parse(xhr.response);
				console.log(matches);
				document.getElementById("match-list").innerHTML = matches;
			}
		}
	};
	xhr.send();
	}


	date_form.addEventListener("submit", (e) => {
	e.preventDefault();
	form_submit();
});


const slide_list = document.querySelectorAll(".slide-list");
slide_list.forEach((e) => {
	e.addEventListener("change", (event) => {
		//무한로딩 방지
		event.preventDefault();
		form_submit();
	});
});


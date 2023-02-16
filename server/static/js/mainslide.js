const thisYear = date.getFullYear();
const thisMonth = date.getMonth();
const thisDate = date.getDate();
const thisDay = date.getDay();
const lastDate = new Date(thisYear, thisMonth + 1, 0).getDate();
daysKorean = ["일", "월", "화", "수", "목", "금", "토"];
days = [];
dates = [];

for (let i = thisDate; i <= lastDate; i++) {
  dates.push(i);
}
thisDateLength = dates.length;
for (let i = 1; i <= 31 - thisDateLength; i++) {
  dates.push(i);
}

let dayIndex = thisDay;
let flag = 0
dates.forEach((date, i) => {
  let condition =
    dayIndex % 7 == 0 ? "sun" : dayIndex % 7 == 6 ? "sat" : "rest_day";
  // i가 0이 아닌데 date가 1이면 달이 넘어갔다는 의미
  if (i != 0 && date == 1) {
    flag = 1
  }
  let now_month = flag ? thisMonth+2 : thisMonth+1
  let now_year = now_month/13 == 1 ? thisYear+1 : thisYear
  const urlstr = window.location.href
  const url = new URL(urlstr)
  const cur_date = url.searchParams.get('date')
  
  console.log(cur_date) 
  
  if (cur_date == `${now_year}-${now_month}-${date}`) {
  days[i] = `<input class = "slide-list" id = "date-${i}" type = "radio" name = "date" value = "${now_year}-${now_month}-${date}" checked>
  <label class = "date-select" style ="background-color:skyblue;" for="date-${i}">
  <li class='date ${condition}' name = "date"><div>${
    daysKorean[dayIndex++ % 7]
  }요일</div><div>${date}일</div></li>
  </label>
  `;
  }
  else {
    days[i] = `<input class = "slide-list" id = "date-${i}" type = "radio" name = "date" value = "${now_year}-${now_month}-${date}">
    <label class = "date-select" for="date-${i}">
    <li class='date ${condition}' name = "date"><div>${
      daysKorean[dayIndex++ % 7]
    }요일</div><div>${date}일</div></li>
    </label>
    `;
  }

});

const week = document.querySelector(".week");
week.innerHTML = days.join("");

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
  viewWidth = window.innerWidth
  if (viewWidth >= 700) {
    slides.style.left = -num * 700 + 'px'
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

const slide_list = document.querySelectorAll(".slide-list")
console.log(slide_list)
const date_form = document.getElementById("date-form")
slide_list.forEach((e) => {
  e.checked = true  
  e.addEventListener('click', event => {
    //무한로딩 방지
    event.preventDefault()
    
    date_form.submit()
  })
})


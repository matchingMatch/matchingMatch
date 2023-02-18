let date = new Date()
const makeCalendar = () => {
  const viewYear = date.getFullYear()
  const viewMonth = date.getMonth()

  document.querySelector('.year_month').textContent = `${viewYear}년 ${viewMonth+1}월`

  //이전달 마지막 날짜 가져오기
  let prevLast = new Date(viewYear, viewMonth, 0) //일을 0으로 지정하면 지난달 마지막 일을 반환
  let prevDate = prevLast.getDate() //이전 달의 마지막 일
  let prevDay = prevLast.getDay() //이전 달의 마지막 요일

  //이번 달 마지막 날짜 가져오기
  const thisLast = new Date(viewYear, viewMonth+1, 0)
  const thisDate = thisLast.getDate()
  const thisDay = thisLast.getDay()

  const prevDates = []  // []
  //Array(32): 길이가 32인 배열 생성. 요소는 모두 undefined
  //keys(): 인덱스를 요소로 바꿔줌
  //slice(i): i번째 인덱스부터...
  const thisDates = [...Array(thisDate + 1).keys()].slice(1)  // 1...31
  const nextDates = []  // [1, ..., 4]

  //이전 달 날짜 배열 채우기
  if (prevDay !== 6) {  //전 달 마지막 요일이 토요일이면, 전 달 날짜 배열이 필요 없음
    for(let i=0; i<=prevDay; i++) {
      prevDates.unshift(prevDate - i)
    }
  }
  //전달 마지막 요일이 목요일이면
  //31-0, 31-1, 31-2, 31-3, 31-4
  //31,   30,   29,   28,   27


  //다음 달 날짜 배열 채우기
  for(let i=1; i<7-thisDay; i++) {
    nextDates.push(i)
  }

  //날짜 그리기
  //dates라는 배열로 모두 합치기
  const dates = prevDates.concat(thisDates, nextDates)
  //[1, ... , 31, 1, ..., 4]
  
  //현재 달 첫번째 시작일의 인덱스, 마지막 일의 인덱스
  const firstDateIndex = dates.indexOf(1) //1이라는 값의 첫번째 인덱스 반환: 0
  const lastDateIndex = dates.lastIndexOf(thisDate) //31의 인덱스를 뒤에서 먼저 오는 것을 반환
  
  dates.forEach((date, i) => {
    const condition = i >= firstDateIndex && i <= lastDateIndex ? 'this' : 'other'
    //선택 대상이 아닌 경우
    dates[i] = `<div class="date"><span class="${condition}">${date}</span></div>`
    //선택 대상인 경우
    // dates[i] = `<input class = "calendar-list" id = "date-${i}" type = "radio" name = "date" value = "${now_year}-${now_month}-${date}" checked><label class="date" for = "date-${i}"><span class="${condition}">${date}</span></label>`    

  })


  
  //html dates 그리기
  document.querySelector('.calendar .dates').innerHTML = dates.join('')

  //오늘 날짜 표시
  const today = new Date()
  //viewMonth와 viewYear는 현재 보여지는 년과 열
  //따라서 이번달이 아닌 달을 보여줄 땐 오늘이 표시되지 않기 때문에 비교문을 진행해야 함
  if(viewMonth === today.getMonth() && viewYear === today.getFullYear()) {
    for (let date of document.querySelectorAll('.this')) {
      //+: 문자열을 숫자로
      if(+date.innerText === today.getDate()) {
        date.classList.add('today')
        break
      }
    }
  }
}

//함수 실행
makeCalendar()

//이전 달 그리는 함수
const prevMonth = () => {
  date.setDate(1) //일을 1로 바꾼다
  date.setMonth(date.getMonth() - 1)
  makeCalendar()
}
//다음 달 그리는 함수
const nextMonth = () => {
  date.setDate(1)
  date.setMonth(date.getMonth() + 1)
  makeCalendar()
}
//현재 달 그리는 함수
const curMonth = () => {
  date = new Date()
  makeCalendar()
}

//버튼에 이벤트 설정하기
const goPrev = document.querySelector('.go_prev')
const goToday = document.querySelector('.go_today')
const goNext = document.querySelector('.go_next')
goPrev.addEventListener('click', ()=>prevMonth())
goToday.addEventListener('click', ()=>curMonth())
goNext.addEventListener('click', ()=>nextMonth())
const checkMode = (e, theother) => {
  document.querySelector(`.${e.target.value}`).style.display = 'block'
  document.querySelector(`.${theother}`).style.display = 'none'
}
const slideModeBtn = document.querySelector('#slide')
const calendarModeBtn = document.querySelector('#calendar')
slideModeBtn.addEventListener('click', (e) => checkMode(e, 'calendar_container'))
calendarModeBtn.addEventListener('click', (e) => checkMode(e, 'week_slideshow'))

const sendRequest = async () => {
  const url = "/match/ended/";
  let userMatches = await axios.get(url);
  userMatches = userMatches.data.userMatches;
  console.log("userMatches:", userMatches);
  createModal(userMatches);
};
//document.querySelector("header h1").addEventListener("click", sendRequest);

sendRequest();
window.setInterval(sendRequest, 10000); //30분마다 Ajax 요청

const createModal = (userMatches) => {
  const alarmModalList = document.querySelector(".alarm_modal_list");
  alarmModalList.innerHTML = "";
  for (let i = 0; i < userMatches.length; i++) {
    match = userMatches[i];
    alarmModalList.innerHTML += `
  <div class="alarm_modal" id="${i}">
    <div>${match.host_teamname} VS ${match.participant_teamname}</div>
    <div>경기 종료 시간: ${match.end_time}</div>
    <div>즐거운 경기 되셨나요? 수고한 상대팀에게 좋은 점수 부탁드려요!</div>
    <form action="/rate/${match.match_id}" method="post">
      {% csrf_token %}
      <label>실력: <input name="level" type="number" max="10"></label>
      <label>매너: <input name="manner" type="number" max="10"></label>
      <div class="rate_save">
        <input type="submit" value="완료">
      </div>
    </form>
  </div>
  `;
  }
};
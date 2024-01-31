# 매칭매치 MatchingMatch

<div align="center">
<img width="300" alt="image" src="./server/static/img/main_logo.png">
</div>

안녕하세요. 웹개발 연합동아리 피로그래밍 18기 '매칭매치'입니다.

매칭매치는 축구 경기의 매칭을 도와주는 웹서비스입니다.

## 배포 주소

> https://www.matchingmatch.site

## 멤버 소개

- 송현지 : 프론트엔드, 팀장
- 최유진 : 프론트엔드
- 김혁수 : 풀스택
- 김태영 : 백엔드
- 김환준 : 백엔드

## 프로젝트 소개

> **축구 경기의 매칭을 도와주는 웹서비스** <br/> **개발기간: 2023.01 ~ 2023.02**

'매칭매치'는 축구 경기의 매칭을 도와주는 웹서비스입니다. 날짜, 지역, 성별, 마감여부 등으로 필터링을 통해 원하는 매치를 생성하거나 조회할 수 있습니다. 경기가 완료된 후 상태팀을 평가할 수 있으며, 이는 추후에 매너점수와 실력점수 평가에 반영됩니다.

## 설치 방법

### Requirements

For building and running the application you need:

- Python 3.11.1
- Django 4.2.7

### Installation

1. 레포지토리 클론

```bash
$ git clone https://github.com/matchingMatch/matchingMatch.git
$ cd server
```

2. 가상 환경 생성

```bash
$ python -m venv venv
$ source venv/bin/activate // Mac
$ venv\Scripts/activate    // Windows
```

3. 필요한 패키지 설치

```bash
$ pip install -r requirements.txt
```

4. 데이터베이스 마이그레이션

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

5. 서버 실행

```bash
$ python manage.py runserver
```

## 기술 스택

### Environment

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)

### Config

![npm](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)

### Development

![HTML5](https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=black)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS3&logoColor=black)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=Bootstrap&logoColor=black)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

### Communication

![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white)
![GoogleMeet](https://img.shields.io/badge/GoogleMeet-00897B?style=for-the-badge&logo=Google%20Meet&logoColor=white)

---

## 주요 페이지

|                                                         메인 페이지                                                          |                                                        팀목록 페이지                                                         |
| :--------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------: |
| <img width="329" src="https://github.com/matchingMatch/matchingMatch/assets/70899438/9c931898-3fde-49b1-8f62-7f84e4aa3f6b"/> | <img width="329" src="https://github.com/matchingMatch/matchingMatch/assets/70899438/413d826f-25d4-4ad0-b23c-4b13b2fd12f8"/> |
|                                                       공지사항 페이지                                                        |                                                      신고게시판 페이지                                                       |
| <img width="329" src="https://github.com/matchingMatch/matchingMatch/assets/70899438/c0336e8a-c920-4c4f-af17-2abe152ac94c"/> | <img width="329" src="https://github.com/matchingMatch/matchingMatch/assets/70899438/01c79685-a2a1-4c16-b247-01b08f35f506"/> |

---

## 주요 기능

### ⭐️ 메인 페이지

- 매치 등록(리캡챠 도입)
- 매치 필터링 조회(날짜, 지역, 성별, 마감여부)
- 로그인/회원가입
- 경기 종료 후 상대팀 평가 알림창이 표시됨

### ⭐️ 매치 상세페이지

- 팀명, 경기장, 시간 조회
- 지도를 통한 위치 조회
- 작성자는 신청자 목록 조회 및 선정 가능
- 신청자는 매치 신청 가능

### ⭐️ 팀목록 페이지

- 팀 조회
- 팀 검색

### ⭐️ 공지사항 페이지

- 공지사항 조회
- 관리자는 공지사항 글 작성 가능

### ⭐️ 신고게시판 페이지

- 애로사항, 신고사항 글 조회 및 작성

---

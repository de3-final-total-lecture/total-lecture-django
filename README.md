# 온라인 강의 통합 서비스 (OLLI) Django

## 프로젝트 소개
1. 프로젝트 개요

온라인 강의 플랫폼이 증가함에 따라 교육 콘텐츠의 폭이 확장되었고, 이로 인해 강의 탐색을 위한 시간과 노력이 많이 소요되어, 여러 인터넷 강의 사이트의 정보를 한 곳에 모아 통합 검색 및 가격 히스토리 추척 기능을 제공하는 웹사이트 **OLLI**를 구축


2. 프로젝트 목표
- Udemy, Cousera, Inflean 주요 인터넷 
- 강의 플랫폼 데이터 크롤링 자동화
- 크롤링한 데이터를 전처리해 규격화된 데이터로 일반화
- 통합 검색을 위한 DJango를 통한 WebUI 구성
- 사용자의 행동 기반 추천 시스템 구성

## 인프라 아키텍쳐
<img width="1350" alt="infra-architecture" src="https://github.com/user-attachments/assets/6685d32e-6533-4031-8258-d9623802c79c"/>


## 기술 스택
- Data Extract: <img src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=Apache%20Airflow&logoColor=white"/>
- Data Store: <img src="https://img.shields.io/badge/Amazon%20S3-569A31?style=flat&logo=Amazon%20S3&logoColor=white"/> <img src="https://img.shields.io/badge/mysql-4479A1.svg?style=flat&logo=mysql&logoColor=white"/>
- Data Processing: <img src="https://img.shields.io/badge/Amazone%20Glue-937401?style=flat&logo=GLUE&logoColor=ffdd54"/> <img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54"/> <img src="https://img.shields.io/badge/OpenAI-228877?style=flat&logo=openai&logoColor=White"/>
- Web Programming: <img src="https://img.shields.io/badge/django-%23092E20.svg?style=flat&logo=django&logoColor=white"/>
- CI/CD Tool: <img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=GitHub&logoColor=white"> <img src="https://img.shields.io/badge/Gather-2535A0?style=flat&logo=Gather&logoColor=white"> <img src="https://img.shields.io/badge/Slack-4A154B?style=flat&logo=Slack&logoColor=white"> <img src="https://img.shields.io/badge/Notion-000000?style=flat&logo=Notion&logoColor=white">



## 데이터 파이프라인
![데이터 파이프라인](https://github.com/user-attachments/assets/f0b8b6ce-2d87-49d5-b23a-8fe43129e3a2)


## Django 프로젝트 구조
Project : IntegrateLecture
- App1 : lecture
<br/>

## 개발환경 시작

1. 실행 환경을 준비합니다.<br/>
  (1) 본 레포지토리를 clone 합니다.<br/>
  (2) python 3.11을 설치합니다.<br/>
  (3) 프로젝트 최상위 경로(IntegrateLecture/)에서 requirements.txt의 라이브러리들을 설치합니다.<br/>
2. 로컬 데이터베이스를 준비합니다.<br/>
  (1) 로컬에 MySQL을 설치합니다.<br/>
  (2) MySQL에 데이터베이스를 생성합니다.<br/>
  (3) 프로젝트 최상위 경로(IntegrateLecture/)에서 .env 파일을 아래와 같이 생성합니다.<br/>
```text
DB_NAME=yourDBName
DB_USER=yourUserName
DB_PASSWORD=yourPassword
DB_HOST=yourHost
DB_PORT=3306
```
3. 데이터를 마이그레이션합니다. 프로젝트 최상위 경로(IntegrateLecture/)에서 다음의 명령어들을 차례대로 실행합니다.<br/>
  (1) python manage.py makemigrations<br/>
  (2) python manage.py migrate<br/>
4. 서버를 실행합니다.<br/>
  (1) 프로젝트 최상위 경로(IntegrateLecture/)에서 'python manage.py runserver'를 실행합니다.<br/>
  (2) 'localhost:8000/main 접속<br/>


## 결과물
### 메인 페이지
<img width="1350" alt="main" src="https://github.com/user-attachments/assets/3ffdcd9b-ba3f-4dca-81fc-7343e0bd6f75"/>
### 사용자 맞춤 추천 베너
<img width="1350" alt="recommendbanenr" src="https://github.com/user-attachments/assets/1b9de65b-69de-41ad-b4d0-0ed5c5a1328d">

### 강의 세부 페이지
<img width="1350" alt="detail" src="https://github.com/user-attachments/assets/ba6983a7-5ad1-4db3-81de-e1ed166d93ae"/>

### 강의 리뷰 분석
<img width="1350" alt="review-analysis" src="https://github.com/user-attachments/assets/e01223e5-24b8-4457-b760-46f34bb60b36"/>

### 강의 가격 히스토리 그래프
- Udemy, Inflearn의 경우
<img width="1350" alt="price-history" src="https://github.com/user-attachments/assets/05557cdc-108f-40e9-a341-997b4f87588d"/>

- Coursera의 경우 (구독제)
<img width="1350" alt="price-history-coursera" src="https://github.com/user-attachments/assets/6e9943ad-affc-48b3-858d-f58e7d388e0e"/>

## 팀원 및 역할
* 김승훈: 인프런 DAG 작성 및 전체 DAG 통합
* 김승현: Coursera DAG 작성, 프론트엔드 및 백엔드 개발
* 김동기: Udemy DAG 작성, 백엔드 및 강의 추천 시스템 개발
* 김유민: 인프라 구축 및 리뷰 분석 및 카테고리 DAG 작성





## 참여자 정보
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/kdk0411"><img src="https://avatars.githubusercontent.com/u/99461483?v=4" width="100px;" alt=""/><br /><sub><b>김동기</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/zjacom"><img src="https://avatars.githubusercontent.com/u/112957047?v=4" width="100px;" alt=""/><br /><sub><b>김승훈</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/Kim-2301"><img src="https://avatars.githubusercontent.com/u/84478606?v=4" width="100px;" alt=""/><br /><sub><b>김승현</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/7xxogre"><img src="https://avatars.githubusercontent.com/u/61622859?v=4" width="100px;" alt=""/><br /><sub><b>김유민</b></sub></a><br /></td>
    </tr>
  </tbody>
</table>





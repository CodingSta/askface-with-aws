# Amazon Web Service AI API와 파이썬/장고를 통해 아이돌 안면인식 장애 해결하기

## 프로젝트 셋업

1. 먼저 파이썬3 최신버전을 설치해주세요.
    - 윈도우에서는 Anaconda Python을 추천합니다.
2. 명령 프롬프트를 띄우신 후, 프로젝트 디렉토리로 이동해주세요.
3. 다음 명령으로 필요한 팩키지를 설치해주세요.

```sh
pip install -r requirements.txt
```

4. 다음 명령으로 데이터베이스를 생성합니다.

```sh
python manage.py migrate
```

5. 다음 명령으로 슈퍼유저 계정을 생성합니다.

```sh
python manage.py createsuperuser
```

## `askcompany/settings.py` 경로에 AWS 설정 정보를 넣어주세요.

다음 코드 부분을 직접 설정을 넣으실 수도 있지만, 보안 상의 이유로 아래 내역대로 환경변수를 통해 읽어들이시기를 추천합니다.

```python
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
```

## 개발서버 구동

다음 명령으로 개발서버를 구동해주세요.

```sh
python manage.py runserver
```

## admin 페이지 접속

1. 웹브라우저를 통해 `http://localhost:8000/admin`으로 접속하고, 조금 전에 생성한 슈퍼유저 계정으로 접속해주세요.
2. `Korean-Idol` Collection을 생성해주세요.
3. 아이돌 별로 개별 Person을 생성하시고, 사진을 등록해주세요.

## 서비스 활용

`http://localhost:8000` 주소로 접속하시어, 학습한 아이돌에 대해서 다른 사진으로 쿼리해보세요. ;)

---

여러분의 파이썬/장고/Pandas 페이스메이커가 되겠습니다.

+ https://fb.com/groups/askdjango
+ https://www.askcompany.kr
+ me@askcompany.kr

---

AskCompany VOD를 통해 파이썬/장고를 효율적으로 익혀보세요. (유료 구독서비스)

+ [개발환경 구축하기](https://www.askcompany.kr/vod/setup/) (공개VOD)
+ [파이썬 차근차근 시작하기](https://www.askcompany.kr/vod/python/) (구독VOD)
+ [파이썬을 통한 자동화](https://www.askcompany.kr/vod/automation/) (구독VOD)
+ [파이썬을 통한 크롤링](https://www.askcompany.kr/vod/crawling/) (구독VOD)
+ Pandas 코스
    - [(초급) Pandas 워밍업](https://www.askcompany.kr/r/sections/f5bf323/) (구독VOD)
    - [(초급) 10 Minutes to Pandas 따라하기](https://www.askcompany.kr/r/sections/d8ccb08/) (구독VOD)
+ [장고 차근차근 시작하기](https://www.askcompany.kr/vod/django/) (구독VOD)
+ [Ask Company 시즌2](https://www.askcompany.kr/r/)

다양한 파이썬 VOD 컨텐츠들이 주단위로 계속 갱신됩니다.


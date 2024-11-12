# Backend User Service

## Directory Tree
```javascript
backend-user/
├── app/
│   ├── routers/
│   │   ├── login.py          # 카카오 소셜 로그인
│   │   ├── onboarding.py     # 초기 회원 회원 가입
│   │   ├── profile.py        # 프로필 관리
│   │   └── admin.py          # 관리자 페이지용
│   ├── database/             # SSH Tunneling & DB 설정
│   ├── models/               # SQLAlchemy ORM 기반 DB 스키마 정의
│   ├── schemas/              # Pydantic 기반 모델 정의
│   └── services/             # CRUD
├── alembic/                  # DB 마이그레이션, 버전 관리
├── alembic.ini               # FastAPI App
├── main.py                   # FastAPI App
├── requirements.txt 
├── .env                 
├── .gitignore           
└── .venv/               # 가상 환경
```

## 개발 환경 세팅
1. virtural env 설정
    ```shell
   pip3 install virtualenv
   virtualenv .venv --python=python3.12
   source .venv/bin/activate
   ```
2. 패키지 설치
   ```shell
   pip3 install -r requirements.txt
   ```


## 개발
1. 브랜치
   - `<category>/<name>`의 네이밍 (e.g. `feat/photo-upload`, `fix/upload-bug`) ([카테고리 참고](https://github.com/pvdlg/conventional-changelog-metahub#commit-types)) 
2. 파일 수정 시 
   - lint 체크 후 메이져 이슈들은 수정 부탁드립니다. pylint 사용합니다.
   ```shell
   make lint
   ```
   - 패키지 체크
   ```shell
   make generate-requirements
   ```
3. 커밋
   - 한글로 쓰시던 영어로 쓰시던 편하신대로. `<category>: <message>` 형식만 지켜주세요
   - 옛날에 읽었던 [좋은 커밋 메세지 쓰는 법](https://chris.beams.io/posts/git-commit/)?? 입니다. 참고만 해주세요
4. Pull Request
   - PR = 1 커밋을 원칙으로 (pr 하나에 커밋이 여러 개면 리뷰가 힘들어요ㅜㅜ)
   - 사소한 내용일 경우 셀프 머지도 허용 
   - 머지 방식은 개인적으로 rebase merge를 선호합니다.

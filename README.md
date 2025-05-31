# 코딩테스트 사이트 문제 풀이 자동 백업
코딩테스트 사이트(백준, 프로그래머스)에서 풀었던 문제들의 코드를 GitHub 저장소에 백업하는 기능의 레포지토리입니다.

## 기능
- 각 사이트 계정으로 로그인
- 해결한 문제 목록 자동 수집
- 각 문제의 해결 코드 자동 다운로드
- GitHub 저장소에 자동 업로드

## 설치 방법
chromedriver는 해당 레포지토리에 설치합니다. (자동화 예정)
```bash
pip install -r requirements.txt
```

## 사용 방법

1. 다음 명령어로 스크립트를 실행합니다:
```bash
python get_solutions_{site}.py
```
2. github token, github repo를 차례대로 입력합니다.
3. 사이트에 로그인 한 후, python파일을 실행한 터미널로 돌아와 엔터를 입력합니다.

## github 업로드 방식

다음과 같은 구조로 파일들이 업로드 됩니다.
```
{your_github_repo}/programmers/~~~~.py
{your_github_repo}/programmers/~~~~.py
{your_github_repo}/programmers/~~~~.py
{your_github_repo}/baekjoon/~~~~.py
{your_github_repo}/baekjoon/~~~~.py
{your_github_repo}/baekjoon/~~~~.py
```

## 주의사항
- 코드를 작성했을 당시의 웹사이트 CSS구조를 기반으로 동작합니다.
- GitHub 토큰은 필요한 권한(repo)이 있어야 합니다.
- API 요청 제한에 주의하세요. 

## 업데이트 내역
- 25.06.01 : get_solutions_programmers.py의 argument로 문제 idx를 받아서 특정 문제를 저장소에 업로드하는 동작 방식 추가
             예시 - python3 get_solutions_programmers.py 258709 : https://school.programmers.co.kr/learn/courses/30/lessons/258709 문제풀이 업로드
             기존 사용법 : 인자를 주지않으면 전체 업로드
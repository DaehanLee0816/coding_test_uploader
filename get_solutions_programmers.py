import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from github import Github

def get_solutions_programmers(solved_num = 0):
    # GitHub 설정
    github_token = input("GitHub 토큰을 입력하세요: ")
    repo_name = input("GitHub 저장소 이름을 입력하세요 (예: coding-test-solutions): ")
    
    # GitHub 연결
    g = Github(github_token)
    user = g.get_user()
    try:
        repo = user.get_repo(repo_name)
    except:
        repo = user.create_repo(repo_name, description="프로그래머스 코딩테스트 풀이 저장소")
    
    # 1. 크롬 브라우저 자동 실행 및 프로그래머스 접속
    driver = webdriver.Chrome()
    driver.get('https://programmers.co.kr/')

    # 2. 로그인
    input("로그인하고 엔터를 누르세요...")

    # 3. 내 프로필(풀이) 페이지로 이동
    driver.get('https://school.programmers.co.kr/learn/challenges?order=recent&page=1&statuses=solved')
    time.sleep(2)

    # 4. 푼 문제 목록에서 문제 링크 수집
    problem_links = []
    page = 1
    
    while True:
        try:
            # 문제 링크 수집
            captured = False
            problems = driver.find_elements(By.CSS_SELECTOR, "a[href*='/learn/courses/30/lessons/']")
            print(problems)
            for elem in problems:
                href = elem.get_attribute('href')
                print(href)
                if href and href not in problem_links:
                    problem_links.append(href)
                
                if solved_num > 0 and len(problem_links) >= solved_num:
                    captured = True
                    break
            if captured:
                break
            
            # 다음 페이지 버튼 클릭
            next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='다음 페이지']")
            if not next_button.is_enabled():
                break
            next_button.click()
            page += 1
            time.sleep(2)
        except:
            break

    print(f"총 {len(problem_links)}개의 문제를 찾았습니다.")

    # 5. 각 문제 페이지에서 코드 크롤링
    for link in problem_links:
        try:
            driver.get(link)
            time.sleep(2)
            
            # 문제 제목
            title_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.challenge-title"))
            )
            title = title_elem.text.strip()

            # 프로그래밍 언어
            language_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-sm.btn-dark.dropdown-toggle"))
            )
            language = language_elem.text.strip()
            
            # 내 코드
            code_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#code"))
            )
            code = code_elem.get_attribute('value')
            
            # 파일명 생성 (특수문자 제거)
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            if language == "Python3":
                filename = f"{safe_title}.py"
            elif language == "C++":
                filename = f"{safe_title}.cpp"
            else:
                continue
            
            # GitHub에 파일 업로드
            path = f"programmers/{filename}"
            try:
                # 파일이 이미 존재하는지 확인
                try:
                    repo.get_contents(path)
                    # 파일이 존재하면 업데이트
                    contents = repo.get_contents(path)
                    repo.update_file(
                        path=path,
                        message=f"Update solution for {title}",
                        content=code,
                        sha=contents.sha
                    )
                except:
                    # 파일이 없으면 새로 생성
                    repo.create_file(
                        path=path,
                        message=f"Add solution for {title}",
                        content=code
                    )
                print(f"Successfully uploaded: {path}")
            except Exception as e:
                print(f"Error uploading {path}: {str(e)}")
                
        except Exception as e:
            print(f"Error processing {link}: {str(e)}")
            continue

    # 6. 작업 끝나면 브라우저 종료
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solved_num = int(sys.argv[1])
    else:
        solved_num = 0
    get_solutions_programmers(solved_num)
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from github import Github

def get_solutions_programmers():
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
    driver.get('https://www.acmicpc.net/')

    # 2. 로그인
    input("로그인하고 엔터를 누르세요...")

    # 3. 개인화면 페이지로 이동
    # 첫 번째 li의 a 태그의 href 가져오기
    username_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.loginbar.pull-right li:first-child a"))
    )
    username_href = username_elem.get_attribute('href')
    driver.get(username_href)

    # 4. 푼 문제 목록에서 문제 링크 수집
    problem_links = []
    page = 1
    
    
    try:
        # 문제 링크 수집
        problems = driver.find_elements(By.CSS_SELECTOR, "div.problem-list a.result-ac")
        for elem in problems:
            href = elem.get_attribute('href')
            if href and href not in problem_links:
                problem_links.append(href)
                print(f"문제 링크 추가: {href}")

        print(f"총 {len(problem_links)}개의 문제를 찾았습니다.")
    except:
        raise Exception("문제 링크 수집 실패")

    # 5. 각 문제 페이지에서 코드 크롤링
    for link in problem_links:
        try:
            # 문제 페이지로 이동
            driver.get(link)
            time.sleep(2)
            
            # 문제 제목
            title_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span#problem_title"))
            )
            title = title_elem.text.strip()

            problem_id = link.split('/')[-1]
            
            # 내 제출 링크로 이동
            submit_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/status?from_mine=1']"))
            )
            submit_href = submit_link.get_attribute('href')
            print(submit_href)
            driver.get(submit_href)
            time.sleep(2)
            
            # 가장 최근의 맞은 제출 코드 링크 찾기
            code_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-can-view='1']:first-child td:nth-child(7) a[href*='/source/']"))
            )
            code_href = code_link.get_attribute('href')
            print(code_href)
            language = code_link.text.strip()
            print(language)
            driver.get(code_href)
            time.sleep(5)
            
            # 코드 가져오기
            code_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='source']"))
            )
            code = code_elem.get_attribute('value')
            print(code)
            
            # 파일명 생성 (특수문자 제거)
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            
            # 언어에 따른 파일 확장자 설정
            if "python" in language.lower():
                filename = f"{problem_id}_{safe_title}.py"
            elif "c++" in language.lower():
                filename = f"{problem_id}_{safe_title}.cpp"
            elif "java" in language.lower():
                filename = f"{problem_id}_{safe_title}.java"
            else:
                continue
            
            print(filename)
            # GitHub에 파일 업로드
            path = f"baekjoon/{filename}"
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
    get_solutions_programmers()
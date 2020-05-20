# Youtube_text_mining
Text mining : Youtube User Preference Analysis
## requirment
- pandas
- selenium
- BeautifulSoup
- konlpy
- numpy
- plotly

## 내용
해당 분석은 크게 두개의 과정으로 나뉩니다. 첫번째는 데이터를 수집하는 과정이고, 두번째는 가공, 분석, 시각화 하는 것입니다.
첫번째로 수집은 Selenium과 bf4를 이용하여 벤치마킹 대상 채널의 게시글들의 제목과 좋아요수, 조회수, 싫어요수, 개시날짜를 수집합니다.
이 과정에서 자연어 데이터의 기본적인 전처리를 진행한 상태로 수집합니다. 분석은 특별히 Jupyter를 사용하는데 그 이유는 해당 프로젝트에서 사용한 Plotly와 같이 데이터를 시각화 하기에 유용한 패키지가 Jupyter에서만 사용이 가능하기 때문입니다.

## 결과 예시

# 임베딩 실습 예제 파일

같은 텍스트를 OpenAIEmbeddings, HuggingFaceEmbeddings, UpstageEmbeddings, OllamaEmbeddings에 넣고 결과를 비교할 수 있도록 만든 데이터입니다.

## 파일 구성

| 파일 | 실습 목적 |
| --- | --- |
| 01_embedding_documents.csv | 기본 문서 임베딩과 의미 검색 |
| 02_search_queries.csv | embed_query와 검색 정확도 평가 |
| 03_similarity_pairs.csv | Cosine Similarity 비교 |
| 04_cache_and_duplicate_test.csv | CacheBackedEmbeddings와 중복 탐지 |
| 05_clustering_documents.csv | 문서 군집 실습 |
| 06_multilingual_documents.csv | 한국어와 영어 다국어 임베딩 비교 |
| 07_basic_documents.txt | 처음 embed_documents 실습에 사용하는 짧은 문서 |
| 08_embedding_metadata.json | 모델, 차원, 정규화, namespace 기록 예시 |

## 추천 실습 순서

1. 07_basic_documents.txt를 읽어 embed_documents()로 벡터를 생성합니다.
2. 질문 하나를 embed_query()로 변환하고 각 문서와 Cosine Similarity를 계산합니다.
3. 01_embedding_documents.csv와 02_search_queries.csv를 이용해 Top 3 검색 결과를 확인합니다.
4. 03_similarity_pairs.csv에서 의미가 비슷한 문장과 관련 없는 문장의 점수 차이를 비교합니다.
5. 04_cache_and_duplicate_test.csv를 두 번 임베딩하여 CacheBackedEmbeddings의 실행 시간을 비교합니다.
6. exact_group 문장은 캐시 재사용을 확인하고 semantic_group 문장은 벡터 유사도로 중복 후보를 찾습니다.
7. 05_clustering_documents.csv를 임베딩한 뒤 군집을 만들고 true_category와 비교합니다.
8. 06_multilingual_documents.csv에서 같은 의미의 한국어와 영어 문장이 서로 가까운지 확인합니다.
9. OpenAI, HuggingFace, Upstage, Ollama에서 같은 질문을 실행해 검색 순위와 처리 시간을 비교합니다.
10. 모델 설정은 08_embedding_metadata.json처럼 기록합니다.

## 추천 질문

- 설비에서 진동 이상이 발생했어
- 베어링이 너무 뜨거워졌어
- 진공이 원하는 수준까지 안 내려가
- 윤활유는 언제 바꿔야 해
- 생산량이 왜 줄었지
- 전기 사용량을 줄이는 방법

## 관찰 포인트

- 문서 벡터와 질문 벡터의 차원이 같은가
- 가장 의미가 가까운 문서가 Top 1에 검색되는가
- 표현은 다르지만 의미가 같은 문장의 유사도가 높은가
- exact duplicate와 semantic duplicate의 차이가 보이는가
- normalize_embeddings=True일 때 Dot Product와 Cosine Similarity가 비슷하게 나오는가
- 임베딩 모델을 바꾸면 검색 순위가 달라지는가
- 같은 텍스트를 다시 임베딩했을 때 캐시가 재사용되는가

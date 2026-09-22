# VectorStore 실습 파일

동일한 Document 집합을 Chroma, FAISS, Pinecone에서 공통으로 사용할 수 있도록 만든 데이터입니다.

## 파일 구성

| 파일 | 실습 목적 |
| --- | --- |
| 01_vectorstore_documents.csv | 기본 인덱싱, 유사도 검색, score, metadata |
| 02_search_queries.csv | 실제 질문 기반 k와 검색 결과 평가 |
| 03_mmr_documents.csv | similarity와 MMR 검색 결과 비교 |
| 04_crud_operations.json | 문서 추가, 수정, 삭제 실습 |
| 05_namespace_documents.json | 버전과 환경별 namespace 분리 |
| 06_index_manifest.json | 모델, 차원, 저장 위치, 복원 설정 기록 |
| 07_filter_challenges.csv | metadata filter 연습 |
| sources/ | 원본 문서를 VectorStore와 별도로 보존하는 예시 |

## 추천 실습 순서

1. 01_vectorstore_documents.csv를 LangChain Document로 변환합니다.
2. document_id를 VectorStore ID로 사용합니다.
3. Chroma에 전체 문서를 저장하고 similarity_search를 실행합니다.
4. 02_search_queries.csv에서 k를 1, 3, 5로 바꿔 결과를 비교합니다.
5. category, equipment, plant, severity 필터를 적용합니다.
6. similarity_search_with_score로 점수와 정렬 방향을 확인합니다.
7. 03_mmr_documents.csv로 similarity와 MMR의 결과 다양성을 비교합니다.
8. Chroma persist_directory와 FAISS save_local, load_local을 이용해 복원합니다.
9. 04_crud_operations.json 순서대로 add, update, delete를 수행합니다.
10. Pinecone에서는 05_namespace_documents.json을 namespace별로 나누어 저장합니다.
11. 06_index_manifest.json처럼 임베딩 모델과 차원 설정을 기록합니다.
12. sources 폴더의 원본 문서는 VectorStore와 별도로 보존합니다.

## 추천 질문

- 모터가 심하게 떨릴 때 무엇을 점검해야 하나요?
- 진공이 목표 압력까지 내려가지 않습니다.
- 베어링 윤활유는 언제 교체하나요?
- 프레스 내부 작업 전 안전 조치는 무엇인가요?
- 생산량 감소와 관련된 문서를 찾아주세요.
- 전력 절감 방법을 다양하게 찾아주세요.

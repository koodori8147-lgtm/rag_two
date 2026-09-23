# Retriever 실습 예제 파일

이 폴더는 LangChain Retriever 실습에서 검색 방식별 차이가 잘 드러나도록 만든 예제 데이터입니다.

| 파일 | 추천 실습 |
| --- | --- |
| 01_common_documents.csv | VectorStoreRetriever, similarity, MMR, filter |
| 02_long_parent_documents.json | ContextualCompressionRetriever, ParentDocumentRetriever |
| 03_keyword_bm25_documents.csv | EnsembleRetriever, BM25 + Vector Search |
| 04_reorder_documents.csv | LongContextReorder |
| 05_multiquery_questions.csv | MultiQueryRetriever |
| 06_multivector_documents.json | MultiVectorRetriever |
| 07_selfquery_documents.csv | SelfQueryRetriever 문서 |
| 08_selfquery_questions.csv | 자연어 조건을 메타데이터 필터로 변환 |
| 09_timeweighted_documents.json | TimeWeightedVectorStoreRetriever |
| 10_retrieval_evaluation.csv | Recall@k, Precision@k, MRR 평가 |
| 11_compression_long_report.md | LLM 기반 문서 압축 |
| sources/ | Parent 문서 원본 Markdown |

## 추천 순서

1. 01_common_documents.csv로 기본 VectorStoreRetriever를 구성합니다.
2. similarity, mmr, filter를 비교합니다.
3. 11_compression_long_report.md로 ContextualCompressionRetriever를 실습합니다.
4. 03_keyword_bm25_documents.csv로 BM25와 Vector Search를 각각 수행하고 EnsembleRetriever로 합칩니다.
5. 04_reorder_documents.csv의 검색 결과에 LongContextReorder를 적용합니다.
6. 02_long_parent_documents.json 또는 sources 폴더로 ParentDocumentRetriever를 실습합니다.
7. 05_multiquery_questions.csv로 MultiQueryRetriever의 질의 확장 효과를 확인합니다.
8. 06_multivector_documents.json의 summary와 hypothetical_questions를 자식 벡터로 저장하고 full_text를 반환합니다.
9. 07_selfquery_documents.csv와 08_selfquery_questions.csv로 year, priority, equipment 조건을 추출합니다.
10. 09_timeweighted_documents.json으로 의미 유사도와 최신성의 영향을 비교합니다.
11. 10_retrieval_evaluation.csv로 Recall@k, Precision@k, MRR을 계산합니다.

## 바로 써볼 질문

- 모터가 평소보다 흔들려요
- MTR-A17 점검 방법
- ALM-0421은 어떤 알람이야
- 2025년에 작성된 중요도 3의 안전 문서 2개
- 진공이 잘 안 잡힐 때 어디부터 확인해
- 프레스 제품 크기가 이상해

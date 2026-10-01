"""교육생용 RAG 구현 템플릿.

이 파일은 완성본이 아닙니다. ``notebook/rag_00.ipynb``에서 실습한 내용을
TODO 블록에 작성하면 ``app.py``와 교육생 평가 파일 생성 기능에서 바로
사용할 수 있습니다.

교육생은 아래 RAG 동작만 구현합니다.
1. PDF 문서 로드
2. 문서 청크 분할
3. 임베딩, Vector Store, retriever 구성
4. 검색 문맥을 사용하는 프롬프트와 LLM 구성

앱과 자동평가가 사용하는 ``PDF_PATH``, ``ask()``, ``get_status()``의 이름과
``ask()``의 구현은 제공됩니다.
"""

from __future__ import annotations

# =============================================================================
# [블록 0] 라이브러리 가져오기
# =============================================================================
# 아래 기본 라이브러리는 제공됩니다.
# rag_00.ipynb에서 사용한 LangChain Loader, Text Splitter, Embeddings,
# Vector Store, Prompt, Chat Model 등의 import 문을 이 영역에 추가하세요.
#
# 주의:
# - `%pip`, `!pip`, `display()` 같은 노트북 전용 명령은 옮기지 않습니다.
# - 사용하지 않는 테스트·출력용 라이브러리는 추가하지 않습니다.

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# TODO 0: 노트북에서 사용한 RAG 관련 import 문을 아래에 작성하세요.
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =============================================================================
# [블록 1] 환경 변수와 문서 경로 - 제공 코드, 수정하지 않음
# =============================================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "data" / "생성형_AI윤리_가이드북_RAG시험용_30쪽.pdf"


def _require_api_key() -> None:
    """OpenAI 호출 전에 API 키 설정 여부를 확인한다."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY가 없습니다. 프로젝트 루트의 .env 파일에 "
            "OPENAI_API_KEY=... 형식으로 설정해 주세요."
        )


# =============================================================================
# [블록 2~5] RAG 구성 - 교육생 작성 영역
# =============================================================================
# 이 함수 안에 PDF 로드부터 retriever, prompt, llm 생성까지 작성하세요.
#
# @lru_cache를 삭제하면 질문할 때마다 PDF 전체를 다시 임베딩하여 시간과
# API 비용이 증가합니다. 데코레이터와 함수 이름은 변경하지 마세요.


@lru_cache(maxsize=1)
def _build_rag() -> tuple[Any, Any, Any]:
    """retriever, prompt, llm을 생성하여 반환한다."""
    _require_api_key()
    if not PDF_PATH.is_file():
        raise FileNotFoundError(f"시험 문서를 찾을 수 없습니다: {PDF_PATH}")

    # 교육생 공통 변수입니다. 이름을 바꾸지 말고 각 단계의 결과를 대입하세요.
    pages: Any = None
    chunks: Any = None
    embeddings: Any = None
    vector_store: Any = None
    retriever: Any = None
    prompt: Any = None
    llm: Any = None

    # -------------------------------------------------------------------------
    # TODO 1: PDF 로드
    # -------------------------------------------------------------------------
    # 목표:
    # - PDF_PATH의 문서를 LangChain Document 목록으로 불러옵니다.
    # - 결과를 pages 변수에 대입합니다.

    # PDF 읽고 페이지 구분 및 Part 구분
    from langchain_community.document_loaders import PyMuPDFLoader

    loader = PyMuPDFLoader(str(PDF_PATH))

    pages = loader.load()

    # 맨 끝의 설문조사 제외하기 위해 범위 설정
    pages = pages[1:28]

    docs = pages

    for doc in docs:

        page = doc.metadata["page"]+1

        if page >= 2 and page <= 4:
                doc.metadata["part"] = "01"
                doc.metadata["chapter"] = "생성형 AI란?"
                doc.metadata["keyword"] = "생성형 AI"

        elif page >= 5 and page <= 9:
            doc.metadata["part"] = "02"
            doc.metadata["chapter"] = "저작권"
            doc.metadata["keyword"] = "저작권"       

        elif page >= 10 and page <= 14:
            doc.metadata["part"] = "03"
            doc.metadata["chapter"] = "책임성"
            doc.metadata["keyword"] = "책임"       
        elif page >= 15 and page <= 19:
            doc.metadata["part"] = "04"
            doc.metadata["chapter"] = "허위조작정보"
            doc.metadata["keyword"] = "허위조작"       
        elif page >= 20 and page <= 23:
            doc.metadata["part"] = "05"
            doc.metadata["chapter"] = "개인정보 인격권"
            doc.metadata["keyword"] = "개인정보"       
        elif page >= 24 and page <= 28:
            doc.metadata["part"] = "06"
            doc.metadata["chapter"] = "오남용"
            doc.metadata["keyword"] = "오남용"

    # 소제목 구분

    import re

    def is_heading(line, chapter):
        line = line.strip()

        if not line:
            return False
        if line == chapter :
            return False
        if line == "관련사례":
            return True
        if line == "PART":
            return False
        if "http" in line:
            return False
        if "?" in line:
            question_position = line.find("?")
            after_question = line[
                question_position +1:
            ].strip()

            if len(after_question) <= 3:
                return True
        return False

    # 자꾸 소제목에 숫자랑 ? 들어간 친구 나와서 추가한 코드

    def merge_question_lines(lines):
        new_lines = []
        question_text = ""
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if question_text != "":
                question_text = question_text + " " + line
                if "?" in line:
                    new_lines.append(question_text)
                    question_text = ""
                continue
            if len(line) > 2:
                if line[0] in "123456789" and line[1] == " ":
                    question_text = line
                    if "?" in line:
                        new_lines.append(question_text)
                        question_text = ""
                    continue
                new_lines.append(line)
        if question_text != "":
            new_lines.append(question_text)
        return new_lines

    from langchain_core.documents import Document

    section_docs = []

    present_section = "개요"
    present_text = []

    present_part = None
    present_chapter = None

    start_page = None
    end_page = None

    for doc in docs:
        page = doc.metadata["page"] +1

        part = doc.metadata["part"]
        chapter = doc.metadata["chapter"]
        lines = doc.page_content.split("\n")
        lines = merge_question_lines(lines)

        if present_part is not None and part != present_part:
            if len(present_text) >0:
                section_docs.append(
                    Document(
                        page_content="\n".join(present_text),

                        metadata={
                            "part": present_part,
                            "chapter": present_chapter,
                            "keyword": present_chapter,
                            "section": present_section,
                            "page": start_page - 1,
                            "page_start": start_page,
                            "page_end": end_page,
                            "content_type": "text",
                        }
                    )
                )
            present_text = []
            present_section = "개요"
            start_page = page

        present_part = part
        present_chapter = chapter

        if start_page == None:
            start_page = page

    # 소제목 기준으로 자르기

        for line in lines :
            line = line.strip()

            if not line:
                continue

            if is_heading(line, chapter):
                if len(present_text) >0:
                    section_docs.append(
                        Document(
                            page_content="\n".join(present_text),
                            metadata={
                            "part": present_part,
                            "chapter": present_chapter,
                            "keyword": present_chapter,
                            "section": present_section,
                            "page": start_page -1,
                            "page_start": start_page,
                            "page_end": end_page,
                            "content_type": "text",
                            }
                        )
                    )

                present_text = []
                present_section = line
                start_page = page

            else:
                present_text.append(line)

                end_page = page

    if len(present_text) >0:
        section_docs.append(
            Document(
                page_content="\n".join(present_text),

                metadata={
                    "part": present_part,
                    "chapter": present_chapter,
                    "keyword": present_chapter,
                    "section": present_section,
                    "page": start_page -1,
                    "page_start": start_page,
                    "page_end": end_page,
                    "content_type": "text",
                }
            )
        )

    # 표 구분

    table_docs = []

    for doc in docs:
        page = doc.metadata["page"] +1
        if page == 12 or page == 22:
            table_doc = Document(
                page_content=doc.page_content,

                metadata={
                    "part": doc.metadata["part"],
                    "chapter": doc.metadata["chapter"],
                    "keyword": doc.metadata["keyword"],
                    "section": "표",
                    "page": page -1,
                    "page_start": page,
                    "page_end": page,
                    "content_type": "table"
                }
            )

            table_docs.append(table_doc)


    # 문서 + 표 합치기

    rag_docs = section_docs + table_docs

    # -------------------------------------------------------------------------
    # TODO 2: 문서 청크 분할
    # -------------------------------------------------------------------------
    # 목표:
    # - 페이지 문서를 적절한 chunk_size와 chunk_overlap으로 분할합니다.
    # - 결과는 Document 목록이어야 합니다.
    # - 결과를 chunks 변수에 대입합니다.
    # - 선택한 크기와 중첩값의 이유를 주석으로 설명하세요.

    # Chunking (큰 Document만 자르기)
    # 이미 문서를 소제목 기준으로 잘게 잘랐기 때문에, 큰 값인 1200으로 설정함. 중첩값도 10%로 좁게 설정했으나, 그럴 때 작은 청크들이 생겨서 100 이하 청크들 무시하도록 추가했음.

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1200,
        chunk_overlap = 120
    )

    chunks = []

    for doc in rag_docs:
        if doc.metadata["content_type"] == "table":
            chunks.append(doc)

        elif len(doc.page_content) <= 1200:
            chunks.append(doc)
        else:
            split_docs = text_splitter.split_documents(
                [doc]
            )

            for split_doc in split_docs:
                chunks.append(split_doc)

    # 짧은 chunk 제거

    final_chunks = []

    for chunk in chunks:
        if(
            chunk.metadata["section"] == "개요"
            and len(chunk.page_content) < 100
        ) :
            continue
        final_chunks.append(chunk)

    chunks = final_chunks

    # -------------------------------------------------------------------------
    # TODO 3: 임베딩, Vector Store, retriever 생성
    # -------------------------------------------------------------------------
    # 목표:
    # - 청크를 임베딩합니다.
    # - Vector Store를 생성합니다.
    # - 질문과 관련된 문맥을 검색할 retriever를 만듭니다.
    # - embeddings, vector_store, retriever 변수에 각각 대입합니다.
    # - 검색 문서 수(k)를 정하고 이유를 주석으로 설명하세요.

    # 임베딩 만들기

    from dotenv import load_dotenv
    from langchain_openai import OpenAIEmbeddings
    load_dotenv()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # metadata 붙이기

    from langchain_core.documents import Document

    embedding_docs = []

    for doc in chunks:
        content = f"""
    PART : {doc.metadata["part"]}
    Chapter : {doc.metadata["chapter"]}
    Section: {doc.metadata["section"]}
    Page: {doc.metadata["page_start"]} ~ {doc.metadata["page_end"]}

    {doc.page_content}
    """
        new_doc = Document(
            page_content=content,
            metadata=doc.metadata
        )
        embedding_docs.append(new_doc)

    # VectorStore 만들기

    from langchain_core.vectorstores import InMemoryVectorStore

    vector_store = InMemoryVectorStore(
        embedding=embeddings
    )

    vector_store.add_documents(
        documents=embedding_docs
    )


    # Retriever 만들기

    retriever = vector_store.as_retriever(
        search_type = "similarity_score_threshold",
        search_kwargs={
            "k": 5,
            "score_threshold": 0.4
        }
    )

    # -------------------------------------------------------------------------
    # TODO 4: 프롬프트 생성
    # -------------------------------------------------------------------------
    # 필수 조건:
    # - 검색 문맥을 받을 {context} 변수가 있어야 합니다.
    # - 사용자 질문을 받을 {question} 변수가 있어야 합니다.
    # - 문서에 없는 내용을 추측하지 않도록 지시해야 합니다.
    # - 결과를 prompt 변수에 대입합니다.

    # 프롬프트

    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_template(
        """
        자, 테스트의 답변이다. 아래 형식으로 질문에 답해라.
        그러나, 만에 하나 문서에서 답을 도저히 못 찾겠으면 "미안합니다." 라고 답해라.
        그리고, 훌륭한 대학원생 답게 당연하게도 답변에 참고한 PART, Chapter, Section, Page는 주석으로 달도록.

        [문서]
        {context}


        [질문]
        {question}


        [답변]
    """
    )

    # -------------------------------------------------------------------------
    # TODO 5: Chat Model 생성 및 반환
    # -------------------------------------------------------------------------
    # 목표:
    # - 답변을 생성할 Chat Model을 만듭니다.
    # - 결과를 llm 변수에 대입합니다.

    # llm 연결하기

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )

    # 아래 검증과 반환 코드는 제공 코드이므로 수정하지 않습니다.
    missing = [
        name
        for name, value in (
            ("pages", pages),
            ("chunks", chunks),
            ("embeddings", embeddings),
            ("vector_store", vector_store),
            ("retriever", retriever),
            ("prompt", prompt),
            ("llm", llm),
        )
        if value is None
    ]
    if missing:
        raise NotImplementedError(
            "_build_rag()의 다음 공통 변수를 완성해 주세요: " + ", ".join(missing)
        )
    return retriever, prompt, llm


# =============================================================================
# [제공 함수] LLM 응답을 문자열로 변환 - 수정하지 않음
# =============================================================================


def _answer_text(content: Any) -> str:
    """LLM 응답의 문자열/블록형 content를 화면용 문자열로 통일한다."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and isinstance(block.get("text"), str):
                parts.append(block["text"])
        return "\n".join(parts).strip()
    return str(content)


# =============================================================================
# [제공 함수] 질문 검색, 답변 생성, 표준 결과 반환 - 수정하지 않음
# =============================================================================
# app.py와 RAGAS 평가 기능이 직접 호출하는 공개 함수입니다.
# 함수 이름, question 매개변수, 반환 키를 변경하면 안 됩니다.


def ask(question: str) -> dict[str, Any]:
    """질문에 답하고 검색 문맥과 페이지 출처를 함께 반환한다."""
    question = question.strip()
    if not question:
        raise ValueError("질문을 입력해 주세요.")

    retriever, prompt, llm = _build_rag()
    documents = list(retriever.invoke(question))

    document_rows: list[tuple[Any, str]] = []
    for document in documents:
        content = str(getattr(document, "page_content", "")).strip()
        if content:
            document_rows.append((document, content))
    if not document_rows:
        raise RuntimeError("질문과 관련된 검색 문맥을 찾지 못했습니다.")

    contexts = [content for _, content in document_rows]
    context_text = "\n\n---\n\n".join(contexts)

    messages = prompt.invoke({"question": question, "context": context_text})
    response = llm.invoke(messages)
    answer = _answer_text(getattr(response, "content", response)).strip()
    if not answer:
        raise RuntimeError("LLM이 빈 답변을 반환했습니다.")

    sources: list[dict[str, Any]] = []
    for document, content in document_rows:
        metadata = getattr(document, "metadata", {}) or {}
        page_value = metadata.get("page", 0)
        try:
            page = int(page_value) + 1
        except (TypeError, ValueError):
            page = 1
        sources.append({"page": page, "content": content})

    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "sources": sources,
    }


# =============================================================================
# [제공 함수] 화면 상태 확인 - 수정하지 않음
# =============================================================================


def get_status() -> dict[str, Any]:
    """외부 API를 호출하지 않고 PDF·API 키·색인 상태를 반환한다."""
    return {
        "pdf_ready": PDF_PATH.is_file(),
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "index_initialized": _build_rag.cache_info().currsize > 0,
    }


# =============================================================================
# [완성 후 확인]
# =============================================================================
# 1. TODO 0~5를 구현해 _build_rag()의 공통 변수에 결과를 대입합니다.
# 2. 문법을 검사합니다.
#
#      .venv\Scripts\python.exe -m py_compile rag.py
#
# 3. Streamlit을 실행해 질문, 답변, 검색 근거를 확인합니다.
#
#      uv run streamlit run app.py
#
# 4. ask() 결과의 answer는 str, contexts는 비어 있지 않은 list[str]인지
#    반드시 확인합니다. 이 규격이 맞아야 제출 파일과 RAGAS 평가가 동작합니다.
# =============================================================================

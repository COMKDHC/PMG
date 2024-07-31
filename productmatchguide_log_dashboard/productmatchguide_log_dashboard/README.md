# Introduction

Product Match Genie 방문자 로그 분석을 위한 대시보드

# Getting Started

## Installation and Setup

### 사전 준비

- python 3.11

### 설치

1. python venv 설치
   ```
   # 설치 전 python --version 으로 버전 확인
   python -m venv .venv
   ```
2. 가상환경 실행
   ```
   (윈도우) .\.venv\Scripts\activate
   (맥) source .venv/bin/activate
   ```
3. requirements 설치
   ```
   # 가상환경 실행 후 (source .venv/bin/activate)
   (.venv) python -m pip install -r requirements.txt
   ```
4. pre-commit hook 설치
   ```
   (.venv) pre-commit install
   ```


## 폴더 구성
```
├── .azuredevops
│    └── pull_request_template.md   <- PR 템플릿
├── dashboard                       <- Streamlit 웹
├── .gitignore                      <- .gitignore
├── README.md                       <- 최상위 리드미 파일
└── requirements.txt                <- 개발 환경을 재구성하는데 필요한 requirements.txt
```
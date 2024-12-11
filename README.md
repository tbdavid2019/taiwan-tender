---
title: Taiwan Tender
emoji: 🦀
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 5.8.0
app_file: app.py
pinned: false
short_description: 台灣政府標案查詢
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


---

# 台灣政府招標查詢工具

## 簡介
「台灣政府招標查詢工具」是一個基於 Gradio 的輕量化網頁應用，提供使用者查詢台灣政府招標公告的便利功能。用戶可以依日期、採購性質、招標方式及相關關鍵字進行篩選，並支持將查詢結果導出為 CSV 文件。

## 功能特色
- **跨日期查詢**：可選擇指定日期進行查詢，或默認使用當日。
- **多條件篩選**：支援依據「採購性質」、「招標方式」、「機關名稱」、「機關代碼」、「標案案號」及「標案名稱」進行篩選。
- **點擊開啟連結**：查詢結果中的「標案名稱」為可點擊超連結，直接跳轉至標案的詳細頁面。
- **導出 CSV**：支持將查詢結果導出為 CSV 文件，方便後續分析與存檔。

## 使用方法
1. 克隆本項目：
   ```bash
   git clone https://github.com/tbdavid2019/taiwan-tender.git
   cd taiwan-tender
   ```

2.	安裝必要依賴：
    ```
    pip install -r requirements.txt
    ```

3.	啟動應用：
    ```
    python app.py
    ```

4.	打開本地瀏覽器訪問 http://127.0.0.1:7860，即可使用本工具。



---
Taiwan Government Tender Query Tool

Introduction

The “Taiwan Government Tender Query Tool” is a lightweight web application built with Gradio. It allows users to search for government tender announcements in Taiwan based on specific criteria such as date, procurement category, and tendering method. The tool also supports exporting query results as CSV files.

Features
	•	Cross-Date Search: Choose specific dates for querying or default to the current day.
	•	Advanced Filtering: Filter results by “Procurement Category,” “Tendering Method,” “Agency Name,” “Agency Code,” “Tender ID,” or “Tender Name.”
	•	Clickable Links: The “Tender Name” in the results is a clickable link that redirects to the detailed tender page.
	•	CSV Export: Export query results as CSV files for further analysis and record-keeping.

Usage

1.	Clone this repository:
```
git clone https://github.com/tbdavid2019/taiwan-tender.git
cd taiwan-tender
```

2.	Install dependencies:

```
pip install -r requirements.txt
```

3.	Launch the application:

```
python app.py
```

4.	Open your browser and visit http://127.0.0.1:7860 to start using the tool.


import gradio as gr
import requests
import datetime
import pandas as pd

# Function to fetch data from the API
def fetch_tenders(date, category, type_, unit_name, unit_id, job_number, name):
    base_url = "https://pcc.mlwmlw.org/api/date/award/"
    try:
        # Validate and format the date
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")  # Default to today's date
        else:
            datetime.datetime.strptime(date, "%Y-%m-%d")  # Ensure correct format
        url = f"{base_url}{date}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Filter data based on inputs
        filtered_data = [
            {
                "標案名稱": f'<a href="{item.get("url", "#")}" target="_blank">{item.get("name", "N/A")}</a>',
                "機關名稱": item.get("unit", "N/A"),
                "類別": item.get("category", "N/A"),
                "招標方式": item.get("type", "N/A"),
                "價格": item.get("price", "N/A"),
                "日期": date,
                "連結": item.get("url", "N/A")
            }
            for item in data
            if (
                (category == "不限" or item.get("category") == category) and
                (type_ == "不限" or item.get("type") == type_) and
                (not unit_name or unit_name in item.get("unit", "")) and
                (not unit_id or unit_id in item.get("unit_id", "")) and
                (not job_number or job_number in item.get("job_number", "")) and
                (not name or name in item.get("name", ""))
            )
        ]
        return pd.DataFrame(filtered_data) if filtered_data else pd.DataFrame([{"查無資料": ""}])

    except ValueError:
        return pd.DataFrame([{"Error": "日期格式錯誤，請使用 YYYY-MM-DD 格式"}])
    except requests.exceptions.RequestException as e:
        return pd.DataFrame([{"Error": f"無法取得資料: {str(e)}"}])


# Gradio Interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## 政府招標查詢工具\n通過日期、採購性質、招標方式以及其他關鍵字篩選政府招標公告。")
        
        with gr.Row():
            date_input = gr.Text(label="查詢日期 (YYYY-MM-DD)", placeholder="可不填, 預設為今天")
            category_dropdown = gr.Dropdown(
                choices=["不限", "工程類", "財物類", "勞務類"],
                label="採購性質",
                value="不限"
            )
            type_dropdown = gr.Dropdown(
                choices=[
                    "不限", "決標公告", "無法決標公告", "定期彙送"
                ],
                label="招標方式",
                value="不限"
            )

        with gr.Row():
            unit_name_input = gr.Text(label="機關名稱", placeholder="輸入機關名稱")
            unit_id_input = gr.Text(label="機關代碼", placeholder="輸入機關代碼")
            job_number_input = gr.Text(label="標案案號", placeholder="輸入標案案號")
            name_input = gr.Text(label="標案名稱", placeholder="輸入標案名稱")
        
        submit_button = gr.Button("查詢")
        download_button = gr.Button("導出 CSV")

        # Output for displaying results
        output = gr.HTML(label="查詢結果")
        csv_data = gr.State()  # Temporary state to store DataFrame

        # Handle fetch and display
        def handle_query(date, category, type_, unit_name, unit_id, job_number, name):
            df = fetch_tenders(date, category, type_, unit_name, unit_id, job_number, name)
            return df.to_html(escape=False, index=False), df

        # Handle CSV export
        def export_csv(df):
            file_path = "/tmp/tender_results.csv"
            df.to_csv(file_path, index=False)
            return file_path

        # Button actions
        submit_button.click(
            handle_query,
            inputs=[date_input, category_dropdown, type_dropdown,
                    unit_name_input, unit_id_input, job_number_input, name_input],
            outputs=[output, csv_data]
        )
        download_button.click(export_csv, inputs=[csv_data], outputs=gr.File())

    demo.launch()

if __name__ == "__main__":
    create_interface()
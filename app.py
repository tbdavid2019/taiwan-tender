import gradio as gr
import requests
import datetime

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
            [
                item.get("name", "N/A"),
                item.get("unit", "N/A"),
                item.get("category", "N/A"),
                item.get("type", "N/A"),
                item.get("price", "N/A"),
                date,  # Add the queried date as a column
                item.get("url", "N/A")
            ]
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
        return filtered_data if filtered_data else [["查無資料"]]

    except ValueError:
        return [["日期格式錯誤，請使用 YYYY-MM-DD 格式"]]
    except requests.exceptions.RequestException as e:
        return [[f"無法取得資料: {str(e)}"]]


# Gradio Interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## 政府招標查詢工具\n通過日期、採購性質、招標方式以及其他關鍵字篩選政府招標公告。")
        
        with gr.Row():
            date_input = gr.Text(label="查詢日期 (YYYY-MM-DD)", placeholder="默認為今天，例如 2024-12-11")
            category_dropdown = gr.Dropdown(
                choices=["不限", "工程", "財物", "勞務"],
                label="採購性質",
                value="不限"
            )
            type_dropdown = gr.Dropdown(
                choices=[
                    "不限", "各式招標公告", "公開招標", "公開取得電子報價單", "公開取得報價單或企劃書",
                    "經公開評選或公開徵求之限制性招標", "選擇性招標 (建立合格廠商名單)", 
                    "選擇性招標 (建立合格廠商名單後續邀標)", "選擇性招標 (個案)", "電子競價", 
                    "限制性招標 (未經公開評選或公開徵求)"
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

        # Output for displaying results
        output = gr.Dataframe(
            headers=["標案名稱", "機關名稱", "類別", "招標方式", "價格", "日期", "連結"],
            label="查詢結果"
        )
        
        submit_button.click(
            fetch_tenders,
            inputs=[date_input, category_dropdown, type_dropdown,
                    unit_name_input, unit_id_input, job_number_input, name_input],
            outputs=output
        )

    demo.launch()

if __name__ == "__main__":
    create_interface()
import pandas as pd
import os
import plotly.graph_objects as go

def generate_clean_CPI_data():
	clean_cpi_path = "res/CPI_[period=(2000,2022.05)].csv"
	if not os.path.exists(clean_cpi_path):
		print("[INFO] 正在產生 [台灣 CPI 資料 CSV] ...")
		cpi_df = pd.read_csv("raw/A030101010-0574514306.csv")
		tmp_df = cpi_df[(~cpi_df["統計期"].str.contains('月', na=False))\
						 | (cpi_df["統計期"].str.contains("111", na=False))]
		info_dict = dict()
		cols = ["資料年月"]
		[cols.append(e) for e in cpi_df.columns if e != "統計期"]
		[info_dict.setdefault(col, list()) for col in cols]
		
		for period in tmp_df["統計期"].iloc[:-2].tolist():
			info_dict["資料年月"].append(period)
			target_df = cpi_df[cpi_df["統計期"]==period]
			for col in cols[1:]:
				info_dict[col].append(target_df[col].iloc[0])
		pd.DataFrame.from_dict(info_dict).to_csv(clean_cpi_path, index=False, encoding="utf-8-sig")
	else:
		print("[INFO] [台灣 CPI 資料 CSV] 檔案已存在")
	return clean_cpi_path
	
def save_CPI_figure(clean_cpi_path):
	cpi_fig_path = "res/台灣 CPI 資料.png"
	if not os.path.exists(clean_cpi_path):
		print("[INFO] 正在產生 [台灣 CPI 折線圖] ...")
		main_cpi_df = pd.read_csv(clean_cpi_path)
		fig = go.Figure()
		x_col, y_cols = main_cpi_df.columns[0], main_cpi_df.columns[1:]
		for y_col in y_cols:
			name_ = y_col.split('.')[-1] if '.' in y_col else y_col
			mode_ = "lines+markers" if "食物類" in y_col else "lines"
			fig.add_trace(go.Scatter(x=main_cpi_df[x_col], y=main_cpi_df[y_col],
			                    mode=mode_, name=name_))
		fig.write_image(cpi_fig_path)
	else:
		print("[INFO] [台灣 CPI 折線圖] 檔案已存在")
	
if __name__ == "__main__":
	clean_cpi_path = generate_clean_CPI_data()
	save_CPI_figure(clean_cpi_path)
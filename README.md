# HEIC 轉 JPG

把 iPhone 拍的 HEIC / HEIF 照片轉成 JPG,保留 EXIF(拍攝時間、GPS 等)與色彩設定檔。

## 下載 exe(免安裝 Python)

到 [Releases](../../releases/latest) 下載 `HEIC-to-JPG.exe`。

**使用方式:** 把 HEIC 檔案或資料夾拖到 exe 上即可。

- JPG 會存在原檔旁邊
- 同名 JPG 已存在時自動改名為「名稱 (1).jpg」、「名稱 (2).jpg」……,不會覆蓋舊檔
- 拖資料夾時會連子資料夾一起轉
- 全部順利完成時視窗自動關閉;有檔案被改名或轉換失敗時,視窗會停住並列出是哪些檔案

> 第一次執行若被 Windows SmartScreen 擋下,按「其他資訊 → 仍要執行」。

## 用 Python 執行

```powershell
pip install pillow pillow-heif
python HEIC轉JPG.py                         # 轉換目前資料夾
python HEIC轉JPG.py 照片.heic               # 單一檔案
python HEIC轉JPG.py D:\照片 -r              # 含子資料夾
python HEIC轉JPG.py D:\照片 -o D:\JPG -q 90 # 指定輸出資料夾與品質
```

| 參數 | 說明 |
|---|---|
| `-o` | 輸出資料夾(預設:原檔旁邊) |
| `-q` | JPG 品質 1–100(預設 95) |
| `-r` | 包含子資料夾 |
| `-f` | 覆寫已存在的 JPG(預設:自動改名) |
| `--delete` | 轉換成功後刪除原始 HEIC |

## 自己打包 exe

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pillow pillow-heif pyinstaller
pyinstaller --onefile --console --name HEIC-to-JPG HEIC轉JPG.py
```

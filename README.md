# HEIC 轉 JPG

把 iPhone 拍的 HEIC / HEIF 照片轉成 JPG,保留 EXIF(拍攝時間、GPS 等)與色彩設定檔。

> 為什麼用line就能把heic轉成jpg了我還要寫一支程式呢?純粹是我喜歡拖放而已...

## 下載 exe(免安裝 Python)

到 [Releases](../../releases/latest) 下載 `HEIC-to-JPG.exe`。

**使用方式:** 把 HEIC 檔案或資料夾拖到 exe 上即可。

- JPG 會存在原檔旁邊
- 同名 JPG 已存在時自動改名為「名稱 (1).jpg」、「名稱 (2).jpg」……,不會覆蓋舊檔
- 拖資料夾時會連子資料夾一起轉
- 全部順利完成時CMD視窗自動關閉;有檔案被改名或轉換失敗時,CMD視窗會停住並列出是哪些檔案

> 第一次執行若被 Windows SmartScreen 擋下,按「其他資訊 → 仍要執行」。

## 畫質說明

預設以**最高畫質**輸出:JPG 品質 **100**、色度取樣 **4:4:4**。

- **品質(`-q`)**:JPG 是有損壓縮格式,數字越高、壓縮造成的損失越小。100 是最高值,但 JPG 本身仍無法做到完全無損。
- **色度取樣(`--subsampling`)**:一般 JPG 常用 4:2:0,會把色彩資訊縮成 1/4 來省空間;4:4:4 則完整保留每個像素的色彩,顏色交界、紅色或藍色的細節會更清楚。

以一張 4032×3024、細節雜訊很多的測試圖為例(對 JPG 最不利的情況):

| 設定 | 與原圖的平均色差 | 檔案大小 |
|---|---|---|
| 品質 95、4:2:0 | 2.81 / 255 | 3.7 MB |
| **品質 100、4:4:4(預設)** | **0.16 / 255** | **12.5 MB** |

最高畫質的代價是檔案較大。一般照片細節沒那麼雜亂,檔案增加的幅度通常會小一些。想要較小的檔案,可以用 Python 版指定 `-q 90 --subsampling 420`。

轉換時**解析度不變**,EXIF(拍攝時間、GPS 等)與色彩設定檔也會保留。但 HEIC 的 HDR 效果、10-bit 色彩、景深資訊、原況照片的動態部分,因為 JPG 格式不支援,轉換後會遺失。要保存原始畫質,請留著原本的 HEIC 檔。

## 用 Python 執行

```powershell
pip install pillow pillow-heif
python HEIC轉JPG.py                         # 轉換目前資料夾
python HEIC轉JPG.py 照片.heic               # 單一檔案
python HEIC轉JPG.py D:\照片 -r              # 含子資料夾
python HEIC轉JPG.py D:\照片 -o D:\JPG       # 指定輸出資料夾
python HEIC轉JPG.py D:\照片 -q 90 --subsampling 420  # 較小的檔案
```

| 參數 | 說明 |
|---|---|
| `-o` | 輸出資料夾(預設:原檔旁邊) |
| `-q` | JPG 品質 1–100(預設 100) |
| `--subsampling` | 色度取樣 `444` / `422` / `420`(預設 `444`) |
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

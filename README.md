# Excel QR Code 產生器

[前面的部分保持不變]

## 專案結構

```
your_project/
├── config/
│   └── custom_config.ini
│
├── qr_codes/
│
├── qrbatch/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── qr_generator.py
│   ├── __init__.py
│   └── main.py
│
├── resources/
│   └── data.xlsx
│
├── .gitignore
├── CHANGELOG.md
├── README.md
├── requirements.txt
└── run.py

```

[中間的部分保持不變]

## 使用方法

在專案根目錄執行以下命令：

### 基本用法（使用默認設置）
```
python run.py
```
這將在專案根目錄下創建一個名為 `qr_codes` 的文件夾，並在其中生成 QR Code。

### 指定資料來源：
```
python run.py resources/data.xlsx
```

### 指定自定義設定檔：
```
python run.py -c config/custom_config.ini
```

### 指定自定義輸出資料夾：
```
python run.py -o qr_codes
```
這將在專案根目錄下創建一個名為 `qr_codes` 的文件夾作為輸出目錄。

### 完整範例（包含所有選項）：
```
python run.py resources/data.xlsx -c config/custom_config.ini -o qr_codes
```
這個命令將使用自定義的 Excel 文件和配置文件，並將輸出保存到指定的 `qr_codes` 目錄。

## 輸出結果

- 默認情況下，QR Code 圖片將保存在專案根目錄下的 `qr_codes` 文件夾中。
- 如果使用 `-o` 或 `--output` 參數指定了自定義輸出目錄，QR Code 圖片將保存在指定的目錄中。
- Script 會為每個處理的 Excel 工作表在輸出目錄中創建一個子文件夾。
- 每個子文件夾將包含該工作表中各項目的 QR Code 圖片。

例如，使用默認設置時，輸出結構可能如下：

```
your_project/
└── qr_codes/
    ├── Sheet1/
    │   ├── qr_Sheet1_item_1.png
    │   ├── qr_Sheet1_item_2.png
    │   └── ...
    ├── Sheet2/
    │   ├── qr_Sheet2_item_1.png
    │   ├── qr_Sheet2_item_2.png
    │   └── ...
    └── ...
```

[注意事項部分保持不變]
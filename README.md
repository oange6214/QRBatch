# Excel QR Code 產生器

## 專案結構

```
your_project/
├── config/
│   └── custom_config.json
│
├── qr_codes/
│
├── qrbatch/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config_handler.py
│   │   ├── data_processor.py
│   │   ├── file_handler.py
│   │   └── qr_generator.py
│   ├── __init__.py
│   ├── exceptions.py
│   ├── qr_batch_processor.py
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

## 前置需求

1. 安裝 Python
   請依照以下指南安裝 Python：
   https://medium.com/@benson890720/python練習筆記-安裝python-8f423dd77c68

2. 安裝所需套件
   執行以下命令一次性安裝所有必要的套件：
   ```
   pip install -r requirements.txt
   ```

## 設定

`custom_config.json` 文件。範例內容如下：

```json
{
    "Header": {
      "row": 1
    },
    "Sheets": {
      "process": [
        "C小樹(雜物&設備) "
      ]
    },
    "Columns": {
      "include": [
        "項目    編號",
        "購買日期",
        "型號/規格/名稱及說明",
        "單位",
        "數量",
        "存放位置",
        "財產編號\n設備編號",
        "備註"
      ],
      "exclude": [
        "圖片"
      ]
    }
  }
```

## 使用方法

在專案根目錄執行以下命令：

### 基本用法（使用默認設置）
```
python run.py
```
這將在專案根目錄下創建一個名為 `qr_codes` 的文件夾，並在其中生成 QR Code。

### 指定資料來源：
```
python run.py -d resources/data.xlsx
```

### 指定自定義設定檔：
```
python run.py -c config/custom_config.json
```

### 指定自定義輸出資料夾：
```
python run.py -o qr_codes
```
這將在專案根目錄下創建一個名為 `qr_codes` 的文件夾作為輸出目錄。

### 完整範例（包含所有選項）：
```
python run.py -d resources/data.xlsx -c config/custom_config.json -o qr_codes
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
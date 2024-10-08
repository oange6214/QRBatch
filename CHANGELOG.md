# Changelog

所有對本項目的重要變更都會記錄在此文件中。

本文件格式基於 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
並且本項目遵循 [語義化版本](https://semver.org/spec/v2.0.0.html)。

## [v1.0.9]

### 變更
- Refactor main.py, split setup_dependencies and process instance. 
- Refactor qr_batch_processor.py, create _load_conifg and use dictionary. 
- Refactor config_handler.py, Edit function name to ConfigHandlerFactory, and add try...catch
- Refactor data_processor.py, Split filter_columns to _include and _exclude function. Add sample.
- Refactor file_handler.py, Add summary. Add sample.
- Refactor qr_generator.py, Add logo and byte function, Add summary. Add sample.

## [v1.0.8]

### 新增
- Add Base confighandler
- Create factory pattern
- Create ini and json configure class. 

### 變更
- Changed config file to json. 
- Refactor config_handler.py

## [v1.0.7]

### 變更
- 編輯 clean_filename function Remove \n 符號
- 編輯 _process_row function File name 組成為 {項目編號}_{財產編號}.png

## [v1.0.6]

### 新增
- Add exceptions.
- Add DI design. 

### 變更
- Refactor qr_batch_processor.py.


## [v1.0.5]

### 新增
- Debugger file launch.json.
- Row value validation is nan will not process.

### 變更
- Edit custom_config.ini, excel column name.
- 拆分 qr_generator.py process_excel 函數，建立了 sheet and row

## [v1.0.4]

### 新增
- Header row setting.

### 變更
- version number.

### 修復
- Fix Error can raise.

## [1.0.3]

### 修復
- 修改 README.md

## [1.0.2] - 2024-08-14

### 修復
- 修改 README.md
- 修改 CHANGEDLOG.md

## [1.0.1] - 2024-08-14

### 新增
- 判斷指令使 run.py 以及 main.py 可以執行

### 變更
- 移除 setup.py 文件，不需要打包和分發，僅使用 Script

## [1.0.0] - 2024-08-14

### 新增
- 初始版本發布
- 支持從 Excel 文件生成 QR 碼
- 支持處理多個工作表
- 實現可自定義列的包含與排除功能
- 添加命令行參數解析功能
- 實現日誌記錄功能
- 添加配置文件 (sheets_config.ini) 支持
- 支持處理包含換行符的列名
- 實現靈活的列匹配邏輯

### 變更
- 優化 QR 碼生成邏輯，提高生成效率
- 改進錯誤處理和異常報告

### 修復
- 修正列名中換行符導致的問題
- 修復文件名生成中的特殊字符處理問題

## [0.2.0] - 2024-08-10

### 新增
- 添加對多個工作表的支持
- 實現列過濾功能(包含/排除)
- 添加基本的命令行界面

### 變更
- 重構代碼以提高可讀性和可維護性

## [0.1.0] - 2024-08-05

### 新增
- 項目初始化
- 基本的 Excel 讀取功能
- 簡單的 QR 碼生成功能


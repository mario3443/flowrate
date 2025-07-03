# flowrate - 自由度分析與質能均衡計算工具
![image](https://github.com/user-attachments/assets/945306b0-88dd-47bd-b4d9-d637b7374fe8)

## 學習背景
這份專案是我在化工系大一下課程-質能均衡中，為了輔助學習課程中所利用到的計算流體流入流出的flowrate計算，所和同學合作的一個計算工具

## 功能介紹
一進畫面會看到 **自由度分析工具**。使用者只需輸入題目所提供的基本資訊，如：

- 成分數 Nc
- Stream 數 Ns
- 設備數 Np

輸入後即可進入第二介面開始輸入題目所提供的流量與後即可送出計算（圖片為舉例題目）

![image](https://github.com/user-attachments/assets/d12a6c8f-f8ce-4a06-89ca-084a077a9408)

系統則會利用公式計算你輸入的值是否是足夠的，若不夠則可回去再次調整值到剛好有一組解

![image](https://github.com/user-attachments/assets/012fb952-d872-4fe7-a8c4-00dc31147e63)

送出後系統便會動態產生表格計算出解矩陣，來省略在人工計算上複雜的部份。

## 如何使用

先clone此專案到你的資料夾後

進入資料夾內並且在終端輸入

### ```python flask_server.py```

即可開啟瀏覽器並前往

### ```http://localhost:5000```

## 學習或利用到的知識
#### - React 前端框架（建立元件、狀態管理）

#### - 基本 HTML / CSS

#### - Flask（後端邏輯運算、自由度計算）

#### - Python（處理矩陣運算）

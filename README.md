针对股票截图，提取文本到csv、xlsx中  
原数据在data中，类似 
![image](static/index.png)  

输出格式类似    

[输出excel](https://github.com/liugehaizaixue/stock_cv/blob/main/res/%E6%96%87%E6%9C%AC2023-04-19.xlsx)


v1 v2 v3 均为单线程  

moremodel 为多线程工作，同时每个线程独享一个cnocr模型  

singlemodel 多线程，每个线程公用一个cnocr  
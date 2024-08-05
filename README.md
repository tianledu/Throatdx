# 基于深度学习的喉癌类病灶区域识别与诊断系统
## 项目介绍
  本项目旨在将深度学习方法应用于喉癌病灶的分割与识别，基于现有喉癌病灶的医学影像数据集进行特征提取和分类，利用 U-Net 和 V-Net 等深度学习方法建立喉癌诊断模型，开发设计一套对应的诊断系统。
## 工程结构
```
# ./model:保存模型参数文件
# ./out:患者诊断结果图片
# ./report:患者诊断报告存放目录
# ./ui:界面ui工程文件
```
## Configuration Environment
```
python==3.7
paddleseg==2.0.0
numpy==1.19.5
opencv-python==4.5.1.48
mysql
pyqt5
```
## Prepare Data
```
Download data from: [喉癌病灶数据集](https://aistudio.baidu.com/datasetdetail/194048)
```
## 实验+模型训练代码
```
# 根据需求自行调参得到训练模型
https://aistudio.baidu.com/projectdetail/5722256
```
## 系统运行
```python
# 运行sql文件建立数据库，在代码中更改对应的数据库连接信息
# 后运行以下代码打开系统
cd throatdx
python app.py
```

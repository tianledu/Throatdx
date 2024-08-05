import os
import paddleseg.transforms as T
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIntValidator, QImage
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from paddle.dataset.image import cv2
from paddleseg.core import infer
import mysql.connector
import numpy as np
import paddle
from PyQt5.QtWidgets import QApplication,  QLabel,  QMessageBox, QDialog, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import SimpleITK as sitk
from paddleseg.models import UNet, U2Net
from pyqt5_plugins.examplebutton import QtWidgets


# 登录界面显示
class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 计数器，防止弹窗弹出多次
        self.failed_count = 0
        self.failed_count1 = 0
        self.failed_count2 = 0
        # 隐藏主窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 加载UI文件
        loadUi('./ui/main.ui', self)
        # 获取登录按钮
        #self.login_button = self.findChild(QtWidgets.QPushButton, 'login_button')
        # 设置登录按钮的事件处理程序
        #self.login_button.clicked.connect(self.on_login_button_clicked)

        self.login_button.clicked.connect(self.on_login_button_clicked)
        # 获取注册按钮
        self.register_button = self.findChild(QtWidgets.QPushButton, 'pushButton_5')
        # 设置注册按钮的事件处理程序
        self.register_button.clicked.connect(self.on_rigister_button_clicked)
        self.pushButton_6.clicked.connect(self.on_close_clicked)

    # 退出界面
    def on_close_clicked(self):
        self.close()


    # 登录处理
    # bug： 登录按钮事件每次点击都会被执行三次，导致弹窗三次
    def on_login_button_clicked(self):

        # 获取单选框
        self.radioButton1 = self.findChild(QtWidgets.QRadioButton, 'radioButton')
        self.radioButton2 = self.findChild(QtWidgets.QRadioButton, 'radioButton_2')


        if self.radioButton2.isChecked():
            self.on_login_doctor_clicked()

        elif self.radioButton.isChecked():
            self.on_login_patient_clicked()


    # 医生登录
    def on_login_doctor_clicked(self):

        # 连接MySQL数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dtl104104",
            database="ThroaDX"
        )
        # 创建游标
        mycursor = mydb.cursor()

        # 获取医生信息表中的所有用户名
        mycursor.execute("SELECT username FROM doctor")
        doctor_usernames = [result[0] for result in mycursor.fetchall()]

        # 获取登录用户名和密码输入框
        self.username_edit = self.findChild(QtWidgets.QLineEdit, 'username1')
        self.password_edit = self.findChild(QtWidgets.QLineEdit, 'password1')

        # 获取用户名和密码输入框的值
        username = self.username_edit.text()
        password = self.password_edit.text()



        # 进行登录验证
        if username in doctor_usernames:
            mycursor.execute("SELECT password FROM doctor WHERE username=%s", (username,))
            correct_password = mycursor.fetchone()[0]
            if password == correct_password:
                self.failed_count2 += 1
                if self.failed_count2 <= 1:
                    self.close()
                    self.newWindow = DoctorWindow()
                    self.newWindow.show()

            else:
                # self.failed_count += 1
                if self.failed_count <= 1:
                    # 登录失败，弹出提示框
                    QMessageBox.warning(self, '错误', '请检查姓名和id是否正确')
        elif username not in doctor_usernames:
            # 不存在该用户
            # self.failed_count += 1
            if self.failed_count <= 1:
                QMessageBox.warning(self, '错误', '不存在该用户')



    # 患者登录
    def on_login_patient_clicked(self):
        # 获取登录用户名和密码输入框
        self.username_edit2 = self.findChild(QtWidgets.QLineEdit, 'username1')
        self.password_edit2 = self.findChild(QtWidgets.QLineEdit, 'password1')

        # 获取用户名和密码输入框的值
        username3 = self.username_edit2.text()
        password3 = self.password_edit2.text()


        # 连接MySQL数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dtl104104",
            database="ThroaDX"
        )
        # 创建游标
        mycursor = mydb.cursor()

        # 获取患者信息表中的所有用户名
        mycursor.execute("SELECT username FROM patient")
        patient_usernames = [result[0] for result in mycursor.fetchall()]

        if username3 in patient_usernames:
            # 根据用户名在数据表中搜寻密码
            #mycursor.execute("SELECT password FROM patient WHERE username=%s", (username3,))
            mycursor.execute("SELECT password FROM patient WHERE username=%s AND password IS NOT NULL", (username3,))
            result = mycursor.fetchone()
            if result:
                correct_password = result[0]

                if password3 == correct_password:
                    self.failed_count1 += 1
                    if self.failed_count1 <= 1:
                        username3 = self.username_edit2.text()
                        self.close()
                        self.newWindow2 = PatientWindow(username3)
                        self.newWindow2.show()

                else:
                    # 登录失败，弹出提示框
                    self.failed_count += 1
                    if self.failed_count <= 1:
                        QMessageBox.warning(self, '错误', '请检查姓名和id是否正确')
            # # 结束时将计数器置0，防止弹窗弹出一次后不再弹出
            # self.failed_count = 0
        elif username3 not in patient_usernames:
            self.failed_count += 1
            if self.failed_count <= 1:
                QMessageBox.warning(self, '错误', '不存在该用户')

    # # 返回患者姓名，传递到患者界面类中
    # def get_username(self):
    #     print(50)
    #     return self.username_edit2.text()  # 返回变量的值


    # 注册处理
    def on_rigister_button_clicked(self):
        # 连接MySQL数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dtl104104",
            database="ThroaDX"
        )
        # 创建游标
        mycursor = mydb.cursor()

        # 获取注册页面的输入框
        self.username_edit2 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_4')
        self.password_edit2 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_5')
        self.password_edit3 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_6')
        # 获取用户名和密码输入框的值
        username1 = self.username_edit2.text()
        password1 = self.password_edit2.text()
        password2 = self.password_edit3.text()

        # 获取单选框
        self.radioButton3 = self.findChild(QtWidgets.QRadioButton, 'radioButton_3')
        self.radioButton4 = self.findChild(QtWidgets.QRadioButton, 'radioButton_4')

        if password1 != password2:
            # 两次密码输入不一致，弹出提示框
            QMessageBox.warning(self, '错误', '两次密码输入不一致')

        else:
            if self.radioButton3.isChecked():
                mycursor.execute("SELECT password FROM doctor")
                doctor_password = [result[0] for result in mycursor.fetchall()]
                if password1  in doctor_password:
                    QMessageBox.warning(self,'错误','该医生已完成注册')
                else:
                    # 注册医生信息
                    mycursor.execute("INSERT INTO doctor (username, password) VALUES (%s, %s)", (username1, password1))

                    mydb.commit()
                    QMessageBox.warning(self, '正确', '医生信息注册成功')


            elif self.radioButton4.isChecked():
                # 注册患者信息
                mycursor.execute("SELECT * FROM patient WHERE username = %s", (username1,))
                result = mycursor.fetchone()
                if not result:
                    mycursor.execute("INSERT INTO patient (username, password) VALUES (%s, %s)", (username1, password1))
                else:
                    mycursor.execute("SELECT * FROM patient WHERE username = %s", (username1,))
                    results = mycursor.fetchall()  # 获取全部结果
                    mycursor.execute("UPDATE patient SET password = %s WHERE username = %s", (password1, username1))

                    # mycursor.execute("INSERT INTO patient (username, password) VALUES (%s, %s)", (username1, password1))
                mydb.commit()
                QMessageBox.warning(self, '正确', '患者信息注册成功')




def wwwc(sitkImage, ww=1500, wc=-550):
    # 设置窗宽窗位
    min = int(wc - ww / 2.0)
    max = int(wc + ww / 2.0)
    intensityWindow = sitk.IntensityWindowingImageFilter()
    intensityWindow.SetWindowMaximum(max)
    intensityWindow.SetWindowMinimum(min)
    sitkImage = intensityWindow.Execute(sitkImage)
    return sitkImage



def readNii(path, ww, wc, isflipud=True, ):
    """读取和加载数据"""
    if type(path) == str:
        img = wwwc(sitk.ReadImage(path), ww, wc)
    else:
        img = wwwc(path, ww, wc)
    data = sitk.GetArrayFromImage(img)
    # 图像是上下翻转的，所有把他们翻转过来
    # 不知道为什么这个肺部CT数据用SimpleITK读取是上下翻转的。
    if isflipud:
        data = np.flip(data, 1)
    return data





class InferThread(QThread):
    """
    建立一个任务线程类,  推理任务
    """

    signal_infer_fail = pyqtSignal()  # 推理失败的信号
    signal_infer_result = pyqtSignal(np.ndarray)  # 这信号用来传递推理结果

    def __init__(self, sitkImage, model):
        super(InferThread, self).__init__()
        self.sitkImage = sitkImage
        self.model = model

        self.transforms = T.Compose([
            T.Resize(target_size=(512, 512)),
            T.Normalize()
        ])


    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        try:
            data = readNii(self.sitkImage, 1500, -500)
            inferData = np.zeros_like(data)
            d, h, w = data.shape

            for i in range(d):
                img = data[i].copy()
                img = img.astype(np.float32)
                pre = self.nn_infer(self.model, img, self.transforms)
                inferData[i] = pre

            self.signal_infer_result.emit(inferData)
        except Exception as e:
            print(e)
            self.signal_infer_fail.emit()

    def nn_infer(self, model, im, transforms):
        # 预测结果

        img, _ = transforms(im)
        img = paddle.to_tensor(img[np.newaxis, :])
        pre = infer.inference(model, img)
        pred = paddle.argmax(pre, axis=1).numpy().reshape((512, 512))
        return pred.astype('uint8')




# 医生界面类
class DoctorWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 加载UI文件
        loadUi('./ui/doctor.ui', self)

        # 隐藏主窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        self.initUI()
        # 获取加载模型按钮
        self.jiazai_button = self.findChild(QtWidgets.QPushButton, 'pushButton_5')

        # 设置加载模型的事件处理程序
        self.jiazai_button.clicked.connect(self.on_jiazai_button_clicked)

        # 获取选择影像按钮
        self.xuanze_button = self.findChild(QtWidgets.QPushButton, 'pushButton_6')

        # 设置选择影像的事件处理程序
        self.xuanze_button.clicked.connect(self.on_xuanze_button_clicked)


        # 获取开始推理按钮
        self.pushButton_9.clicked.connect(self.on_tuili_button_clicked)  # 推理按钮


        # 获取诊断报告按钮并设置事件处理程序
        self.pushButton_11.clicked.connect(self.on_baogao_button_clicked)  # 诊断报告按钮
        self.pushButton_4.clicked.connect(self.on_close_button_clicked) # 退出按钮
        self.pushButton_7.clicked.connect(self.on_back_clicked) # 返回登录按钮
        self.pushButton_3.clicked.connect(self.on_history_clicked)  # 查看历史按钮



        self.sitkImage = object()

        self.npImage = object()

        self.currIndex = 0  # 记录当前第几层

        self.maxCurrIndex = 0  # 记录数据的最大层

        self.minCurrIndex = 0  # 记录数据的最小层，其实就是0

        self.baseFileName = ''

        self.isInferSucceed = False

        # 判断是否按下鼠标右键
        self.isRightPressed = bool(False)

        self.model = object()
        # 判断模型是否加载成功
        self.isModelReady = False

        # 宽宽窗位滑动条
        self.slider_ww.valueChanged.connect(self.resetWWWcAndShow)
        self.slider_wc.valueChanged.connect(self.resetWWWcAndShow)
        # 窗宽窗位下来框选择器
        self.cb_wwwc.currentIndexChanged.connect(self.resetWWWcAndShow)

        # 设置窗宽窗位文本框只能输入一定范围的整数
        intValidator = QIntValidator(self)

        intValidator.setRange(-2000, 2000)

        self.line_ww.setValidator(intValidator)

        self.line_ww.editingFinished.connect(self.resetWWWcAndShow)

        self.line_wc.setValidator(intValidator)

        self.line_wc.editingFinished.connect(self.resetWWWcAndShow)

        self.listWidget.itemDoubleClicked.connect(self.changeLayer)

    def on_history_clicked(self):
        self.close()
        self.newWindow5 = HistoryWindow()
        self.newWindow5.show()


    # 关闭窗口
    def on_close_button_clicked(self):
        self.close()

    # 返回登录界面
    def on_back_clicked(self):
        self.close()
        self.newWindow4 = LoginWindow()
        self.newWindow4.show()


    # 选择模型
    def on_jiazai_button_clicked(self):
        """
        打开模型文件选择器
        """
        filename, _ = QFileDialog.getOpenFileName(self, "选取文件", "./", "model Files (*.pdparams)")

        if filename:
            try:

                self.model_name = self.findChild(QtWidgets.QComboBox, 'comboBox_5')
                self.num_class = self.findChild(QtWidgets.QSpinBox, 'spinBox_2')
                model_name = self.model_name.currentText()
                num_class = self.num_class.value()
                if model_name == "UNet":
                    self.model = UNet(num_classes=num_class)
                elif model_name == "U2Net":
                    self.model = U2Net(num_classes=num_class)
                para_state_dict = paddle.load(filename)
                self.model.set_dict(para_state_dict)
                QMessageBox.warning(self, '正确', '模型加载成功')
                self.isModelReady = True
            except Exception as e:
                QMessageBox.warning(self, '错误', '模型加载失败')
                print(e)



    def wheelEvent(self, event):
        """
        鼠标滑轮事件
        """
        try:
            if self.maxCurrIndex != self.minCurrIndex:
                self.angle = event.angleDelta() / 8
                self.angleY = self.angle.y()
                if self.angleY > 0:
                    if self.currIndex < self.maxCurrIndex - 1:
                        self.currIndex += 1
                        if self.isInferSucceed:
                            # self.npImage = self.drawContours(self.npImage, self.inferData)
                            self.showImg(self.drawContours(self.npImage, self.inferData, self.currIndex))
                        else:
                            self.showImg(self.npImage[self.currIndex])
                elif self.angleY < 0:
                    if self.currIndex != self.minCurrIndex:
                        self.currIndex -= 1
                        if self.isInferSucceed:
                            # self.npImage = self.drawContours(self.npImage, self.inferData)
                            self.showImg(self.drawContours(self.npImage, self.inferData, self.currIndex))
                        else:
                            self.showImg(self.npImage[self.currIndex])
        except Exception as e:
            print(e)


    def mousePressEvent(self, event):
        """
        重载一下鼠标按下事件(单击)

        """
        if event.buttons() == Qt.RightButton:  # 左键按下
            self.isRightPressed = True  # 左键按下(图片被点住),置Ture
            self.preMousePosition = event.pos()
        elif event.buttons() == Qt.MidButton | Qt.RightButton:
            self.isRightPressed = False

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.isRightPressed = False

    def mouseMoveEvent(self, event):
        """
        重载一下鼠标移动事件
        """
        try:
            if self.maxCurrIndex != self.minCurrIndex:
                if self.isRightPressed:  # 右键按下
                    self.endMousePosition = event.pos() - self.preMousePosition  # 鼠标当前位置-先前位置=单次偏移量
                    self.preMousePosition = event.pos()
                    ww = self.endMousePosition.x() + self.currWw
                    wc = self.endMousePosition.y() + self.currWc
                    if ww < -2000:
                        ww = -2000
                    elif ww > 2000:
                        ww = 2000
                    if wc < -2000:
                        wc = -2000
                    elif wc > 2000:
                        wc = 2000
                    self.currWw = ww
                    self.currWc = wc
                    self.slider_ww.setValue(int(self.currWw))
                    self.slider_wc.setValue(int(self.currWc))
                    self.line_ww.setText(str(self.currWw))
                    self.line_wc.setText(str(self.currWc))
                    self.resetWWWcAndShow()
        except Exception as e:
            print(e)


    # 选择影像文件
    def on_xuanze_button_clicked(self):
        """
        打开医学影像文件选择器
        """
        try:
            filename, _ = QFileDialog.getOpenFileName(self,
                                                      "选取文件",
                                                      "./",
                                                      "Nii Files (*.nii);;Nii Files (*.nii.gz);;All Files (*)")
            if filename:

                self.isInferSucceed = False
                QMessageBox.warning(self, '正确', '数据加载成功')
                self.baseFileName = os.path.basename(filename).split('.')[0]
                self.sitkImage = sitk.ReadImage(filename)
                self.npImage = readNii(self.sitkImage, self.ww, self.wc)
                self.maxCurrIndex = self.npImage.shape[0]
                self.currIndex = int(self.maxCurrIndex / 2)
                self.showImg(self.npImage[self.currIndex])
        except Exception as e:
            print(e)


    # 开始推理
    def on_tuili_button_clicked(self):
        """
        模型分割预测
        """
        if self.maxCurrIndex != self.minCurrIndex and self.isModelReady:
            self.pushButton_9.setEnabled(True)


            # 创建推理线程
            self.infer_thread = InferThread(self.sitkImage, self.model)

            # 绑定推理失败的槽函数
            self.infer_thread.signal_infer_fail.connect(self.infer_fail)

            # 绑定推理成功的槽函数
            self.infer_thread.signal_infer_result.connect(self.infer_result)

            self.infer_thread.start()

            self.text_loadModel.setText("模型推理中！")
        else:
            QMessageBox.warning(self, "警告", "请加载模型或者加载数据再进行推理", QMessageBox.Yes, QMessageBox.Yes)


    # 推理成功
    def infer_result(self, inferData):
        """
        分割模型预测成功后，结果保存在self.inferData
        """
        # 推理成功，并显示结果
        try:
            self.inferData = inferData.astype(np.uint8)
            QMessageBox.information(self, "信息", "模型推理成功！", QMessageBox.Yes, QMessageBox.Yes)
            self.isInferSucceed = True
            self.infer_thread.quit()
            self.addListInfo(self.inferData)
            # 推理成功后，这里会进行显示图片的操作，要将这段代码显示的图片显示在诊断报告界面
            self.showImg(self.drawContours(self.npImage, self.inferData, self.currIndex))

            # 发出信号，将需要传递的变量作为参数传递
            # self.signal_data.emit(self.npImage, self.inferData, self.currIndex)
            # 信号发送成功
        except Exception as e:
            print(e)


    # 推理失败
    def infer_fail(self):
        """
        推理失败的情况
        """
        QMessageBox.warning(self, "警告", "推理失败！", QMessageBox.Yes, QMessageBox.Yes)



    # 窗宽窗位
    def resetWWWcAndShow(self):
        """
        有四个方式可以修改医学图像的窗宽窗位，
        每次修改后都会在界面呈现出来
        """
        if hasattr(self.sender(), "objectName"):
            objectName = self.sender().objectName()
        else:
            objectName = None
        try:

            if objectName == 'cb_wwwc':
                windowWidth = self.cb_wwwc.currentText()
                self.line_ww.setText(str(self.wwwcList[windowWidth][0]))
                self.line_wc.setText(str(self.wwwcList[windowWidth][1]))
                self.slider_ww.setValue(self.wwwcList[windowWidth][0])
                self.slider_wc.setValue(self.wwwcList[windowWidth][1])
                self.ww = self.wwwcList[windowWidth][0]
                self.wc = self.wwwcList[windowWidth][1]
                self.currWw = self.ww
                self.currWc = self.wc
            elif objectName == 'slider_ww' or objectName == 'slider_wc':
                self.currWw = self.slider_ww.value()
                self.currWc = self.slider_wc.value()
                self.line_ww.setText(str(self.currWw))
                self.line_wc.setText(str(self.currWc))
            elif objectName == 'line_ww' or objectName == 'line_wc':
                self.currWw = int(self.line_ww.text())
                self.currWc = int(self.line_wc.text())
                self.slider_ww.setValue(self.currWw)
                self.slider_wc.setValue(self.currWc)
            if self.maxCurrIndex != self.minCurrIndex:
                self.npImage = readNii(self.sitkImage, self.currWw, self.currWc)
                if self.isInferSucceed:
                    self.showImg(self.drawContours(self.npImage, self.inferData, self.currIndex))
                else:
                    self.showImg(self.npImage[self.currIndex])
        except Exception as e:
            print(e)



    def initUI(self):
        try:
            self.wwwcList = {'软组织窗': [350, 80],
                             "纵隔窗": [300, 40],
                             "脑窗": [100, 40],
                             '肺窗': [1700, -700],
                             '骨窗': [1400, 350]}

            windowWidth = self.cb_wwwc.currentText()
            self.line_ww.setText(str(self.wwwcList[windowWidth][0]))
            self.line_wc.setText(str(self.wwwcList[windowWidth][1]))

            self.slider_ww.setValue(self.wwwcList[windowWidth][0])
            self.slider_wc.setValue(self.wwwcList[windowWidth][1])
            self.ww = self.wwwcList[windowWidth][0]
            self.wc = self.wwwcList[windowWidth][1]

            self.currWw = self.ww
            self.currWc = self.wc
        except Exception as e:
            print(e)


    # 显示图片
    def showImg(self, img):
        """
        显示图片
        """
        try:
            if img.ndim == 2:
                img = np.expand_dims(img, axis=2)
                img = np.concatenate((img, img, img), axis=-1).astype(np.uint8)
            elif img.ndim == 3:
                img = img.astype(np.uint8)
            qimage = QImage(img, img.shape[0], img.shape[1], img.shape[1] * 3, QImage.Format_RGB888)
            pixmap_imgSrc = QPixmap.fromImage(qimage)

            self.canvas.setPixmap(pixmap_imgSrc.scaled(393,589))
        except Exception as e:
            print(e)



    def drawContours(self, npImage, inferData, currIndex):
        """
        把mask转换成轮廓绘制在原图上
        """
        img = npImage[currIndex]
        img = np.expand_dims(img, axis=2)
        img = np.concatenate((img, img, img), axis=-1).astype(np.uint8)
        ret, thresh = cv2.threshold(inferData[currIndex], 0, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, kernel=np.ones((5, 5), np.uint8), iterations=1)
        contours, hierarchy = cv2.findContours(thresh, 1, 2)
        # 这是画轮廓
        img = cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
        cv2.imwrite("./out./predict.jpg", img)
        # 发送信号
        # self.signal_data.emit(self.npImage, self.inferData, self.currIndex)

        return img

    def addListInfo(self, inferData):
        """
        增加列表信息
        """
        self.listWidget.clear()
        d, h, w = inferData.shape
        result = {}
        for i in range(d):
            img = inferData[i]
            if np.sum(img > 0) != 0:
                result[str(i)] = np.sum(img > 0)

        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for key, value in result:
            self.listWidget.addItem("层 " + str(int(key) + 1))

    def changeLayer(self, item):
        """点击列表自动展示该层"""
        self.currIndex = int(item.text().split(' ')[1]) - 1
        if self.isInferSucceed:
            self.showImg(self.drawContours(self.npImage, self.inferData, self.currIndex))
        else:
            self.showImg(self.npImage[self.currIndex])


    def on_baogao_button_clicked(self):
        try:
            self.newWindow3 = MyDialog()
            self.newWindow3.show()
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            QMessageBox.critical(self, "Error", error_msg, QMessageBox.Ok)






# 诊断报告表单填写
class MyDialog(QDialog):
    def __init__(self, parent = None):
        super(MyDialog, self).__init__(parent)
        loadUi('./ui/baogao.ui', self)  # 加载自定义的对话框UI文件
        # 隐藏主窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        image_path = './out/predict.jpg'
        pixmap = QPixmap(image_path)

        self.canvas.setPixmap(pixmap.scaled(461,191))

        # # 连接信号和槽函数
        # doctor_window = DoctorWindow()
        # doctor_window.signal_data.connect(self.handle_infer_data)
        # canvas = MyDialog.findChild(QtWidgets.QLabel, "canvas")
        # 获取保存信息按钮并设置事件处理程序
        self.pushButton.clicked.connect(self.on_save_button_clicked)  # 保存信息按钮
        self.pushButton_4.clicked.connect(self.on_close_clicked)   # 退出按钮


    # 保存信息
    def on_save_button_clicked(self):


        # 连接MySQL数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dtl104104",
            database="ThroaDX"
        )

        # 创建游标
        mycursor = mydb.cursor()
        username = self.lineEdit1.text()
        sex = self.lineEdit2.text()
        id = self.lineEdit4.text()
        age = self.lineEdit5.text()
        cred = self.lineEdit3.text()
        diagdate = self.dateEdit.date().toString("yyyy-MM-dd")
        today = QDate.currentDate()
        today_str = today.toString("yyyy-MM-dd")
        folder_path = "./out/predict.jpg"
        # # 诊断报告命名
        # new_name1 = today_str + "_" + id

        # # 拼接图片路径
        # path = 'C:\\Users\\86184\\Desktop\\throat_system\\report\\{}.png'.format(new_name1)
        #
        #
        #
        # image = QImage(self.frame.size(), QImage.Format_ARGB32)
        # # 创建QPainter对象
        # painter = QPainter(image)
        # # 将QFrame绘制到QImage上
        # self.frame.render(painter)
        # # 保存图片
        # image.save(path)
        #


        # 影像图命名
        new_name = today_str + "_" + id
        new_path = os.path.dirname(folder_path) + "/" + new_name + os.path.splitext( folder_path)[1]
        os.rename(folder_path, new_path)
        new_folder_path = r"E:\throat_system\out" +"\\" + new_name + ".jpg"
        # 构造 SQL INSERT 语句并插入数据到数据库表中
        #mycursor.execute("INSERT INTO patient (username, id,sex,age,cred,diagdate,file_path,report) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (username, id, sex, age, cred, diagdate,new_folder_path,path))
        mycursor.execute(
            "INSERT INTO patient (username, id,sex,age,cred,diagdate,file_path) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (username, id, sex, age, cred, diagdate, new_folder_path))

        mydb.commit()

        QMessageBox.warning(self, '正确', '患者信息保存成功')


    def on_close_clicked(self):
        self.close()


# 患者界面类
class PatientWindow(QMainWindow):
    def __init__(self,username):
        super().__init__()
        # 加载UI文件
        self.name = username
        loadUi('./ui/patients.ui', self)

        # 隐藏主窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.pushButton_5.clicked.connect(self.on_close_clicked)  # 退出按钮
        self.pushButton_6.clicked.connect(self.on_backlogin_clicked)  # 返回登陆按钮




        # 连接MySQL数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dtl104104",
            database="ThroaDX"
        )
        # 创建游标
        mycursor = mydb.cursor()
        # 在数据库中查询该患者名字的记录
        mycursor.execute("SELECT file_path FROM patient WHERE username = %s", (self.name,))
        file_paths = mycursor.fetchall()

        #file_paths = mycursor.execute("SELECT file_path FROM patient WHERE username = %s", (self.name,)).fetchall()
        # 遍历file_paths列表，将每个图片展示到对应的QLabel上
        for i, file_path in enumerate(file_paths):
            try:
                # print(file_path)
                # print(file_path[0])
                # 创建一个QPixmap对象
                pixmap = QPixmap(file_path[0])
                # 将pixmap缩放到(221,173)的大小
                pixmap = pixmap.scaled(221, 173)
                # 获取要展示图片的QLabel对象的名称
                canvas_name = "canvas" + str(i + 1)
                # 获取对应图片名称的QLabel对象的名称
                label_name = "label" + str(i + 1)
                # 获取对应的QLabel对象
                canvas = self.findChild(QLabel, canvas_name)
                label = self.findChild(QLabel, label_name)
                # 在QLabel上展示图片和图片名称
                canvas.setPixmap(pixmap)
                label.setText(os.path.basename(file_path[0]))
                # 为QLabel添加双击放大功能
                canvas.setScaledContents(True)
                #canvas.mouseDoubleClickEvent = lambda event, canvas=canvas: self.show_image(canvas)
                canvas.mouseDoubleClickEvent = lambda event, file_path=file_path[0]: self.show_image(file_path)


            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                print(error_msg)



    def show_image(self, file_path):

        # 创建一个新窗口
        dialog = QDialog(self)
        dialog.setWindowTitle(os.path.basename(file_path))

        # 创建一个QPixmap对象并缩放到指定大小
        pixmap = QPixmap(file_path).scaled(393, 589)

        # 创建一个QLabel对象用于展示放大的图片
        label = QLabel(dialog)
        label.setPixmap(pixmap)

        # 调整窗口大小并展示
        dialog.resize(pixmap.width(), pixmap.height())
        dialog.show()

    # 关闭窗口
    def on_close_clicked(self):
        self.close()

    def on_backlogin_clicked(self):
        self.close()
        self.newWindow3 = LoginWindow()
        self.newWindow3.show()



# 医生查看历史界面
class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 加载UI文件
        loadUi('./ui/report.ui', self)
        # 隐藏主窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.pushButton_4.clicked.connect(self.on_close_clicked)  # 退出按钮
        self.pushButton_7.clicked.connect(self.on_diagnose_clicked) # 返回一键诊断
        self.pushButton_9.clicked.connect(self.on_find_clicked) # 搜索按钮

        # 退出
    def on_close_clicked(self):
        self.close()


    # 返回一键诊断
    def on_diagnose_clicked(self):
        self.close()
        self.newWindow5 = DoctorWindow()
        self.newWindow5.show()


    def on_find_clicked(self):
        # 连接MySQL数据库
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dtl104104",
            database="ThroaDX"
        )
        # 创建游标
        mycursor = mydb.cursor()
        # 获取患者姓名
        username = self.lineEdit1.text()
        # 在数据库中查询该患者名字的记录
        mycursor.execute("SELECT file_path FROM patient WHERE username = %s", (username,))
        file_paths = mycursor.fetchall()

        # 遍历file_paths列表，将每个图片展示到对应的QLabel上
        for i, file_path in enumerate(file_paths):
            try:

                # 创建一个QPixmap对象
                pixmap = QPixmap(file_path[0])
                # 将pixmap缩放到(221,173)的大小
                pixmap = pixmap.scaled(221, 173)
                # 获取要展示图片的QLabel对象的名称
                canvas_name = "canvas" + str(i + 1)
                # 获取对应图片名称的QLabel对象的名称
                label_name = "label" + str(i + 1)
                # 获取对应的QLabel对象
                canvas = self.findChild(QLabel, canvas_name)
                label = self.findChild(QLabel, label_name)
                # 在QLabel上展示图片和图片名称
                canvas.setPixmap(pixmap)
                label.setText(os.path.basename(file_path[0]))
                # 为QLabel添加双击放大功能
                canvas.setScaledContents(True)
                canvas.mouseDoubleClickEvent = lambda event, file_path=file_path[0]: self.show_image(file_path)
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                print(error_msg)

    # 放大图片
    def show_image(self, file_path):

        # 创建一个新窗口
        dialog = QDialog(self)
        dialog.setWindowTitle(os.path.basename(file_path))

        # 创建一个QPixmap对象并缩放到指定大小
        pixmap = QPixmap(file_path).scaled(393, 589)

        # 创建一个QLabel对象用于展示放大的图片
        label = QLabel(dialog)
        label.setPixmap(pixmap)

        # 调整窗口大小并展示
        dialog.resize(pixmap.width(), pixmap.height())
        dialog.show()



if __name__ == "__main__":
    app = QApplication([])
    loginWindow = LoginWindow()
    loginWindow.show()

    app.exec_()
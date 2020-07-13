# Nao 视觉处理

> 本文主要记录和 Nao 视觉处理相关的 API 
>
> 同时也包括了网络传输的API 
>
> 和 opencv 样例代码说明 



## Nao Vision

核心API 包括有： 

* ALPhtoCapture 

  注意使用方法，为了节省时间，最好先 subscribe to ALVideoDevice , 然后再调用 takePicture 

* ALVideoRecorder 



## Nao Connection API 

核心API 包括有： 

* ALConnectionManager 



## Opencv sample

数据传输： 

* python 发送和接收代码 (network)
* 图像数据转化



opencv 代码样例： 

* 图像校正
* qrcode 识别 
* 色块识别
* 形态识别（多边形 / 圆形 ） 



## 定位代码 

### 多边形定位

尝试使用多边形进行定位（选定6边形和园）

多边形识别思路：

* 对图像进行预处理： 高斯滤波，灰度处理，二值化，开运算 / 腐蚀膨胀 
  * 问题：需要加一个颜色的 Mask，将黑色单独提取出来
* 对图像进行轮廓提取（本质为Canny 算法） 
* 以最大面积轮廓为基准，排除其他干扰轮廓 (contour wash) 
* 对于剩下的轮廓进行多边形近似
* 所得多边形为6边的即为原6边形

圆形识别思路： 

* 步骤与上述步骤基本相同，只不过要求最后检测的出的多边形轮廓边数多于10则认为是圆形



但是在这个过程中出现了不少问题： 

1. 【仿真】环境中的其他形状造成干扰

   * 首先进行最大的轮廓提取，在直接抛弃之外的 contour (contour wash) 

   <img src="C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200712115704351.png" alt="image-20200712115704351" style="zoom: 25%;" />

2. 【仿真】发现由于特征图案和边框相近，在预处理过程中，开运算会将特征图案相连 

   * 为此我去除了开运算，并且为了清晰度，在sim中还去除了高斯滤波

   ![image-20200712120007802](C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200712120007802.png)

3. 【仿真】六边形有时会被识别为八边形 （拟合情况不好时，会多/顶点）

   * 处理方法：调整 approxPoly 中的 epsilon 参数，epsilon 越大，approx 精度越低，对于六边形而言，0.02% 正适合

     （由于问题简单故不附图） 

4. 【实际】尝试在现实中进行识别，发现即使识别目标在镜头内，仍然会时不时的丢失目标（可能还是由于现实中的亮度原因） 

   （具体例子见第一张图片） 

   * 暂未去找原因（还没时间），最迟可以到实验走出仿真进入实际世界时再行解决。

     感觉主要原因应该还是环境噪声（包括最麻烦的亮度） 



代码运行方法： 

1. 首先切换到工作目录下
2. 然后运行命令
   * 静态图片识别：`python findShape.py --pic sim.png --side_num 6`
   * 动态识别          : ``python findShape_realtime.py --o output.avi`` 



### （备用方法）色块定位： 

使用红色作为四角定位色，使用蓝色作为小车定位色

识别思路： 

* 



代码未编写，但是由于主体和多边形定位很相似，所以修改起来应该也不慢 



## Appendix 

### 学习网址

* 官方API 手册： https://developer.softbankrobotics.com/nao-naoqi-2-1/naoqi-developer-guide/naoqi-framework/naoqi-apis#naoqi-api
* Opencv (python) 官方手册： https://docs.opencv.org/4.1.2/d6/d00/tutorial_py_root.html
* opencv 典型形态学操作： https://www.cnblogs.com/Undo-self-blog/p/8438808.html 


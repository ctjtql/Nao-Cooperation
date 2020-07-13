# Opencv 形态学

> 本文只是记录了一些 Opencv 中的形态学操作
>
> 只涉及到项目中使用过的函数
>
> 顺便补充一点背景知识





## PreProcess 预处理

* 高斯模糊： 去噪声，但是画面的清晰度下降
* 灰度处理/二值化：便于提取形态学特征，忽略色彩特征，但是要求色彩比较特殊
  - 如果需要提取特定颜色，可以用一些颜色 Mask 来替代这一步
* 开运算操作：将一些基本相连的域连接起来，用于二值化以后的图像，缺点是可能导致一些原本靠的较近，但是不想连的区域也相连



具体的函数接口和实现方法见 ``./vision/utils.py``



## Contours 轮廓提取

* Contours： 

  轮廓，在 Opencv 中存储为顶点列表

* Hierarchy： 	

  轮廓之间的关系，在 Opencv 存储为一个数组列表

  数组元素的格式为： [Next ，Previous ，First_Child ，Parent]（不存在则为-1）
  
  由于本质上是 Tree 结构，所以说需要使用深度/广度优先搜索



具体函数和接口实现见 ``./vision/findShape.py`` 下的 ``cv2.findContours`` 函数



## Wash 背景清洗 

> 注：这个是之后根据实际情况最可能更改的 section

目前的方法： 

* 首先提取画面中最大面积的轮廓
* 根据 hierarchy 信息，排除在最大面积轮廓以外的所有轮廓



方法较为简单，在后面的仿真/现实 中都可能会出现问题

其中 hierarchy 信息的查找用到了 **广度优先搜索**

具体函数和实现见 ``./vision/findShape.py`` 下注释为 ``wash contours`` 的代码段



## Approx Poly 轮廓的多边形近似

将之前提取出的轮廓用多边形（不确保为凸多边形，但可以进行凸性检测）进行近似

近似程度由参数 ``epsilon`` 控制，参数越小，近似越精确，所得多边形顶点数增加 ；反之亦然。 



实现函数： 

```python
cv2.approxPolyDP(contour,epsilon)
```



其中 epsilon 的计算方法为查字典法： 

- 六边形使用的 epsilon： 0.02% x length(contour)
- 四边形使用的 epsilon： 0.01% x length(contour) 
- 圆形使用的 epsilon     :   0.01% x length(contour)
- 其他                             ：  0.01% x length(contour)



具体函数和实现见 ``./vision/findShape.py`` 下注释为 ``approx contours`` 的代码段





## Appendix

### 学习资源

* Opencv (python) 官方手册： https://docs.opencv.org/4.1.2/d6/d00/tutorial_py_root.html
* opencv 典型形态学操作： https://www.cnblogs.com/Undo-self-blog/p/8438808.html 


# Nao 运动控制

> 本文是关于 Naoqi 的运动接口整理
>
> 核心目的为：完成基本的关节控制和姿态结算
>
> 需要按照本文顺序依次阅读官方手册，运行样例代码
>
> 所有样例代码都已经整理在文件夹 */Nao/sample-code* 中
>
> 注：暂时不确样例代码保能100%运行，有些功能貌似webots-nao还不支持



## 基础： Core 核心

核心 Module

* ALBehaviorManager 
* ALConnectionManager （这个貌似virtual robot 不支持，所以没有再尝试进行实际的和电脑的连接 ）
* ALMemory 





## 基本运动控制： Motion 

核心 Module : 

* ALPosutre：提供基本的动作 (predefined)
* ALMotion ：核心 



ALMotion 的控制目标包括： 

**低层次**

* stiffness： 0.0 is no torque / 1.0 is 100 percent torque 
* angle : the angle of one joint 
* trace： 只需要给定关键位置，就可以

**高层次** 

* Locomotion (moveTo): 

  can't promise anything, e.g. 无法保证机器人重心同一水平面

* [核心] Cartesian (末端位置控制) :

  其中涉及到的基本概念需要仔细看看



## Appendix

### A：各个关节名称表 

<img src="C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200706160520221.png" alt="image-20200706160520221" style="zoom:67%;" />

链接： 

http://doc.aldebaran.com/2-5/family/robots/bodyparts.html#nao-chains





### B： 各个 Effector 名称

<img src="C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200706174557253.png" alt="image-20200706174557253" style="zoom: 67%;" />

链接： 

https://developer.softbankrobotics.com/nao-naoqi-2-1/nao-documentation/nao-technical-guide/nao-technical-overview/effector-chain#nao-effector



### C： ALMath Module

一个和机器人运动学解算有关的工具库

模块核心为几个比较有用的类 (Rotation,Transform,Pose6D,etc)

* 官方文档： http://doc.aldebaran.com/2-4/ref/libalmath/overview.html





### 其他资料： 

* Naoqi2.1 API 官方文档： https://developer.softbankrobotics.com/nao-naoqi-2-1/naoqi-developer-guide/naoqi-framework/naoqi-apis#naoqi-api
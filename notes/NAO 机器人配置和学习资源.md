# NAO 机器人配置和学习资源

> 本文是关于Nao 机器人的配置和学习总结
>
> 主要包括以下几个内容：
>
> * Nao : 简介
> * Nao IDE：Choregraphe 学习
> * Nao 仿真环境： Webots / Webots for nao 
> * Nao API (python): naoqi 学习



## Nao

版本参数

|            | version |
| ---------- | ------- |
| 实物       | v5.0    |
| simulation | v5.0    |



硬件配置： 

https://developer.softbankrobotics.com/nao-naoqi-2-1/nao-documentation/nao-technical-guide/nao-technical-overview



坐标规定（xyz轴和对应的旋转角） 

<img src="C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200706172151378.png" alt="image-20200706172151378" style="zoom:67%;" />

所涉及的旋转角均为沿坐标轴右手螺旋



## Choregraphe

### 使用入门

（来自 B 站学习视频）https://www.bilibili.com/video/BV18s411B7cN?from=search&seid=10821786020985820482



### 深入理解

本质是图形化的一个IDE

核心概念就是行为 (Behavior) 和  指令盒 (command box)

一个行为，本质就是各个指令盒构成的线性序列或非线性序列

指令盒是真正的最小编程单元，使用的是 Python API (naoqi)

具体的创建指令盒的操作方法： 

http://doc.aldebaran.com/2-5/getting_started/helloworld_choregraphe_script.html



### 安装说明： 

下载网址（日本，翻墙快些）：https://www.softbankrobotics.com/jp/developer/document/

需要选择V5的版本

注：有免费密钥： 

> 启动Choregraphe时，将提示您输入有效的许可证密钥。请复制并粘贴以下免费许可证密钥以供使用。
> **654e-4564-153c-6518-2f44-7562-206e-4c60-5f47-5f45**





## Webots

### 入门

同样来自B站视频： https://www.bilibili.com/video/BV11V411f7ko?p=7



### 深入理解

和 vrep ，gazebo 并列的一个机器人仿真环境

在 webots 中，不论是机器人还是仿真世界 (sim world) ,都是由一个个属性节点构成的节点树

一个webots 仿真项目（Project）中包括的核心概念有：

* world 节点：提供仿真环境的各个属性

* viewpoint 节点：控制观察视角

* robot 节点：机器人节点，规定了机器人的各个属性

  其下的 controller 节点最为重要，可以用于控制机器人行为

  如果要使用naoqi 控制 webots，需要保证controller 为 naoqisim.exe



### 补充：安装说明

一共有两种安装方式： 

1. 直接安装 webots8（2017年版本，较老）

   好处：可以直接使用webots并和 choregraphe无缝连接

   操作方法：http://doc.aldebaran.com/2-4/software/webots/webots_index.html#webots 

   注：

   1. 我用的版本是8.5.2，目测运行良好
   2. 需要注意controller 是不是 naoqisim

> 注：邮箱和密码为： 
>
> ![image-20200710161258771](C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200710161258771.png)



2. 使用高版本 webots + 已经编译好的 world

   可以使用这里的世界（内含naoqisim [未编译] )：https://github.com/cyberbotics/naoqisim

   其安装流程见其主页 ReadMe.md 下 Build 部分



我最终使用了第一种方式，原因是在第二种方式中，我遇到了 naoqisim 编译失败的问题： 

1. 我直接 make 失败多次，遇到的问题分别为： 

   * 【已解决】 命令行编译：初步安装的msys2 上不含unzip,make,mingw等工具，需要自行安装，方法自搜

   * 【未解决】 命令行编译：在compile simulation-sdk一步，遇到编译错误，错误提示为： 

     ~~~
     gcc:Error Code = 1 
     ~~~

     由于无法从make过程中获取更加详细的出错信息，所以我放弃使用命令行编译，改用VS2019编译

2. 改用VS2019后成功编译，但是程序会crash

   * VS2019 编译：配置好项目信息后，成功编译出 naoqisim.exe，具体配置见： 

     https://cyberbotics.com/doc/guide/using-your-ide?tab-language=c++

     但是build 出来的exe 在运行过程中居然会 crash，也是神奇了

     解决方式：使用 VS2010 进行编译就成功了，是windows自己的框架不匹配的问题
   
   



> 注：如果后面需要提高 webots 版本，几个可能的问题解决方向：
>
> 是否可以把8.5.2的 naoqisim.exe 
>
> 放在高版本的 webots 中使用
>
> 毕竟编译出来的这个 naoqisim.exe 没有 crash 过
>
> 说不定可以解决问题
>
> ---
>
> 或者再干脆一点，直接把整个world 都用高版本打开？ 



### 补充：使用说明

在使用webots之前记得后台删除两个进程： 

* hal.exe 
* qi-*.exe

有时候webots关闭不正常会在后台留下这两个进程

它们会影响下一次的 naoqisim 运行



## Naoqi

### 入门

整合网站： https://www.jianshu.com/p/1389128870da



### 深入理解

核心概念为： 

* Proxy
* module
* method

基本样例代码： 

~~~python
# -*- encoding: UTF-8 -*-
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "<IP of your robot>", 9559)
tts.setLanguage("English")
tts.say("Hello world")
~~~

API 详细学习请参见文档： 

* Nao 运动控制.md 



### 补充：windows 下 Nao 的纯 Python 环境配置

> 说明：
>
> 为了更方便的运行官方代码，
>
> 以及后续合作编写代码的需要
>
> 可以自行安装win10 下的纯 Python 环境。
>
> 此步也可以不选，只工作在 Choregraphe 下
>
> 但是推荐抽时间安装一下，后续项目可能会用到 



官方教程： 

https://developer.softbankrobotics.com/nao6/naoqi-developer-guide/sdks/python-sdk/python-sdk-installation-guide#python-install-guide

但实际上中间有几个坑

1. windows 下需要先把 python2 和 python 3 区分开来

   详细方法：https://blog.csdn.net/xc_zhou/article/details/80700626

   我稍微做了点改变，将原 python 和 pip 仍然指向python3.7 

   而只是使用python2 和 pip2 来控制 python2.7 下所有包

2. 真实的SDK 网址在这里：

   https://www.softbankrobotics.com/jp/developer/document/

   选择 V4&V5 下 <u>*Python 2.7 SDK 2.1.4 Win 32 Setup.exe*</u> 下载

3. 所应该使用的 python 版本应该是 win32 版本。如果使用 python2.7-64 版本，会导致如下问题：

   ~~~ 
   Import Error: %1 is not a valid win64 application
   ~~~

   但是最新的SDK (2.8.x) 却需要 python2.7- 64版本，所以千万别看错官方提供的教程是给哪个版本的机器人使用的

4. （未查明）SDK 版本需要和使用的机器人相匹配？，官网提供的只有两个版本： 

   * Nao6 --- 2.8.x : 版本过高，会出现如下所示的问题 

     <img src="C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200706125935586.png" alt="image-20200706125935586" style="zoom: 67%;" />

     即在仿真环境下部分 service 无法找到

   * Naoqi2.1 : 版本是不是有点太低？ 现在官方推荐的是这个版本

   

安装成功的结果图： 

<img src="C:\Users\lvgr2\AppData\Roaming\Typora\typora-user-images\image-20200704164244034.png" alt="image-20200704164244034" style="zoom:67%;" />



最终也成功的用默认端口号和IP（127.0.0.1 + 9553）控制 webots 中的虚拟机器人



### API 手册

* 官方：https://developer.softbankrobotics.com/nao-naoqi-2-1/naoqi-developer-guide/naoqi-framework/naoqi-apis#naoqi-api




## Appendix

### A：学习资源

* Naoqi (python) 官方手册：https://developer.softbankrobotics.com/nao-naoqi-2-1/naoqi-developer-guide/naoqi-framework/naoqi-apis#naoqi-api
* Naoqi 之家（中文）： http://twoq.gitee.io/naoqi.net/
* B 站视频若干



### B：下载网址： 

* SDK：  https://developer.softbankrobotics.com/nao6/downloads/nao6-downloads-windows
* Choregraphe: https://www.softbankrobotics.com/jp/developer/document/
* Webots ： https://github.com/cyberbotics/webots/releases
* naoqisim（未编译） ： https://github.com/cyberbotics/naoqisim





### C：已成功的环境版本

| software    | version  |
| :---------- | :------- |
| python      | 2.7.16   |
| pynaoqi     | 2.1.4.13 |
| webots      | 8.5.2    |
| Choregraphe | 2.1.4.13 |


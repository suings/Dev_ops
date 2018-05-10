# 第一次任务内容
## 任务1 了解web组工作流程，psd提取素材，并整合到自己的网页中
- web组工作流程：切图+写结构（HTML）+写样式（Css）
- psd提取素材：打开ps->图层找到图片->右键导出
- 整合
## 任务2 学会简单的html等
我觉得这个问题不大，毕竟有基础
## 任务3 psd完成为首页
已解决，在同级目录中。
## 任务4 建立Dev_ops仓库
已解决
## 任务5 建立Task-x文件夹
已解决
## 任务6 上传文件到此
已解决。git push
## 遇到的问题
代码不规范。不具可拓展性。几乎全部采用了class命名。命名含义不特别清晰。全部采用了单class形式（没采用class="class1 class2"形式。
偶尔直接使用style=""形式。
无大局观。
![](https://raw.githubusercontent.com/suings/Dev_ops/master/Task-1/questionimg/1.png)  
在解决此处时，我采用的是  

	<div>
		<img>
		<span></span>
		<span></span>	
		<span></span>
	</div>  

形式，然后span各自左右浮动，产生的问题是三个span的大小不一，效果如下图上面的一部分<br>
![](https://raw.githubusercontent.com/suings/Dev_ops/master/Task-1/questionimg/2.png)

想要实现的是上图的下半部分,没能解决。我最终采用的是全部垂直居中。
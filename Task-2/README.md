# 试用期第二周任务
## 学会使用简单的Linux命令  
这条可以囊括在下面的任务里  
## 使用Apache搭建Web服务器，将自己上周写的网页放上去。

![](https://raw.githubusercontent.com/suings/Dev_ops/master/Task-2/res/apache.png)  
yum安装：yum -y install httpd  
由yum自己解决依赖关系。  
  
apache的启动：  
启动：
	httpd -k start  
重启：
	httpd -k restart  
关闭：
	httpd -k stop  

启动一下试试：
	httpd -k start  
报错了：Could not reliably determine the server's fully qualified domain name, using localhost.localdomain. Set the 'ServerName' directive globally to suppress this message  
解决：在配置文件中找到ServerName  localhost:80，将前面的注释去了。  
配置文件：见下一条  
## 修改Apache服务器的根目录到/var/www/ops
使用
	find / -name "httpd.conf"
查找配置文件位置  
位于/etc/httpd/conf/httpd.conf  
文件备份：
	cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak  
改变配置文件：
	vim /etc/httpd/conf/httpd.conf  
117行左右：更改/var/www/html为/var/www/ops即可  
  
然后：  
	cd /var/www  
	mkdir ops  
	cd ops  
	touch index.html  
重启apache:  
	httpd -k restart  
试一下：  
	wget 127.0.0.1  
  
## 修改Apache服务器的端口号到8080  
在配置文件中：  
	Listen:80 -> Listen:8080  
	ServerName  localhost:80 -> ServerName  localhost:8080  

重启：httpd -k restart  
试下：wget 127.0.0.1:8080  

## 启动Mariadb数据库　并设置为开机自启动，并设置密码  
先安装：yum -y install mariadb  
启动：systemctl start mariadb  
设置开机启动：systemctl enable mariadb  
配置：mysql_secure_installation  
其余见于<a href="https://www.linuxidc.com/Linux/2016-03/128880.htm">https://www.linuxidc.com/Linux/2016-03/128880.htm</a>  
和原文几乎相同，不做重复功。  
 
## github上使用公钥,并写个脚本将自己写的脚本和一些需要交的作业上传到自己的Dev_ops仓库中  
这一项我有点不明白，脚本是bat脚本？git上传也很easy，这样我反倒觉得有点麻烦。  
之前我就是用的git上传的。  
使用方法：  
可参考<a href="https://blog.sujinpeng.net/173.html">https://blog.sujinpeng.net/173.html</a>  
我本地有克隆的仓库，在本地更改完毕后，进入目录，然后:  
	git add Task-2  
	git commit -m Task-2  
	git push  
就好了。  
![](https://raw.githubusercontent.com/suings/Dev_ops/master/Task-2/res/gitpush.png) 
## 附  
### 在实机上访问虚拟机web环境  
更改vmware中网络为桥接模式  
打开防火墙80/8080端口  
暂时开启80端口方法如下：  
	firewall-cmd --zone=public --add-port=80/tcp  
永久开启：  
	firewall-cmd --zone=public --add-port=80/tcp --permanent  
防火墙解决方法，保留来源：<a href="https://blog.csdn.net/codepen/article/details/52738906">https://blog.csdn.net/codepen/article/details/52738906</a>  


## 图文并茂
我觉得这个很难做到啊，都是黑窗口，直接上命令不就好了。  
还是上了一些图。  

## 学长学姐
学长学姐们各有所长，网络也有很多方向，全部学好是不可能的，只要挑其中一个做好，就很好了。
其实对学长学姐还是没多少要说的，我可能是属于那种整天不说话的。硬要我说也说不出来什么。  
话题结束。  
现在就觉得团队分工挺重要的。
话题结束。


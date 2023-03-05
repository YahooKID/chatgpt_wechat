# Wechat-gpt-simple
ChatGPT微信小程序，简单部署.

效果演示：

![演示](/img/onfoot.png)

*部署教程：
1. 本教程基于HBuilderX + 微信开发者工具

*小程序端：
1. HBuilderX导入除server文件夹与img文件夹外的其他文件夹

2. [保证HBuilderX配置正确](https://blog.csdn.net/weixin_56650035/article/details/125188476)

3. 打开manifest.json,修改第53行，"appid"为你微信小程序的appid。[appid申请教程](https://zhuanlan.zhihu.com/p/537389642)

4. 打开pages/index/index.vue, 修改第63行"apiurl"为你的服务器IP地址或者域名(有端口号请注意端口转发或者写成域名:端口的形式)。
P.S. 没有服务器？试试内网穿透。[花生壳内网穿透教程](https://service.oray.com/question/15507.html), 端口默认5001

5. 打开微信开发者工具，保证【设置 -> 安全设置 -> 服务端口】处于打开状态

6. HBuilderX 打开pages/index/index.vue， 【运行 -> 运行到小程序模拟器 -> 微信开发者工具(指定页面) -> 运行当前页面为启动页】

7. Done, 发布请去微信开发者官网查看发布教程

*服务器端
1. [安装python](https://www.python.org)，不要忘记安装过程中点击添加到路径(ADD PATH)

2. 在 shell/terminal/命令提示符中, 逐条运行（mac和部分linux请将pip更换为pip3）
pip install openai
pip install flask

3. 更改server/chatgpt.py第5行"openai.api_key = " 后面添加上你的openai apikey

4. 更改server/main.py第19行 "if pif["cc"]!="随便定一个密码":"，更改随便定一个密码为你自定义的口令
P.S. 该口令作为打开微信小程序时第一条发给小程序的口令，验证正确才可以继续使用.

5. 更改 server/main.py 第46行"app.run(host='192.168.1.*',port=5001)" 192.168.1.*为你的服务器IP地址，内网穿透时更改为你的
内网ip地址，可通过ipconfig/ifconfig查询

6. 在 shell/terminal/命令提示符中, 进入server目录, 运行（mac和部分linux请将python更换为python3）
python main.py

7. 如果好用，卑微求个star，谢谢！🙏

问题咨询请提issue

# 参考项目：

https://github.com/super6wenzi/chatGPT-wx

https://github.com/w15565133664/chatgpt-uniapp

# 常见问题：

1. 实机debug时无法访问网络 : [解决方法](https://zhuanlan.zhihu.com/p/490558510)

2. HBuilderX提示 OPEN IDE ERROR, 检查微信开发者工具所登录账号是否为appid所绑定的账号

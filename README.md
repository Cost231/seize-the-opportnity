1.需要安装浏览器驱动（暂时只支持Firefox浏览器）
python 环境: 安装splinter库
>>pip install splinter

将浏览器驱动geckodriver.exe单独放在一个文件夹内放在firefox安装目录下（默认为C:\Program Files\Mozilla Firefox），并将此文件夹添加至环境变量

测试代码


`from splinter import Browser `


`b=Browser()`


无报错则运行成功

2.运行
建议在Anaconda prompt Shell 中运行，>>python GUI_beta.py
输入姓名学号后点击OK确认以后再点击Log_in 登录，如果输错点modify修改
体育馆目前只支持三天内预定，本程序支持第四天抢票功能【+3（rush）】
本程序支持退订功能，预定后点击update可查询已经预定信息。

3.
体育馆没有个人订场限制，请酌情订场，尽量不要外传

4.
好用点个star吧，谢谢，你的赞赏是我前进的动力。

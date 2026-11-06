# 手机复用调查（2026-11-06）

## 已查证的基础事实

- GitHub Codespaces是运行在云端Linux容器中的开发环境，可从浏览器连接。浏览器只是入口，代码在服务器执行；这不能证明手机浏览GitHub仓库本身就具备执行能力。[官方介绍](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces)
- Termux提供Android本地终端与Linux用户空间，并提供Python等软件包，不要求root。它是安卓本地运行的可能路径，但仍需用户处理项目文件、依赖和导出。[Termux官方](https://termux.dev/en/)
- python-docx依赖lxml；能安装Python不等于所有平台都能安装这些依赖。Android与iOS本地环境须实测，不把云端Linux或其他CPU架构的安装结果当作保证。[python-docx安装说明](https://python-docx.readthedocs.io/en/latest/user/install.html)

上述官方文档只支持对应基础事实，不是本项目已在相应手机或云产品上通过完整测试的证据。

## 适合本项目的优先路径

手机拍照上传 → 支持图片视觉、文件访问和Python执行的AI云端 → 生成DOCX → 宿主导出 → 手机下载/打开。这个路径通常不要求手机本地Python、IDE或编译器；服务端仍须具备可用的Python和项目依赖。是否支持技能导入、联网安装和文件下载，由具体平台、账号和版本决定。

| 场景 | 当前结论 |
| --- | --- |
| 手机只打开GitHub | 能看源码，不代表可执行或自动识图 |
| 手机连接具备执行与导出能力的AI云端 | 符合设计条件；每个产品仍需实际照片与文件下载测试 |
| Android本地Termux | 有可行基础，但本项目未做真机安装及拍照导出实测 |
| iPhone本地Python应用 | 本轮没有足够官方兼容证据及真机结果，不承诺通用可运行 |
| 纯聊天、没有执行或导出能力 | 不能独立完成拍照到DOCX |

用户曾反馈豆包生成考研Word成功、手机能访问GitHub；两项均是用户反馈。没有足够官方证据断言豆包所有手机端、云电脑镜像或账号均支持本技能。模拟单词照片只能验证当前宿主的演示路径，不能替代手机摄像头、网络传输和客户端下载实测。

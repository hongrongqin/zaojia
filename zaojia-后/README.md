由开源模板改写而来
来源：https://gitee.com/codetty/fastapi-demo

## 目录结构
```angular2html
├─📁 common/------------------- # 公共目录
│ ├─📁 exception/-------------- # 异常
│ │ ├─📄 __init__.py
│ │ ├─📄 exception_base.py----- # 自定义基本异常
│ │ ├─📄 exception_sms.py------ # 自定义sms异常
│ │ ├─📄 exception_user.py----- # 自定义用户异常
│ │ └─📄 handler.py------------ # 异常捕获
│ ├─📁 response/--------------- # 响应目录
│ │ ├─📄 __init__.py
│ │ ├─📄 code_base.py---------- # 基本状态码
│ │ ├─📄 code_sms.py----------- # sms状态码
│ │ ├─📄 code_user.py---------- # 用户状态码
│ │ └─📄 schema.py------------- # 返回响应
│ └─📄 __init__.py
├─📁 controller/--------------- # 接口层
│ ├─📁 v1/--------------------- # api v1版本目录
│ │ ├─📄 __init__.py
│ │ └─📄 user.py--------------- # 用户接口
│ ├─📄 __init__.py
│ └─📄 routers.py-------------- # 路由接口
├─📁 core/--------------------- # 核心配置目录
│ ├─📄 __init__.py
│ ├─📄 config.py--------------- # 系统配置文件
│ └─📄 register.py------------- # 注册函数
├─📁 dao/---------------------- # 数据操作层
│ ├─📄 __init__.py
│ ├─📄 base.py
│ └─📄 user.py----------------- # 用户数据层
├─📁 database/----------------- # 数据库配置
│ ├─📄 __init__.py
│ ├─📄 db.py------------------- # mysql配置
│ ├─📄 mongo.py---------------- # mongo配置
│ └─📄 redis.py---------------- # redis配置
├─📁 logger/------------------- # 日志目录
│ └─📄 logger.py
├─📁 middleware/--------------- # 中间件目录
│ ├─📄 __init__.py
│ └─📄 access_middleware.py---- # 记录请求日志
├─📁 schemas/------------------ # 模型参数
│ ├─📄 __init__.py
│ ├─📄 base.py----------------- # 基础参数
│ ├─📄 jwt.py------------------ # jwt参数
│ └─📄 user.py----------------- # 用户参数
├─📁 services/----------------- # 业务层
│ ├─📄 __init__.py
│ ├─📄 jwt.py------------------ # jwt业务
│ └─📄 user.py----------------- # 用户业务
├─📁 tests/-------------------- # 测试目录
│ ├─📄 __init__.py
│ └─📄 test.py
├─📁 utils/-------------------- # 工具类
│ ├─📄 __init__.py
│ └─📄 health_check.py
├─📄 .env.dev------------------ # 开发环境配置
├─📄 .env.local---------------- # 本地环境配置
├─📄 .env.prod----------------- # 生产环境配置
├─📄 .gitignore---------------- # git忽略文件
├─📄 docker-compose.yml
├─📄 Dockerfile
├─📄 main.py------------------- # 程序启动入口
├─📄 README.md
└─📄 requirements.txt---------- # 依赖文件列表
```

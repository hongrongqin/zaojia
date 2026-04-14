# 软件造价自动评估系统 (Software Cost Automatic Evaluation System)

## 📌 项目简介

这是一个基于人工智能的软件造价自动评估系统。系统通过融合 **BERT机器阅读模型** 和 **大语言模型 (LLM)** 的自然语言处理技术，自动化解析用户上传的需求或工程技术文档，智能提取系统的核心业务功能点并进行测算。
最终结合内置的造价标准，为软件开发项目提供科学、客观的造价评估分析结果，解决传统人工评估耗时长、主观性强的问题。

## ✨ 核心功能

1. **文档智能上传与解析**：支持用户上传各类项目文档（如需求规格说明书）。
2. **功能点智能提取 (基于BERT)**：使用微调训练后的 BERT 模型，对文档内容进行深度词法/句法分析，精准抽取出系统涉及的底层软件功能点。
3. **功能点智能分类 (基于大模型 LLM)**：凭借大模型强大的上下文和语义综合理解能力，将散乱的功能点自动归类汇总（如外部输入、外部输出、内部逻辑文件等），匹配造价测算规范。
4. **一键导出评估报告**：系统依据提取分类的功能点及系数权重计算出最终软件造价测算结果，支持一键**下载为 Excel (xlsx) 格式文档**。
5. **完整的业务闭环**：包含用户注册/登录、个人中心、我的历史评估报告管理、运维与权限系统（内置完整的JWT鉴权和角色管理）以及造价基准参数维护。

## 🛠️ 技术栈

### 后端环境 (`zaojia-后`)
- **Web框架**：[FastAPI](https://fastapi.tiangolo.com/) (构建高性能异步API)
- **数据库及ORM**：MySQL + [SQLAlchemy](https://www.sqlalchemy.org/) / SQLModel 
- **数据库驱动**：asyncmy / motor
- **鉴权**：PyJWT
- **服务器与工具**：Uvicorn, Pydantic, Loguru, python-dotenv

### 前端环境 (`zaojia-前`)
- **核心框架**：[Vue 3](https://vuejs.org/) (Composition API) 
- **构建工具**：[Vite](https://vitejs.dev/)
- **UI 组件库**：[Element Plus](https://element-plus.org/)
- **状态与路由管理**：[Pinia](https://pinia.vuejs.org/) + Vue Router 4
- **网络与文件下载**：Axios + xlsx + file-saver

## 📁 核心目录结构

```text
zaojia/
 README.md               # 项目说明文档
 zaojia-后/             # FastAPI 后端目录
    controller/         # 路由分发 (用户、造价标准、个人中心、造价评估等核心接口)
    core/               # 核心配置 (Config, 路由注册)
    dao/                # 数据库操作层 (CRUD封装)
    database/           # 数据库连接初始化
    models/             # 数据库模型 (SQLModel/SQLAlchemy)
    schemas/            # Pydantic 校验模型 (入参/出参接口定义)
    services/           # 核心业务逻辑层 
    utils/              # 通用工具 (验证码、各类分析处理方法等)
    main.py             # 后端应用启动入口
    requirements.txt    # 后端环境依赖包
 zaojia-前/             # Vue3 前端目录
     src/ 
        api/            # 统一接口请求封装
        components/     # 全局复用组件
        router/         # Vue-Router 路由配置
        store/          # Pinia 全局状态管理
        utils/          # 网络请求拦截(request.js)等工具类
        views/          # 页面视图 (工作台、造价评估、报告明细、设置中心等)
     vite.config.js      # Vite 配置文件
     package.json        # 前端依赖包配置
```

## 🚀 快速启动

### 1. 后端服务启动
进入后端目录，并配置好本地虚拟环境 (建议 Python 3.9+) 与数据库:
```bash
cd zaojia-后

# 安装依赖文件
pip install -r requirements.txt

# 配置环境变量(若有.env), 可修改数据库连接配置
# 启动 FastAPI 服务 (默认运行在 8000 端口)
python main.py
# 或使用 uvicorn main:app --reload
```

### 2. 前端服务启动
确保本地已安装 Node.js (推荐 v16+)，进入前端目录:
```bash
cd zaojia-前

# 安装前端依赖
npm install

# 启动本地开发服务
npm run dev
```

启动成功后，根据终端提示的本地地址 (通常为 `http://localhost:5173`) 在浏览器中打开即可使用本系统。

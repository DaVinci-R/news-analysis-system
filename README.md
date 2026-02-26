# 财经新闻智能分析系统 (News Analysis System)

这是一个基于大语言模型（LLM）的模块化财经新闻分析系统。系统拆分为四个独立的层级，每个层级均可独立运行，并支持通过 Docker 容器化快速部署。

## 🏗️ 系统架构

系统由以下四个核心层级组成：

1.  **数据层 (Data Layer)**:
    - 负责通过 `akshare` API 定时获取财联社新闻。
    - 自动初始化数据库表结构，并执行新闻去重。
    - 独立配置：`data_layer/config.py`

2.  **LLM 处理层 (LLM Layer)**:
    - **主处理 (`main.py`)**: 调用大模型对原始新闻进行结构化处理（分类、情感评分、关键词提取等）。
    - **分类总结 (`summary_main.py`)**: 定时对不同资产类别的新闻进行深度汇总分析。
    - 独立配置：`llm_layer/config.py`

3.  **交互层 (Interactive Layer)**:
    - 提供 FastAPI 接口，支持用户通过自然语言进行智能问答。
    - 具备独立的 Q&A 逻辑与 Prompt 管理。
    - 独立配置：`interactive_layer/config.py`

4.  **前端展示层 (Frontend Layer)**:
    - 基于 Streamlit 构建的 Web 界面。
    - 提供新闻可视化看板、高频词云、情绪分析以及智能问答对话框。
    - 独立配置：`frontend_layer/config.py`

---

## 📁 目录结构

```text
news-analysis-system/
├── data_layer/          # 数据采集与存储层
├── llm_layer/           # LLM 处理与总结层
├── interactive_layer/   # 交互 API 层
├── frontend_layer/      # Web 展示层
├── docker/              # Docker 配置文件目录
│   ├── docker-compose.yml
│   ├── data_layer.Dockerfile
│   ├── llm_layer_main.Dockerfile
│   ├── llm_layer_summary.Dockerfile
│   ├── interactive_layer.Dockerfile
│   └── frontend_layer.Dockerfile
├── requirements.txt     # 项目依赖
└── README.md            # 项目说明
```

---

## 🚀 快速启动

### 方式一：使用 Docker 部署 (推荐)

项目已完成全容器化封装，你可以一键启动所有服务：

```powershell
# 进入 docker 目录
cd docker

# 构建镜像
docker-compose build

# 启动所有服务
docker-compose up -d
```

**访问服务：**
- **Web 界面**: [http://localhost:8501](http://localhost:8501)
- **交互接口**: [http://localhost:8001](http://localhost:8001) 

### 方式二：本地运行

1.  **安装环境**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **分步启动**:
    - 启动数据层: `python -m data_layer.main`
    - 启动 LLM 处理: `python -m llm_layer.main`
    - 启动交互层: `python -m interactive_layer.main`
    - 启动前端: `python -m frontend_layer.main`

---

## ⚙️ 配置说明

每个层级下都有各自的 `config.py`。
- 在 **Docker 部署** 模式下，项目会自动将宿主机的 `config.py` 挂载到容器内部。
- 修改本地配置文件后，只需重启对应容器即可生效：
  ```bash
  docker-compose restart [service_name]
  ```

---

## 🛠️ 技术栈

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Database**: MySQL (SQLAlchemy)
- **NLP/LLM**: OpenAI SDK 协议 (支持 DeepSeek, GPT 等), Akshare
- **DevOps**: Docker, Docker Compose
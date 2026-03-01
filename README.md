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
    - 启动 LLM 处理: `python -m llm_layer.main` 和 `python -m llm_layer.summary_main`
    - 启动交互层: `python -m interactive_layer.main`
    - 启动前端: `python -m frontend_layer.main`

---

## ⚙️ 配置说明

系统采用环境变量与配置文件结合的方式进行管理。在 Docker 部署中，主要通过项目根目录下的 `.env` 文件进行统一配置。

### 1. 统一环境配置 (.env)

| 变量名 | 说明 | 示例值 |
| :--- | :--- | :--- |
| `DB_HOST` | 数据库地址（Docker 模式下为 `db_mysql`） | `db_mysql` |
| `DB_PASSWORD` | MySQL root 密码 | `yourpassword` |
| `ONLINE_API_KEY` | 大模型 API Key | `sk-xxxx` |
| `ONLINE_BASE_URL`| 大模型 API 基础路径 | `https://api.deepseek.com` |
| `ONLINE_MODEL` | 使用的模型名称 | `deepseek-chat` |

### 2. 各层级详细参数

#### 📊 数据层 (Data Layer)
- `SPIDER_INTERVAL`: 新闻爬取的时间间隔（秒），默认 `60`。

#### 🧠 LLM 处理层 (LLM Layer)
- `BATCH_SIZE`: 主处理模块单次从数据库读取并处理的新闻条数。
- `CONCURRENCY`: 并发处理的线程/协程数量。
- `PROCESS_INTERVAL`: 轮询未处理新闻的间隔时间（秒）。
- **分类总结配置 (Summary)**:
    - `SUMMARY_TRIGGER_MODE`: 触发模式，可选 `fixed` (定点) 或 `interval` (间隔)。
    - `SUMMARY_FIXED_TIME`: 定点触发的时间点（如 `08:30`）。
    - `SUMMARY_INTERVAL`: 间隔模式下的循环时间（秒）。
    - `SUMMARY_DEFAULT_WINDOW_HOURS`: 总结任务向前回溯的时间范围（小时）。

#### 💬 交互层 (Interactive Layer)
- `API_PORT`: 后端 API 服务端口，默认 `8001`。
- `DEFAULT_MODEL_NAME`: 智能问答默认调用的模型。

#### 🎨 前端展示层 (Frontend Layer)
- `INTERACTIVE_API_HOST`: 交互层服务的地址（Docker 模式下为 `interactive_layer`）。
- `WEB_PORT`: Streamlit 服务运行端口，默认 `8501`。

---

## 🛠️ 运维与调试

- **查看日志**: 
  ```bash
  docker-compose logs -f [service_name]
  ```
- **配置生效**: 修改 `.env` 后，建议重新启动服务：
  ```bash
  docker-compose up -d
  ```

---

## 🛠️ 技术栈

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Database**: MySQL (SQLAlchemy)
- **NLP/LLM**: OpenAI SDK 协议 (支持 DeepSeek, GPT 等), Akshare
- **DevOps**: Docker, Docker Compose
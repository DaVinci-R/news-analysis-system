# 财经新闻智能分析系统

一个基于大语言模型的财经新闻自动获取、分析和可视化系统。该系统能够自动获取财联社新闻，使用大语言模型进行智能分析分类，并提供Web界面进行结果展示。

## 📋 功能特性

- **自动新闻获取**：通过akshare API定时获取财联社新闻
- **智能去重**：采用hash值方法进行新闻去重
- **双模型支持**：支持API调用和本地部署两种大语言模型使用方式
- **智能分析**：调用LLM对新闻进行分类和深度总结分析
- **数据持久化**：MySQL数据库存储和管理
- **错误处理**：完善的JSON格式检查和修复机制
- **可视化展示**：基于Streamlit的Web界面
- **数据备份**：自动备份分析结果

## 🛠️ 技术栈

- **编程语言**：Python
- **大语言模型**：Qwen3-4B（本地） / API调用
- **数据库**：MySQL
- **机器学习框架**：Transformers (HuggingFace)
- **数据获取**：akshare
- **Web框架**：Streamlit
- **其他**：JSON处理、Hash去重

## 🖥️ 系统要求

- **推荐配置**：Intel i9 13代 + 64GB RAM + RTX 5070Ti
- **最低配置**：8GB RAM（仅API模式）
- **操作系统**：Windows/Linux/macOS
- **Python版本**：3.12
- **数据库**：MySQL 8.0+

## 📁 项目结构

```
news-analysis-system/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包
├── src/                        # 源代码目录
├── ├──config/
│   │   ├──config.py            #  数据库配置信息
│   │   └── sql_table_create.txt # 数据表创建语句
│   ├── models/                 # 模型相关
│   │   ├── api_model.py        # API调用大语言模型
│   │   └── local_model.py      # 本地Qwen3-4B模型加载
│   ├── database/               # 数据库相关
│   │   └── db_handle.py        # MySQL连接和数据操作
│   ├── data_processing/        # 数据处理相关
│   │   ├── get_cls_news.py     # 财联社新闻获取
│   │   ├── review_json.py      # JSON格式检查修复
│   │   └── import_json.py      # JSON数据导入数据库
│   ├── analysis/               # 分析相关
│   │   ├── main.py             # 主分析程序
│   │   └── categories_summary.py # 分类总结分析程序
│   └── visualization/          # 可视化相关
│       └── streamlit_web.py    # Web可视化界面
└── data/                       # 数据目录
    ├── backup_results/         # JSON分析结果备份
    └── summary_results/        # 总结分析结果备份
```

## 🚀 快速开始

### 1. 环境准备

在安装依赖时要先将requirements.txt文件的torch版本修改成匹配你电脑的gpu版本

```bash
# 克隆项目
git clone https://github.com/DaVinci-R/news-analysis-system.git
cd news-analysis-system

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

配置MySQL数据库连接信息在 `src/database/db_handle.py` 中。
创建具体的表结构与列名在`src/datebase/sql_table_create.txt`中。


### 3. 模型配置

**本地模型**：
- 系统将自动下载Qwen3-4B模型，采用huggingface的transformers
- 确保有足够的存储空间和显存，本机配置为i9 + 5070ti +64ram 
- 实际运行qwen3-4B占用显存约10G左右

**API模型**：
- 在 `src/models/api_model.py` 中的Client位置配置API密钥，同样可切换成支持openai client的其他LLM

### 4. 运行系统

**获取新闻数据**：
```bash
python src/data_processing/get_cls_news.py
```

**执行新闻分析**：
```bash
python src/analysis/main.py
```

**处理JSON错误**（如需要）：
```bash
python src/data_processing/review_json.py
python src/data_processing/import_json.py
```

**生成分类总结**：
```bash
python src/analysis/categories_summary.py
```

**启动Web界面**：
```bash
streamlit run src/visualization/streamlit_web.py
```


## 📊 系统架构

```
新闻获取 → 数据库存储 → LLM分析 → 结果处理 → 可视化展示
    ↓           ↓          ↓         ↓          ↓
get_cls_news → db_handle → main.py → review → streamlit_web
    ↓                       ↓         ↓
  去重处理              本地/API模型   import_json
                                      ↓
                              categories_summary
```

## 🔧 核心模块说明

### 数据获取模块
- `get_cls_news.py`：获取财联社新闻，采用hash值去重

### 模型模块
- `local_model.py`：本地加载Qwen3-4B模型，采用huggingface的transformers
- `api_model.py`：API调用模式，适合资源受限环境

### 分析模块
- `main.py`：主分析引擎，支持模型切换，包含备份和数据库写入功能
- `categories_summary.py`：深度分类分析，生成总结报告

### 数据处理模块
- `review_json.py`：检查和修复LLM输出的JSON格式错误
- `import_json.py`：将处理后的JSON数据导入数据库

### 可视化模块
- `streamlit_web.py`：基于Streamlit的Web界面，展示分析结果

## 📋 使用说明

1. **首次运行**：先运行 `get_cls_news.py` 获取新闻数据
2. **选择模型**：根据硬件配置选择本地模型或API模型
3. **执行分析**：运行 `main.py` 进行新闻分析，默认运行local_model
4. **错误处理**：如遇JSON格式问题，使用 `review_json.py` 修复
5. **深度分析**：运行 `categories_summary.py` 生成分类总结
6. **结果查看**：通过Streamlit界面查看可视化结果


## :📃 文件说明

`get_cls_news.py`: 可以通过akshare的api获取到财联社的新闻，并定时运行，结果保存在news数据表中.  

`db_handle.py`: 用于配置mysql数据库信息。  

`sql_table_create.txt`: 包含创建数据表的sql语句。  

`api_model.py` :通过调用API加载LLM，可切换成其他支持openai client的LLM.  

`local_model.py`:通过调用transformers库加载的LLM，更多的model可以在huggingface的model hub中查找。

`main.py` 默认加载的是local_model，主要负责将news数据表中的新闻进行分类、关键词提取、情感评分、总结等，结果储存在analysis_results表中，备份在`data/backup_results`文件夹下，是主程序执行文件.  

`review_json.py`: 通常用于main.py文件执行完但结果写入数据库失败，功能为检查LLM输出的错误json格式文件，因为LLM通常在输出双引号时，偶尔会出现json格式错误，导致写入数据库失败。该py文件能够快速帮你定位到哪一行有错误.  

`import_json.py`: 则是将你修正后的json格式文件导入到数据库中，在导入到数据库中之后，需要手动更新processed_hashes数据表中的hash值，因为processed_hashes表中的内容只有在main.py程序正确写入到数据表中，才会自动更新，主要方法是analysis_results表中的最后一条新闻的news_index列值定位news表中的id，复制对应id列的content_hash值，粘贴至processed_hashes表中即可。(analysis_results的news_index列值来源于news表中的id值，主要目的是方便溯源)  

`categories_summary.py`:文件主要用于将某日的所有新闻，按照六大类进行汇总摘要，进一步总结，结果保存在summary数据表中。  

`streamlit_web.py`:文件主要用于新闻的可视化，数据来源于analysis_resluts表和summary表，能够显示当日的高频关键词、整体市场平均情绪、受到影响的市场以及各分类总结等。


## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 📄 许可证

[MIT License](LICENSE)

## 🙋‍♂️ 支持

如有问题请提交Issue或联系项目维护者。
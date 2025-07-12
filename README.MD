# DlDataCollector_LITE 轻量级数据采集工具

> 仅供学习交流，禁止用于商业用途 | 数据采集频率需遵守目标网站Robots协议

## 项目简介
DlDataCollector_LITE 是基于Python的多模板数据采集工具集，采用自动化技术实现网页数据提取。当前支持招聘网站（Boss直聘/51Job）和音乐平台（网易云音乐）的数据采集，提供可扩展的模板架构，持续更新适配新网站。

## 核心功能
- 🌐 多平台支持：支持招聘网站和音乐平台数据采集
- 🧩 模块化设计：每个网站独立模板，可单独运行
- 🚀 快速部署：简单配置即可启动采集任务
- 📊 数据导出：自动保存CSV格式至指定目录
- 🔄 持续更新：定期新增模板适配主流网站

## 环境要求
- Python 3.10+
- 依赖库：
  ```bash
  pip install DrissionPage pandas requests pathlib
```
- 浏览器环境（Chrome/Chromium 119+）

## 目录结构
```
DlDataCollector_LITE/
├── templates/              # 采集模板目录
│   ├── boss/               # Boss直聘模板
│   ├── job51/              # 51Job模板
│   └── wy/                 # 网易云音乐模板
├── exports/                # CSV数据导出目录
├── download/               # 文件下载目录（如音乐）
└── README.md               # 项目文档
```

## 快速开始
1. **克隆项目**
   ```bash
   git clone https://github.com/yourname/DlDataCollector_LITE.git
```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置参数**
   - 修改模板文件中的搜索参数：
     ```python
     keywords = ["python", "java"]      # 搜索关键词
     city_code = '101180100'           # 城市区号（郑州）
     max_page = 3                      # 采集页数
     ```

4. **运行采集**
   - Boss直聘模板：
     ```bash
     python templates/boss/boss_search_keywords.py
     ```
   - 51Job模板：
     ```bash
     python templates/job51/job51_search_keywords_dp.py
     ```
   - 网易云音乐模板：
     ```bash
     python templates/wy/wy_music_free_downloader.py
     ```

## 注意事项
1. **登录要求**
   - Boss直聘模板需手动登录后继续执行
   - 51Job模板无需登录（请遵守其服务条款）

2. **请求频率控制**
   - 默认随机延迟1-3秒
   - 建议并发数不超过CPU核心数的2倍

3. **数据存储**
   - CSV文件按时间戳命名，保存在`exports/`目录
   - 音乐文件保存在`download/`目录

4. **法律声明**
   - 禁止大规模商业用途
   - 数据下载后24小时内请删除
   - 遵守《网络安全法》等相关法律法规

## 模板开发指南
1. **新增模板**
   - 在`templates/`目录新建网站文件夹
   - 继承`BaseCrawler`类实现采集逻辑
   - 使用统一的字段命名规范

2. **贡献代码**
   - Fork项目 → 创建功能分支 → 提交PR
   - 需提供完整测试用例

## 版本更新
- **v1.0.0** 初始版本

## 许可协议
MIT License，详情见[LICENSE](LICENSE)文件

> ⚠️ 使用前请务必阅读并同意《数据采集伦理规范》

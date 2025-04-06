# PEP-book-downloader

PEP-book-downloader 是一个 Python 脚本，用于下载人民教育出版社电子教材的所有页面并合并为 PDF 文件。

## 准备

1. **克隆仓库**

   ```bash
   git clone https://github.com/BI4LGZ/pep-book-downloader.git
   ```

2. **进入项目目录**

   ```bash
   cd pep-book-downloader
   ```

3. **创建并激活虚拟环境**

   - Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. **准备请求头文件**  
   根据浏览器获取的请求头信息，编辑`headers.json`，内容示例如下：

   ```json
   {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
     "Referer": "https://book.pep.com.cn/1311001202171/",
     "Cookie": "YOUR_COOKIE_HERE"
   }
   ```

2. **运行脚本**  
   在[中小学教材电子版](https://jc.pep.com.cn/)中找到合适的电子教材，进入教材阅读页面后复制完整的 URL。在命令行中运行脚本并传入电子教材的 URL。例如：

   ```bash
   python main.py "https://book.pep.com.cn/1311001202171/mobile/index.html"
   ```

   **参数说明**：

   - `--headers_file`：自定义请求头文件路径（默认：`headers.json`）。
   - `--start_page`：起始页码（默认从 1 开始下载）。
   - `--max_failures`：连续下载失败次数达到设定值后停止下载（默认 3）。
   - `--output`：输出 PDF 文件名（默认：`output.pdf`）。

## 注意事项

- **合法性**：请合理适当使用，以避免为人民教育出版社服务器造成负担。非必要请在其网页在线阅读，如需使用也应保证合理适当并符合相关法律法规规定和政策要求，自行承担相应责任（具体见“免责声明”）。
- **环境清理**：程序会清空 `images` 目录和删除旧的 PDF 文件，请确保该目录下没有其他重要文件。
- **请求头更新**：如果下载失败，请检查并更新 `headers.json` 中的请求头信息。

## 免责声明

本项目仅供技术交流和学习使用。使用者需自行承担使用本项目代码所产生的任何风险和法律责任。作者不对因使用本项目代码而引起的任何直接或间接损失承担责任。

## 贡献

欢迎提交 Issue 和 Pull Request！

- **Issue**：如果你在使用过程中遇到问题或有改进建议，请在 [Issue 区](https://github.com/BI4LGZ/pep-book-downloader/issues) 提交 Issue。
- **Pull Request**：欢迎 Fork 本项目，并提交 PR。请确保你的代码风格统一，并附上必要的说明。

## 许可证

本项目采用`MIT License`开源许可证，详细许可证信息请参见 [LICENSE](./LICENSE) 文件。

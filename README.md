Video DownloadHelper (VDH) 深度破解教程

本教程通过 Python 自动化脚本修改插件核心逻辑，彻底绕过 HLS/MPD 视频下载的 **2 小时等待限制**。

---

## 🛠️ 准备工作
1. **安装 Python**：确保电脑已安装 Python 环境。
2. **关闭 IDM**：操作时建议关闭 IDM 插件，防止干扰 Chrome 原生下载流程。

---

## 📖 操作步骤

### 第一步：定位插件目录
1. 打开 Chrome 浏览器，地址栏输入 `chrome://version/` 并回车。
2. 找到 **“个人资料路径”** (Profile Path)，复制该路径。
3. 在文件资源管理器中打开该路径，进入 `Extensions` 文件夹。
4. 找到文件夹 `lmjnegcaeklhafolokijcfjliaokphfk` (这是 VDH 的唯一 ID)。
5. 进入版本号文件夹（例如 `10.2.40.2_0`）。

### 第二步：建立工作区
1. 将 `10.2.40.2_0` 文件夹完整复制到 **桌面**。
2. 进入桌面上的文件夹，找到 `service` 目录（里面存有 `main.js`）。

### 第三步：运行破解脚本
1. 在 `service` 目录中新建一个文本文件，重命名为 `crack_vdh.py`。
2. 将以下代码复制并保存到该文件中：

```python
import os
import re

def final_crack():
    file_path = 'main.js'
    if not os.path.exists(file_path):
        return print("❌ 错误：请将脚本放在 main.js 所在的 service 文件夹内运行。")

    # 备份原始文件
    backup_path = file_path + '.bak'
    if not os.path.exists(backup_path):
        with open(file_path, 'rb') as f_in, open(backup_path, 'wb') as f_out:
            f_out.write(f_in.read())
        print("✅ 已创建 main.js.bak 备份")

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 逻辑 1：任务删除时触发重置 (清空列表即重置)
    code = re.sub(r'(\w+)\.downloading\.delete\(i\.download_id\)', 
                  r'ie(state => state.lsd = yc),\\1.downloading.delete(i.download_id)', code)

    # 逻辑 2：预判重置 (核心：绕过并发报错)
    # 将 a = state.lsd || yc 替换为 ie(state => state.lsd = yc), a = yc
    code = code.replace('a = state.lsd || yc', 'ie(state => state.lsd = yc), a = yc')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print("🚀 深度破解完成！")
    print("现在下载不再需要等待 2 小时限制。")

if __name__ == '__main__':
    final_crack()
```
3.在该目录下打开命令行（Shift + 右键 -> 在此处打开 PowerShell），执行：
```
python crack_vdh.py
```

第四步：加载破解版插件
回到 Chrome，地址栏输入 chrome://extensions/。

开启右上角的“开发者模式”。

移除或禁用原来的官方版插件。

点击左上角 “加载解压的扩展程序”。

选择 桌面 上那个修改好的 10.2.40.2_0 文件夹。

使用小技巧
并发下载：你可以连续点击下载多个视频。如果同时跑 3 个后第 4 个显示排队，只需等前几个结束，新的会自动开启。

手动重置：如果偶然报错，在插件下载列表里点击任务右上角的 “X” 取消任务，会立刻触发代码中的重置逻辑。

永久保留：建议保留好桌面的这个文件夹，这是你的专属无限制版。

免责声明：本教程仅供技术交流学习，请支持正版软件。

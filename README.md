# Browser Automation - 浏览器自动化技能

> ⚠️ **使用声明**: 本技能仅用于技术学习、UI 自动化测试、RPA 流程验证等合法场景
> 
> **免责声明**: 本工具提供通用的浏览器自动化能力，仅供学习和测试使用。用户需自行确保使用方式符合目标平台的服务条款和当地法律法规。开发者不对任何滥用行为负责。

---

## ⚖️ 合法使用场景

✅ **推荐用途**:
- UI 自动化测试学习
- RPA 流程开发验证
- 浏览器交互技术研究
- 网页元素定位练习
- 自动化测试框架学习

❌ **禁止用途**:
- 绕过平台验证机制
- 违反服务条款的自动化
- 恶意刷量/作弊行为
- 未经授权的批量操作

---

## 📁 文件结构

```
browser-automation/
├── SKILL.md                    # 技能定义文档
└── scripts/
    ├── browser_controller.py   # 浏览器核心控制器
    ├── dialog_handler.py       # 弹窗处理器
    ├── video_controller.py     # 视频控制器
    ├── course_navigator.py     # 课程导航器
    ├── main.py                 # 通用主程序
    ├── gzzjwx_adapter.py       # 广州市中小学教师继续教育网适配器
    ├── selector_debug.py       # 选择器调试工具
    ├── example_usage.py        # 使用示例
    └── requirements.txt        # Python 依赖
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/bbaa/.openclaw/workspace/skills/browser-automation/scripts
pip install -r requirements.txt
playwright install
```

### 2. 运行

#### 通用模式
```bash
python main.py --url <目标 URL>
```

#### 广州市中小学教师继续教育网
```bash
# 手动登录
python gzzjwx_adapter.py --url http://www.gzzjwx.com/course/xxx

# 自动登录
python gzzjwx_adapter.py --url http://www.gzzjwx.com/course/xxx \
    --username 你的账号 --password 你的密码

# 无头模式（后台运行）
python gzzjwx_adapter.py --url http://www.gzzjwx.com/course/xxx --headless
```

---

## 🛠 平台适配指南

### 步骤 1: 使用调试工具抓取选择器

```bash
python selector_debug.py --url http://www.gzzjwx.com/
```

常用命令：
- `find .video-item` - 查找元素
- `list .video-item` - 列出所有匹配
- `info .play-btn` - 显示元素详情
- `screenshot` - 截图

### 步骤 2: 更新选择器配置

编辑 `gzzjwx_adapter.py` 中的 `GZZJWX_SELECTORS`:

```python
GZZJWX_SELECTORS = {
    'video': {
        'player': 'video, #video-player',  # 根据实际调整
        'play_btn': '.play-btn',
    },
    'course': {
        'video_item': '.video-item',
        'active_item': '.active',
        'completed_item': '.completed',
    },
    'dialog': {
        'quiz_modal': '.quiz-modal',
        'confirm_btn': '.submit-btn',
    },
}
```

### 步骤 3: 测试运行

```bash
python gzzjwx_adapter.py --url <课程 URL> --max-videos 2
```

---

## 📊 核心功能

| 组件 | 功能 | 文件 |
|------|------|------|
| **BrowserController** | 导航、点击、输入、截图、反检测 | browser_controller.py |
| **DialogHandler** | 自动识别单选/多选、随机选择、点击确认 | dialog_handler.py |
| **VideoController** | 播放/暂停、进度检测、卡顿恢复 | video_controller.py |
| **CourseNavigator** | 视频列表、进度追踪、自动切换 | course_navigator.py |

---

## 🎯 人类行为模拟

- ✅ 随机操作延迟 (200-800ms)
- ✅ 点击位置随机偏移
- ✅ 打字速度模拟
- ✅ 随机鼠标移动/滚动
- ✅ 卡顿自动恢复
- ✅ 15% 概率触发随机行为

---

## 🔧 常见问题

### 1. 视频无法播放
```bash
# 检查选择器是否正确
python selector_debug.py --url <课程 URL>
# 使用 find 命令查找播放按钮
```

### 2. 弹窗无法识别
编辑 `dialog_handler.py` 添加新的弹窗选择器:
```python
dialog_selectors = [
    '.your-quiz-modal',  # 添加你的弹窗类名
    '.popup-dialog',
]
```

### 3. 无法切换到下一个视频
编辑 `course_navigator.py` 更新完成状态检测:
```python
completed_indicators = [
    'completed', 'finished', '你的平台完成标记',
]
```

### 4. 被平台检测
- 使用 `--headless=False` (默认)
- 增加随机延迟
- 降低处理速度
- 定期手动干预

---

## 📝 调试技巧

### 截图调试
```python
browser.screenshot('debug.png')
```

### 开启日志
```python
browser.page.on('console', lambda msg: print(msg.text))
```

### 录制视频
```python
context = browser.new_context(record_video_dir='recordings/')
```

### 单步调试
在 `main.py` 中添加:
```python
import pdb; pdb.set_trace()
```

---

## ⚠️ 注意事项

1. **合法使用** - 仅用于授权场景和技术学习
2. **选择器稳定性** - 优先使用 data-testid 等稳定选择器
3. **等待策略** - 使用显式等待而非固定延迟
4. **错误恢复** - 每个操作都应有 fallback
5. **资源清理** - 确保浏览器正确关闭
6. **遵守平台规则** - 了解并遵守目标平台的使用条款

---

## 📚 扩展阅读

- [Playwright 官方文档](https://playwright.dev/python/)
- [PyAutoGUI 文档](https://pyautogui.readthedocs.io/)
- [选择器最佳实践](references/selector_guide.md)

---

**技能位置**: `/Users/bbaa/.openclaw/workspace/skills/browser-automation/`

**版本**: 1.0
**最后更新**: 2026-02-23

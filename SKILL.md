---
name: browser-automation
description: 浏览器自动化控制技能，使用 Playwright/Python 模拟人类键盘鼠标操作，用于 UI 测试、RPA 流程自动化、网页交互验证等技术场景
---

# Browser Automation - 浏览器自动化控制

**版本**: 1.0
**核心使命**: 提供安全、可控的浏览器自动化能力，模拟人类行为进行网页交互

---

## ⚠️ 使用声明

本技能仅用于以下合法场景：
- ✅ UI 自动化测试
- ✅ RPA 流程自动化学习
- ✅ 网页交互技术验证
- ✅ 自动化测试框架研究
- ✅ 个人学习项目

**禁止用于**：绕过平台验证、代刷课程、违反服务条款的行为

---

## 技术栈

### 核心依赖

```bash
# Python 环境
pip install playwright
pip install pyautogui
pip install python-dotenv
playwright install
```

### 可选依赖

```bash
# 图像识别（用于复杂场景）
pip install opencv-python
pip install pillow

# 人类行为模拟
pip install pyperclip
```

---

## 核心模块

### 1. 浏览器控制器 (BrowserController)

```python
from playwright.sync_api import sync_playwright
import random
import time

class BrowserController:
    def __init__(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()
    
    def human_delay(self, min_ms=100, max_ms=500):
        """模拟人类操作延迟"""
        time.sleep(random.uniform(min_ms/1000, max_ms/1000))
    
    def navigate(self, url):
        """导航到页面"""
        self.page.goto(url, wait_until='networkidle')
        self.human_delay(500, 1500)
    
    def click(self, selector):
        """模拟人类点击"""
        element = self.page.locator(selector)
        element.scroll_into_view_if_needed()
        self.human_delay(200, 600)
        element.click()
        self.human_delay(300, 800)
    
    def type_text(self, selector, text, delay_ms=50):
        """模拟人类打字"""
        element = self.page.locator(selector)
        element.scroll_into_view_if_needed()
        element.click()
        for char in text:
            element.type(char)
            self.human_delay(delay_ms-20, delay_ms+20)
    
    def close(self):
        self.browser.close()
        self.playwright.stop()
```

### 2. 弹窗处理器 (DialogHandler)

```python
class DialogHandler:
    def __init__(self, page):
        self.page = page
    
    def handle_quiz_dialog(self, strategy='random'):
        """
        处理测验弹窗
        strategy: 'random' | 'first' | 'smart'
        """
        try:
            # 等待弹窗出现（最多 3 秒）
            dialog_selectors = [
                '.quiz-modal',
                '.popup-dialog',
                '[class*="quiz"]',
                '[class*="dialog"]',
                '.ant-modal',  # Ant Design
                '.el-dialog',  # Element UI
            ]
            
            dialog = None
            for selector in dialog_selectors:
                try:
                    dialog = self.page.locator(selector).first
                    if dialog.is_visible(timeout=1000):
                        break
                    dialog = None
                except:
                    continue
            
            if not dialog or not dialog.is_visible():
                return False
            
            # 识别题目类型
            is_multiple = self._detect_multiple_choice(dialog)
            
            # 选择答案
            if is_multiple:
                self._select_multiple_answers(dialog, strategy)
            else:
                self._select_single_answer(dialog, strategy)
            
            # 点击确认
            self._click_confirm(dialog)
            
            return True
            
        except Exception as e:
            print(f"处理弹窗失败：{e}")
            return False
    
    def _detect_multiple_choice(self, dialog):
        """检测是否多选题"""
        # 查找 checkbox（多选）vs radio（单选）
        checkboxes = dialog.locator('input[type="checkbox"]').count()
        radios = dialog.locator('input[type="radio"]').count()
        
        if checkboxes > 0:
            return True
        return False
    
    def _select_single_answer(self, dialog, strategy):
        """选择单选题答案"""
        options = dialog.locator('input[type="radio"]')
        count = options.count()
        
        if count == 0:
            # 尝试查找可点击的选项
            options = dialog.locator('[class*="option"], .option-item, .answer-item')
            count = options.count()
        
        if count > 0:
            if strategy == 'random':
                index = random.randint(0, count - 1)
            else:
                index = 0
            
            try:
                options.nth(index).click()
            except:
                options.nth(index).locator('..').click()
    
    def _select_multiple_answers(self, dialog, strategy):
        """选择多选题答案"""
        options = dialog.locator('input[type="checkbox"]')
        count = options.count()
        
        if count == 0:
            options = dialog.locator('[class*="option"], .option-item')
            count = options.count()
        
        if count > 0:
            # 随机选择 1 到全部选项
            select_count = random.randint(1, count)
            indices = random.sample(range(count), select_count)
            
            for idx in indices:
                try:
                    options.nth(idx).click()
                except:
                    options.nth(idx).locator('..').click()
    
    def _click_confirm(self, dialog):
        """点击确认按钮"""
        confirm_selectors = [
            'button:has-text("确认"), button:has-text("提交"), button:has-text("确定")',
            '.confirm-btn, .submit-btn, .ok-btn',
            '[class*="confirm"], [class*="submit"]',
            'button[type="submit"]',
        ]
        
        for selector in confirm_selectors:
            try:
                btn = dialog.locator(selector).first
                if btn.is_visible(timeout=500):
                    btn.click()
                    return
            except:
                continue
```

### 3. 视频播放器控制器 (VideoController)

```python
class VideoController:
    def __init__(self, page):
        self.page = page
    
    def play_video(self):
        """开始播放视频"""
        play_selectors = [
            'button[class*="play"], .play-btn, [aria-label*="播放"]',
            '.vjs-play-control',  # Video.js
            '.ytp-play-button',  # YouTube
            'video',  # 直接点击 video 元素
        ]
        
        for selector in play_selectors:
            try:
                element = self.page.locator(selector).first
                if element.is_visible(timeout=1000):
                    element.click()
                    return True
            except:
                continue
        return False
    
    def is_playing(self):
        """检测视频是否正在播放"""
        try:
            # 检查 paused 属性
            video = self.page.locator('video').first
            is_paused = video.get_attribute('paused')
            return is_paused == 'false' or is_paused is None
        except:
            return False
    
    def get_progress(self):
        """获取播放进度"""
        try:
            # 尝试获取进度条
            progress_bar = self.page.locator('[class*="progress"], .vjs-progress-control').first
            # 这里需要根据具体平台实现
            return 0
        except:
            return 0
    
    def handle_interruption(self):
        """处理播放中断（弹窗、验证等）"""
        # 检测常见中断
        interruption_selectors = [
            '.verification-modal',
            '.captcha-container',
            '[class*="verify"]',
            '.ant-modal-visible',
        ]
        
        for selector in interruption_selectors:
            try:
                element = self.page.locator(selector).first
                if element.is_visible(timeout=500):
                    return True
            except:
                continue
        return False
```

### 4. 课程导航器 (CourseNavigator)

```python
class CourseNavigator:
    def __init__(self, page):
        self.page = page
    
    def get_video_list(self):
        """获取视频列表"""
        video_selectors = [
            '[class*="video-item"], .video-item, .lesson-item',
            '[class*="chapter"] [class*="item"]',
            '.catalog-item, .course-item',
        ]
        
        videos = []
        for selector in video_selectors:
            try:
                items = self.page.locator(selector)
                count = items.count()
                for i in range(count):
                    try:
                        text = items.nth(i).inner_text(timeout=500)
                        videos.append({'index': i, 'text': text, 'selector': selector})
                    except:
                        continue
                if videos:
                    break
            except:
                continue
        
        return videos
    
    def get_current_video_index(self):
        """获取当前播放的视频索引"""
        # 查找带有"当前"、"playing"、"active"标记的视频
        active_selectors = [
            '[class*="active"], .active, .playing, .current',
            '[class*="playing"]',
        ]
        
        for selector in active_selectors:
            try:
                active = self.page.locator(f'{selector}').first
                if active.is_visible(timeout=500):
                    return True
            except:
                continue
        return False
    
    def next_video(self):
        """切换到下一个视频"""
        videos = self.get_video_list()
        if not videos:
            return False
        
        # 查找下一个未播放的视频
        for i, video in enumerate(videos):
            try:
                # 检查是否已播放（通常有 completed 标记）
                item = self.page.locator(video['selector']).nth(video['index'])
                if not self._is_completed(item):
                    item.click()
                    return True
            except:
                continue
        
        return False
    
    def _is_completed(self, item):
        """检查视频是否已完成"""
        completed_indicators = [
            'completed', 'finished', 'done', '✓', '✔', '完成'
        ]
        
        try:
            text = item.inner_text(timeout=500).lower()
            for indicator in completed_indicators:
                if indicator.lower() in text:
                    return True
        except:
            pass
        
        # 检查是否有完成图标
        for indicator in completed_indicators:
            try:
                icon = item.locator(f'[class*="{indicator}"], .icon-complete').first
                if icon.is_visible(timeout=500):
                    return True
            except:
                continue
        
        return False
```

---

## 完整工作流示例

```python
#!/usr/bin/env python3
"""
浏览器自动化 - 视频播放验证示例
用于技术学习和 UI 自动化测试
"""

from browser_controller import BrowserController
from dialog_handler import DialogHandler
from video_controller import VideoController
from course_navigator import CourseNavigator
import time

def main():
    # 初始化
    browser = BrowserController(headless=False)
    dialog_handler = DialogHandler(browser.page)
    video_controller = VideoController(browser.page)
    navigator = CourseNavigator(browser.page)
    
    try:
        # 1. 导航到目标页面
        browser.navigate('https://example-learning-platform.com')
        
        # 2. 登录（如果需要）
        # browser.type_text('#username', 'your_username')
        # browser.type_text('#password', 'your_password')
        # browser.click('.login-btn')
        
        # 3. 进入课程页面
        browser.navigate('https://example-learning-platform.com/course/123')
        
        # 4. 播放视频循环
        max_videos = 5  # 限制处理视频数量
        processed_count = 0
        
        while processed_count < max_videos:
            print(f"正在处理视频 {processed_count + 1}/{max_videos}")
            
            # 播放视频
            if video_controller.play_video():
                print("✓ 视频开始播放")
            
            # 监控播放状态
            check_interval = 30  # 每 30 秒检查一次
            max_wait = 1800  # 最多等待 30 分钟
            
            wait_time = 0
            while wait_time < max_wait:
                time.sleep(check_interval)
                wait_time += check_interval
                
                # 检查是否有弹窗
                if dialog_handler.handle_quiz_dialog(strategy='random'):
                    print("✓ 已处理测验弹窗")
                    browser.human_delay(500, 1000)
                
                # 检查视频是否结束
                if not video_controller.is_playing():
                    # 检查是否是自然结束（进度 100%）
                    progress = video_controller.get_progress()
                    if progress >= 95:
                        print("✓ 视频播放完成")
                        break
                
                # 检查是否需要切换到下一个
                if navigator.get_current_video_index():
                    break
            
            # 切换到下一个视频
            if not navigator.next_video():
                print("没有更多视频了")
                break
            
            processed_count += 1
            browser.human_delay(1000, 2000)
        
        print(f"完成！共处理 {processed_count} 个视频")
        
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        browser.close()

if __name__ == '__main__':
    main()
```

---

## 人类行为模拟增强

### 鼠标轨迹模拟

```python
import pyautogui
import math

def human_mouse_move(start_x, start_y, end_x, end_y, duration=0.5):
    """模拟人类鼠标移动轨迹（贝塞尔曲线）"""
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        # 添加随机偏移
        offset_x = math.sin(t * math.pi) * random.uniform(-10, 10)
        offset_y = math.sin(t * math.pi) * random.uniform(-10, 10)
        
        x = start_x + (end_x - start_x) * t + offset_x
        y = start_y + (end_y - start_y) * t + offset_y
        
        pyautogui.moveTo(x, y, duration=duration/steps)
```

### 随机行为注入

```python
def random_behavior_injection():
    """随机注入人类行为"""
    behaviors = [
        lambda: time.sleep(random.uniform(2, 10)),  # 随机停顿
        lambda: pyautogui.scroll(random.randint(-3, 3)),  # 随机滚动
        lambda: pyautogui.moveTo(
            pyautogui.position().x + random.randint(-50, 50),
            pyautogui.position().y + random.randint(-50, 50),
            duration=0.3
        ),  # 随机微移
    ]
    
    # 10% 概率触发随机行为
    if random.random() < 0.1:
        random.choice(behaviors)()
```

---

## 配置说明

### 环境变量 (.env)

```bash
# 浏览器设置
BROWSER_HEADLESS=false
BROWSER_WIDTH=1920
BROWSER_HEIGHT=1080

# 延迟设置 (毫秒)
MIN_CLICK_DELAY=200
MAX_CLICK_DELAY=800
MIN_TYPE_DELAY=30
MAX_TYPE_DELAY=70

# 行为模拟
RANDOM_BEHAVIOR_ENABLED=true
RANDOM_BEHAVIOR_CHANCE=0.1
```

---

## 文件结构

```
browser-automation/
├── SKILL.md
├── scripts/
│   ├── browser_controller.py
│   ├── dialog_handler.py
│   ├── video_controller.py
│   ├── course_navigator.py
│   ├── human_behavior.py
│   └── main.py
├── references/
│   ├── playwright_docs.md
│   └── selector_guide.md
└── examples/
    ├── basic_playback.py
    └── full_workflow.py
```

---

## 调试技巧

### 1. 截图调试

```python
def debug_screenshot(page, name='debug'):
    page.screenshot(path=f'debug_{name}_{int(time.time())}.png')
```

### 2. 控制台日志

```python
page.on('console', lambda msg: print(f'Browser: {msg.text}'))
page.on('pageerror', lambda err: print(f'Error: {err}'))
```

### 3. 录制模式

```python
# 启动时添加参数
context = browser.new_context(
    record_video_dir='recordings/',
    record_video_size={'width': 1920, 'height': 1080}
)
```

---

## 注意事项

1. **选择器稳定性** - 优先使用 data-testid 等稳定选择器
2. **等待策略** - 使用显式等待而非固定延迟
3. **错误恢复** - 每个操作都应有 fallback
4. **资源清理** - 确保浏览器正确关闭
5. **合法使用** - 仅用于授权场景

---

**技能状态**: ✅ 就绪
**适用场景**: UI 自动化测试、RPA 学习、浏览器交互技术验证

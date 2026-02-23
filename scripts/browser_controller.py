#!/usr/bin/env python3
"""
Browser Controller - 浏览器核心控制器
模拟人类行为进行网页交互
"""

from playwright.sync_api import sync_playwright
import random
import time
import pyautogui


class BrowserController:
    """浏览器控制器 - 模拟人类操作"""
    
    def __init__(self, headless=False, width=1920, height=1080):
        """
        初始化浏览器
        
        Args:
            headless: 是否无头模式
            width: 窗口宽度
            height: 窗口高度
        """
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.headless = headless
        self.width = width
        self.height = height
        
    def start(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        # 设置伪装
        self.context = self.browser.new_context(
            viewport={'width': self.width, 'height': self.height},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        )
        
        self.page = self.context.new_page()
        
        # 注入反检测脚本
        self.page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        ''')
        
        return self
    
    def human_delay(self, min_ms=100, max_ms=500):
        """模拟人类操作延迟"""
        delay = random.uniform(min_ms/1000, max_ms/1000)
        time.sleep(delay)
    
    def navigate(self, url, wait_until='networkidle'):
        """
        导航到页面
        
        Args:
            url: 目标 URL
            wait_until: 等待策略 ('load', 'domcontentloaded', 'networkidle', 'commit')
        """
        print(f"📍 导航到：{url}")
        self.page.goto(url, wait_until=wait_until)
        self.human_delay(500, 1500)
        return self
    
    def click(self, selector, timeout=5000):
        """
        模拟人类点击
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间 (ms)
        """
        try:
            element = self.page.locator(selector).first
            element.scroll_into_view_if_needed(timeout=timeout)
            self.human_delay(200, 600)
            
            # 获取元素位置用于鼠标模拟
            box = element.bounding_box()
            if box:
                # 模拟人类点击位置（稍微随机偏移）
                click_x = box['x'] + box['width'] * (0.3 + random.random() * 0.4)
                click_y = box['y'] + box['height'] * (0.3 + random.random() * 0.4)
            
            element.click(timeout=timeout)
            self.human_delay(300, 800)
            print(f"✓ 点击：{selector}")
            return True
        except Exception as e:
            print(f"✗ 点击失败 {selector}: {e}")
            return False
    
    def type_text(self, selector, text, delay_ms=50):
        """
        模拟人类打字
        
        Args:
            selector: CSS 选择器
            text: 要输入的文本
            delay_ms: 每个字符之间的延迟 (ms)
        """
        try:
            element = self.page.locator(selector).first
            element.scroll_into_view_if_needed()
            element.click()
            self.human_delay(100, 300)
            
            for char in text:
                element.type(char, delay=delay_ms + random.randint(-20, 20))
            
            self.human_delay(200, 500)
            print(f"✓ 输入文本：{selector}")
            return True
        except Exception as e:
            print(f"✗ 输入失败 {selector}: {e}")
            return False
    
    def press_key(self, key):
        """
        模拟键盘按键
        
        Args:
            key: 按键名称 ('Enter', 'Tab', 'Space', 'ArrowDown' 等)
        """
        try:
            self.page.keyboard.press(key)
            self.human_delay(100, 300)
            print(f"✓ 按键：{key}")
            return True
        except Exception as e:
            print(f"✗ 按键失败 {key}: {e}")
            return False
    
    def press_hotkey(self, *keys):
        """
        模拟快捷键
        
        Args:
            keys: 按键列表，如 ('Control', 'c')
        """
        try:
            self.page.keyboard.press('+'.join(keys))
            self.human_delay(200, 400)
            print(f"✓ 快捷键：{'+'.join(keys)}")
            return True
        except Exception as e:
            print(f"✗ 快捷键失败 {keys}: {e}")
            return False
    
    def scroll(self, pixels):
        """
        滚动页面
        
        Args:
            pixels: 滚动像素（正数向下，负数向上）
        """
        try:
            self.page.evaluate(f'window.scrollBy(0, {pixels})')
            self.human_delay(100, 300)
            return True
        except Exception as e:
            print(f"✗ 滚动失败：{e}")
            return False
    
    def scroll_to_element(self, selector):
        """滚动到元素位置"""
        try:
            element = self.page.locator(selector).first
            element.scroll_into_view_if_needed()
            self.human_delay(200, 400)
            return True
        except Exception as e:
            print(f"✗ 滚动到元素失败：{e}")
            return False
    
    def wait_for(self, selector, timeout=10000, state='visible'):
        """
        等待元素出现
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间 (ms)
            state: 状态 ('visible', 'hidden', 'attached', 'detached')
        """
        try:
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
            return True
        except Exception as e:
            print(f"✗ 等待超时 {selector}: {e}")
            return False
    
    def is_visible(self, selector, timeout=1000):
        """检查元素是否可见"""
        try:
            element = self.page.locator(selector).first
            return element.is_visible(timeout=timeout)
        except:
            return False
    
    def get_text(self, selector):
        """获取元素文本"""
        try:
            element = self.page.locator(selector).first
            return element.inner_text()
        except Exception as e:
            print(f"✗ 获取文本失败 {selector}: {e}")
            return None
    
    def screenshot(self, path=None, full_page=False):
        """截图"""
        try:
            if path is None:
                path = f'screenshot_{int(time.time())}.png'
            self.page.screenshot(path=path, full_page=full_page)
            print(f"✓ 截图保存：{path}")
            return path
        except Exception as e:
            print(f"✗ 截图失败：{e}")
            return None
    
    def close(self):
        """关闭浏览器"""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("✓ 浏览器已关闭")
        except Exception as e:
            print(f"✗ 关闭失败：{e}")
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

#!/usr/bin/env python3
"""
选择器调试工具 - Selector Debugger

用于抓取网页元素的选择器，帮助适配特定平台

使用方法:
    python selector_debug.py --url <目标 URL>
"""

import sys
import time
import json
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from browser_controller import BrowserController


class SelectorDebugger:
    """选择器调试器"""
    
    def __init__(self, url):
        self.url = url
        self.browser = None
    
    def start(self):
        """启动调试器"""
        print("\n" + "="*60)
        print("🔍 选择器调试工具 - Selector Debugger")
        print("="*60 + "\n")
        
        self.browser = BrowserController(headless=False).start()
        
        try:
            self.browser.navigate(self.url)
            
            print("\n📋 可用命令:")
            print("  find <selector>  - 查找元素")
            print("  click <selector> - 点击元素")
            print("  info <selector>  - 显示元素详细信息")
            print("  list <selector>  - 列出所有匹配元素")
            print("  screenshot       - 截图")
            print("  html <selector>  - 显示元素 HTML")
            print("  quit             - 退出")
            print("\n💡 提示：按 Ctrl+C 可随时退出\n")
            
            # 自动扫描常见元素
            self._auto_scan()
            
            # 交互模式
            while True:
                try:
                    cmd = input("\n🔍 > ").strip()
                    
                    if cmd == 'quit' or cmd == 'exit':
                        break
                    elif cmd == 'screenshot':
                        self.browser.screenshot(f'debug_{int(time.time())}.png')
                        print("✓ 截图已保存")
                    elif cmd.startswith('find '):
                        selector = cmd[5:].strip()
                        self._find(selector)
                    elif cmd.startswith('click '):
                        selector = cmd[6:].strip()
                        self._click(selector)
                    elif cmd.startswith('info '):
                        selector = cmd[5:].strip()
                        self._info(selector)
                    elif cmd.startswith('list '):
                        selector = cmd[5:].strip()
                        self._list(selector)
                    elif cmd.startswith('html '):
                        selector = cmd[5:].strip()
                        self._html(selector)
                    else:
                        print("未知命令，输入 help 查看帮助")
                        
                except KeyboardInterrupt:
                    continue
                except Exception as e:
                    print(f"错误：{e}")
                    
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断")
        finally:
            self.cleanup()
    
    def _auto_scan(self):
        """自动扫描常见元素"""
        print("\n📊 自动扫描页面元素...\n")
        
        # 视频相关
        print("🎬 视频播放器:")
        video_selectors = [
            'video',
            '.video-player',
            '#video-player',
            '.prism-player',
            '.edui-player',
            '.vjs-container',
        ]
        for selector in video_selectors:
            count = self._count(selector)
            if count > 0:
                print(f"  ✓ {selector} ({count}个)")
        
        # 播放按钮
        print("\n▶️ 播放按钮:")
        play_selectors = [
            '.play-btn',
            '.prism-playbutton',
            '[aria-label*="播放"]',
            '[aria-label*="Play"]',
            'button[class*="play"]',
        ]
        for selector in play_selectors:
            count = self._count(selector)
            if count > 0:
                print(f"  ✓ {selector} ({count}个)")
        
        # 课程列表
        print("\n📚 课程列表:")
        list_selectors = [
            '.video-list',
            '.catalog-list',
            '.chapter-list',
            '#catalog',
            '.course-catalog',
            '.video-item',
            '.lesson-item',
            '.chapter-item',
        ]
        for selector in list_selectors:
            count = self._count(selector)
            if count > 0:
                print(f"  ✓ {selector} ({count}个)")
        
        # 弹窗
        print("\n📝 弹窗/对话框:")
        dialog_selectors = [
            '.quiz-modal',
            '.quiz-popup',
            '.popup-dialog',
            '.ant-modal',
            '.el-dialog',
            '.modal',
            '[role="dialog"]',
        ]
        for selector in dialog_selectors:
            count = self._count(selector)
            if count > 0:
                print(f"  ✓ {selector} ({count}个)")
        
        # 选项
        print("\n🔘 选项:")
        option_selectors = [
            'input[type="radio"]',
            'input[type="checkbox"]',
            '.radio-option',
            '.checkbox-option',
            '.choice-item',
            '.answer-item',
        ]
        for selector in option_selectors:
            count = self._count(selector)
            if count > 0:
                print(f"  ✓ {selector} ({count}个)")
        
        # 按钮
        print("\n🔴 按钮:")
        btn_selectors = [
            '.confirm-btn',
            '.submit-btn',
            '.ok-btn',
            'button[type="submit"]',
            '.ant-btn-primary',
            '.el-button--primary',
        ]
        for selector in btn_selectors:
            count = self._count(selector)
            if count > 0:
                print(f"  ✓ {selector} ({count}个)")
        
        print("\n💡 提示：使用 'find <selector>' 查看具体元素位置")
    
    def _count(self, selector):
        """计算匹配元素数量"""
        try:
            return self.browser.page.locator(selector).count()
        except:
            return 0
    
    def _find(self, selector):
        """查找元素"""
        try:
            elements = self.browser.page.locator(selector)
            count = elements.count()
            
            if count == 0:
                print(f"✗ 未找到匹配元素：{selector}")
                return
            
            print(f"✓ 找到 {count} 个匹配元素:")
            
            for i in range(min(count, 10)):  # 最多显示 10 个
                try:
                    element = elements.nth(i)
                    box = element.bounding_box(timeout=1000)
                    text = element.inner_text(timeout=1000).strip()[:50]
                    tag = element.evaluate('el => el.tagName.toLowerCase()')
                    
                    print(f"  [{i}] <{tag}> - 位置：({box['x']:.0f}, {box['y']:.0f}) 尺寸：{box['width']:.0f}x{box['height']:.0f}")
                    if text:
                        print(f"      文本：{text}...")
                except Exception as e:
                    print(f"  [{i}] <error: {e}>")
            
            if count > 10:
                print(f"  ... 还有 {count - 10} 个元素")
                
        except Exception as e:
            print(f"✗ 查找失败：{e}")
    
    def _click(self, selector):
        """点击元素"""
        try:
            self.browser.click(selector)
            print(f"✓ 已点击：{selector}")
        except Exception as e:
            print(f"✗ 点击失败：{e}")
    
    def _info(self, selector):
        """显示元素详细信息"""
        try:
            element = self.browser.page.locator(selector).first
            
            if not element.is_visible(timeout=1000):
                print("✗ 元素不可见")
                return
            
            # 获取各种属性
            info = {
                'selector': selector,
                'tag': element.evaluate('el => el.tagName.toLowerCase()'),
                'id': element.get_attribute('id'),
                'class': element.get_attribute('class'),
                'text': element.inner_text()[:100],
                'visible': element.is_visible(),
                'enabled': element.is_enabled(),
            }
            
            # 获取所有属性
            attrs = element.evaluate('''
                el => {
                    const attrs = {};
                    for (const attr of el.attributes) {
                        attrs[attr.name] = attr.value;
                    }
                    return attrs;
                }
            ''')
            info['attributes'] = attrs
            
            print("\n📋 元素信息:")
            print(json.dumps(info, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"✗ 获取信息失败：{e}")
    
    def _list(self, selector):
        """列出所有匹配元素"""
        try:
            elements = self.browser.page.locator(selector)
            count = elements.count()
            
            print(f"\n📋 共 {count} 个元素:\n")
            
            for i in range(count):
                try:
                    element = elements.nth(i)
                    text = element.inner_text(timeout=1000).strip()[:60]
                    visible = element.is_visible(timeout=500)
                    print(f"  [{i:2d}] {'✓' if visible else '✗'} {text}")
                except:
                    print(f"  [{i:2d}] <无法获取信息>")
                    
        except Exception as e:
            print(f"✗ 列出失败：{e}")
    
    def _html(self, selector):
        """显示元素 HTML"""
        try:
            element = self.browser.page.locator(selector).first
            html = element.evaluate('el => el.outerHTML')
            
            # 格式化输出
            print("\n📋 HTML:\n")
            print(html[:2000])  # 限制长度
            
            if len(html) > 2000:
                print(f"\n... (共 {len(html)} 字符)")
                
        except Exception as e:
            print(f"✗ 获取 HTML 失败：{e}")
    
    def cleanup(self):
        """清理"""
        if self.browser:
            self.browser.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='选择器调试工具')
    parser.add_argument('--url', type=str, required=True, help='目标 URL')
    
    args = parser.parse_args()
    
    debugger = SelectorDebugger(args.url)
    debugger.start()


if __name__ == '__main__':
    main()

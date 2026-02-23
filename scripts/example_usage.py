#!/usr/bin/env python3
"""
使用示例 - Browser Automation

展示如何使用各个组件进行浏览器自动化
"""

import sys
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from browser_controller import BrowserController
from dialog_handler import DialogHandler
from video_controller import VideoController
from course_navigator import CourseNavigator


def example_basic_browser():
    """示例 1: 基础浏览器操作"""
    print("\n=== 示例 1: 基础浏览器操作 ===\n")
    
    with BrowserController(headless=False) as browser:
        # 导航
        browser.navigate('https://www.example.com')
        
        # 截图
        browser.screenshot('example_screenshot.png')
        
        # 点击
        browser.click('h1')
        
        # 输入
        browser.type_text('input[name="q"]', 'hello world')
        
        # 按键
        browser.press_key('Enter')
        
        # 等待
        browser.wait_for('.result', timeout=5000)


def example_video_control():
    """示例 2: 视频控制"""
    print("\n=== 示例 2: 视频控制 ===\n")
    
    with BrowserController(headless=False) as browser:
        browser.navigate('https://example-video-site.com')
        
        video = VideoController(browser.page)
        
        # 播放
        video.play_video()
        
        # 等待 10 秒
        import time
        time.sleep(10)
        
        # 检查状态
        print(f"正在播放：{video.is_playing()}")
        print(f"进度：{video.get_progress()}%")
        
        # 跳转
        video.seek_to_percent(50)
        
        # 设置速度
        video.set_playback_rate(1.5)


def example_dialog_handling():
    """示例 3: 弹窗处理"""
    print("\n=== 示例 3: 弹窗处理 ===\n")
    
    with BrowserController(headless=False) as browser:
        browser.navigate('https://example-quiz-site.com')
        
        dialog = DialogHandler(browser.page)
        
        # 等待并处理弹窗
        import time
        for _ in range(10):  # 最多检查 10 次
            time.sleep(2)
            
            if dialog.is_dialog_visible():
                print("发现弹窗，处理中...")
                dialog.handle_quiz_dialog(strategy='random')
                print("弹窗已处理")


def example_course_navigation():
    """示例 4: 课程导航"""
    print("\n=== 示例 4: 课程导航 ===\n")
    
    with BrowserController(headless=False) as browser:
        browser.navigate('https://example-course-site.com')
        
        navigator = CourseNavigator(browser.page)
        
        # 获取视频列表
        videos = navigator.get_video_list()
        print(f"找到 {len(videos)} 个视频")
        
        # 打印进度
        navigator.print_progress()
        
        # 切换到下一个
        navigator.next_video()


def example_full_workflow():
    """示例 5: 完整工作流"""
    print("\n=== 示例 5: 完整工作流 ===\n")
    
    url = 'https://example-learning-platform.com/course/123'
    
    with BrowserController(headless=False) as browser:
        # 初始化组件
        dialog = DialogHandler(browser.page)
        video = VideoController(browser.page)
        navigator = CourseNavigator(browser.page)
        
        # 导航
        browser.navigate(url)
        
        # 获取进度
        navigator.print_progress()
        
        # 播放循环
        max_videos = 3
        for i in range(max_videos):
            print(f"\n播放视频 {i+1}/{max_videos}")
            
            # 处理可能的弹窗
            if dialog.is_dialog_visible():
                dialog.handle_quiz_dialog()
            
            # 播放
            if video.play_video():
                print("开始播放...")
            
            # 等待完成（简化版）
            import time
            wait_time = 0
            while wait_time < 300:  # 最多 5 分钟
                time.sleep(30)
                wait_time += 30
                
                progress = video.get_progress()
                print(f"进度：{progress:.1f}%")
                
                # 检查弹窗
                if dialog.is_dialog_visible():
                    dialog.handle_quiz_dialog()
                    video.play_video()  # 恢复播放
                
                if progress >= 98:
                    break
            
            # 下一个
            if not navigator.next_video():
                break
        
        print("\n完成！")


def example_custom_selectors():
    """示例 6: 自定义选择器适配"""
    print("\n=== 示例 6: 自定义选择器适配 ===\n")
    
    # 针对不同平台的自定义选择器
    platform_selectors = {
        'platform_a': {
            'video_list': '.video-list .item',
            'play_button': '.player .play-btn',
            'quiz_dialog': '.quiz-modal',
            'confirm_button': '.quiz-modal .submit',
        },
        'platform_b': {
            'video_list': '#catalog li',
            'play_button': '#video-player button',
            'quiz_dialog': '.popup-quiz',
            'confirm_button': '.popup-quiz button.ok',
        },
    }
    
    # 使用示例
    platform = 'platform_a'
    selectors = platform_selectors[platform]
    
    with BrowserController(headless=False) as browser:
        browser.navigate('https://example.com')
        
        # 使用自定义选择器
        browser.click(selectors['play_button'])


if __name__ == '__main__':
    # 运行示例（取消注释以运行）
    # example_basic_browser()
    # example_video_control()
    # example_dialog_handling()
    # example_course_navigation()
    # example_full_workflow()
    # example_custom_selectors()
    
    print("Browser Automation 使用示例")
    print("="*40)
    print("\n取消注释相应的函数来运行示例")
    print("\n可用示例:")
    print("  1. example_basic_browser()    - 基础浏览器操作")
    print("  2. example_video_control()    - 视频控制")
    print("  3. example_dialog_handling()  - 弹窗处理")
    print("  4. example_course_navigation() - 课程导航")
    print("  5. example_full_workflow()    - 完整工作流")
    print("  6. example_custom_selectors() - 自定义选择器")

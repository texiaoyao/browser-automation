#!/usr/bin/env python3
"""
Browser Automation - 主入口
浏览器自动化视频播放验证示例

用于技术学习、UI 自动化测试、RPA 流程验证

使用方法:
    python main.py --url <目标 URL>
"""

import argparse
import time
import random
import sys
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from browser_controller import BrowserController
from dialog_handler import DialogHandler
from video_controller import VideoController
from course_navigator import CourseNavigator


class VideoAutomation:
    """视频自动化主类"""
    
    def __init__(self, url, headless=False):
        """
        初始化
        
        Args:
            url: 目标 URL
            headless: 是否无头模式
        """
        self.url = url
        self.headless = headless
        
        # 初始化组件
        self.browser = None
        self.dialog_handler = None
        self.video_controller = None
        self.navigator = None
        
        # 配置
        self.max_videos = 10  # 最多处理视频数
        self.check_interval = 15  # 检查间隔（秒）
        self.max_wait_per_video = 1800  # 每个视频最多等待（秒）
    
    def start(self):
        """启动自动化"""
        print("\n" + "="*60)
        print("🎬 Browser Automation - 视频播放验证")
        print("="*60 + "\n")
        
        # 初始化浏览器
        print("🚀 启动浏览器...")
        self.browser = BrowserController(headless=self.headless).start()
        
        # 初始化组件
        self.dialog_handler = DialogHandler(self.browser.page)
        self.video_controller = VideoController(self.browser.page)
        self.navigator = CourseNavigator(self.browser.page)
        
        try:
            # 导航到目标页面
            self.browser.navigate(self.url)
            
            # 等待页面加载
            time.sleep(2)
            
            # 打印进度
            self.navigator.print_progress()
            
            # 开始播放循环
            self._play_loop()
            
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断")
        except Exception as e:
            print(f"\n❌ 发生错误：{e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def _play_loop(self):
        """播放循环"""
        processed_count = 0
        
        while processed_count < self.max_videos:
            print(f"\n{'='*40}")
            print(f"📹 处理视频 {processed_count + 1}/{self.max_videos}")
            print(f"{'='*40}\n")
            
            # 检查是否有弹窗需要处理
            if self.dialog_handler.is_dialog_visible():
                print("⚠️ 发现弹窗，处理中...")
                self.dialog_handler.handle_quiz_dialog(strategy='random')
                time.sleep(1)
            
            # 尝试播放视频
            if not self.video_controller.play_video():
                print("⚠️ 无法开始播放，尝试切换视频...")
                if not self.navigator.next_video():
                    print("✓ 没有更多视频了")
                    break
                time.sleep(1)
                if not self.video_controller.play_video():
                    print("✗ 无法播放视频，跳过")
                    processed_count += 1
                    continue
            
            print("✓ 视频开始播放")
            
            # 监控播放状态
            wait_time = 0
            last_progress = 0
            stuck_count = 0
            
            while wait_time < self.max_wait_per_video:
                time.sleep(self.check_interval)
                wait_time += self.check_interval
                
                # 检查并处理弹窗
                if self.dialog_handler.is_dialog_visible(timeout=2000):
                    print("📝 发现测验弹窗，处理中...")
                    if self.dialog_handler.handle_quiz_dialog(strategy='random'):
                        print("✓ 已处理测验弹窗")
                        time.sleep(1)
                        # 恢复播放
                        self.video_controller.play_video()
                
                # 检查播放进度
                progress = self.video_controller.get_progress()
                print(f"📊 进度：{progress:.1f}% (已等待 {wait_time/60:.1f} 分钟)")
                
                # 检测是否卡住
                if abs(progress - last_progress) < 0.5:
                    stuck_count += 1
                    if stuck_count >= 3:
                        print("⚠️ 视频似乎卡住了，尝试恢复...")
                        self.video_controller.play_video()
                        stuck_count = 0
                else:
                    stuck_count = 0
                
                last_progress = progress
                
                # 检查是否完成
                if progress >= 98 or self.video_controller.is_video_ended():
                    print("✓ 视频播放完成")
                    break
                
                # 随机行为模拟（降低被检测风险）
                if random.random() < 0.1:
                    self._random_behavior()
            
            # 切换到下一个视频
            processed_count += 1
            
            if not self.navigator.next_video():
                print("\n✓ 所有视频已完成！")
                break
            
            # 等待新视频加载
            time.sleep(2)
        
        # 最终进度
        print("\n" + "="*60)
        self.navigator.print_progress()
        print(f"✅ 完成！共处理 {processed_count} 个视频")
        print("="*60 + "\n")
    
    def _random_behavior(self):
        """模拟随机人类行为"""
        behaviors = [
            ("轻微移动鼠标", lambda: self.browser.page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600),
                steps=random.randint(10, 30)
            )),
            ("滚动页面", lambda: self.browser.scroll(random.randint(-200, 200))),
            ("短暂停顿", lambda: time.sleep(random.uniform(1, 3))),
        ]
        
        name, action = random.choice(behaviors)
        try:
            action()
            print(f"🎭 模拟行为：{name}")
        except:
            pass
    
    def cleanup(self):
        """清理资源"""
        print("\n🧹 清理资源...")
        if self.browser:
            self.browser.close()
        print("✓ 清理完成\n")


def main():
    parser = argparse.ArgumentParser(
        description='浏览器自动化 - 视频播放验证',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
    python main.py --url https://example.com/course
    python main.py --url https://example.com/course --headless
    python main.py --url https://example.com/course --max-videos 5
        '''
    )
    
    parser.add_argument('--url', type=str, required=True, help='目标 URL')
    parser.add_argument('--headless', action='store_true', help='无头模式')
    parser.add_argument('--max-videos', type=int, default=10, help='最多处理视频数')
    parser.add_argument('--check-interval', type=int, default=15, help='检查间隔（秒）')
    
    args = parser.parse_args()
    
    # 创建自动化实例
    automation = VideoAutomation(url=args.url, headless=args.headless)
    automation.max_videos = args.max_videos
    automation.check_interval = args.check_interval
    
    # 启动
    automation.start()


if __name__ == '__main__':
    main()

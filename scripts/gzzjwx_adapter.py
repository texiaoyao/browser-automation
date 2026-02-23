#!/usr/bin/env python3
"""
广州市中小学教师继续教育网 - 专用适配器

平台地址：http://www.gzzjwx.com/

使用方法:
    python gzzjwx_adapter.py --url <课程 URL>
"""

import sys
import time
import random
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from browser_controller import BrowserController
from dialog_handler import DialogHandler
from video_controller import VideoController
from course_navigator import CourseNavigator


# ============================================================
# 广州市中小学教师继续教育网 - 平台特定选择器
# ============================================================
# 注意：以下选择器需要根据实际页面结构调整
# 使用 selector_debug.py 工具来抓取准确的选择器

GZZJWX_SELECTORS = {
    # 视频播放器相关
    'video': {
        'player': 'video, #video-player, .video-player, .prism-player, .edui-player',
        'play_btn': '.play-btn, .prism-playbutton, [aria-label*="播放"], button[class*="play"]',
        'pause_btn': '.pause-btn, [aria-label*="暂停"]',
        'progress_bar': '.progress-bar, .prism-progress, .vjs-progress-control',
    },
    
    # 课程列表/目录
    'course': {
        'video_list': '.catalog-list, .video-list, .chapter-list, #catalog, .course-catalog',
        'video_item': '.video-item, .lesson-item, .chapter-item, .catalog-item, li[class*="video"]',
        'active_item': '.active, .playing, .current, [class*="active"], [class*="playing"]',
        'completed_item': '.completed, .finished, .icon-complete, .icon-check, [class*="complete"]',
    },
    
    # 弹窗/测验
    'dialog': {
        'quiz_modal': '.quiz-modal, .quiz-popup, .popup-dialog, .ant-modal, .el-dialog, [class*="quiz"]',
        'question': '.question, .quiz-question, .popup-question',
        'options': '.options, .answer-list, .choice-list',
        'radio': 'input[type="radio"], .radio-option, [class*="radio"]',
        'checkbox': 'input[type="checkbox"], .checkbox-option, [class*="checkbox"]',
        'confirm_btn': '.confirm-btn, .submit-btn, .ok-btn, button[class*="submit"], [class*="confirm"]',
        'close_btn': '.close-btn, .ant-modal-close, [aria-label="Close"]',
    },
    
    # 登录相关（如果需要）
    'login': {
        'username': '#username, #account, input[name="username"], input[name="account"], input[type="text"]',
        'password': '#password, input[name="password"], input[type="password"]',
        'submit': '.login-btn, #login-btn, button[type="submit"], input[type="submit"]',
        'captcha': '#captcha, input[name="captcha"], input[placeholder*="验证码"]',
    },
    
    # 导航/分页
    'navigation': {
        'next_btn': '.next-btn, .next-lesson, [class*="next"], a:contains("下一节"), a:contains("下一个")',
        'prev_btn': '.prev-btn, .prev-lesson, [class*="prev"]',
    },
}


class GZZJWXAdapter:
    """广州市中小学教师继续教育网专用适配器"""
    
    def __init__(self, url, username=None, password=None, headless=False):
        """
        初始化
        
        Args:
            url: 课程 URL
            username: 用户名（可选）
            password: 密码（可选）
            headless: 是否无头模式
        """
        self.url = url
        self.username = username
        self.password = password
        self.headless = headless
        
        self.browser = None
        self.selectors = GZZJWX_SELECTORS
    
    def start(self):
        """启动自动化流程"""
        print("\n" + "="*60)
        print("🎓 广州市中小学教师继续教育网 - 自动化助手")
        print("="*60 + "\n")
        
        # 初始化浏览器
        print("🚀 启动浏览器...")
        self.browser = BrowserController(headless=self.headless).start()
        
        try:
            # 导航到网站
            self.browser.navigate(self.url)
            time.sleep(2)
            
            # 检查是否需要登录
            if self._check_login_required():
                print("📝 需要登录...")
                if self.username and self.password:
                    self._login()
                else:
                    print("⚠️ 请手动登录，登录后按回车继续...")
                    input()
            
            # 进入课程页面
            print("📚 加载课程页面...")
            time.sleep(2)
            
            # 开始播放流程
            self._play_course()
            
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断")
        except Exception as e:
            print(f"\n❌ 发生错误：{e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def _check_login_required(self):
        """检查是否需要登录"""
        login_indicators = [
            '#username', '#account', 'input[name="password"]',
            '.login-form', '[class*="login"]',
        ]
        
        for selector in login_indicators:
            if self.browser.is_visible(selector, timeout=2000):
                return True
        return False
    
    def _login(self):
        """执行登录"""
        print("🔑 执行登录...")
        
        try:
            # 输入用户名
            self.browser.type_text(self.selectors['login']['username'], self.username)
            time.sleep(0.5)
            
            # 输入密码
            self.browser.type_text(self.selectors['login']['password'], self.password)
            time.sleep(0.5)
            
            # 检查是否有验证码
            if self.browser.is_visible(self.selectors['login']['captcha'], timeout=2000):
                print("⚠️ 检测到验证码，请手动输入后按回车继续...")
                input()
            
            # 点击登录
            self.browser.click(self.selectors['login']['submit'])
            time.sleep(3)
            
            print("✓ 登录完成")
            
        except Exception as e:
            print(f"✗ 登录失败：{e}")
            print("⚠️ 请手动登录，登录后按回车继续...")
            input()
    
    def _play_course(self):
        """课程播放主流程"""
        # 初始化组件
        dialog_handler = DialogHandler(self.browser.page)
        video_controller = VideoController(self.browser.page)
        navigator = CourseNavigator(self.browser.page)
        
        # 获取课程进度
        print("\n📊 获取课程进度...")
        navigator.print_progress()
        
        max_videos = 20  # 最多处理视频数
        processed_count = 0
        
        while processed_count < max_videos:
            print(f"\n{'='*40}")
            print(f"📹 处理视频 {processed_count + 1}/{max_videos}")
            print(f"{'='*40}\n")
            
            # 检查并处理弹窗
            if dialog_handler.is_dialog_visible(timeout=3000):
                print("📝 发现弹窗，处理中...")
                self._handle_quiz(dialog_handler, video_controller)
            
            # 尝试播放视频
            if not video_controller.play_video():
                print("⚠️ 无法开始播放，尝试切换视频...")
                if not navigator.next_video():
                    print("✓ 没有更多视频了")
                    break
                time.sleep(1)
                if not video_controller.play_video():
                    print("✗ 无法播放视频，跳过")
                    processed_count += 1
                    continue
            
            print("✓ 视频开始播放")
            
            # 监控播放状态
            wait_time = 0
            max_wait = 1800  # 30 分钟
            last_progress = 0
            stuck_count = 0
            
            while wait_time < max_wait:
                time.sleep(20)  # 每 20 秒检查一次
                wait_time += 20
                
                # 检查弹窗
                if dialog_handler.is_dialog_visible(timeout=2000):
                    print("\n📝 发现测验弹窗！")
                    self._handle_quiz(dialog_handler, video_controller)
                
                # 检查进度
                progress = video_controller.get_progress()
                current_time = video_controller.get_current_time()
                duration = video_controller.get_duration()
                
                if duration > 0:
                    print(f"📊 进度：{progress:.1f}% ({current_time/60:.1f}/{duration/60:.1f} 分钟)")
                else:
                    print(f"📊 进度：{progress:.1f}%")
                
                # 检测卡顿
                if abs(progress - last_progress) < 0.5:
                    stuck_count += 1
                    if stuck_count >= 3:
                        print("⚠️ 视频似乎卡住了，尝试恢复...")
                        video_controller.play_video()
                        stuck_count = 0
                else:
                    stuck_count = 0
                
                last_progress = progress
                
                # 检查是否完成
                if progress >= 98 or video_controller.is_video_ended():
                    print("✓ 视频播放完成")
                    break
                
                # 随机行为模拟
                if random.random() < 0.15:
                    self._random_behavior()
            
            processed_count += 1
            
            # 切换到下一个视频
            if not navigator.next_video():
                print("\n✓ 所有视频已完成！")
                break
            
            time.sleep(2)
        
        # 最终进度
        print("\n" + "="*60)
        navigator.print_progress()
        print(f"✅ 完成！共处理 {processed_count} 个视频")
        print("="*60 + "\n")
    
    def _handle_quiz(self, dialog_handler, video_controller):
        """
        处理测验弹窗
        
        广州市中小学教师继续教育网的测验特点：
        - 可能是单选题或多选题
        - 通常有"确认"或"提交"按钮
        - 完成后自动继续播放
        """
        success = dialog_handler.handle_quiz_dialog(strategy='random')
        
        if success:
            print("✓ 测验已提交")
            time.sleep(1)
            
            # 确保视频继续播放
            video_controller.play_video()
        else:
            print("⚠️ 未能自动处理弹窗，请手动处理...")
            # 等待用户手动处理
            timeout = 60
            while timeout > 0:
                time.sleep(2)
                timeout -= 2
                if not dialog_handler.is_dialog_visible():
                    print("✓ 弹窗已关闭")
                    video_controller.play_video()
                    break
    
    def _random_behavior(self):
        """模拟随机人类行为"""
        behaviors = [
            ("轻微移动鼠标", lambda: self.browser.page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600),
                steps=random.randint(10, 30)
            )),
            ("滚动页面", lambda: self.browser.scroll(random.randint(-100, 100))),
            ("短暂停顿", lambda: time.sleep(random.uniform(1, 3))),
        ]
        
        name, action = random.choice(behaviors)
        try:
            action()
        except:
            pass
    
    def cleanup(self):
        """清理资源"""
        print("\n🧹 清理资源...")
        if self.browser:
            self.browser.close()
        print("✓ 清理完成\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='广州市中小学教师继续教育网 - 自动化助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
    # 手动登录
    python gzzjwx_adapter.py --url http://www.gzzjwx.com/course/123
    
    # 自动登录
    python gzzjwx_adapter.py --url http://www.gzzjwx.com/course/123 --username your_user --password your_pass
    
    # 无头模式
    python gzzjwx_adapter.py --url http://www.gzzjwx.com/course/123 --headless
        '''
    )
    
    parser.add_argument('--url', type=str, required=True, help='课程 URL')
    parser.add_argument('--username', type=str, help='用户名')
    parser.add_argument('--password', type=str, help='密码')
    parser.add_argument('--headless', action='store_true', help='无头模式')
    parser.add_argument('--max-videos', type=int, default=20, help='最多处理视频数')
    
    args = parser.parse_args()
    
    adapter = GZZJWXAdapter(
        url=args.url,
        username=args.username,
        password=args.password,
        headless=args.headless
    )
    adapter.start()


if __name__ == '__main__':
    main()

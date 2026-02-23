#!/usr/bin/env python3
"""
Video Controller - 视频播放器控制器
控制视频播放、暂停、进度检测等
"""

import time


class VideoController:
    """视频播放器控制器"""
    
    def __init__(self, page):
        self.page = page
    
    def play_video(self):
        """
        开始播放视频
        
        Returns:
            bool: 是否成功开始播放
        """
        play_selectors = [
            'button[class*="play"], .play-btn, [aria-label*="播放"]',
            'button[class*="Play"], [aria-label*="Play"]',
            '.vjs-play-control',  # Video.js
            '.ytp-play-button',  # YouTube
            '.txp-play',  # 腾讯云播放器
            '.prism-playbutton',  # 保利威
            'video',  # 直接点击 video 元素
        ]
        
        for selector in play_selectors:
            try:
                element = self.page.locator(selector).first
                if element.is_visible(timeout=1000):
                    element.click()
                    print("✓ 点击播放按钮")
                    time.sleep(0.5)
                    return True
            except:
                continue
        
        # 尝试直接调用 video.play()
        try:
            self.page.evaluate('''
                document.querySelector('video')?.play()
            ''')
            print("✓ 调用 video.play()")
            return True
        except:
            pass
        
        print("✗ 未找到播放按钮")
        return False
    
    def pause_video(self):
        """暂停视频"""
        pause_selectors = [
            'button[class*="pause"], .pause-btn, [aria-label*="暂停"]',
            'button[class*="Pause"], [aria-label*="Pause"]',
            '.vjs-play-control',
            '.ytp-play-button',
        ]
        
        for selector in pause_selectors:
            try:
                element = self.page.locator(selector).first
                if element.is_visible(timeout=1000):
                    element.click()
                    print("✓ 点击暂停按钮")
                    return True
            except:
                continue
        
        try:
            self.page.evaluate('''
                const video = document.querySelector('video');
                if (video && !video.paused) video.pause()
            ''')
            return True
        except:
            pass
        
        return False
    
    def is_playing(self):
        """
        检测视频是否正在播放
        
        Returns:
            bool: 是否正在播放
        """
        try:
            # 检查 paused 属性
            is_paused = self.page.evaluate('''
                () => {
                    const video = document.querySelector('video');
                    return video ? video.paused : null;
                }
            ''')
            
            if is_paused is None:
                return False
            return not is_paused
        except Exception as e:
            print(f"检测播放状态失败：{e}")
            return False
    
    def get_progress(self):
        """
        获取播放进度百分比
        
        Returns:
            float: 进度百分比 (0-100)
        """
        try:
            progress = self.page.evaluate('''
                () => {
                    const video = document.querySelector('video');
                    if (!video) return 0;
                    return (video.currentTime / video.duration) * 100;
                }
            ''')
            return float(progress) if progress else 0
        except:
            return 0
    
    def get_current_time(self):
        """获取当前播放时间（秒）"""
        try:
            return self.page.evaluate('''
                () => document.querySelector('video')?.currentTime || 0
            ''')
        except:
            return 0
    
    def get_duration(self):
        """获取视频总时长（秒）"""
        try:
            return self.page.evaluate('''
                () => document.querySelector('video')?.duration || 0
            ''')
        except:
            return 0
    
    def seek_to(self, seconds):
        """
        跳转到指定时间
        
        Args:
            seconds: 目标时间（秒）
        """
        try:
            self.page.evaluate(f'''
                () => {{
                    const video = document.querySelector('video');
                    if (video) video.currentTime = {seconds};
                }}
            ''')
            print(f"✓ 跳转到 {seconds}秒")
            return True
        except Exception as e:
            print(f"跳转失败：{e}")
            return False
    
    def seek_to_percent(self, percent):
        """
        跳转到指定进度
        
        Args:
            percent: 进度百分比 (0-100)
        """
        try:
            self.page.evaluate(f'''
                () => {{
                    const video = document.querySelector('video');
                    if (video) video.currentTime = (video.duration * {percent / 100});
                }}
            ''')
            print(f"✓ 跳转到 {percent}%")
            return True
        except Exception as e:
            print(f"跳转失败：{e}")
            return False
    
    def set_playback_rate(self, rate):
        """
        设置播放速度
        
        Args:
            rate: 播放速度 (0.5, 1, 1.5, 2 等)
        """
        try:
            self.page.evaluate(f'''
                () => {{
                    const video = document.querySelector('video');
                    if (video) video.playbackRate = {rate};
                }}
            ''')
            print(f"✓ 设置播放速度：{rate}x")
            return True
        except Exception as e:
            print(f"设置速度失败：{e}")
            return False
    
    def is_video_ended(self):
        """
        检测视频是否已结束
        
        Returns:
            bool: 是否已结束
        """
        try:
            ended = self.page.evaluate('''
                () => {
                    const video = document.querySelector('video');
                    return video ? video.ended : false;
                }
            ''')
            return ended
        except:
            # 如果进度超过 98%，认为已结束
            return self.get_progress() >= 98
    
    def wait_for_completion(self, timeout=3600, check_interval=10):
        """
        等待视频播放完成
        
        Args:
            timeout: 最大等待时间（秒）
            check_interval: 检查间隔（秒）
        
        Returns:
            bool: 是否自然完成（非超时）
        """
        start_time = time.time()
        last_progress = self.get_progress()
        stuck_count = 0
        
        print(f"⏳ 等待视频完成...")
        
        while time.time() - start_time < timeout:
            time.sleep(check_interval)
            
            # 检查是否有弹窗
            current_progress = self.get_progress()
            print(f"📊 进度：{current_progress:.1f}%")
            
            # 检测是否卡住
            if abs(current_progress - last_progress) < 0.1:
                stuck_count += 1
                if stuck_count >= 3:
                    print("⚠️ 视频似乎卡住了，尝试恢复播放")
                    self.play_video()
                    stuck_count = 0
            else:
                stuck_count = 0
            
            last_progress = current_progress
            
            # 检查是否完成
            if current_progress >= 98:
                print("✓ 视频播放完成")
                return True
        
        print("⏰ 等待超时")
        return False
    
    def mute(self):
        """静音"""
        try:
            self.page.evaluate('''
                () => {
                    const video = document.querySelector('video');
                    if (video) video.muted = true;
                }
            ''')
            return True
        except:
            return False
    
    def unmute(self):
        """取消静音"""
        try:
            self.page.evaluate('''
                () => {
                    const video = document.querySelector('video');
                    if (video) video.muted = false;
                }
            ''')
            return True
        except:
            return False
    
    def set_volume(self, volume):
        """
        设置音量
        
        Args:
            volume: 音量 (0-1)
        """
        try:
            self.page.evaluate(f'''
                () => {{
                    const video = document.querySelector('video');
                    if (video) video.volume = {volume};
                }}
            ''')
            return True
        except:
            return False

#!/usr/bin/env python3
"""
Course Navigator - 课程导航器
管理视频列表、切换视频、进度追踪
"""

import time


class CourseNavigator:
    """课程导航器"""
    
    def __init__(self, page):
        self.page = page
        self.video_list_cache = []
        self.current_index = -1
    
    def get_video_list(self, refresh=False):
        """
        获取视频列表
        
        Args:
            refresh: 是否刷新缓存
        
        Returns:
            list: 视频列表 [{'index': 0, 'text': '...', 'completed': False}]
        """
        if self.video_list_cache and not refresh:
            return self.video_list_cache
        
        videos = []
        
        # 常见视频列表选择器
        list_selectors = [
            '[class*="video-item"], .video-item, .lesson-item',
            '[class*="chapter"] [class*="item"]',
            '.catalog-item, .course-item, .section-item',
            '[class*="catalog"] li, [class*="list"] li',
            '.ant-tree li, .el-tree-node',  # UI 框架
            '[role="listitem"], [data-type="video"]',
        ]
        
        for selector in list_selectors:
            try:
                items = self.page.locator(selector)
                count = items.count()
                
                if count == 0:
                    continue
                
                print(f"✓ 找到视频列表：{count} 个 (selector: {selector})")
                
                for i in range(count):
                    try:
                        item = items.nth(i)
                        text = item.inner_text(timeout=500).strip()
                        
                        # 跳过空项
                        if not text or len(text) < 2:
                            continue
                        
                        # 检查是否已完成
                        completed = self._is_completed(item)
                        
                        videos.append({
                            'index': i,
                            'text': text,
                            'completed': completed,
                            'selector': selector,
                        })
                    except:
                        continue
                
                if videos:
                    self.video_list_cache = videos
                    return videos
                    
            except Exception as e:
                continue
        
        print(f"⚠️ 未找到视频列表")
        return []
    
    def _is_completed(self, item):
        """
        检查视频是否已完成
        
        Args:
            item: 视频项元素
        
        Returns:
            bool: 是否已完成
        """
        completed_indicators = [
            'completed', 'finished', 'done', '✓', '✔', '完成', '已学',
            'checked', 'selected', 'active-done'
        ]
        
        # 检查类名
        try:
            class_names = item.get_attribute('class', timeout=500)
            if class_names:
                for indicator in completed_indicators:
                    if indicator.lower() in class_names.lower():
                        return True
        except:
            pass
        
        # 检查文本
        try:
            text = item.inner_text(timeout=500).lower()
            for indicator in completed_indicators:
                if indicator in text:
                    return True
        except:
            pass
        
        # 检查子元素（图标等）
        for indicator in completed_indicators:
            try:
                icon = item.locator(f'[class*="{indicator}"], .icon-complete, .icon-check, .icon-done').first
                if icon.is_visible(timeout=500):
                    return True
            except:
                continue
        
        # 检查是否有完成状态属性
        try:
            status = item.get_attribute('data-status')
            if status and status.lower() in ['completed', 'finished', 'done']:
                return True
        except:
            pass
        
        return False
    
    def get_current_video_index(self):
        """
        获取当前播放的视频索引
        
        Returns:
            int: 当前索引，-1 表示未找到
        """
        videos = self.get_video_list()
        
        # 查找带有"当前"、"playing"、"active"标记的视频
        active_indicators = ['active', 'playing', 'current', 'now', '当前']
        
        for i, video in enumerate(videos):
            try:
                item = self.page.locator(video['selector']).nth(video['index'])
                
                # 检查类名
                class_names = item.get_attribute('class', timeout=500)
                if class_names:
                    for indicator in active_indicators:
                        if indicator.lower() in class_names.lower():
                            self.current_index = i
                            return i
            except:
                continue
        
        return -1
    
    def next_video(self):
        """
        切换到下一个未播放的视频
        
        Returns:
            bool: 是否成功切换
        """
        videos = self.get_video_list(refresh=True)
        
        if not videos:
            print("✗ 没有可用的视频列表")
            return False
        
        # 查找下一个未播放的视频
        for i, video in enumerate(videos):
            if not video['completed']:
                try:
                    item = self.page.locator(video['selector']).nth(video['index'])
                    item.scroll_into_view_if_needed()
                    item.click()
                    
                    print(f"✓ 切换到视频 {i + 1}/{len(videos)}: {video['text'][:30]}...")
                    self.current_index = i
                    time.sleep(1)
                    return True
                except Exception as e:
                    print(f"✗ 切换失败：{e}")
                    continue
        
        print("⚠️ 所有视频都已完成")
        return False
    
    def play_video_by_index(self, index):
        """
        播放指定索引的视频
        
        Args:
            index: 视频索引
        
        Returns:
            bool: 是否成功
        """
        videos = self.get_video_list()
        
        if index < 0 or index >= len(videos):
            print(f"✗ 索引超出范围：{index}")
            return False
        
        video = videos[index]
        try:
            item = self.page.locator(video['selector']).nth(video['index'])
            item.scroll_into_view_if_needed()
            item.click()
            
            print(f"✓ 播放视频 {index + 1}: {video['text'][:30]}...")
            self.current_index = index
            time.sleep(1)
            return True
        except Exception as e:
            print(f"✗ 播放失败：{e}")
            return False
    
    def get_progress_summary(self):
        """
        获取进度摘要
        
        Returns:
            dict: {'total': 总数，'completed': 已完成，'remaining': 剩余}
        """
        videos = self.get_video_list(refresh=True)
        
        total = len(videos)
        completed = sum(1 for v in videos if v['completed'])
        remaining = total - completed
        
        return {
            'total': total,
            'completed': completed,
            'remaining': remaining,
            'percent': (completed / total * 100) if total > 0 else 0
        }
    
    def print_progress(self):
        """打印进度信息"""
        summary = self.get_progress_summary()
        print(f"\n📊 课程进度：{summary['completed']}/{summary['total']} "
              f"({summary['percent']:.1f}%) - 剩余 {summary['remaining']} 个视频\n")
    
    def get_all_completed(self):
        """检查是否所有视频都已完成"""
        summary = self.get_progress_summary()
        return summary['remaining'] == 0

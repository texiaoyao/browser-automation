#!/usr/bin/env python3
"""
Dialog Handler - 弹窗处理器
自动识别和处理测验、验证等弹窗
"""

import random
import time


class DialogHandler:
    """弹窗处理器"""
    
    def __init__(self, page):
        self.page = page
    
    def handle_quiz_dialog(self, strategy='random'):
        """
        处理测验弹窗
        
        Args:
            strategy: 选择策略 ('random' | 'first' | 'smart')
        
        Returns:
            bool: 是否成功处理
        """
        try:
            # 等待弹窗出现（最多 3 秒）
            dialog_selectors = [
                '.quiz-modal',
                '.quiz-popup',
                '.popup-dialog',
                '[class*="quiz"]',
                '[class*="dialog"]',
                '.ant-modal',  # Ant Design
                '.el-dialog',  # Element UI
                '.modal-dialog',
                '.v-modal',
                '[role="dialog"]',
            ]
            
            dialog = None
            for selector in dialog_selectors:
                try:
                    dialog = self.page.locator(selector).first
                    if dialog.is_visible(timeout=1000):
                        print(f"✓ 发现弹窗：{selector}")
                        break
                    dialog = None
                except:
                    continue
            
            if not dialog or not dialog.is_visible():
                return False
            
            # 识别题目类型
            is_multiple = self._detect_multiple_choice(dialog)
            print(f"📝 题目类型：{'多选题' if is_multiple else '单选题'}")
            
            # 选择答案
            if is_multiple:
                self._select_multiple_answers(dialog, strategy)
            else:
                self._select_single_answer(dialog, strategy)
            
            # 点击确认
            self._click_confirm(dialog)
            
            # 等待弹窗关闭
            time.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"✗ 处理弹窗失败：{e}")
            return False
    
    def _detect_multiple_choice(self, dialog):
        """
        检测是否多选题
        
        Returns:
            bool: True=多选题，False=单选题
        """
        try:
            # 查找 checkbox（多选）vs radio（单选）
            checkboxes = dialog.locator('input[type="checkbox"]').count()
            radios = dialog.locator('input[type="radio"]').count()
            
            if checkboxes > 0:
                return True
            
            # 尝试通过文本检测
            text = dialog.inner_text(timeout=1000).lower()
            if '多选' in text or 'multiple' in text or '选择所有' in text:
                return True
            
            return False
        except:
            return False
    
    def _select_single_answer(self, dialog, strategy):
        """
        选择单选题答案
        
        Args:
            dialog: 弹窗元素
            strategy: 选择策略
        """
        # 优先查找 radio 按钮
        options = dialog.locator('input[type="radio"]')
        count = options.count()
        
        if count == 0:
            # 尝试查找可点击的选项容器
            options = dialog.locator('[class*="option"], .option-item, .answer-item, .choice-item')
            count = options.count()
        
        if count == 0:
            # 尝试查找 label
            options = dialog.locator('label')
            count = options.count()
        
        if count > 0:
            if strategy == 'random':
                index = random.randint(0, count - 1)
            else:
                index = 0
            
            print(f"🎯 选择选项：{index + 1}/{count}")
            
            try:
                options.nth(index).click()
            except:
                try:
                    options.nth(index).locator('..').click()
                except:
                    options.nth(index).dispatch_event('click')
    
    def _select_multiple_answers(self, dialog, strategy):
        """
        选择多选题答案
        
        Args:
            dialog: 弹窗元素
            strategy: 选择策略
        """
        options = dialog.locator('input[type="checkbox"]')
        count = options.count()
        
        if count == 0:
            options = dialog.locator('[class*="option"], .option-item, .choice-item')
            count = options.count()
        
        if count > 0:
            # 随机选择 1 到全部选项（避免全选太明显）
            select_count = random.randint(1, min(count, 3))
            indices = random.sample(range(count), select_count)
            
            print(f"🎯 选择 {select_count} 个选项：{[i+1 for i in indices]}")
            
            for idx in indices:
                try:
                    options.nth(idx).click()
                    time.sleep(0.1)
                except:
                    try:
                        options.nth(idx).locator('..').click()
                        time.sleep(0.1)
                    except:
                        pass
    
    def _click_confirm(self, dialog):
        """
        点击确认按钮
        
        Args:
            dialog: 弹窗元素
        """
        confirm_selectors = [
            'button:has-text("确认"), button:has-text("提交"), button:has-text("确定")',
            'button:has-text("Confirm"), button:has-text("Submit"), button:has-text("OK")',
            '.confirm-btn, .submit-btn, .ok-btn, .submit-button',
            '[class*="confirm"], [class*="submit"]',
            'button[type="submit"]',
            '.ant-btn-primary, .el-button--primary',  # UI 框架
        ]
        
        for selector in confirm_selectors:
            try:
                btn = dialog.locator(selector).first
                if btn.is_visible(timeout=500):
                    btn.click()
                    print("✓ 点击确认按钮")
                    return
            except:
                continue
        
        # 如果没找到，尝试找最后一个按钮
        try:
            buttons = dialog.locator('button')
            count = buttons.count()
            if count > 0:
                buttons.nth(count - 1).click()
                print("✓ 点击最后一个按钮")
                return
        except:
            pass
        
        print("✗ 未找到确认按钮")
    
    def handle_verification(self):
        """
        处理简单验证弹窗
        
        Returns:
            bool: 是否成功处理
        """
        verification_selectors = [
            '.verification-modal',
            '.captcha-container',
            '[class*="verify"]',
            '.ant-modal-visible',
        ]
        
        for selector in verification_selectors:
            try:
                element = self.page.locator(selector).first
                if element.is_visible(timeout=500):
                    print(f"⚠️ 发现验证弹窗：{selector}")
                    # 简单验证通常有关闭或跳过按钮
                    skip_btn = element.locator('button:has-text("跳过"), button:has-text("关闭"), .close-btn').first
                    if skip_btn.is_visible(timeout=500):
                        skip_btn.click()
                        return True
            except:
                continue
        
        return False
    
    def is_dialog_visible(self, timeout=1000):
        """
        检查是否有弹窗 visible
        
        Returns:
            bool: 是否有弹窗
        """
        dialog_selectors = [
            '.quiz-modal', '.popup-dialog', '.ant-modal',
            '.el-dialog', '.modal-dialog', '[role="dialog"]',
        ]
        
        for selector in dialog_selectors:
            try:
                if self.page.locator(selector).first.is_visible(timeout=timeout):
                    return True
            except:
                continue
        
        return False
    
    def close_dialog(self):
        """
        关闭弹窗（如果有）
        
        Returns:
            bool: 是否成功关闭
        """
        close_selectors = [
            '.close-btn', '.ant-modal-close', '.el-dialog__close',
            'button[aria-label="Close"], button[aria-label="关闭"]',
            '.modal-close', '[class*="close-icon"]',
        ]
        
        for selector in close_selectors:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=500):
                    btn.click()
                    print("✓ 关闭弹窗")
                    return True
            except:
                continue
        
        return False

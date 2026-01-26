import flet as ft
import calendar
from datetime import datetime
import traceback # 用于捕获错误详情

def main(page: ft.Page):
    # --- 1. 全局错误捕获 (防止黑屏) ---
    # 如果发生错误，会在屏幕上显示错误信息，而不是直接黑屏
    try:
        # --- 2. 设置 APP 基础样式 ---
        page.title = "每日打卡"
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = "#0D1117"
        page.padding = 0 # 移动端通常不需要外边距，最大化利用屏幕
        
        # 【关键修复】：移动端使用 ListView 时，必须关闭 page 自身的滚动
        # 否则会产生“无限高度”冲突导致黑屏
        page.scroll = None 

        # 颜色阶梯
        COLOR_MAP = {
            0: "#161B22",
            1: "#0E4429",
            2: "#006D32",
            3: "#26A641",
            4: "#39D353",
        }

        # --- Helper 函数 ---
        def get_storage_key(year, month, day):
            return f"checkin_{year}_{month}_{day}"

        def get_checkin_count(year, month, day):
            key = get_storage_key(year, month, day)
            # 增加安全性：确保存储中取出的必须是整数
            val = page.client_storage.get(key)
            if val is None:
                return 0
            return int(val)

        # --- 组件定义 ---
        class DayTile(ft.UserControl):
            def __init__(self, year, month, day):
                super().__init__()
                self.year = year
                self.month = month
                self.day = day
                self.count = get_checkin_count(year, month, day)
                
                self.container = ft.Container(
                    width=30,
                    height=30,
                    border_radius=4,
                    alignment=ft.alignment.center,
                    on_click=self.on_click_date,
                    animate_container=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT),
                )

            def build(self):
                self.update_style()
                return self.container

            def update_style(self):
                bg_color = COLOR_MAP.get(min(self.count, 4), COLOR_MAP[4]) if self.count > 0 else COLOR_MAP[0]
                text_color = "white" if self.count > 0 else "#2d333b"
                
                self.container.bgcolor = bg_color
                self.container.content = ft.Text(
                    value=str(self.count) if self.count > 0 else "", 
                    color=text_color,
                    size=10,
                    weight=ft.FontWeight.BOLD
                )
                self.container.update()

            def on_click_date(self, e):
                self.count += 1
                key = get_storage_key(self.year, self.month, self.day)
                page.client_storage.set(key, self.count)
                self.update_style()
                page.show_snack_bar(ft.SnackBar(content=ft.Text(f"{self.month}月{self.day}日 打卡 +1"), duration=500))

        def build_month_grid(year, month):
            _, num_days = calendar.monthrange(year, month)
            
            month_label = ft.Text(f"{year}年{month}月", size=14, weight=ft.FontWeight.BOLD, color="#8b949e")
            
            # 使用 Wrap 组件自动换行，比 Row 更稳定
            days_layout = ft.Row(
                wrap=True, 
                spacing=6, 
                run_spacing=6,
                alignment=ft.MainAxisAlignment.START,
            )

            for day in range(1, num_days + 1):
                days_layout.controls.append(DayTile(year, month, day))

            return ft.Container(
                content=ft.Column([
                    month_label,
                    days_layout
                ]),
                padding=ft.padding.only(bottom=20)
            )

        # --- 3. 构建主视图 ---
        today = datetime.now()
        curr_year = today.year
        curr_month = today.month

        # 列表视图
        list_view = ft.ListView(
            expand=True, # 关键：占满剩余空间
            spacing=10,
            padding=20,
        )
        
        for i in range(12):
            calc_month = curr_month - i
            calc_year = curr_year
            if calc_month <= 0:
                calc_month += 12
                calc_year -= 1
            
            list_view.controls.append(build_month_grid(calc_year, calc_month))

        # 顶部导航栏
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("统计", size=16, color="white", weight="bold"),
                    ft.Text("事件", size=16, color="#8b949e"),
                    ft.Text("设置", size=16, color="#8b949e"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            ),
            padding=ft.padding.only(top=10, bottom=10),
            bgcolor="#161B22" # 顶部栏背景色
        )

        # 页面结构
        page.add(
            ft.Column(
                [
                    header,
                    ft.Divider(height=1, color="#30363d"),
                    list_view
                ],
                spacing=0,
                expand=True # 关键：Column 必须 expand 才能撑开 ListView
            )
        )

    except Exception as e:
        # --- 错误处理 ---
        # 如果出错，屏幕显示红色错误信息，方便调试
        error_trace = traceback.format_exc()
        page.add(
            ft.Column([
                ft.Text("App 启动出错 (Error launching App):", color="red", size=20),
                ft.Text(str(e), color="red"),
                ft.Container(
                    content=ft.Text(error_trace, size=10, color="yellow", font_family="monospace"),
                    bgcolor="black",
                    padding=10
                )
            ], scroll=ft.ScrollMode.ALWAYS)
        )

ft.app(target=main)

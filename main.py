import flet as ft
import calendar
from datetime import datetime

def main(page: ft.Page):
    # 1. 设置 APP 基础样式 (深色模式)
    page.title = "每日打卡 (Daily Check-in)"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0D1117"  # 类似 GitHub 的深色背景
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # 颜色阶梯 (GitHub 风格绿色)
    # 0次: 灰色, 1次: 浅绿 -> 4次+: 深绿
    COLOR_MAP = {
        0: "#161B22",  # 未打卡 (深灰)
        1: "#0E4429",  # 1次
        2: "#006D32",  # 2次
        3: "#26A641",  # 3次
        4: "#39D353",  # 4次及以上
    }

    # 获取数据的 helper 函数
    def get_storage_key(year, month, day):
        return f"checkin_{year}_{month}_{day}"

    def get_checkin_count(year, month, day):
        key = get_storage_key(year, month, day)
        return page.client_storage.get(key) or 0

    # 2. 定义单个日期方块组件
    class DayTile(ft.UserControl):
        def __init__(self, year, month, day):
            super().__init__()
            self.year = year
            self.month = month
            self.day = day
            self.count = get_checkin_count(year, month, day)
            
            # 这里的 Container 是显示的方块
            self.container = ft.Container(
                width=30,  # 方块大小
                height=30,
                border_radius=4,
                alignment=ft.alignment.center,
                on_click=self.on_click_date,
                animate_container=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
            )
            self.text = ft.Text(size=12, weight=ft.FontWeight.BOLD)

        def build(self):
            self.update_style()
            return self.container

        def update_style(self):
            # 根据次数决定颜色
            bg_color = COLOR_MAP.get(min(self.count, 4), COLOR_MAP[4]) if self.count > 0 else COLOR_MAP[0]
            text_color = "white" if self.count > 0 else "#2d333b" # 未打卡时文字暗一点或不显示
            
            self.container.bgcolor = bg_color
            self.container.content = ft.Text(
                value=str(self.count) if self.count > 0 else "", 
                color=text_color,
                size=12
            )
            self.container.update()

        def on_click_date(self, e):
            # 点击增加打卡次数
            self.count += 1
            # 保存数据
            key = get_storage_key(self.year, self.month, self.day)
            page.client_storage.set(key, self.count)
            self.update_style()
            # 可以加一个SnackBar提示
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"{self.month}月{self.day}日 打卡 +1!"), duration=500))

    # 3. 构建月份视图
    def build_month_grid(year, month):
        # 获取该月有多少天
        _, num_days = calendar.monthrange(year, month)
        
        # 标题 (例如: 2025年12月)
        month_label = ft.Text(f"{year}年{month}月", size=16, weight=ft.FontWeight.BOLD, color="white")
        
        # 日期方块的容器 (使用 Row wrap=True 实现自动换行，模拟 Grid)
        days_layout = ft.Row(
            wrap=True, 
            spacing=5, 
            run_spacing=5,
            width=300, # 限制宽度以强制换行，适应手机屏幕
        )

        for day in range(1, num_days + 1):
            days_layout.controls.append(DayTile(year, month, day))

        return ft.Column([
            ft.Container(height=10), # 间距
            month_label,
            days_layout
        ])

    # 4. 主布局：生成最近 12 个月的视图
    # 我们倒序生成，最近的月份在最上面
    today = datetime.now()
    curr_year = today.year
    curr_month = today.month

    # 生成一个 ListView 包含所有月份
    list_view = ft.ListView(expand=True, spacing=10)
    
    # 简单的逻辑：生成过去 12 个月
    for i in range(12):
        calc_month = curr_month - i
        calc_year = curr_year
        if calc_month <= 0:
            calc_month += 12
            calc_year -= 1
        
        list_view.controls.append(build_month_grid(calc_year, calc_month))

    # 顶部导航栏模仿
    header = ft.Row(
        [
            ft.Text("统计", size=16, color="white", weight="bold"),
            ft.Text("事件", size=16, color="grey"),
            ft.Text("设置", size=16, color="grey"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    page.add(
        ft.Column([
            ft.Container(content=header, padding=10),
            ft.Divider(color="grey"),
            list_view
        ], expand=True)
    )

ft.app(target=main)

import flet as ft
import random

def main(page: ft.Page):
    # --- 1. 页面基础设置 ---
    page.title = "PixelLog"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0d1117"  # GitHub Dark 背景色
    page.scroll = ft.ScrollMode.HIDDEN # 主页面不滚动，内容区域滚动

    # 自定义颜色板
    colors = {
        "bg": "#0d1117",
        "card": "#161b22",
        "text_main": "#c9d1d9",
        "text_sub": "#8b949e",
        "l0": "#161b22",      # 空数据
        "l1": "#0e4429",      # 1次
        "l2": "#26a641",      # 2次
        "l3": "#39d353",      # 4次+ (荧光绿)
        "border": "#30363d"
    }

    # --- 2. 组件生成函数 ---

    # 生成单个格子的函数
    def create_day_cell(count=0):
        # 根据次数决定颜色
        bg_color = colors["l0"]
        text_color = ft.colors.TRANSPARENT
        border_color = colors["border"]
        
        if count == 1:
            bg_color = ft.colors.with_opacity(0.4, "#26a641")
            text_color = ft.colors.WHITE70
            border_color = ft.colors.with_opacity(0.5, "#26a641")
        elif count == 2:
            bg_color = ft.colors.with_opacity(0.8, "#26a641")
            text_color = ft.colors.WHITE
            border_color = colors["l2"]
        elif count >= 3:
            bg_color = colors["l3"]
            text_color = ft.colors.BLACK
            border_color = colors["l3"]

        return ft.Container(
            content=ft.Text(
                str(count) if count > 0 else "", 
                size=10, 
                weight=ft.FontWeight.BOLD,
                color=text_color
            ),
            bgcolor=bg_color,
            border=ft.border.all(1, border_color),
            border_radius=4,
            alignment=ft.alignment.center,
            aspect_ratio=1, # 保持正方形
        )

    # 生成一个月份的卡片
    def create_month_card(month_name):
        # 模拟生成30天的数据
        cells = []
        for _ in range(30):
            # 随机生成打卡数据模拟真实感
            rand = random.random()
            count = 0
            if rand > 0.6: count = 1
            if rand > 0.85: count = 2
            if rand > 0.95: count = random.randint(3, 5)
            cells.append(create_day_cell(count))

        return ft.Container(
            bgcolor=colors["card"],
            border=ft.border.all(1, colors["border"]),
            border_radius=12,
            padding=15,
            content=ft.Column([
                ft.Text(f"2026年{month_name}", size=14, weight=ft.FontWeight.BOLD, color=colors["text_main"]),
                ft.GridView(
                    controls=cells,
                    runs_count=7,  # 一行7个 (代表一周)
                    spacing=4,
                    run_spacing=4,
                    child_aspect_ratio=1, # 格子宽高比
                )
            ])
        )

    # --- 3. 界面布局组装 ---

    # 顶部导航栏 (自定义)
    top_nav = ft.Container(
        bgcolor=ft.colors.with_opacity(0.9, colors["bg"]),
        blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
        padding=ft.padding.only(left=20, right=20, top=15, bottom=15),
        border=ft.border.only(bottom=ft.border.BorderSide(1, colors["border"])),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([
                    ft.Container(
                        content=ft.Text("统计", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                        border=ft.border.only(bottom=ft.border.BorderSide(2, colors["l3"])),
                        padding=ft.padding.only(bottom=5)
                    ),
                    ft.Text("事件", color=colors["text_sub"]),
                    ft.Text("设置", color=colors["text_sub"]),
                ], spacing=20),
                ft.CircleAvatar(
                    bgcolor=colors["card"],
                    content=ft.Icon(ft.icons.PERSON, size=16, color=colors["text_main"]),
                    radius=16
                )
            ]
        )
    )

    # 年度统计头图
    stats_header = ft.Container(
        padding=20,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END,
            controls=[
                ft.Column([
                    ft.Text("2026年", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Row([
                        ft.Text("已打卡", size=14, color=colors["text_sub"]),
                        ft.Text("403", size=14, color=colors["l3"], weight=ft.FontWeight.BOLD),
                        ft.Text("次", size=14, color=colors["text_sub"]),
                    ], spacing=5)
                ], spacing=2),
                ft.ElevatedButton(
                    "+ 今日打卡",
                    color=ft.colors.WHITE,
                    bgcolor="#238636", # GitHub Green Button
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        padding=ft.padding.symmetric(horizontal=15, vertical=10)
                    )
                )
            ]
        )
    )

    # 月份网格布局 (响应式Grid)
    # 使用 ResponsiveRow 可以在大屏显示多列，小屏显示单列/双列
    months_layout = ft.ResponsiveRow(
        columns=2, # 把屏幕分为2份
        spacing=15,
        run_spacing=15,
        controls=[
            ft.Column(col={"xs": 2, "md": 1}, controls=[create_month_card(m)]) 
            for m in ["12月", "11月", "10月", "09月", "08月", "07月", "06月", "05月"]
        ]
    )

    # 主要内容滚动区
    content_scroll = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True, # 占满剩余空间
        controls=[
            stats_header,
            ft.Container(padding=ft.padding.symmetric(horizontal=15), content=months_layout),
            ft.Container(height=80) # 底部留白，防止被导航栏遮挡
        ]
    )

    # 底部导航栏
    bottom_nav = ft.NavigationBar(
        bgcolor=colors["card"],
        indicator_color=ft.colors.with_opacity(0.1, colors["l3"]),
        destinations=[
            ft.NavigationDestination(icon=ft.icons.BAR_CHART, label="统计", selected_icon=ft.icons.BAR_CHART_ROUNDED),
            ft.NavigationDestination(icon=ft.icons.LIST, label="项目"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="偏好"),
        ]
    )

    # 将所有元素放入页面
    page.add(
        ft.Column(
            spacing=0,
            expand=True,
            controls=[
                top_nav,
                content_scroll,
                bottom_nav
            ]
        )
    )

# 运行 App
ft.app(target=main)
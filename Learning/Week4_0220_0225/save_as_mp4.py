import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

# ====== 1) 读取 CSV, 假设其在同目录下 ======
df = pd.read_csv("selected_cities_pm25.csv")

# ====== 2) 你要输出动画的文件夹 ======
output_dir = r"E:\Master2\FYP\Global\Global\cities_animations"
os.makedirs(output_dir, exist_ok=True)

# ====== 3) 定义色阶 (BoundaryNorm) 和离散颜色 ListedColormap ======
bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99999]
c_list = [
    (164 / 255, 255 / 255, 255 / 255),  # 0 - 5    Very Good
    (176 / 255, 218 / 255, 233 / 255),  # 5 - 10   Fair(down)
    (176 / 255, 206 / 255, 237 / 255),  # 10 - 15  Fair(up)
    (249 / 255, 224 / 255, 71 / 255),  # 15 - 20  Moderate(down)
    (242 / 255, 200 / 255, 75 / 255),  # 20 - 30  Moderate(up)
    (241 / 255, 166 / 255, 63 / 255),  # 30 - 40  Poor(down)
    (233 / 255, 135 / 255, 37 / 255),  # 40 - 50  Poor(up)
    (175 / 255, 69 / 255, 83 / 255),  # 50 - 60  Very Poor(down)
    (134 / 255, 59 / 255, 71 / 255),  # 60 - 70  Very Poor(up)
    (103 / 255, 58 / 255, 61 / 255),  # 70 - 80  Extremely Poor(down)
    (70 / 255, 47 / 255, 48 / 255),  # 80 - 90  Extremely Poor(mid)
    (37 / 255, 36 / 255, 36 / 255),  # 90+      Extremely Poor(up)
]
cmap = mcolors.ListedColormap(c_list)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# ====== 4) 获取年份列，以及城市列表 ======
years = df["Year"].to_numpy()
city_cols = [col for col in df.columns if col != "Year"]


# -- 为了演示，把生成动画打包成一个函数 --
def create_animation_for_city(city_name, years, pm25_values, output_path):
    """
    city_name: str, 城市名
    years: 1D array-like, 年份
    pm25_values: 1D array-like, PM2.5 浓度
    output_path: str, 最终要保存的 .mp4 文件路径
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # (A) 用 imshow 绘制“条带” (整块显示，保持不变)
    ax.imshow(
        pm25_values.reshape(1, -1),
        aspect="auto",
        cmap=cmap,
        norm=norm,
        extent=[years[0], years[-1] + 1, 0, 1]
    )
    ax.set_yticks([])
    ax.set_xlim([years[0], years[-1] + 1])

    # (B) 在第二个 y 轴上叠加白色折线，但先让它是空的
    ax2 = ax.twinx()
    line, = ax2.plot([], [], color="white", linewidth=5)
    ax2.set_xlim([years[0], years[-1] + 1])
    ax2.set_ylim([0, 120])  # 固定在 0~120

    # (C) 设置标题
    ax.set_title(
        f"{city_name}\nAir pollution (PM2.5) concentrations",
        fontsize=14, fontweight="bold", pad=20
    )
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # -- 定义动画帧的 init 函数 --
    def init():
        line.set_data([], [])
        return (line,)

    # -- 定义逐帧更新函数: 只显示前 i 个点 --
    def update(frame):
        # frame 从 0 到 len(years)-1
        xdata = years[:frame + 1]
        ydata = pm25_values[:frame + 1]
        line.set_data(xdata, ydata)
        return (line,)

    # -- 创建动画对象: frames 用年份数目即可，interval=100 表示100ms一帧 --
    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(years),
        interval=100,
        blit=True
    )

    # -- 用 ffmpegwriter 或者默认 writer 保存到 mp4 --
    #    请确认你安装了 ffmpeg
    anim.save(output_path, fps=10, dpi=150)
    plt.close(fig)  # 及时关闭


# ====== 5) 遍历城市列，为每个城市生成一份动画 mp4 ======
for city_name in city_cols:
    pm25_values = df[city_name].to_numpy()

    # 输出 mp4 文件名
    save_path = os.path.join(output_dir, f"{city_name}.mp4")

    create_animation_for_city(
        city_name,
        years,
        pm25_values,
        save_path
    )

print("All done! Animations saved to:", output_dir)

import matplotlib.pyplot as plt
import geopandas as gpd
import adjustText  # 防止文字重叠

# 使用正确的 Shapefile 文件路径
shapefile_path = "/Users/shuoshuo/Downloads/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
world = gpd.read_file(shapefile_path)

# 标注学生来自的国家及人数
students_by_country = {
    "China": 1,
    "Vietnam": 4,
    "Cambodia": 1,
    "Ethiopia": 1,
    "Bangladesh": 2,
    "Turkey": 1,
    "Senegal": 1,
    "Nigeria": 1,
    "Uganda": 3,
    "Algeria": 1,
    "Ukraine": 1,
    "United States": 1,
    "Egypt": 2,
    "Dominican Rep.": 1,
    "Sudan": 1,
    "Kenya": 1,
    "Libya": 1,
}

# 颜色映射（优化 Sudan 颜色）
color_map = {
    "China": "#e41a1c",  # 红色
    "Vietnam": "#ff7f00",  # 橙色
    "Cambodia": "#ffff33",  # 黄色
    "Ethiopia": "#984ea3",  # 紫色
    "Bangladesh": "#f781bf",  # 粉色
    "Turkey": "#377eb8",  # 蓝色
    "Senegal": "#4daf4a",  # 绿色
    "Nigeria": "#2ca02c",  # 深绿
    "Uganda": "#a65628",  # 棕色
    "Algeria": "#66c2a5",  # 淡绿
    "Ukraine": "#999999",  # 灰色
    "United States": "#000000",  # 黑色
    "Egypt": "#ffd700",  # 金色
    "Dominican Rep.": "#ff1493",  # 深粉
    "Sudan": "#1f78b4",  # 深蓝（优化对比度）
    "Kenya": "#87ceeb",  # 浅蓝
    "Libya": "#006400",  # 深绿
}

# 为国家添加颜色列，默认填充灰色
world["color"] = "#e0e0e0"
for country in students_by_country.keys():
    if country in world["NAME"].values:
        world.loc[world["NAME"] == country, "color"] = color_map.get(country, "#bdbdbd")  # 备用灰色

# 获取国家的地理中心点
world["centroid"] = world.geometry.representative_point()
centroids = world.set_index("NAME")["centroid"]  # "NAME" 是国家名称字段

# 创建地图
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
world.plot(ax=ax, color=world["color"], edgecolor="black", linewidth=0.8)  # 颜色填充的地图

# 标注国家位置及人数（优化 Sudan 文字对比度）
texts = []
for country, count in students_by_country.items():
    if country in centroids.index:
        x, y = centroids[country].x, centroids[country].y
        offset_x = 1 if x > 0 else -1  # 向右或向左偏移文本
        offset_y = 1.5 if country == "Sudan" else (0.8 if y > 0 else -0.8)  # Sudan 特别处理，偏移更多

        # 让标注文本颜色和国家颜色形成对比
        country_color = color_map.get(country, "#bdbdbd")  # 取默认灰色
        if country in ["Sudan", "Nigeria", "Libya"]:  # 深色国家使用白色字体
            text_color = "white"
        else:
            text_color = "blue"

        # 使用 annotate 优化文本位置
        text = ax.annotate(f"{country}\n({count})", xy=(x, y), xytext=(x + offset_x, y + offset_y),
                           fontsize=10, color=text_color, fontweight='bold',
                           bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'),
                           arrowprops=dict(arrowstyle="-", color='black', alpha=0.5, lw=0.7))  # 半透明黑色引导线
        texts.append(text)

# 自动调整文本位置，防止重叠
adjustText.adjust_text(texts, arrowprops=dict(arrowstyle="-", color='gray', lw=0.5))

# 设置标题
ax.set_title("Geographical Distribution of MIU ComPro Jan25", fontsize=14, fontweight='bold')

# 添加网格，使地图更清晰
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

# 隐藏坐标轴
ax.set_xticks([])
ax.set_yticks([])

# 保存高清图片
plt.savefig("MIU_CS500_Student_Distribution_Final_Optimized.png", dpi=300, bbox_inches="tight")

# 显示地图
plt.show()

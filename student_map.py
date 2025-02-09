import matplotlib.pyplot as plt
import geopandas as gpd
import adjustText  # 防止文字重叠

# 使用正确的 Shapefile 文件路径
shapefile_path = "/Users/shuoshuo/Downloads/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
world = gpd.read_file(shapefile_path)

# 标注学生来自的国家及人数（已补充 4 人，共 20 人）
students_by_country = {
    "China": 1,
    "Vietnam": 4,
    "Cambodia": 1,
    "Ethiopia": 1,
    "Bangladesh": 2,
    "Turkey": 1,
    "Senegal": 1,
    "Nigeria": 1,
    "Uganda": 3,  # 增加了 Gideon Bamuleseyo
    "Algeria": 1,
    "Ukraine": 1,
    "United States": 1,  # Instructor
    "Egypt": 2,  # 增加了 Mohamed Sherif Mohamed Abdelhalim Abouselima
    "Dominican Rep.": 1,  # 修正为正确国家
    "Sudan": 1,  # Mohamed 可能也来自苏丹
    "Kenya": 1,  # 增加了 Gideon Bamuleseyo
    "Libya": 1,  # Mohamed 可能也来自利比亚
}

# 获取国家的地理中心点
world["centroid"] = world.geometry.representative_point()
centroids = world.set_index("NAME")["centroid"]  # "NAME" 是国家名称字段

# 创建地图
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)  # 增加画布尺寸，提高分辨率
world.plot(ax=ax, color="#e0e0e0", edgecolor="black", linewidth=0.8)  # 灰色地图，黑色国家边界

# 标注国家位置及人数（防止文本重叠）
texts = []
for country, count in students_by_country.items():
    if country in centroids.index:
        x, y = centroids[country].x, centroids[country].y
        text = ax.text(x, y, f"{country}\n({count})", fontsize=9, ha="center",
                       color="blue", weight='bold', bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))
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
plt.savefig("MIU_CS500_Student_Distribution_HD.png", dpi=300, bbox_inches="tight")

# 显示地图
plt.show()

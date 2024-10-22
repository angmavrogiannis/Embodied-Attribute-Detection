import matplotlib.pyplot as plt
# plt.style.use('ggplot')
plt.rcParams.update({'font.size': 30})

fig, ax = plt.subplots()

weight_modules = ['OVD', 'OVD (sup)', 'VQA', 'VQA (sup)', 'VQA\nGPT-3.5', 'VQA\nGPT-4']
weight_averages = [0.42, 0.36, 0.54, 0.36, 0.84, 0.93]
size_modules = ['OVD', 'OVD (sup)', 'OVD\nGPT-3.5', 'OVD (sup)\nGPT-3.5', 'OVD\nGPT-4']
size_averages = [0.445, 0.501, 0.82, 0.8, 0.84]
location_modules = ['OVD', 'OVD + GPT-3.5', 'OVD + GPT-4']
location_averages = [0.35, 0.6, 0.82]
# bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = colors = [color['color'] for color in list(plt.rcParams['axes.prop_cycle'])]# ['tab:red', 'tab:blue', 'tab:red', 'tab:orange', 'tab:blue', 'tab:gray']
# width = 0.1
# positions = (0.2, 0.4, 0.6)
# ax.bar(positions, averages, color=bar_colors, width=width)
ax.grid()
ax.set_axisbelow(True)
location_colors = ['#edf8b1','#7fcdbb','#2c7fb8']
size_colors = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3']# ['#ffffcc','#a1dab4','#41b6c4','#2c7fb8','#253494']
weight_colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c']
ax.bar(weight_modules, weight_averages, color=weight_colors, edgecolor="black", linewidth=5) # ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3']
# ax.bar(location_modules, location_averages, color=location_colors, edgecolor="black", linewidth=5)
# ax.bar(size_modules, size_averages, color=size_colors, edgecolor="black", linewidth=5)

ax.set_ylabel('Accuracy', weight="bold")
ax.set_title('Weight Attribute - Model Accuracy', weight="bold")
# plt.xticks(positions, modules)
# ax.legend(title='Fruit color')
# ax.set_xlim(-margin, len(modules))
plt.legend(title='sup: superlative \nadjective form', fontsize="1")
plt.show()
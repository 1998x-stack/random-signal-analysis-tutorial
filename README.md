# 随机信号分析 · 从不确定性到可计算的规律

面向通信、控制、信号处理和统计推断的 **28 章中文开放教程**。把概率事件、随机变量、相关与功率谱、随机系统、估计与检测连接成一条推理路线。每一篇文章应当独立可读，不依赖教师口述，也不假定读者已经阅读其他章节。

**课程首页**：https://1998x-stack.github.io/random-signal-analysis-tutorial/ （是否已对外部署请以 GitHub Pages 状态和构建日志为准）。

## 学习路线

| 阶段 | 章节 | 核心问题 |
| --- | --- | --- |
| I · 概率基础 | 01–05 | 如何以事件、分布和数字特征描述不确定性？ |
| II · 随机过程与谱 | 06–11 | 过程是否平稳？相关结构如何映射到频谱？ |
| III · 系统与模型 | 12–19 | 随机输入经过系统如何改变？常见过程怎么建模？ |
| IV · 统计推断与应用 | 20–28 | 怎样从带噪数据中估计、滤波、检测并验证算法？ |

## 本轮已深度重写

- **[01 概率与贝叶斯检测](chapters/01.html)**：随机相位与样本路径、概率空间、条件概率、10,000 次观测的期望计数贝叶斯树、不相关但不独立的反例。
- **[02 随机变量与分布](chapters/02.html)**：样本空间映射、离散 CDF 跳跃、连续 PDF 面积、含原子质量的混合分布。
- **[03 高斯与多维分布](chapters/03.html)**：中心极限定理的条件、高斯覆盖率、联合/边缘/条件分布、协方差椭圆和联合高斯条件推断。
- **[04 数字特征](chapters/04.html)**：条件期望、方差和切比雪夫、协方差、反例与特征函数（4 SVG）。
- **[05 变量变换与极限定理](chapters/05.html)**：平方变换 Jacobian、Rayleigh/Rice、特征函数和 LLN/CLT（4 SVG）。
- **[06 随机过程基本概念](chapters/06.html)**：样本路径、相同边缘不同相关、WSS 与各态历经（4 SVG）。

这三篇采用统一的语义化 HTML、独立 SVG、原生 MathML、轻量交互与可复现校验。**04–06 章已完成第二批深度改写；07–28 章仍是原有正文，仅作结构迁移。**

## 本地预览

无需打包工具，也不依赖在线字体或数学排版 CDN：

```bash
python3 -m http.server 8000
# 浏览 http://localhost:8000/
```

首页和阅读页面的基本内容在关闭 JavaScript 时仍然存在。JS 仅增强目录检索与三个数值交互。

## 仓库布局

```text
.
├── index.html                 # GitHub Pages 静态课程首页
├── courses.json               # 全课程元数据（路径/精修状态）
├── chapters/
│   ├── 01.html … 03.html      # 第一轮深度重构
│   ├── 04.html … 28.html      # 完整迁移的现有正文
│   ├── index.html             # 历史章节导航兼容入口
│   └── theme.css              # 历史页面兼容样式
├── assets/
│   ├── css/site.css           # 全站新设计系统
│   ├── js/site.js             # 渐进增强交互
│   └── svg/*.svg              # 21 张原创科学示意图
├── examples/test_intro_math.py
├── scripts/validate_site.py
├── .github/workflows/site.yml
├── AGENTS.md
├── 01.html … 28.html          # 旧地址的轻量跳转页
└── README.md
```

历史链接 `/01.html` 至 `/28.html` 使用 HTML 跳转到 `/chapters/NN.html`。原始 07–28 章的相互链接仍然相对于 `chapters/` 解析，不修改其未经审校的正文语义。

## 验收

```bash
python3 scripts/validate_site.py
python3 -m unittest discover -s examples -p 'test_*.py' -v
```

校验覆盖全部 28 章是否存在、旧 URL 跳转、首页静态课程链接、局部资源和站内锚点、图片替代文本、首次重写章节唯一 H1 与 MathML、SVG XML 结构和 21 张图解的标题/描述。另需按 `AGENTS.md` 在浏览器中人工检查 1440px / 390px / 360px、键盘焦点、MathML 与图形实际显示；**自动静态检查不等于浏览器截图验收**。

## GitHub Pages

静态网站的入口是**仓库根目录的** `index.html`，所有 URL 使用适用于项目子路径的相对路径。GitHub 仓库中选择 **Settings → Pages → Deploy from a branch → main / (root)**（如果当前配置尚未启用）。代码合并并不等于 Pages 已成功部署，必须检查 Pages 构建状态与在线链接。

## 参考资料

- [MIT OpenCourseWare — Introduction to Probability](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/)
- [NIST — Engineering Statistics Handbook](https://www.itl.nist.gov/div898/handbook/)
- [Penn State — STAT 414 Bivariate Normal](https://online.stat.psu.edu/stat414/Lesson21)
- [Penn State — STAT 505 Multivariate Normal](https://online.stat.psu.edu/stat505/Lesson04)
- [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts) 用作叙事、视觉与验证流程的参考，所有插图与正文均独立创作。

欢迎通过 Issues / Pull Requests 纠正错误、补充可复现例子或提交后续章节精修。贡献前阅读 [AGENTS.md](AGENTS.md)。

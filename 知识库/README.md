# 割草机产品知识库

本知识库基于当前工程目录中的单页、官网文档、参数表、快速指南、说明书、竞品分析与产品 ID 图自动整理生成。

## 使用说明
- 适合产品运营、市场、售前在内部快速查找产品定位、卖点、参数与素材覆盖情况。
- 产品分类与部分场景标签为基于现有资料的整理性推断，不等同于最终对外发布口径。
- 如目录内新增或替换资料，可重新运行 `python3 知识库/scripts/build_knowledge_base.py` 刷新。

## 产品总览

| 产品 | 推断分类 | 主要场景 | 关键指标 | 资料完备度 | 页面 |
| --- | --- | --- | --- | --- | --- |
| FL3000 | 家用 / 轻商用 LiDAR 智能割草机（基于现有文案推断） | 家庭庭院、小型商业场所 | Recommended mowing area：3000 m² (0.75 acre) | 高（7/8） | [FL3000.md](products/FL3000.md) |
| FR4000 | 大面积住宅 / 轻商用智能割草机（基于参数与资料分布推断） | 大宅草坪、轻商用园林 | Recommended mowing area: 4000 m² (1 acre)* | 中高（6/8） | [FR4000.md](products/FR4000.md) |
| FRX | 专业运动场 / 高尔夫割草机器人（基于单页文案推断） | 运动场、高尔夫球场 | Max mowing area per charge: / 8000㎡ | 中高（5/8） | [FRX.md](products/FRX.md) |
| FV2000 | 家用智能割草机（基于单页文案推断） | 家庭庭院 | Recommended mowing area: 2000 m² (0.5 acres)* | 高（7/8） | [FV2000.md](products/FV2000.md) |
| RCM01 | 高端滚刀式专业草坪机器人（基于单页与官网文案推断） | 高尔夫球场、体育场 premium turf | Max mowing area* / 72h Maximum coverage 28,800㎡ (7 acres) / 24h Maximum coverage 86,400… | 高（7/8） | [RCM01.md](products/RCM01.md) |
| RM21 | 多功能平台型草坪机器人（基于单页与官网文案推断） | 运动场、高尔夫球场、果园、草皮农场 | 72-hour max mowing area: / Fast charging mode: 108,000㎡ (26.7 acres) / Standard chargin… | 高（7/8） | [RM21.md](products/RM21.md) |
| Titan | 大型场地旗舰级割草 / 划线二合一平台（基于单页与官网文案推断） | 高尔夫球场、运动场、公共绿地 | Max mowing area* / 72 h Maximum coverage 108,000 ㎡ (26.7 acres) / 24 h Maximum coverage… | 高（7/8） | [Titan.md](products/Titan.md) |

## 资料缺口提醒
- FL3000：缺少 单页源文档
- FR4000：缺少 单页源文档；缺少 官网文档
- FRX：缺少 官网文档；缺少 竞品分析；缺少 产品 ID 图
- FV2000：缺少 官网文档
- RCM01：缺少 快速指南
- RM21：缺少 竞品分析
- Titan：缺少 竞品分析

## 目录说明
- `products/`：每个产品一页，包含定位摘要、核心卖点、参数、资料索引和竞品参考。
- `agent/`：深色产品资料集成网页，支持搜索、点选和在线预览。
- `scripts/`：知识库生成脚本，便于后续重复整理。

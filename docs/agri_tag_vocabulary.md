# 农业领域 Tag 词表（devbase repo_tags 命名空间约定）

**版本：** 0.1.0  
**日期：** 2026-04-17  
**命名空间：** `agri:` 前缀由农业领域独占，其他领域仿照（如 `med:`、`edu:`）。

---

## 一、词表结构

```
agri:<category>:<value>
```

| Category | 说明 | 示例 |
|----------|------|------|
| `crop` | 作物种类 | `agri:crop:rice`, `agri:crop:tomato` |
| `disease` | 病害/虫害名称 | `agri:disease:blast`, `agri:disease:leaf_blight` |
| `region` | 地理区域 | `agri:region:jiangsu`, `agri:region:heilongjiang` |
| `severity` | 严重程度 | `agri:severity:mild`, `agri:severity:severe` |
| `source` | 数据来源 | `agri:source:usda_ipm`, `agri:source:ai_agribench` |
| `status` | 记录状态 | `agri:status:verified`, `agri:status:draft` |

---

## 二、合法取值列表（基于当前 30 seed records + 扩展预留）

### 2.1 作物（crop）

```
rice, wheat, corn, tomato, potato, soybean, cotton,
apple, grape, citrus, pepper, cucumber, cabbage, strawberry
```

### 2.2 区域（region）

```
jiangsu, heilongjiang, henan, sichuan, guangdong,
xinjiang, shandong, hunan, hubei, anhui, yunnan
```

### 2.3 严重程度（severity）

```
mild, moderate, severe, critical
```

### 2.4 数据来源（source）

```
usda_ipm, ai_agribench, expert_manual, local_observation,
plantvillage, uc_ipm, ipmcenters
```

---

## 三、查询示例

```bash
# 查询所有水稻相关仓库/记录
devbase query --tag "agri:crop:rice"

# 前缀匹配：所有江苏地区的农业记录
devbase query --tag "agri:region:jiangsu"

# 组合查询：江苏地区的水稻病害
devbase query --tag "agri:crop:rice" --tag "agri:region:jiangsu"
```

> 注：前缀匹配 `LIKE 'agri:crop:%'` 在 SQLite 中可利用索引（当前 39 仓库规模无压力；破千后追加前缀索引）。

---

## 四、与 agri_observations 表的映射

| tag 形式 | 对应表字段 | 说明 |
|----------|-----------|------|
| `agri:crop:rice` | `agri_observations.crop = 'rice'` | 一对一 |
| `agri:region:jiangsu` | `agri_observations.region = 'jiangsu'` | 一对一 |
| `agri:severity:moderate` | `agri_observations.severity = 'moderate'` | 一对一 |
| `agri:source:usda_ipm` | `agri_observations.source = 'usda_ipm'` | 一对一 |

**设计意图**：`repo_tags` 提供轻量聚合索引，`agri_observations` 提供结构化详情。两者通过 `repo_id` 外键关联。

---

*本词表由 agri-paper 窗口代理维护，变更需同步通知 devbase 与 clarity-core。*

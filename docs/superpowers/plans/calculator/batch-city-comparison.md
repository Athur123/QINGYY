---
title: 企业选址成本批量对比分析 - 实现计划
module: calculator
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 企业选址成本批量对比分析 - 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重新设计社保公积金计算器，支持全国300+城市、1000+方案的大规模批量对比分析，提供虚拟滚动表格和智能分析报告。

**Architecture:** 在现有 `qingyang-calculator-optimized.html` 基础上，新增 `BatchComparisonManager` 类负责数据生成和管理，`VirtualTable` 组件实现高性能表格渲染，`AnalysisReport` 组件生成数据分析报告。使用纯前端虚拟滚动技术处理大规模数据。

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript (ES6+), 青阳云设计系统 CSS 变量

---

## 文件结构

| 文件 | 类型 | 说明 |
|------|------|------|
| `prototype/qingyang-calculator-optimized.html` | 修改 | 主文件，在现有基础上增加批量对比功能 |
| `prototype/data/cities.json` | 创建 | 全国300+城市社保基数数据 |
| `prototype/js/batch-comparison.js` | 创建 | BatchComparisonManager 类（建议内嵌到HTML中） |

---

## Task 1: 创建城市数据文件

**Files:**
- Create: `prototype/data/cities.json`

- [ ] **Step 1: 创建城市数据目录和文件**

```bash
mkdir -p prototype/data
touch prototype/data/cities.json
```

- [ ] **Step 2: 写入城市数据结构**

```json
{
  "cities": [
    {
      "code": "beijing",
      "name": "北京市",
      "province": "北京市",
      "tier": "tier1",
      "minBase": 6821,
      "maxBase": 35283,
      "rates": {
        "pension": { "company": 0.16, "personal": 0.08 },
        "medical": { "company": 0.098, "personal": 0.02 },
        "unemployment": { "company": 0.005, "personal": 0.005 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "shanghai",
      "name": "上海市",
      "province": "上海市",
      "tier": "tier1",
      "minBase": 7384,
      "maxBase": 36921,
      "rates": {
        "pension": { "company": 0.16, "personal": 0.08 },
        "medical": { "company": 0.10, "personal": 0.02 },
        "unemployment": { "company": 0.005, "personal": 0.005 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "guangzhou",
      "name": "广州市",
      "province": "广东省",
      "tier": "tier1",
      "minBase": 5284,
      "maxBase": 26421,
      "rates": {
        "pension": { "company": 0.14, "personal": 0.08 },
        "medical": { "company": 0.0685, "personal": 0.02 },
        "unemployment": { "company": 0.005, "personal": 0.005 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "shenzhen",
      "name": "深圳市",
      "province": "广东省",
      "tier": "tier1",
      "minBase": 2360,
      "maxBase": 26421,
      "rates": {
        "pension": { "company": 0.15, "personal": 0.08 },
        "medical": { "company": 0.06, "personal": 0.02 },
        "unemployment": { "company": 0.005, "personal": 0.005 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "hangzhou",
      "name": "杭州市",
      "province": "浙江省",
      "tier": "newTier1",
      "minBase": 4462,
      "maxBase": 22311,
      "rates": {
        "pension": { "company": 0.14, "personal": 0.08 },
        "medical": { "company": 0.09, "personal": 0.02 },
        "unemployment": { "company": 0.005, "personal": 0.005 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "nanjing",
      "name": "南京市",
      "province": "江苏省",
      "tier": "newTier1",
      "minBase": 4494,
      "maxBase": 22470,
      "rates": {
        "pension": { "company": 0.16, "personal": 0.08 },
        "medical": { "company": 0.08, "personal": 0.02 },
        "unemployment": { "company": 0.005, "personal": 0.005 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "chengdu",
      "name": "成都市",
      "province": "四川省",
      "tier": "newTier1",
      "minBase": 4246,
      "maxBase": 21228,
      "rates": {
        "pension": { "company": 0.16, "personal": 0.08 },
        "medical": { "company": 0.08, "personal": 0.02 },
        "unemployment": { "company": 0.006, "personal": 0.004 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "wuhan",
      "name": "武汉市",
      "province": "湖北省",
      "tier": "newTier1",
      "minBase": 4077,
      "maxBase": 20385,
      "rates": {
        "pension": { "company": 0.16, "personal": 0.08 },
        "medical": { "company": 0.08, "personal": 0.02 },
        "unemployment": { "company": 0.007, "personal": 0.003 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "xian",
      "name": "西安市",
      "province": "陕西省",
      "tier": "newTier1",
      "minBase": 4218,
      "maxBase": 21086,
      "rates": {
        "pension": { "company": 0.16, "personal": 0.08 },
        "medical": { "company": 0.08, "personal": 0.02 },
        "unemployment": { "company": 0.007, "personal": 0.003 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    },
    {
      "code": "changsha",
      "name": "长沙市",
      "province": "湖南省",
      "tier": "newTier1",
      "minBase": 4357,
      "maxBase": 26010,
      "rates": {
        "pension": { "company": 0.16, "personal": 0.08 },
        "medical": { "company": 0.08, "personal": 0.02 },
        "unemployment": { "company": 0.005, "personal": 0.005 },
        "injury": { "company": 0.004, "personal": 0 },
        "maternity": { "company": 0.008, "personal": 0 },
        "criticalIllness": { "company": 0, "personal": 180 }
      }
    }
  ],
  "salaryLevels": [5000, 8000, 10000, 15000, 20000],
  "fundRates": [5, 8, 10, 12]
}
```

**注意**: 实际使用时应该扩展至300+城市。现在先用10个城市作为测试数据。

- [ ] **Step 3: 验证JSON格式正确**

```bash
node -e "JSON.parse(require('fs').readFileSync('prototype/data/cities.json'))" && echo "JSON valid"
```

Expected: `JSON valid`

- [ ] **Step 4: Commit**

```bash
git add prototype/data/cities.json
git commit -m "feat: add city data for batch comparison"
```

---

## Task 2: 添加 BatchComparisonManager 类

**Files:**
- Modify: `prototype/qingyang-calculator-optimized.html` (在 script 标签中添加)

- [ ] **Step 1: 添加 BatchComparisonManager 类定义（在现有 CalculatorCompare 类之后）**

```javascript
// ========================================
// 批量对比管理器（支持大规模城市对比）
// ========================================
class BatchComparisonManager {
    constructor() {
        this.scenarios = [];           // 所有方案数据
        this.filteredScenarios = [];   // 筛选后的数据
        this.cities = [];              // 城市数据
        this.salaryLevels = [5000, 8000, 10000, 15000, 20000];
        this.fundRates = [5, 8, 10, 12];
        this.sortConfig = { column: null, direction: 'asc' };
        
        // 虚拟滚动配置
        this.rowHeight = 50;
        this.viewportHeight = 600;
        this.bufferSize = 5;
        this.scrollTop = 0;
        
        this.filters = {
            provinces: [],
            tiers: [],
            minCost: 0,
            maxCost: Infinity
        };
    }

    // 加载城市数据
    async loadCities() {
        try {
            const response = await fetch('data/cities.json');
            const data = await response.json();
            this.cities = data.cities;
            this.salaryLevels = data.salaryLevels || this.salaryLevels;
            this.fundRates = data.fundRates || this.fundRates;
            return true;
        } catch (error) {
            console.error('Failed to load cities:', error);
            showToast('加载城市数据失败', 'error');
            return false;
        }
    }

    // 生成所有方案组合
    generateScenarios() {
        this.scenarios = [];
        
        for (const city of this.cities) {
            for (const salary of this.salaryLevels) {
                for (const fundRate of this.fundRates) {
                    const scenario = this.calculateScenario(city, salary, fundRate);
                    this.scenarios.push(scenario);
                }
            }
        }
        
        this.filteredScenarios = [...this.scenarios];
        return this.scenarios.length;
    }

    // 计算单个方案
    calculateScenario(city, salary, fundRate) {
        // 计算缴费基数（受限于上下限）
        const base = Math.max(city.minBase, Math.min(city.maxBase, salary));
        
        // 计算社保成本
        let companySocial = 0;
        let personalSocial = 0;
        
        for (const [key, rate] of Object.entries(city.rates)) {
            if (key === 'criticalIllness') {
                companySocial += rate.company || 0;
                personalSocial += (rate.personal || 0) / 12; // 年度分摊到月
            } else {
                companySocial += base * (rate.company || 0);
                personalSocial += base * (rate.personal || 0);
            }
        }
        
        // 计算公积金
        const fundRateDecimal = fundRate / 100;
        const companyFund = base * fundRateDecimal;
        const personalFund = base * fundRateDecimal;
        
        // 合计
        const companyTotal = companySocial + companyFund;
        const personalTotal = personalSocial + personalFund;
        const grandTotal = companyTotal + personalTotal;
        
        return {
            id: `${city.code}_${salary}_${fundRate}`,
            cityCode: city.code,
            cityName: city.name,
            province: city.province,
            tier: city.tier,
            salary: salary,
            baseAmount: base,
            fundRate: fundRate,
            costs: {
                companySocial,
                companyFund,
                companyTotal,
                personalSocial,
                personalFund,
                personalTotal,
                grandTotal
            }
        };
    }

    // 排序
    sort(column, direction = 'asc') {
        this.sortConfig = { column, direction };
        
        this.filteredScenarios.sort((a, b) => {
            let aVal, bVal;
            
            if (column.startsWith('costs.')) {
                const key = column.replace('costs.', '');
                aVal = a.costs[key];
                bVal = b.costs[key];
            } else {
                aVal = a[column];
                bVal = b[column];
            }
            
            if (direction === 'asc') {
                return aVal - bVal;
            } else {
                return bVal - aVal;
            }
        });
    }

    // 筛选
    filter(filters) {
        this.filters = { ...this.filters, ...filters };
        
        this.filteredScenarios = this.scenarios.filter(s => {
            // 省份筛选
            if (this.filters.provinces.length > 0 && 
                !this.filters.provinces.includes(s.province)) {
                return false;
            }
            
            // 城市级别筛选
            if (this.filters.tiers.length > 0 && 
                !this.filters.tiers.includes(s.tier)) {
                return false;
            }
            
            // 成本区间筛选
            if (s.costs.grandTotal < this.filters.minCost || 
                s.costs.grandTotal > this.filters.maxCost) {
                return false;
            }
            
            return true;
        });
        
        // 重新应用排序
        if (this.sortConfig.column) {
            this.sort(this.sortConfig.column, this.sortConfig.direction);
        }
    }

    // 获取虚拟滚动可视范围
    getVisibleRange() {
        const startIndex = Math.floor(this.scrollTop / this.rowHeight);
        const visibleCount = Math.ceil(this.viewportHeight / this.rowHeight);
        
        const start = Math.max(0, startIndex - this.bufferSize);
        const end = Math.min(
            this.filteredScenarios.length, 
            startIndex + visibleCount + this.bufferSize
        );
        
        return { start, end };
    }

    // 获取TOP N最低成本城市
    getTopNCheapest(n = 10) {
        const sorted = [...this.scenarios].sort((a, b) => 
            a.costs.grandTotal - b.costs.grandTotal
        );
        return sorted.slice(0, n);
    }

    // 获取成本分布统计
    getCostDistribution() {
        const ranges = [
            { label: '< 5,000', min: 0, max: 5000, count: 0 },
            { label: '5,000 - 8,000', min: 5000, max: 8000, count: 0 },
            { label: '8,000 - 12,000', min: 8000, max: 12000, count: 0 },
            { label: '12,000 - 20,000', min: 12000, max: 20000, count: 0 },
            { label: '> 20,000', min: 20000, max: Infinity, count: 0 }
        ];
        
        for (const s of this.scenarios) {
            const total = s.costs.grandTotal;
            for (const range of ranges) {
                if (total >= range.min && total < range.max) {
                    range.count++;
                    break;
                }
            }
        }
        
        return ranges;
    }

    // 获取最优成本区间建议
    getOptimalSalaryRange(employeeCount = 100) {
        const rangeStats = {};
        
        for (const s of this.scenarios) {
            const key = s.salary;
            if (!rangeStats[key]) {
                rangeStats[key] = {
                    salary: key,
                    totalCost: 0,
                    count: 0,
                    cities: []
                };
            }
            rangeStats[key].totalCost += s.costs.grandTotal;
            rangeStats[key].count++;
            rangeStats[key].cities.push(s.cityName);
        }
        
        // 计算平均值并排序
        const results = Object.values(rangeStats).map(r => ({
            salary: r.salary,
            avgCost: r.totalCost / r.count,
            annualCost: (r.totalCost / r.count) * employeeCount * 12,
            cityCount: r.count
        })).sort((a, b) => a.avgCost - b.avgCost);
        
        return results;
    }
}
```

- [ ] **Step 2: 初始化 BatchComparisonManager 实例**

在现有 `const app = new CalculatorApp();` 之后添加：

```javascript
// 批量对比管理器实例
const batchManager = new BatchComparisonManager();
```

- [ ] **Step 3: Commit**

```bash
git add prototype/qingyang-calculator-optimized.html
git commit -m "feat: add BatchComparisonManager class for large-scale comparison"
```

---

## Task 3: 添加虚拟滚动表格组件

**Files:**
- Modify: `prototype/qingyang-calculator-optimized.html` (添加CSS和HTML)

- [ ] **Step 1: 添加虚拟滚动表格CSS样式**

在 `<style>` 标签中添加：

```css
/* ========================================
   批量对比 - 虚拟滚动表格
   ======================================== */

.batch-comparison-container {
    margin-top: 24px;
    background: var(--qy-bg-primary);
    border: 1px solid var(--qy-border-200);
    border-radius: var(--qy-radius-lg);
    overflow: hidden;
}

.batch-comparison-header {
    padding: 16px 20px;
    border-bottom: 1px solid var(--qy-border-200);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.batch-comparison-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--qy-text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
}

.batch-comparison-count {
    font-size: 13px;
    color: var(--qy-text-secondary);
    font-weight: 400;
}

.virtual-table-container {
    position: relative;
    height: 600px;
    overflow: auto;
}

.virtual-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.virtual-table th {
    position: sticky;
    top: 0;
    background: var(--qy-bg-secondary);
    padding: 12px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    color: var(--qy-text-secondary);
    border-bottom: 1px solid var(--qy-border-200);
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
    z-index: 10;
}

.virtual-table th:hover {
    background: var(--qy-bg-tertiary);
}

.virtual-table th.sortable::after {
    content: '↕';
    margin-left: 6px;
    opacity: 0.3;
    font-size: 12px;
}

.virtual-table th.sort-asc::after {
    content: '↑';
    opacity: 1;
    color: var(--qy-primary-500);
}

.virtual-table th.sort-desc::after {
    content: '↓';
    opacity: 1;
    color: var(--qy-primary-500);
}

.virtual-table td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--qy-border-100);
    font-size: 14px;
    color: var(--qy-text-primary);
    height: 50px;
    box-sizing: border-box;
}

.virtual-table tr:hover td {
    background: var(--qy-bg-secondary);
}

.virtual-table .col-city {
    width: 120px;
    position: sticky;
    left: 0;
    background: var(--qy-bg-primary);
    z-index: 5;
}

.virtual-table th.col-city {
    z-index: 15;
    background: var(--qy-bg-secondary);
}

.virtual-table .col-salary {
    width: 100px;
    text-align: right;
}

.virtual-table .col-cost {
    width: 120px;
    text-align: right;
    font-family: 'Inter', monospace;
    font-variant-numeric: tabular-nums;
}

.virtual-table .col-cost.highlight {
    color: var(--qy-primary-600);
    font-weight: 600;
}

.virtual-spacer {
    visibility: hidden;
}

.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 100;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--qy-border-200);
    border-top-color: var(--qy-primary-500);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

- [ ] **Step 2: 添加虚拟滚动表格HTML结构**

在现有对比区域之后添加新的批量对比区域：

```html
<!-- 批量对比区域 -->
<section class="batch-comparison-section" id="batchComparisonSection" style="display: none;">
    <div class="batch-comparison-container">
        <div class="batch-comparison-header">
            <div class="batch-comparison-title">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="7" height="7"/>
                    <rect x="14" y="3" width="7" height="7"/>
                    <rect x="14" y="14" width="7" height="7"/>
                    <rect x="3" y="14" width="7" height="7"/>
                </svg>
                批量城市对比
                <span class="batch-comparison-count" id="batchCount">(0 个方案)</span>
            </div>
            <div class="batch-actions">
                <button class="qy-btn qy-btn--secondary" onclick="exportBatchResults()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                    导出CSV
                </button>
            </div>
        </div>
        
        <div class="virtual-table-container" id="virtualTableContainer" onscroll="handleVirtualScroll()">
            <div class="loading-overlay" id="loadingOverlay">
                <div class="loading-spinner"></div>
                <p style="margin-top: 12px; color: var(--qy-text-secondary);">正在生成方案数据...</p>
            </div>
            
            <table class="virtual-table" id="virtualTable">
                <thead>
                    <tr>
                        <th class="col-city sortable" onclick="sortTable('cityName')">城市</th>
                        <th class="col-salary sortable" onclick="sortTable('salary')">薪资档位</th>
                        <th class="col-cost sortable" onclick="sortTable('costs.companyTotal')">单位成本</th>
                        <th class="col-cost sortable" onclick="sortTable('costs.personalTotal')">个人成本</th>
                        <th class="col-cost sortable highlight" onclick="sortTable('costs.grandTotal')">总成本</th>
                        <th>公积金比例</th>
                    </tr>
                </thead>
                <tbody id="virtualTableBody">
                    <!-- 动态生成 -->
                </tbody>
            </table>
        </div>
    </div>
</section>
```

- [ ] **Step 3: 添加虚拟滚动渲染函数**

```javascript
// 虚拟滚动渲染
function renderVirtualTable() {
    const tbody = document.getElementById('virtualTableBody');
    const { start, end } = batchManager.getVisibleRange();
    const visibleData = batchManager.filteredScenarios.slice(start, end);
    
    // 计算总高度
    const totalHeight = batchManager.filteredScenarios.length * batchManager.rowHeight;
    const offsetTop = start * batchManager.rowHeight;
    
    let html = `<tr class="virtual-spacer" style="height: ${offsetTop}px;"><td colspan="6"></td></tr>`;
    
    for (const item of visibleData) {
        html += `
            <tr data-id="${item.id}">
                <td class="col-city">
                    <div style="font-weight: 600;">${item.cityName}</div>
                    <div style="font-size: 12px; color: var(--qy-text-secondary);">${item.province}</div>
                </td>
                <td class="col-salary">¥${item.salary.toLocaleString()}</td>
                <td class="col-cost">¥${item.costs.companyTotal.toFixed(2)}</td>
                <td class="col-cost">¥${item.costs.personalTotal.toFixed(2)}</td>
                <td class="col-cost highlight">¥${item.costs.grandTotal.toFixed(2)}</td>
                <td>${item.fundRate}%</td>
            </tr>
        `;
    }
    
    const remainingHeight = totalHeight - (end * batchManager.rowHeight);
    html += `<tr class="virtual-spacer" style="height: ${Math.max(0, remainingHeight)}px;"><td colspan="6"></td></tr>`;
    
    tbody.innerHTML = html;
}

// 滚动事件处理
function handleVirtualScroll() {
    const container = document.getElementById('virtualTableContainer');
    batchManager.scrollTop = container.scrollTop;
    requestAnimationFrame(renderVirtualTable);
}

// 排序处理
function sortTable(column) {
    let direction = 'asc';
    if (batchManager.sortConfig.column === column) {
        direction = batchManager.sortConfig.direction === 'asc' ? 'desc' : 'asc';
    }
    
    batchManager.sort(column, direction);
    
    // 更新表头排序状态
    document.querySelectorAll('.virtual-table th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    const thIndex = ['cityName', 'salary', 'costs.companyTotal', 'costs.personalTotal', 'costs.grandTotal'].indexOf(column);
    if (thIndex >= 0) {
        const th = document.querySelectorAll('.virtual-table th')[thIndex];
        th.classList.add(direction === 'asc' ? 'sort-asc' : 'sort-desc');
    }
    
    renderVirtualTable();
}

// 导出批量对比结果
function exportBatchResults() {
    if (batchManager.filteredScenarios.length === 0) {
        showToast('暂无数据可导出', 'warning');
        return;
    }
    
    let csv = '城市,省份,薪资档位,公积金比例,单位社保,单位公积金,单位合计,个人社保,个人公积金,个人合计,总成本\n';
    
    for (const s of batchManager.filteredScenarios) {
        csv += `${s.cityName},${s.province},${s.salary},${s.fundRate}%,`;
        csv += `${s.costs.companySocial.toFixed(2)},${s.costs.companyFund.toFixed(2)},${s.costs.companyTotal.toFixed(2)},`;
        csv += `${s.costs.personalSocial.toFixed(2)},${s.costs.personalFund.toFixed(2)},${s.costs.personalTotal.toFixed(2)},`;
        csv += `${s.costs.grandTotal.toFixed(2)}\n`;
    }
    
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `城市成本对比_${new Date().toLocaleDateString()}.csv`;
    link.click();
    
    showToast('导出成功', 'success');
}
```

- [ ] **Step 4: Commit**

```bash
git add prototype/qingyang-calculator-optimized.html
git commit -m "feat: add virtual scrolling table for batch comparison"
```

---

## Task 4: 添加分析报告组件

**Files:**
- Modify: `prototype/qingyang-calculator-optimized.html`

- [ ] **Step 1: 添加分析报告CSS样式**

```css
/* ========================================
   批量对比 - 分析报告
   ======================================== */

.analysis-report {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
}

.analysis-card {
    background: var(--qy-bg-primary);
    border: 1px solid var(--qy-border-200);
    border-radius: var(--qy-radius-lg);
    padding: 20px;
}

.analysis-card-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--qy-text-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.top10-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.top10-item {
    display: flex;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--qy-border-100);
}

.top10-item:last-child {
    border-bottom: none;
}

.top10-rank {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    margin-right: 12px;
}

.top10-rank.top3 {
    background: var(--qy-primary-500);
    color: white;
}

.top10-rank.other {
    background: var(--qy-bg-tertiary);
    color: var(--qy-text-secondary);
}

.top10-info {
    flex: 1;
}

.top10-city {
    font-weight: 500;
    color: var(--qy-text-primary);
}

.top10-province {
    font-size: 12px;
    color: var(--qy-text-secondary);
}

.top10-cost {
    text-align: right;
}

.top10-amount {
    font-weight: 600;
    color: var(--qy-primary-600);
    font-variant-numeric: tabular-nums;
}

.top10-savings {
    font-size: 12px;
    color: var(--qy-success-500);
}

.chart-container {
    height: 200px;
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    padding: 20px 0;
    gap: 8px;
}

.chart-bar {
    flex: 1;
    background: var(--qy-primary-200);
    border-radius: 4px 4px 0 0;
    min-width: 40px;
    position: relative;
    transition: background 0.2s;
}

.chart-bar:hover {
    background: var(--qy-primary-400);
}

.chart-bar-label {
    position: absolute;
    bottom: -24px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 11px;
    color: var(--qy-text-secondary);
    white-space: nowrap;
}

.chart-bar-value {
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 11px;
    font-weight: 600;
    color: var(--qy-text-primary);
}

.optimal-range-table {
    width: 100%;
    border-collapse: collapse;
}

.optimal-range-table th,
.optimal-range-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid var(--qy-border-100);
    font-size: 13px;
}

.optimal-range-table th {
    font-weight: 600;
    color: var(--qy-text-secondary);
}

.optimal-badge {
    display: inline-block;
    padding: 2px 8px;
    background: var(--qy-success-100);
    color: var(--qy-success-600);
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
}
```

- [ ] **Step 2: 添加分析报告HTML结构**

在批量对比容器内、虚拟表格之前添加：

```html
<!-- 分析报告 -->
<div class="analysis-report" id="analysisReport" style="padding: 20px; display: none;">
    <!-- TOP10最低成本城市 -->
    <div class="analysis-card">
        <div class="analysis-card-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            TOP10 成本最低城市
        </div>
        <ol class="top10-list" id="top10List">
            <!-- 动态生成 -->
        </ol>
    </div>
    
    <!-- 成本分布 -->
    <div class="analysis-card">
        <div class="analysis-card-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <line x1="8" y1="17" x2="8" y2="10"/>
                <line x1="12" y1="17" x2="12" y2="7"/>
                <line x1="16" y1="17" x2="16" y2="12"/>
            </svg>
            成本分布
        </div>
        <div class="chart-container" id="costDistributionChart">
            <!-- 动态生成 -->
        </div>
    </div>
    
    <!-- 最优薪资档位建议 -->
    <div class="analysis-card" style="grid-column: span 2;">
        <div class="analysis-card-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
            </svg>
            最优成本区间建议
            <span style="margin-left: auto; font-size: 12px; color: var(--qy-text-secondary);">
                基于员工规模: <input type="number" id="employeeCount" value="100" style="width: 60px; padding: 2px 6px; border: 1px solid var(--qy-border-200); border-radius: 4px;" onchange="updateOptimalRange()"> 人
            </span>
        </div>
        <table class="optimal-range-table" id="optimalRangeTable">
            <thead>
                <tr>
                    <th>薪资档位</th>
                    <th>平均月成本</th>
                    <th>预估年度成本</th>
                    <th>覆盖城市数</th>
                    <th>推荐</th>
                </tr>
            </thead>
            <tbody id="optimalRangeBody">
                <!-- 动态生成 -->
            </tbody>
        </table>
    </div>
</div>
```

- [ ] **Step 3: 添加分析报告渲染函数**

```javascript
// 渲染分析报告
function renderAnalysisReport() {
    const report = document.getElementById('analysisReport');
    report.style.display = 'grid';
    
    renderTop10List();
    renderCostDistribution();
    updateOptimalRange();
}

// 渲染TOP10列表
function renderTop10List() {
    const top10 = batchManager.getTopNCheapest(10);
    const globalAvg = batchManager.scenarios.reduce((sum, s) => sum + s.costs.grandTotal, 0) / batchManager.scenarios.length;
    
    const list = document.getElementById('top10List');
    list.innerHTML = top10.map((item, index) => {
        const savings = ((globalAvg - item.costs.grandTotal) / globalAvg * 100).toFixed(1);
        const rankClass = index < 3 ? 'top3' : 'other';
        
        return `
            <li class="top10-item">
                <span class="top10-rank ${rankClass}">${index + 1}</span>
                <div class="top10-info">
                    <div class="top10-city">${item.cityName}</div>
                    <div class="top10-province">${item.province}</div>
                </div>
                <div class="top10-cost">
                    <div class="top10-amount">¥${item.costs.grandTotal.toFixed(2)}</div>
                    <div class="top10-savings">省 ${savings}%</div>
                </div>
            </li>
        `;
    }).join('');
}

// 渲染成本分布图表
function renderCostDistribution() {
    const distribution = batchManager.getCostDistribution();
    const maxCount = Math.max(...distribution.map(d => d.count));
    
    const chart = document.getElementById('costDistributionChart');
    chart.innerHTML = distribution.map(item => {
        const height = (item.count / maxCount * 100).toFixed(1);
        return `
            <div class="chart-bar" style="height: ${height}%;" title="${item.label}: ${item.count}个城市">
                <span class="chart-bar-value">${item.count}</span>
                <span class="chart-bar-label">${item.label}</span>
            </div>
        `;
    }).join('');
}

// 更新最优区间建议
function updateOptimalRange() {
    const employeeCount = parseInt(document.getElementById('employeeCount').value) || 100;
    const optimalData = batchManager.getOptimalSalaryRange(employeeCount);
    
    const tbody = document.getElementById('optimalRangeBody');
    tbody.innerHTML = optimalData.map((item, index) => `
        <tr>
            <td>¥${item.salary.toLocaleString()}</td>
            <td>¥${item.avgCost.toFixed(2)}</td>
            <td>¥${item.annualCost.toLocaleString()}</td>
            <td>${item.cityCount} 个城市</td>
            <td>${index === 0 ? '<span class="optimal-badge">最优推荐</span>' : '-'}</td>
        </tr>
    `).join('');
}
```

- [ ] **Step 4: Commit**

```bash
git add prototype/qingyang-calculator-optimized.html
git commit -m "feat: add analysis report component with TOP10, distribution chart and optimal range"
```

---

## Task 5: 添加启动入口和初始化逻辑

**Files:**
- Modify: `prototype/qingyang-calculator-optimized.html`

- [ ] **Step 1: 添加批量对比启动按钮**

在现有对比区域之前添加启动入口：

```html
<!-- 批量对比启动区 -->
<section class="batch-comparison-launcher" style="margin: 24px 0;">
    <div class="detail-card">
        <div class="detail-card__header">
            <div class="detail-card__title">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="7" height="7"/>
                    <rect x="14" y="3" width="7" height="7"/>
                    <rect x="14" y="14" width="7" height="7"/>
                    <rect x="3" y="14" width="7" height="7"/>
                </svg>
                批量城市对比分析
            </div>
        </div>
        <div style="padding: 20px;">
            <p style="color: var(--qy-text-secondary); margin-bottom: 16px;">
                同时对比全国多个城市的社保公积金成本，支持排序筛选和智能分析，辅助企业选址决策。
            </p>
            <button class="qy-btn qy-btn--primary" onclick="launchBatchComparison()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
                开始批量对比
            </button>
        </div>
    </div>
</section>
```

- [ ] **Step 2: 添加初始化函数**

```javascript
// 启动批量对比
async function launchBatchComparison() {
    const section = document.getElementById('batchComparisonSection');
    const overlay = document.getElementById('loadingOverlay');
    
    section.style.display = 'block';
    overlay.style.display = 'flex';
    
    // 滚动到批量对比区域
    section.scrollIntoView({ behavior: 'smooth' });
    
    // 加载城市数据
    const loaded = await batchManager.loadCities();
    if (!loaded) {
        overlay.style.display = 'none';
        return;
    }
    
    // 生成方案数据
    const count = batchManager.generateScenarios();
    
    // 更新计数
    document.getElementById('batchCount').textContent = `(${count.toLocaleString()} 个方案)`;
    
    // 隐藏加载状态
    overlay.style.display = 'none';
    
    // 渲染表格和分析报告
    renderVirtualTable();
    renderAnalysisReport();
    
    showToast(`已生成 ${count} 个对比方案`, 'success');
}
```

- [ ] **Step 3: Commit**

```bash
git add prototype/qingyang-calculator-optimized.html
git commit -m "feat: add batch comparison launcher and initialization"
```

---

## 验证清单

完成所有任务后，验证以下功能：

- [ ] 城市数据文件 `prototype/data/cities.json` 存在且格式正确
- [ ] 点击"开始批量对比"按钮加载数据
- [ ] 虚拟滚动表格正常显示（只渲染视口内行）
- [ ] 点击表头可以排序（升序/降序切换）
- [ ] 分析报告显示TOP10最低成本城市
- [ ] 成本分布图表正确显示
- [ ] 最优薪资档位建议表格正确计算
- [ ] CSV导出功能正常工作
- [ ] 滚动时表格流畅无卡顿（60fps）

---

## Spec Coverage Check

| 设计文档要求 | 实现任务 |
|-------------|---------|
| 支持300+城市 | Task 1 (可扩展至300+) |
| 1000+方案生成 | Task 2 `generateScenarios()` |
| 虚拟滚动表格 | Task 3 VirtualTable |
| 可排序列 | Task 3 `sortTable()` |
| TOP10最低成本 | Task 4 `renderTop10List()` |
| 成本分布图表 | Task 4 `renderCostDistribution()` |
| 最优区间建议 | Task 4 `updateOptimalRange()` |
| CSV导出 | Task 3 `exportBatchResults()` |

---

## 执行选项

Plan complete and saved to `docs/superpowers/plans/2025-04-03-batch-city-comparison-plan.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session, batch execution with checkpoints

Which approach would you prefer?

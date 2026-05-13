(function () {
  const modules = [
    { id: 'reconciliation', name: '对账复核', mark: '对', description: '社保对账复核当前主线，包括规则汇总和统一明细核对。' },
    { id: 'calculator', name: '社保计算', mark: '算', description: '覆盖费用计算器、地区规则、政策库、二级户、参保档案和智能识别等原型。' },
    { id: 'employee', name: '员工管理', mark: '员', description: '员工档案、社保异动、费用明细和档案版本相关页面。' },
    { id: 'insurance-config', name: '参保配置', mark: '配', description: '参保规则配置和字段配置相关页面。' },
    { id: 'settlement', name: '结算方案', mark: '结', description: '结算计划、账单明细、费用分摊、费用归属和垫付相关页面。' },
    { id: 'approval', name: '审批管理', mark: '审', description: '审批模板配置和同步管理页面。' },
    { id: 'system', name: '系统', mark: '系', description: '日志查看、系统操作日志和汇总统计组件演示。' }
  ];

  const pages = [
    { id: 'reconciliation.summary', moduleId: 'reconciliation', title: '规则汇总', path: 'reconciliation/summary.html', status: 'main', isMain: true, description: '按规则、月度和状态汇总对账结果，支持进入明细核对。' },
    { id: 'reconciliation.unified', moduleId: 'reconciliation', title: '明细核对', path: 'reconciliation/unified.html', status: 'main', isMain: true, description: '统一承载系统账单、台账导入、自动匹配和人工确认流程。' },
    { id: 'reconciliation.obsolete', moduleId: 'reconciliation', title: '旧版三账单探索', path: 'reconciliation/obsolete/index.html', status: 'obsolete', isMain: false, description: '历史探索版本，仅保留参考，不作为当前对账复核原型入口。' },
    { id: 'calculator.index', moduleId: 'calculator', title: '费用计算器', path: 'calculator/index.html', status: 'main', isMain: true, description: '社保公积金费用测算入口，包含筛选和计算结果展示。' },
    { id: 'calculator.policy', moduleId: 'calculator', title: '政策库', path: 'calculator/policy.html', status: 'main', isMain: true, description: '社保公积金政策维护和查看页面。' },
    { id: 'calculator.regionRules', moduleId: 'calculator', title: '地区规则配置', path: 'calculator/region-rules.html', status: 'main', isMain: true, description: '按地区维护社保公积金规则配置。' },
    { id: 'calculator.subAccount', moduleId: 'calculator', title: '二级户管理', path: 'calculator/sub-account.html', status: 'main', isMain: true, description: '参保规则编辑中的二级户维护页面。' },
    { id: 'calculator.addInsuranceV2', moduleId: 'calculator', title: '社保增员 V2', path: 'calculator/add-insurance-v2.html', status: 'iteration', isMain: false, description: '社保增员流程的新版本原型。' },
    { id: 'calculator.addInsurance', moduleId: 'calculator', title: '社保增员旧版', path: 'calculator/add-insurance.html', status: 'iteration', isMain: false, description: '社保增员早期重设计页面。' },
    { id: 'calculator.formulaRecognitionV2', moduleId: 'calculator', title: '智能公式识别 V2', path: 'calculator/formula-recognition-v2.html', status: 'iteration', isMain: false, description: '公式识别交互的新版探索。' },
    { id: 'calculator.formulaRecognition', moduleId: 'calculator', title: '智能公式识别', path: 'calculator/formula-recognition.html', status: 'iteration', isMain: false, description: '公式识别能力的早期页面。' },
    { id: 'calculator.insuranceArchiveV2', moduleId: 'calculator', title: '参保档案 V2', path: 'calculator/insurance-archive-v2.html', status: 'iteration', isMain: false, description: '参保档案新版设计页面。' },
    { id: 'calculator.insuranceArchive', moduleId: 'calculator', title: '参保档案', path: 'calculator/insurance-archive.html', status: 'iteration', isMain: false, description: '参保档案优化设计页面。' },
    { id: 'calculator.redesign', moduleId: 'calculator', title: '计算器重设计', path: 'calculator/redesign.html', status: 'iteration', isMain: false, description: '社保公积金计算器重设计稿。' },
    { id: 'calculator.redesigned', moduleId: 'calculator', title: '费用计算器改版', path: 'calculator/redesigned.html', status: 'iteration', isMain: false, description: '费用计算器改版后的候选页面。' },
    { id: 'calculator.v2', moduleId: 'calculator', title: '计算器 V2', path: 'calculator/v2.html', status: 'iteration', isMain: false, description: '计算器第二版历史迭代。' },
    { id: 'calculator.v3', moduleId: 'calculator', title: '计算器 V3', path: 'calculator/v3.html', status: 'iteration', isMain: false, description: '计算器第三版历史迭代。' },
    { id: 'employee.detail', moduleId: 'employee', title: '员工档案', path: 'employee/detail.html', status: 'main', isMain: true, description: '员工档案详情的当前重设计页面。' },
    { id: 'employee.changeField', moduleId: 'employee', title: '异动字段采集', path: 'employee/change-field.html', status: 'main', isMain: true, description: '社保异动操作中的增员字段采集页面。' },
    { id: 'employee.costDetail', moduleId: 'employee', title: '员工费用明细', path: 'employee/cost-detail.html', status: 'main', isMain: true, description: '单员工费用明细查看页面。' },
    { id: 'employee.transactionList', moduleId: 'employee', title: '社保异动列表', path: 'employee/transaction-list.html', status: 'iteration', isMain: false, description: '社保异动列表优化设计页面。' },
    { id: 'employee.archiveVersion', moduleId: 'employee', title: '档案版本管理', path: 'employee/archive-version.html', status: 'iteration', isMain: false, description: '员工档案版本管理页面。' },
    { id: 'employee.detailV3', moduleId: 'employee', title: '员工详情 V3', path: 'employee/detail-v3.html', status: 'iteration', isMain: false, description: '员工详情第三版历史迭代。' },
    { id: 'employee.detailV2', moduleId: 'employee', title: '员工详情 V2', path: 'employee/detail-v2.html', status: 'iteration', isMain: false, description: '员工详情第二版历史迭代。' },
    { id: 'employee.detailOld', moduleId: 'employee', title: '员工详情旧版', path: 'employee/detail-old.html', status: 'iteration', isMain: false, description: '员工详情早期版本。' },
    { id: 'insuranceConfig.stepper', moduleId: 'insurance-config', title: '参保规则配置向导', path: 'insurance-config/stepper.html', status: 'main', isMain: true, description: '使用分步向导配置社保参保规则。' },
    { id: 'insuranceConfig.fieldCollection', moduleId: 'insurance-config', title: '字段采集配置', path: 'insurance-config/field-collection.html', status: 'main', isMain: true, description: '全局字段采集配置页面。' },
    { id: 'insuranceConfig.globalField', moduleId: 'insurance-config', title: '全局字段配置', path: 'insurance-config/global-field.html', status: 'iteration', isMain: false, description: '全局字段配置早期或备选页面。' },
    { id: 'insuranceConfig.fieldOnboarding', moduleId: 'insurance-config', title: '入职字段配置', path: 'insurance-config/field-onboarding.html', status: 'iteration', isMain: false, description: '入职管理场景字段配置页面。' },
    { id: 'insuranceConfig.fieldSettlement', moduleId: 'insurance-config', title: '结算字段配置', path: 'insurance-config/field-settlement.html', status: 'iteration', isMain: false, description: '结算明细场景字段配置页面。' },
    { id: 'settlement.plan', moduleId: 'settlement', title: '办理结算计划', path: 'settlement/plan.html', status: 'main', isMain: true, description: '结算方案列表和办理计划页面。' },
    { id: 'settlement.detail', moduleId: 'settlement', title: '账单明细', path: 'settlement/detail.html', status: 'main', isMain: true, description: '结算方案中的账单明细优化页面。' },
    { id: 'settlement.costAllocation', moduleId: 'settlement', title: '保险福利核算', path: 'settlement/cost-allocation.html', status: 'main', isMain: true, description: '保险福利费用核算和分摊页面。' },
    { id: 'settlement.advancePayment', moduleId: 'settlement', title: '申请垫付', path: 'settlement/advance-payment.html', status: 'iteration', isMain: false, description: '结算相关垫付申请页面。' },
    { id: 'settlement.costAttribution', moduleId: 'settlement', title: '费用归属固化', path: 'settlement/cost-attribution.html', status: 'demo', isMain: false, description: '调动和费用归属固化规则演示页面。' },
    { id: 'approval.templateManagement', moduleId: 'approval', title: '审批模板管理', path: 'approval/template-management.html', status: 'main', isMain: true, description: '审批模板列表、配置、同步状态和抽屉详情页面。' },
    { id: 'system.logViewer', moduleId: 'system', title: '日志查看', path: 'system/log-viewer.html', status: 'main', isMain: true, description: 'HRO 系统日志查看页面。' },
    { id: 'system.sysLog', moduleId: 'system', title: '系统操作日志', path: 'system/sys-log.html', status: 'main', isMain: true, description: '系统操作日志查询和浏览页面。' },
    { id: 'system.summaryDemo', moduleId: 'system', title: '汇总统计项演示', path: 'system/summary-demo.html', status: 'demo', isMain: false, description: '3 到 4 项汇总统计组件效果演示。' }
  ];

  const statusLabels = {
    main: '主线',
    iteration: '迭代',
    demo: '演示',
    obsolete: '已废弃'
  };

  function getRelativePrefix() {
    const marker = document.querySelector('[data-prototype-nav-root]');
    if (marker) return marker.getAttribute('data-prototype-nav-root') || '';
    return document.body.getAttribute('data-prototype-root') || '';
  }

  function resolvePath(path, rootPrefix) {
    return `${rootPrefix || ''}${path}`;
  }

  function renderSidebar(target) {
    const current = target.getAttribute('data-current') || '';
    const rootPrefix = target.getAttribute('data-root') || getRelativePrefix();
    const moduleBlocks = modules.map((module) => {
      const modulePages = pages.filter((page) => page.moduleId === module.id && page.isMain);
      if (!modulePages.length) return '';
      const pageLinks = modulePages.map((page) => {
        const active = page.id === current ? ' is-active' : '';
        const ariaCurrent = page.id === current ? ' aria-current="page"' : '';
        return `<a class="prototype-nav__item${active}" href="${resolvePath(page.path, rootPrefix)}"${ariaCurrent}>${page.title}</a>`;
      }).join('');
      return `<section class="prototype-nav__group"><h3 class="prototype-nav__group-title">${module.name}</h3>${pageLinks}</section>`;
    }).join('');

    target.innerHTML = `
      <aside class="prototype-nav" aria-label="原型导航">
        <div class="prototype-nav__brand">
          <strong>青阳云 HRO</strong>
          <span>Prototype</span>
        </div>
        <a class="prototype-nav__home" href="${rootPrefix || ''}index.html">返回原型入口</a>
        <nav class="prototype-nav__body">${moduleBlocks}</nav>
      </aside>
    `;
  }

  function renderIndex(target) {
    const rootPrefix = target.getAttribute('data-root') || '';
    const moduleCards = modules.map((module) => {
      const modulePages = pages.filter((page) => page.moduleId === module.id);
      const cards = modulePages.map((page) => `
        <a class="page-card${page.status === 'obsolete' ? ' page-card--obsolete' : ''}" href="${resolvePath(page.path, rootPrefix)}">
          <div>
            <div class="page-card__top">
              <h3 class="page-card__title">${page.title}</h3>
              <span class="badge badge--${page.status}">${statusLabels[page.status]}</span>
            </div>
            <p class="page-card__desc">${page.description}</p>
          </div>
          <span class="page-card__path">${page.path}</span>
        </a>
      `).join('');

      return `
        <section class="module" id="${module.id}">
          <div class="module__header">
            <div>
              <h2 class="module__title"><span class="module__mark">${module.mark}</span>${module.name}</h2>
              <p class="module__desc">${module.description}</p>
            </div>
            <span class="module__meta">${modulePages.length} 个页面</span>
          </div>
          <div class="page-grid">${cards}</div>
        </section>
      `;
    }).join('');

    target.innerHTML = moduleCards;
  }

  function init() {
    document.querySelectorAll('[data-prototype-nav]').forEach(renderSidebar);
    document.querySelectorAll('[data-prototype-index]').forEach(renderIndex);
  }

  window.QYPrototypeNav = {
    modules,
    pages,
    statusLabels,
    renderSidebar,
    renderIndex,
    init
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

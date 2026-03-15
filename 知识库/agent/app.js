(function () {
  const data = window.__FJD_AGENT_DATA__;
  const UI = {
    all: "All",
    noProductsFound: "No matching products found. Try another keyword.",
    noGridResults: "No products match the current search.",
    keyMetricFallback: "To be added",
    assetsUnit: "assets",
    gapCountSuffix: "items missing",
    noGaps: "No major gaps",
    noHighlights: "No core highlights extracted yet.",
    noSpecs: "No key specs extracted yet.",
    noCompetitors: "No competitor sheet detected, or no competitor names could be identified.",
    noGapsList: "Core materials are largely complete.",
    noMaterialsInFilter: "No materials under the current filter.",
    previewTitle: "Material Preview",
    noMaterialPreview: "No previewable materials are available for this product yet.",
    pdfHint: "If embedded PDF preview is not supported in this environment, use “Open Source File” in the top right.",
    noSpreadsheetData: "No spreadsheet data could be read.",
    emptyTable: "Empty sheet",
    noImages: "No images were found.",
    currentImage: "Current image",
    imageCount: "images",
    unsupportedPreview: "This file type does not support inline preview yet. Use “Open Source File” instead.",
    imageCountUnit: "images",
    spreadsheetPreview: "Spreadsheet preview",
    clickToPreview: "Preview on the right",
    coveragePrefix: "Coverage",
    docCountLabel: "assets",
  };
  const GROUP_LABELS = {
    "知识页": "Knowledge Page",
    "单页 PDF": "Brochure PDF",
    "单页源文档": "Brochure Source",
    "官网文档": "Website Copy",
    "参数表": "Specification Sheet",
    "快速指南": "Quick Start Guide",
    "说明书": "User Manual",
    "竞品分析": "Competitor Analysis",
    "产品 ID 图": "Product ID Images",
  };
  const FIXED_TRANSLATIONS = [
    ["家用 / 轻商用 LiDAR 智能割草机（基于现有文案推断）", "Residential / light commercial LiDAR robotic mower (inferred from current materials)"],
    ["大面积住宅 / 轻商用智能割草机（基于参数与资料分布推断）", "Large-property residential / light commercial robotic mower (inferred from specs and material coverage)"],
    ["专业运动场 / 高尔夫割草机器人（基于单页文案推断）", "Professional sports field / golf-course robotic mower (inferred from brochure copy)"],
    ["家用智能割草机（基于单页文案推断）", "Residential robotic mower (inferred from brochure copy)"],
    ["高端滚刀式专业草坪机器人（基于单页与官网文案推断）", "Premium reel-based turf robot (inferred from brochure and website materials)"],
    ["多功能平台型草坪机器人（基于单页与官网文案推断）", "Multi-function robotic turf platform (inferred from brochure and website materials)"],
    ["大型场地旗舰级割草 / 划线二合一平台（基于单页与官网文案推断）", "Flagship large-area mowing and line-marking platform (inferred from brochure and website materials)"],
    ["家庭庭院、小型商业场所", "Home gardens, small commercial sites"],
    ["大宅草坪、轻商用园林", "Large private lawns, light commercial landscaping"],
    ["运动场、高尔夫球场", "Sports fields, golf courses"],
    ["家庭庭院", "Home gardens"],
    ["高尔夫球场、体育场 premium turf", "Golf courses, stadium premium turf"],
    ["运动场、高尔夫球场、果园、草皮农场", "Sports fields, golf courses, orchards, turf farms"],
    ["高尔夫球场、运动场、公共绿地", "Golf courses, sports fields, public green spaces"],
    ["未提取到", "Not extracted"],
    ["缺少 单页源文档", "Missing brochure source file"],
    ["缺少 单页 PDF", "Missing brochure PDF"],
    ["缺少 官网文档", "Missing website copy file"],
    ["缺少 参数表", "Missing specification sheet"],
    ["缺少 快速指南", "Missing quick start guide"],
    ["缺少 说明书", "Missing user manual"],
    ["缺少 竞品分析", "Missing competitor analysis"],
    ["缺少 产品 ID 图", "Missing product ID images"],
    ["高（", "High ("],
    ["中高（", "Medium-High ("],
    ["中（", "Medium ("],
    ["低（", "Low ("],
    ["高", "High"],
    ["中高", "Medium-High"],
    ["中", "Medium"],
    ["低", "Low"],
    ["资料完备度", "Coverage"],
    ["当前目录下未发现该产品的竞品分析表，或表头未提取到竞品名称。", "No competitor sheet was found for this product, or competitor names could not be extracted from the header."],
    ["知识页", "Knowledge Page"],
    ["定位摘要", "Positioning Summary"],
    ["一句话定位", "One-line Positioning"],
    ["产品分类", "Product Classification"],
    ["主要场景", "Primary Scenarios"],
    ["描述摘要", "Description Summary"],
    ["核心卖点", "Core Highlights"],
    ["关键参数", "Key Specs"],
    ["资料覆盖", "Material Coverage"],
    ["完备度", "Coverage"],
    ["当前缺口", "Current Gaps"],
    ["文件索引", "File Index"],
    ["竞品参考", "Competitor Reference"],
    ["运营备注", "Operations Note"],
    ["单页源文档", "Brochure Source"],
    ["单页 PDF", "Brochure PDF"],
    ["官网文档", "Website Copy"],
    ["参数表", "Specification Sheet"],
    ["快速指南", "Quick Start Guide"],
    ["说明书", "User Manual"],
    ["竞品分析", "Competitor Analysis"],
    ["产品 ID 图", "Product ID Images"],
  ];

  if (!data || !Array.isArray(data.products) || data.products.length === 0) {
    document.body.innerHTML = '<main style="padding:24px;color:#edf5ef;background:#061117;font-family:Arial,sans-serif">Product data could not be loaded.</main>';
    return;
  }

  const state = {
    query: "",
    activeProductKey: getInitialProductKey(),
    activeMaterialPath: null,
    activeFilter: UI.all,
    activeSheetByPath: {},
    activeImageByPath: {},
  };

  const elements = {
    productSearch: document.getElementById("productSearch"),
    sidebarCount: document.getElementById("sidebarCount"),
    sidebarList: document.getElementById("sidebarList"),
    heroTitle: document.getElementById("heroTitle"),
    heroSlogan: document.getElementById("heroSlogan"),
    heroDescription: document.getElementById("heroDescription"),
    heroMeta: document.getElementById("heroMeta"),
    knowledgePageLink: document.getElementById("knowledgePageLink"),
    jumpPreviewButton: document.getElementById("jumpPreviewButton"),
    productGrid: document.getElementById("productGrid"),
    metricValue: document.getElementById("metricValue"),
    coverageValue: document.getElementById("coverageValue"),
    docCountValue: document.getElementById("docCountValue"),
    gapCountValue: document.getElementById("gapCountValue"),
    highlightsList: document.getElementById("highlightsList"),
    specList: document.getElementById("specList"),
    competitorList: document.getElementById("competitorList"),
    gapList: document.getElementById("gapList"),
    materialFilters: document.getElementById("materialFilters"),
    materialGroups: document.getElementById("materialGroups"),
    previewTitle: document.getElementById("previewTitle"),
    previewOpenLink: document.getElementById("previewOpenLink"),
    previewMeta: document.getElementById("previewMeta"),
    previewContainer: document.getElementById("previewContainer"),
    materialsSection: document.getElementById("materialsSection"),
  };

  elements.productSearch.addEventListener("input", (event) => {
    state.query = event.target.value.trim();
    const visibleProducts = getVisibleProducts();
    if (visibleProducts.length > 0 && !visibleProducts.some((product) => product.key === state.activeProductKey)) {
      state.activeProductKey = visibleProducts[0].key;
      state.activeFilter = UI.all;
      syncActiveMaterial();
      updateHash();
    }
    render();
  });

  elements.jumpPreviewButton.addEventListener("click", () => {
    elements.materialsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  window.addEventListener("hashchange", () => {
    const hashKey = getInitialProductKey();
    if (hashKey !== state.activeProductKey) {
      state.activeProductKey = hashKey;
      state.activeFilter = UI.all;
      syncActiveMaterial();
      render();
    }
  });

  syncActiveMaterial();
  render();

  function getInitialProductKey() {
    const raw = decodeURIComponent(window.location.hash.replace("#", ""));
    return getProduct(raw) ? raw : data.products[0].key;
  }

  function getProduct(key) {
    return data.products.find((product) => product.key === key);
  }

  function getVisibleProducts() {
    const query = state.query.toLowerCase();
    if (!query) {
      return data.products;
    }
    return data.products.filter((product) => {
      const haystack = [
        product.key,
        product.fullName,
        product.classification,
        product.scenarios,
        product.slogan,
      ]
        .join(" ")
        .toLowerCase();
      return haystack.includes(query);
    });
  }

  function flattenMaterials(product) {
    return product.documentGroups.flatMap((group) =>
      group.items.map((item) => ({
        ...item,
        groupLabel: group.label,
        groupKey: group.key,
      }))
    );
  }

  function syncActiveMaterial() {
    const product = getProduct(state.activeProductKey);
    if (!product) {
      state.activeMaterialPath = null;
      return;
    }
    const materials = flattenMaterials(product);
    if (materials.length === 0) {
      state.activeMaterialPath = null;
      return;
    }
    const hasCurrent = materials.some((item) => item.path === state.activeMaterialPath);
    if (!hasCurrent) {
      const firstPdf = materials.find((item) => item.type === "pdf");
      state.activeMaterialPath = (firstPdf || materials[0]).path;
    }
  }

  function getActiveMaterial(product) {
    const materials = flattenMaterials(product);
    return materials.find((item) => item.path === state.activeMaterialPath) || materials[0] || null;
  }

  function setActiveProduct(key) {
    if (!getProduct(key)) {
      return;
    }
    state.activeProductKey = key;
    state.activeFilter = UI.all;
    syncActiveMaterial();
    updateHash();
    render();
  }

  function updateHash() {
    window.location.hash = encodeURIComponent(state.activeProductKey);
  }

  function setActiveMaterial(path) {
    state.activeMaterialPath = path;
    renderMaterials();
    renderPreview();
  }

  function setActiveFilter(filter) {
    state.activeFilter = filter;
    renderMaterials();
  }

  function render() {
    renderSidebar();
    renderHero();
    renderProductGrid();
    renderStats();
    renderSummary();
    renderFilters();
    renderMaterials();
    renderPreview();
  }

  function renderSidebar() {
    const visibleProducts = getVisibleProducts();
    elements.sidebarCount.textContent = String(visibleProducts.length);
    if (visibleProducts.length === 0) {
      elements.sidebarList.innerHTML = `<div class="empty-state">${UI.noProductsFound}</div>`;
      return;
    }

    elements.sidebarList.innerHTML = visibleProducts
      .map((product) => {
        const activeClass = product.key === state.activeProductKey ? " active" : "";
        return `
          <button class="sidebar-item${activeClass}" type="button" data-product-key="${escapeHtml(product.key)}">
            <div class="sidebar-title">${escapeHtml(product.key)}</div>
            <div class="sidebar-meta">${escapeHtml(translateText(product.scenarios))}</div>
            <div class="sidebar-meta">${escapeHtml(coverageLabel(product.coverageLabel))} · ${product.docCount} ${UI.assetsUnit}</div>
          </button>
        `;
      })
      .join("");

    elements.sidebarList.querySelectorAll("[data-product-key]").forEach((button) => {
      button.addEventListener("click", () => setActiveProduct(button.dataset.productKey));
    });
  }

  function renderHero() {
    const product = getProduct(state.activeProductKey);
    elements.heroTitle.textContent = product.fullName;
    elements.heroSlogan.textContent = translateText(product.slogan);
    elements.heroDescription.textContent = translateText(product.description);
    elements.knowledgePageLink.href = product.knowledgePage;

    const chips = [
      translateText(product.classification),
      translateText(product.scenarios),
      `${UI.coveragePrefix} ${coverageLabel(product.coverageLabel)} (${product.coverageCount}/8)`,
    ];
    elements.heroMeta.innerHTML = chips.map((chip) => `<span class="chip">${escapeHtml(chip)}</span>`).join("");
  }

  function renderProductGrid() {
    const visibleProducts = getVisibleProducts();
    if (visibleProducts.length === 0) {
      elements.productGrid.innerHTML = `<div class="empty-state">${UI.noGridResults}</div>`;
      return;
    }

    elements.productGrid.innerHTML = visibleProducts
      .map((product) => {
        const activeClass = product.key === state.activeProductKey ? " active" : "";
        return `
          <button class="product-tile${activeClass}" type="button" data-product-key="${escapeHtml(product.key)}">
            <div>
              <div class="product-title">${escapeHtml(product.fullName)}</div>
              <div class="product-meta">${escapeHtml(translateText(product.classification))}</div>
            </div>
            <div>
              <div class="product-tagline">${escapeHtml(translateText(product.slogan))}</div>
              <div class="product-meta">${escapeHtml(translateText(product.scenarios))}</div>
            </div>
          </button>
        `;
      })
      .join("");

    elements.productGrid.querySelectorAll("[data-product-key]").forEach((button) => {
      button.addEventListener("click", () => setActiveProduct(button.dataset.productKey));
    });
  }

  function renderStats() {
    const product = getProduct(state.activeProductKey);
    elements.metricValue.textContent = translateText(product.specs[0] || UI.keyMetricFallback);
    elements.coverageValue.textContent = `${coverageLabel(product.coverageLabel)} (${product.coverageCount}/8)`;
    elements.docCountValue.textContent = `${product.docCount} ${UI.docCountLabel}`;
    elements.gapCountValue.textContent = product.gaps.length ? `${product.gaps.length} ${UI.gapCountSuffix}` : UI.noGaps;
  }

  function renderSummary() {
    const product = getProduct(state.activeProductKey);
    renderTextList(elements.highlightsList, product.highlights, UI.noHighlights);
    renderTextList(elements.specList, product.specs, UI.noSpecs);

    if (product.competitors.length > 0) {
      elements.competitorList.innerHTML = product.competitors
        .map((item) => `<span class="pill">${escapeHtml(translateText(item))}</span>`)
        .join("");
    } else {
      elements.competitorList.innerHTML = `<div class="empty-state">${UI.noCompetitors}</div>`;
    }

    renderTextList(elements.gapList, product.gaps, UI.noGapsList);
  }

  function renderTextList(container, items, emptyText) {
    if (!items || items.length === 0) {
      container.innerHTML = `<div class="empty-state">${escapeHtml(emptyText)}</div>`;
      return;
    }
    container.innerHTML = items.map((item) => `<div class="text-item">${escapeHtml(translateText(item))}</div>`).join("");
  }

  function renderFilters() {
    const product = getProduct(state.activeProductKey);
    const filters = [UI.all, ...product.documentGroups.map((group) => translateGroupLabel(group.label))];
    elements.materialFilters.innerHTML = filters
      .map((filter) => {
        const activeClass = filter === state.activeFilter ? " active" : "";
        return `<button class="chip is-filter${activeClass}" type="button" data-filter="${escapeHtml(filter)}">${escapeHtml(filter)}</button>`;
      })
      .join("");

    elements.materialFilters.querySelectorAll("[data-filter]").forEach((button) => {
      button.addEventListener("click", () => setActiveFilter(button.dataset.filter));
    });
  }

  function renderMaterials() {
    const product = getProduct(state.activeProductKey);
    const groups = product.documentGroups.filter(
      (group) => state.activeFilter === UI.all || translateGroupLabel(group.label) === state.activeFilter
    );

    if (groups.length === 0) {
      elements.materialGroups.innerHTML = `<div class="empty-state">${UI.noMaterialsInFilter}</div>`;
      return;
    }

    elements.materialGroups.innerHTML = groups
      .map((group) => {
        const cards = group.items
          .map((item) => {
            const activeClass = item.path === state.activeMaterialPath ? " active" : "";
            const meta =
              item.type === "gallery"
                ? `${item.count} ${UI.imageCountUnit}`
                : item.type === "spreadsheet"
                  ? UI.spreadsheetPreview
                  : UI.clickToPreview;
            return `
              <button class="material-card${activeClass}" type="button" data-material-path="${escapeHtml(item.path)}">
                <span class="material-type">${escapeHtml(materialTypeName(item.type))}</span>
                <div class="material-title">${escapeHtml(translateMaterialTitle(item))}</div>
                <div class="material-meta">${escapeHtml(meta)}</div>
              </button>
            `;
          })
          .join("");

        return `
          <section class="material-group">
            <h4>${escapeHtml(translateGroupLabel(group.label))}</h4>
            <div class="material-card-grid">${cards}</div>
          </section>
        `;
      })
      .join("");

    elements.materialGroups.querySelectorAll("[data-material-path]").forEach((button) => {
      button.addEventListener("click", () => setActiveMaterial(button.dataset.materialPath));
    });
  }

  function renderPreview() {
    const product = getProduct(state.activeProductKey);
    const material = getActiveMaterial(product);

    if (!material) {
      elements.previewTitle.textContent = UI.previewTitle;
      elements.previewMeta.innerHTML = "";
      elements.previewContainer.innerHTML = `<div class="empty-state">${UI.noMaterialPreview}</div>`;
      elements.previewOpenLink.href = product.knowledgePage;
      return;
    }

    elements.previewTitle.textContent = translateMaterialTitle(material);
    elements.previewOpenLink.href = material.path;
    elements.previewMeta.innerHTML = `
      <span class="chip">${escapeHtml(translateGroupLabel(material.groupLabel))}</span>
      <span class="chip">${escapeHtml(materialTypeName(material.type))}</span>
    `;

    if (material.type === "pdf") {
      elements.previewContainer.innerHTML = `
        <div class="preview-frame-wrap">
          <iframe src="${material.path}" title="${escapeHtml(material.title)}"></iframe>
        </div>
        <div class="empty-state">${UI.pdfHint}</div>
      `;
      return;
    }

    if (material.type === "spreadsheet") {
      renderSpreadsheet(material);
      return;
    }

    if (material.type === "gallery") {
      renderGallery(material);
      return;
    }

    if (material.type === "markdown") {
      elements.previewContainer.innerHTML = `
        <div class="markdown-preview">${formatMarkdown(translateText(material.content || ""))}</div>
      `;
      return;
    }

    elements.previewContainer.innerHTML = `
      <div class="markdown-preview">${UI.unsupportedPreview}</div>
    `;
  }

  function renderSpreadsheet(material) {
    const sheets = material.preview && Array.isArray(material.preview.sheets) ? material.preview.sheets : [];
    if (sheets.length === 0) {
      elements.previewContainer.innerHTML = `<div class="empty-state">${UI.noSpreadsheetData}</div>`;
      return;
    }

    const sheetIndex = Math.min(state.activeSheetByPath[material.path] || 0, sheets.length - 1);
    const activeSheet = sheets[sheetIndex];
    const headerHtml = activeSheet.headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("");
    const rowHtml = activeSheet.rows
      .map((row) => {
        const cells = activeSheet.headers
          .map((header) => `<td>${formatCell(row[header] || "")}</td>`)
          .join("");
        return `<tr>${cells}</tr>`;
      })
      .join("");

    elements.previewContainer.innerHTML = `
      <div class="sheet-tabs">
        ${sheets
          .map((sheet, index) => {
            const activeClass = index === sheetIndex ? " active" : "";
            return `<button class="sheet-tab${activeClass}" type="button" data-sheet-index="${index}">${escapeHtml(sheet.name)} <span class="muted">(${sheet.rowCount})</span></button>`;
          })
          .join("")}
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>${headerHtml}</tr>
          </thead>
          <tbody>${rowHtml || `<tr><td colspan="${activeSheet.headers.length || 1}">${UI.emptyTable}</td></tr>`}</tbody>
        </table>
      </div>
    `;

    elements.previewContainer.querySelectorAll("[data-sheet-index]").forEach((button) => {
      button.addEventListener("click", () => {
        state.activeSheetByPath[material.path] = Number(button.dataset.sheetIndex);
        renderPreview();
      });
    });
  }

  function renderGallery(material) {
    const images = Array.isArray(material.images) ? material.images : [];
    if (images.length === 0) {
      elements.previewContainer.innerHTML = `<div class="empty-state">${UI.noImages}</div>`;
      return;
    }
    const activeIndex = Math.min(state.activeImageByPath[material.path] || 0, images.length - 1);
    const activeImage = images[activeIndex];

    elements.previewOpenLink.href = activeImage.path;
    elements.previewContainer.innerHTML = `
      <div class="gallery-feature">
        <img src="${activeImage.path}" alt="${escapeHtml(activeImage.name)}">
      </div>
      <div class="preview-meta">${UI.currentImage}: ${escapeHtml(activeImage.name)} · ${images.length} ${UI.imageCount}</div>
      <div class="gallery-strip">
        ${images
          .map((image, index) => {
            const activeClass = index === activeIndex ? " active" : "";
            return `
              <button class="gallery-thumb${activeClass}" type="button" data-image-index="${index}">
                <img src="${image.path}" alt="${escapeHtml(image.name)}">
              </button>
            `;
          })
          .join("")}
      </div>
    `;

    elements.previewContainer.querySelectorAll("[data-image-index]").forEach((button) => {
      button.addEventListener("click", () => {
        state.activeImageByPath[material.path] = Number(button.dataset.imageIndex);
        renderPreview();
      });
    });
  }

  function materialTypeName(type) {
    if (type === "pdf") {
      return "PDF";
    }
    if (type === "spreadsheet") {
      return "Spreadsheet";
    }
    if (type === "gallery") {
      return "Gallery";
    }
    if (type === "markdown") {
      return "Knowledge Page";
    }
    return "File";
  }

  function translateGroupLabel(label) {
    return GROUP_LABELS[label] || translateText(label);
  }

  function translateMaterialTitle(material) {
    if (material.type === "markdown") {
      return String(material.title).replace("知识页", "Knowledge Page");
    }
    return translateText(material.title);
  }

  function coverageLabel(value) {
    return translateText(value);
  }

  function translateText(value) {
    let output = String(value);
    for (const [source, target] of FIXED_TRANSLATIONS) {
      output = output.split(source).join(target);
    }
    return output;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function formatCell(value) {
    return escapeHtml(translateText(value)).replace(/\n/g, "<br>");
  }

  function formatMarkdown(value) {
    return escapeHtml(value)
      .replace(/^### (.+)$/gm, "<strong>$1</strong>")
      .replace(/^## (.+)$/gm, "<strong>$1</strong>")
      .replace(/^# (.+)$/gm, "<strong>$1</strong>")
      .replace(/^- (.+)$/gm, "&bull; $1")
      .replace(/\n/g, "<br>");
  }
})();

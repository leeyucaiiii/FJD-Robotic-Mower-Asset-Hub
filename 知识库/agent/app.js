(function () {
  const data = window.__FJD_AGENT_DATA__;
  const UI = {
    onlineVersion: "Online Version",
    printVersion: "Print Version",
    noProductsFound: "No matching products found. Try another keyword.",
    noHighlights: "No core highlights extracted yet.",
    noCompetitors: "No competitor sheet detected, or no competitor names could be identified.",
    noMaterialsAvailable: "No materials are available for this product yet.",
    noSpecs: "No key specs extracted yet.",
    previewTitle: "Material Preview",
    noMaterialPreview: "No previewable materials are available for this product yet.",
    pdfHint: "PDF files are not auto-loaded in the public site. Use Download when you need the file.",
    noSpreadsheetData: "No spreadsheet data could be read.",
    emptyTable: "Empty sheet",
    noImages: "No images were found.",
    currentImage: "Current image",
    imageCount: "images",
    unsupportedPreview: "This file type does not support inline preview yet. Use “Open Source File” instead.",
    imageCountUnit: "images",
    spreadsheetPreview: "Spreadsheet preview",
    clickToPreview: "Preview on the right",
    downloadFile: "Download",
    previewFile: "Preview",
  };
  const PRODUCT_DISPLAY_ORDER = ["RCM01", "RM21", "Titan", "FRX", "FR4000", "FL3000", "FV2000"];
  const CATEGORY_ORDER = [
    "Golf Course Robots",
    "Residential Robotic Mowers",
  ];
  const PRODUCT_CATEGORY_MAP = {
    RCM01: "Golf Course Robots",
    RM21: "Golf Course Robots",
    Titan: "Golf Course Robots",
    FRX: "Golf Course Robots",
    FR4000: "Residential Robotic Mowers",
    FL3000: "Residential Robotic Mowers",
    FV2000: "Residential Robotic Mowers",
  };
  const BROCHURE_LANGUAGE_ORDER = ["EN", "DE", "FR", "ES", "JA", "IT", "CN"];
  const MATERIAL_GROUP_ORDER = ["单页 PDF", "说明书", "快速指南", "参数表"];
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
  const SLOGAN_FALLBACKS = {
    FRX: "Professional Lawn Management Made Affordable.",
    FR4000: "Smart Mowing for Larger Lawns.",
    FV2000: "PRECISE MOWING, PERFECT LAWNS.",
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
    highlightsList: document.getElementById("highlightsList"),
    competitorList: document.getElementById("competitorList"),
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
      syncActiveMaterial();
      updateHash();
    }
    render();
  });

  window.addEventListener("hashchange", () => {
    const hashKey = getInitialProductKey();
    if (hashKey !== state.activeProductKey) {
      state.activeProductKey = hashKey;
      syncActiveMaterial();
      render();
    }
  });

  syncActiveMaterial();
  render();

  function getInitialProductKey() {
    const raw = decodeURIComponent(window.location.hash.replace("#", ""));
    return getProduct(raw) ? raw : PRODUCT_DISPLAY_ORDER.find((key) => getProduct(key)) || data.products[0].key;
  }

  function getProduct(key) {
    return data.products.find((product) => product.key === key);
  }

  function getVisibleProducts() {
    const query = state.query.toLowerCase();
    const filtered = data.products.filter((product) => {
      const haystack = [
        product.key,
        product.fullName,
        getProductCategory(product),
        product.classification,
        product.scenarios,
        product.slogan,
      ]
        .join(" ")
        .toLowerCase();
      return !query || haystack.includes(query);
    });
    return filtered.sort((a, b) => productRank(a.key) - productRank(b.key));
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
    const materials = getVisibleMaterialGroups(product).flatMap((group) =>
      group.items.map((item) => ({
        ...item,
        groupLabel: group.label,
        groupKey: group.key,
      }))
    );
    if (materials.length === 0) {
      state.activeMaterialPath = null;
      return;
    }
    const preferredPath = product.defaultPreview && product.defaultPreview.path;
    if (preferredPath && materials.some((item) => item.path === preferredPath)) {
      state.activeMaterialPath = preferredPath;
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

  function render() {
    renderSidebar();
    renderHero();
    renderSummary();
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

    const grouped = groupProductsByCategory(visibleProducts);
    elements.sidebarList.innerHTML = grouped
      .map(({ category, products }) => `
        <section class="sidebar-group">
          <h3 class="sidebar-group-title">${escapeHtml(category)}</h3>
          <div class="sidebar-group-items">
            ${products
              .map((product) => {
                const activeClass = product.key === state.activeProductKey ? " active" : "";
                return `
                  <button class="sidebar-item${activeClass}" type="button" data-product-key="${escapeHtml(product.key)}">
                    <div class="sidebar-title">${escapeHtml(product.key)}</div>
                    <div class="sidebar-meta">${escapeHtml(translateText(product.scenarios))}</div>
                  </button>
                `;
              })
              .join("")}
          </div>
        </section>
      `)
      .join("");

    elements.sidebarList.querySelectorAll("[data-product-key]").forEach((button) => {
      button.addEventListener("click", () => setActiveProduct(button.dataset.productKey));
    });
  }

  function renderHero() {
    const product = getProduct(state.activeProductKey);
    elements.heroTitle.textContent = product.fullName;
    const slogan = getDisplaySlogan(product);
    elements.heroSlogan.textContent = slogan;
    elements.heroSlogan.style.display = slogan ? "block" : "none";
    elements.heroDescription.textContent = translateText(product.description);

    const chips = [
      getProductCategory(product),
      translateText(product.classification),
      translateText(product.scenarios),
    ];
    elements.heroMeta.innerHTML = chips.map((chip) => `<span class="chip">${escapeHtml(chip)}</span>`).join("");
  }

  function renderSummary() {
    const product = getProduct(state.activeProductKey);
    renderTextList(elements.highlightsList, product.highlights, UI.noHighlights);

    if (product.competitors.length > 0) {
      elements.competitorList.innerHTML = product.competitors
        .map((item) => `<span class="pill">${escapeHtml(translateText(item))}</span>`)
        .join("");
    } else {
      elements.competitorList.innerHTML = `<div class="empty-state">${UI.noCompetitors}</div>`;
    }
  }

  function renderTextList(container, items, emptyText) {
    if (!items || items.length === 0) {
      container.innerHTML = `<div class="empty-state">${escapeHtml(emptyText)}</div>`;
      return;
    }
    container.innerHTML = items.map((item) => `<div class="text-item">${escapeHtml(translateText(item))}</div>`).join("");
  }

  function renderMaterials() {
    const product = getProduct(state.activeProductKey);
    const groups = getVisibleMaterialGroups(product);

    if (groups.length === 0) {
      elements.materialGroups.innerHTML = `<div class="empty-state">${UI.noMaterialsAvailable}</div>`;
      return;
    }

    elements.materialGroups.innerHTML = groups
      .map((group) => {
        const cards =
          group.label === "单页 PDF"
            ? renderBrochureSections(group)
            : group.label === "参数表"
              ? renderSpecificationCards(group)
              : `
                <div class="material-card-grid">
                  ${sortMaterialsForDisplay(group).map((item) => renderMaterialCard(group, item)).join("")}
                </div>
              `;

        return `
          <section class="material-group">
            <h4>${escapeHtml(translateGroupLabel(group.label))}</h4>
            ${cards}
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
      elements.previewOpenLink.style.display = "none";
      return;
    }

    const isSpecification = material.groupLabel === "参数表";
    elements.previewTitle.textContent = isSpecification ? translateGroupLabel(material.groupLabel) : translateMaterialTitle(material);
    elements.previewMeta.innerHTML = isSpecification
      ? ""
      : `
        <span class="chip">${escapeHtml(translateGroupLabel(material.groupLabel))}</span>
        <span class="chip">${escapeHtml(materialTypeName(material.type))}</span>
      `;
    elements.previewOpenLink.style.display = isSpecification ? "none" : "inline-flex";
    if (!isSpecification) {
      elements.previewOpenLink.href = material.path;
    }

    if (material.type === "pdf") {
      elements.previewContainer.innerHTML = `
        <div class="pdf-preview-placeholder">
          <div class="pdf-preview-label">PDF Selected</div>
          <div class="pdf-preview-title">${escapeHtml(translateMaterialTitle(material))}</div>
          <div class="pdf-preview-copy">${escapeHtml(UI.pdfHint)}</div>
        </div>
      `;
      return;
    }

    if (material.type === "spreadsheet") {
      renderSpreadsheet(material, product);
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

  function renderSpreadsheet(material, product) {
    if (material.groupLabel === "参数表") {
      elements.previewContainer.innerHTML = renderSpecificationPreview(product);
      return;
    }
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

  function getProductCategory(product) {
    return PRODUCT_CATEGORY_MAP[product.key] || "Other Products";
  }

  function groupProductsByCategory(products) {
    return CATEGORY_ORDER
      .map((category) => ({
        category,
        products: products
          .filter((product) => getProductCategory(product) === category)
          .sort((a, b) => productRank(a.key) - productRank(b.key)),
      }))
      .filter((group) => group.products.length > 0);
  }

  function productRank(productKey) {
    const index = PRODUCT_DISPLAY_ORDER.indexOf(productKey);
    return index === -1 ? PRODUCT_DISPLAY_ORDER.length : index;
  }

  function getVisibleMaterialGroups(product) {
    return MATERIAL_GROUP_ORDER
      .map((label) => product.documentGroups.find((group) => group.label === label))
      .filter(Boolean);
  }

  function renderBrochureSections(group) {
    const sorted = sortMaterialsForDisplay(group);
    const online = sorted.filter((item) => !isPrintBrochure(item));
    const print = sorted.filter((item) => isPrintBrochure(item));
    return [online.length ? renderMaterialSubgroup(UI.onlineVersion, group, online) : "", print.length ? renderMaterialSubgroup(UI.printVersion, group, print) : ""]
      .filter(Boolean)
      .join("");
  }

  function renderMaterialSubgroup(title, group, items) {
    return `
      <section class="material-subgroup">
        <h5>${escapeHtml(title)}</h5>
        <div class="material-card-grid">
          ${items.map((item) => renderMaterialCard(group, item)).join("")}
        </div>
      </section>
    `;
  }

  function renderMaterialCard(group, item) {
    const activeClass = item.path === state.activeMaterialPath ? " active" : "";
    const meta =
      item.type === "gallery"
        ? `${item.count} ${UI.imageCountUnit}`
        : item.type === "spreadsheet"
          ? UI.spreadsheetPreview
          : UI.clickToPreview;
    const downloadable = isDownloadableMaterial(group.label, item);
    const footer = `
      <div class="material-actions">
        <button class="material-action preview" type="button" data-material-path="${escapeHtml(item.path)}">${UI.previewFile}</button>
        ${downloadable ? `<a class="material-action download" href="${item.path}" download>${UI.downloadFile}</a>` : ""}
      </div>
    `;
    return `
      <article class="material-card${activeClass}">
        <span class="material-type">${escapeHtml(materialTypeName(item.type))}</span>
        <div class="material-title">${escapeHtml(translateMaterialTitle(item))}</div>
        <div class="material-meta">${escapeHtml(meta)}</div>
        ${footer}
      </article>
    `;
  }

  function renderSpecificationCards(group) {
    return `
      <div class="material-card-grid">
        ${sortMaterialsForDisplay(group).map((item) => renderSpecificationCard(item)).join("")}
      </div>
    `;
  }

  function renderSpecificationCard(item) {
    const activeClass = item.path === state.activeMaterialPath ? " active" : "";
    return `
      <article class="material-card${activeClass}">
        <span class="material-type">Specification</span>
        <div class="material-title">Specification Sheet</div>
        <div class="material-meta">${escapeHtml(UI.clickToPreview)}</div>
        <div class="material-actions">
          <button class="material-action preview" type="button" data-material-path="${escapeHtml(item.path)}">${UI.previewFile}</button>
        </div>
      </article>
    `;
  }

  function renderSpecificationPreview(product) {
    if (!product.specs || product.specs.length === 0) {
      return `<div class="empty-state">${escapeHtml(UI.noSpecs)}</div>`;
    }
    return `
      <div class="spec-preview-list">
        ${product.specs.map((item) => `<div class="text-item">${escapeHtml(translateText(item))}</div>`).join("")}
      </div>
    `;
  }

  function isDownloadableMaterial(groupLabel, material) {
    if (!material || !material.path) {
      return false;
    }
    return ["单页 PDF", "快速指南", "说明书"].includes(groupLabel);
  }

  function sortMaterialsForDisplay(group) {
    const items = Array.isArray(group.items) ? [...group.items] : [];
    if (group.label !== "单页 PDF") {
      return items;
    }
    return items.sort((a, b) => compareBrochures(a, b));
  }

  function compareBrochures(a, b) {
    const languageDiff = brochureLanguageRank(a.title) - brochureLanguageRank(b.title);
    if (languageDiff !== 0) {
      return languageDiff;
    }
    const printDiff = Number(isPrintBrochure(a)) - Number(isPrintBrochure(b));
    if (printDiff !== 0) {
      return printDiff;
    }
    return String(a.title).localeCompare(String(b.title));
  }

  function brochureLanguageRank(title) {
    const code = normalizeBrochureLanguage(title);
    const index = BROCHURE_LANGUAGE_ORDER.indexOf(code);
    return index === -1 ? BROCHURE_LANGUAGE_ORDER.length : index;
  }

  function normalizeBrochureLanguage(title) {
    const raw = String(title).match(/^([A-Z]+(?:\([A-Za-z]+\))?)/);
    const code = raw ? raw[1] : "";
    if (code.startsWith("JP")) {
      return "JA";
    }
    if (code.startsWith("CN")) {
      return "CN";
    }
    return code;
  }

  function isPrintBrochure(item) {
    return String(item.title).toLowerCase().includes("(for print)");
  }

  function getDisplaySlogan(product) {
    const slogan = translateText(product.slogan || "");
    if (slogan && slogan !== "Not extracted") {
      return slogan;
    }
    return SLOGAN_FALLBACKS[product.key] || "";
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

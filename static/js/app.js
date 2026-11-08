// Project Udyam Digital - Core Frontend Application
let currentLanguage = 'en';
let currentSegment = 'micro';
let currentContractTerm = 12;
let currentRecommendation = null;
let activeAddons = new Set();
let debounceTimer = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  triggerRecommendation();
  loadFunnelSummary();
  fetchLeads();
  runSpecimenVerification('K03'); // Default to clean specimen
});

// ==========================================
// LANGUAGE SWITCHER
// ==========================================
function changeLanguage(lang) {
  currentLanguage = lang;
  triggerRecommendation();
  
  const welcomeReplies = {
    en: "Namaste! I am your Airtel Udyam Digital Advisor. Tell me about your business (e.g. 'I run a 2-doctor clinic in Nagpur with 6 staff') and I will configure the ideal bundle in seconds.",
    hi: "नमस्ते! मैं आपका एयरटेल उद्यम डिजिटल सलाहकार हूँ। मुझे अपने व्यापार के बारे में बताएं (जैसे: 'नागपुर में 2 डॉक्टरों का क्लिनिक है जिसमें 6 कर्मचारी हैं') और मैं तुरंत आपके लिए सही बंडल तैयार करूँगा।",
    hinglish: "Namaste! Main aapka Airtel Udyam Advisor hoon. Apne business ke baare me batayein aur main aapke liye best digital bundle configure karunga.",
    ta: "வணக்கம்! நான் உங்கள் ஏர்டெல் உத்யம் டிஜிட்டல் ஆலோசகர். உங்கள் வணிகத்தைப் பற்றி கூறுங்கள், உங்களுக்கான சரியான பேக்கை உருவாக்குகிறேன்."
  };

  const consentTexts = {
    en: "We collect your Business Registration (GSTIN/Udyam), Address Proof, and Signatory ID strictly for the purpose of statutory telecommunications service provisioning. Raw documents are automatically purged after 30 days. PII is masked across all partner dashboards.",
    hi: "हम आपके व्यापार पंजीकरण (जीएसटीआईएन/उद्यम), पते का प्रमाण, और हस्ताक्षरकर्ता पहचान केवल दूरसंचार सेवा चालू करने के उद्देश्य से एकत्र करते हैं। 30 दिनों के बाद मूल दस्तावेज स्वतः मिटा दिए जाते हैं।",
    hinglish: "Hum aapke business documents strictly telecom verification ke liye collect karte hain. 30 days ke baad raw documents auto-purge ho jaate hain.",
    ta: "தொலைத்தொடர்பு சேவைகளுக்காக மட்டுமே உங்கள் வணிக ஆவணங்களை சேகரிக்கிறோம். 30 நாட்களுக்குப் பிறகு அசல் ஆவணங்கள் அழிக்கப்படும்."
  };

  document.getElementById('consentText').innerText = consentTexts[lang] || consentTexts['en'];
  appendChatMessage(welcomeReplies[lang] || welcomeReplies['en'], 'bot');
}

// ==========================================
// SLIDER & ARCHETYPE CONTROLS
// ==========================================
function updateSlider(elementId, value) {
  document.getElementById(elementId).innerText = value;
}

function selectArchetype(seg) {
  currentSegment = seg;
  document.querySelectorAll('.archetype-btn').forEach(btn => btn.classList.remove('active'));
  event.currentTarget.classList.add('active');

  const empSlider = document.getElementById('inputEmployees');
  const sitesSlider = document.getElementById('inputSites');

  if (seg === 'micro') {
    empSlider.value = 4;
    sitesSlider.value = 1;
  } else if (seg === 'prof') {
    empSlider.value = 8;
    sitesSlider.value = 1;
  } else if (seg === 'multi') {
    empSlider.value = 25;
    sitesSlider.value = 3;
  } else if (seg === 'mfg') {
    empSlider.value = 40;
    sitesSlider.value = 2;
  }

  updateSlider('valEmployees', empSlider.value);
  updateSlider('valSites', sitesSlider.value);
  triggerRecommendation();
}

// ==========================================
// RECOMMENDATION ENGINE CALL
// ==========================================
async function triggerRecommendation() {
  const employees = parseInt(document.getElementById('inputEmployees').value);
  const sites = parseInt(document.getElementById('inputSites').value);
  const cityTier = parseInt(document.getElementById('selectCityTier').value);
  const hasGstin = document.getElementById('selectGstinStatus').value;

  const payload = {
    segment: currentSegment,
    employees: employees,
    sites: sites,
    city_tier: cityTier,
    has_gstin: hasGstin,
    language: currentLanguage
  };

  try {
    const res = await fetch('/api/advisor/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    currentRecommendation = data;
    renderRecommendation(data);
    renderAddonsMatrix(data);
    updateQuoteSummary();
  } catch (err) {
    console.error('Error fetching recommendation:', err);
  }
}

function renderRecommendation(data) {
  const container = document.getElementById('recommendationBanner');
  const bundle = data.primary_bundle;

  let itemsHtml = bundle.products.map(p => `
    <div class="rec-item">
      <div class="rec-item-title">
        <span>${p.name}</span>
        <span class="rec-item-cat">${p.category}</span>
      </div>
      <p class="rec-item-desc">${p.description}</p>
      <div class="rec-item-rationale">
        <strong>Why for you:</strong> ${p.rationale}
      </div>
    </div>
  `).join('');

  container.innerHTML = `
    <div class="rec-header">
      <div class="rec-title-group">
        <small class="badge-tag">RECOMMENDED DIGITAL BUNDLE</small>
        <h3>${data.bundle_title}</h3>
      </div>
      <div class="text-right">
        <div class="stat-num">₹${bundle.total_monthly_with_gst} <small style="font-size:14px;color:var(--text-muted);">/mo (incl. GST)</small></div>
        <small class="text-muted">Installation in ~${bundle.estimated_install_days} days</small>
      </div>
    </div>
    <div class="rec-items-grid">
      ${itemsHtml}
    </div>
    <div class="d-flex justify-between align-center">
      <small class="text-muted">⚡ Includes 18% GST · 10% Bundle Discount Applied · Zero Paperwork</small>
      <a href="#quote" class="btn btn-primary btn-sm">Customize & Review Quote ➔</a>
    </div>
  `;
}

// ==========================================
// CONVERSATIONAL CHAT ADVISOR
// ==========================================
async function handleChatSubmit(e) {
  e.preventDefault();
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;

  appendChatMessage(text, 'user');
  input.value = '';

  try {
    const res = await fetch('/api/advisor/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        context: {
          language: currentLanguage,
          segment: currentSegment,
          employees: parseInt(document.getElementById('inputEmployees').value)
        }
      })
    });
    const data = await res.json();
    appendChatMessage(data.reply, 'bot');
    if (data.recommendation) {
      currentRecommendation = data.recommendation;
      renderRecommendation(data.recommendation);
      renderAddonsMatrix(data.recommendation);
      updateQuoteSummary();
    }
  } catch (err) {
    appendChatMessage("I'm having trouble connecting right now. Please try again.", 'bot');
  }
}

function appendChatMessage(msg, sender) {
  const container = document.getElementById('chatMessages');
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${sender}`;
  bubble.innerHTML = `<p>${msg}</p>`;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function simulateVoiceInput() {
  const prompts = [
    "I run a 2-doctor clinic in Nagpur with 8 staff. We need reliable internet for patient records and billing.",
    "Hamari Jaipur me kirana dukan hai, UPI payment atakna nahi chahiye.",
    "We operate a 3-outlet restaurant chain and need CCTV and backup line under one bill."
  ];
  const chosen = prompts[Math.floor(Math.random() * prompts.length)];
  document.getElementById('chatInput').value = chosen;
  handleChatSubmit(new Event('submit'));
}

// ==========================================
// QUOTE & ADD-ONS CALCULATOR
// ==========================================
function renderAddonsMatrix(data) {
  const container = document.getElementById('addonsList');
  if (!data || !data.primary_bundle) return;

  const currentProductIds = new Set(data.primary_bundle.products.map(p => p.product_id));

  // Available catalog add-ons
  const availableAddons = [
    { id: 'P09', name: 'Backup 4G/5G Wireless Failover', price: 499, desc: 'Auto-switches to 4G/5G if fiber line is interrupted' },
    { id: 'P11', name: 'Static Public IP', price: 200, desc: 'Required for Tally, billing server & CCTV remote access' },
    { id: 'P15', name: 'WhatsApp Business API Starter', price: 999, desc: 'Automated order alerts, bills & verified green badge' },
    { id: 'P17', name: 'Cloud Backup 1 TB Secure', price: 499, desc: 'Daily automated encrypted backup for Tally & customer data' },
    { id: 'P20', name: 'Endpoint Security Antivirus (5 PCs)', price: 495, desc: 'Protects office laptops and POS from malware & ransomware' },
    { id: 'P23', name: 'Cloud CCTV Surveillance (2 Cams)', price: 398, desc: 'Live mobile view without expensive on-premise DVR' }
  ];

  let html = '';
  availableAddons.forEach(addon => {
    const isIncludedInBase = currentProductIds.has(addon.id);
    const isChecked = isIncludedInBase || activeAddons.has(addon.id);

    html += `
      <div class="addon-row">
        <div class="addon-left">
          <input type="checkbox" id="chk_${addon.id}" ${isChecked ? 'checked' : ''} onchange="toggleAddon('${addon.id}', ${addon.price})">
          <div class="addon-text">
            <strong>${addon.name} ${isIncludedInBase ? '<span class="badge-tag">INCLUDED</span>' : ''}</strong>
            <small>${addon.desc}</small>
          </div>
        </div>
        <div class="addon-price">₹${addon.price}/mo</div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function toggleAddon(addonId, price) {
  if (activeAddons.has(addonId)) {
    activeAddons.delete(addonId);
  } else {
    activeAddons.add(addonId);
  }
  updateQuoteSummary();
}

function setContractTerm(months) {
  currentContractTerm = months;
  document.querySelectorAll('.term-btn').forEach(btn => btn.classList.remove('active'));
  event.currentTarget.classList.add('active');
  updateQuoteSummary();
}

function updateQuoteSummary() {
  if (!currentRecommendation) return;

  const bundle = currentRecommendation.primary_bundle;
  let baseMonthly = bundle.base_monthly_inr;

  // Add extra add-ons
  const currentProductIds = new Set(bundle.products.map(p => p.product_id));
  const addonPrices = { 'P09': 499, 'P11': 200, 'P15': 999, 'P17': 499, 'P20': 495, 'P23': 398 };

  activeAddons.forEach(id => {
    if (!currentProductIds.has(id)) {
      baseMonthly += addonPrices[id] || 0;
    }
  });

  // Term discount
  let discountPct = 10;
  if (currentContractTerm === 24) discountPct = 15;
  if (currentContractTerm === 36) discountPct = 20;

  const discountAmount = Math.round(baseMonthly * (discountPct / 100));
  const discountedMonthly = baseMonthly - discountAmount;
  const gst = Math.round(discountedMonthly * 0.18);
  const total = discountedMonthly + gst;

  document.getElementById('quoteBundleTitle').innerText = currentRecommendation.bundle_title;
  document.getElementById('priceBase').innerText = `₹${baseMonthly.toLocaleString('en-IN')}`;
  document.getElementById('labelDiscount').innerText = `Commitment Discount (${discountPct}%)`;
  document.getElementById('priceDiscount').innerText = `- ₹${discountAmount.toLocaleString('en-IN')}`;
  document.getElementById('priceGst').innerText = `₹${gst.toLocaleString('en-IN')}`;
  document.getElementById('priceTotal').innerHTML = `₹${total.toLocaleString('en-IN')} <small>/mo</small>`;

  if (currentContractTerm >= 24) {
    document.getElementById('priceSetup').innerText = '₹0 (Waived for 2yr+ Contract)';
  } else {
    document.getElementById('priceSetup').innerText = `₹${bundle.setup_fee_inr || 0}`;
  }

  document.getElementById('valInstallDays').innerText = `${bundle.estimated_install_days} Days`;
}

function proceedToKYC() {
  window.location.hash = '#kyc';
}

// ==========================================
// SMART KYC VALIDATOR ENGINE
// ==========================================
function switchKycTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  event.currentTarget.classList.add('active');

  if (tabName === 'specimen') document.getElementById('tabSpecimen').classList.add('active');
  if (tabName === 'fasttrack') document.getElementById('tabFasttrack').classList.add('active');
  if (tabName === 'upload') document.getElementById('tabUpload').classList.add('active');
}

async function runSpecimenVerification(applicantCode) {
  const container = document.getElementById('specimenResults');
  container.innerHTML = '<div class="text-center p-4">⏳ Running Computer Vision & Registry Cross-Checks...</div>';

  try {
    const res = await fetch('/api/kyc/verify-specimen', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ applicant_code: applicantCode })
    });
    const data = await res.json();
    renderKycResults(data);
  } catch (err) {
    container.innerHTML = '<div class="text-danger p-3">Error running verification check.</div>';
  }
}

function renderKycResults(data) {
  const container = document.getElementById('specimenResults');
  const isApproved = data.overall_status === 'APPROVED';

  let checksHtml = data.checks.map(c => `
    <div class="check-item">
      <div>
        <strong>${c.rule}</strong>
        <p class="text-muted" style="font-size:12px; margin-top:2px;">${c.detail}</p>
      </div>
      <div>
        <span class="check-status-badge ${c.passed ? 'badge-pass' : 'badge-fail'}">
          ${c.passed ? 'VERIFIED ✓' : 'FAILED ✗'}
        </span>
      </div>
    </div>
  `).join('');

  let issuesHtml = '';
  if (data.known_issues && data.known_issues.length > 0) {
    issuesHtml = `
      <div style="background:var(--danger-bg); border:1px solid var(--danger); padding:14px; border-radius:8px; margin-top:16px;">
        <strong style="color:var(--danger);">Planted KYC Issues Detected (Answer Key Match):</strong>
        <ul style="margin:8px 0 0 20px; font-size:12px; color:var(--text-dark);">
          ${data.known_issues.map(iss => `<li>${iss}</li>`).join('')}
        </ul>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="overall-status-box ${isApproved ? 'approved' : 'rejected'}">
      <div>
        <h4 style="font-size:16px; font-weight:800;">
          ${isApproved ? '✅ SMART KYC VERIFICATION PASSED' : '⚠️ KYC VERIFICATION FLAGGED / REJECTED'}
        </h4>
        <small>Applicant: <strong>${data.legal_name}</strong> | Constitution: ${data.constitution}</small>
        <div style="font-size:11px; margin-top:4px;">
          Masked GSTIN: <code>${data.masked_gstin}</code> · Masked Udyam: <code>${data.masked_udyam || 'N/A'}</code>
        </div>
      </div>
      <div>
        <span class="badge-tag" style="font-size:13px;">${data.applicant_code}</span>
      </div>
    </div>

    <div style="background:#FFF; border:1px solid var(--border-color); border-radius:8px;">
      ${checksHtml}
    </div>

    ${issuesHtml}

    ${isApproved ? `
      <div class="mt-4 text-right">
        <button class="btn btn-primary" onclick="confirmOrder('${data.business_name}')">
          Confirm Order & Generate Live Tracker ➔
        </button>
      </div>
    ` : `
      <div class="mt-4 text-right">
        <small class="text-danger" style="margin-right:12px;">Rectify flagged document before proceeding</small>
        <button class="btn btn-outline" onclick="document.getElementById('selectSpecimen').value='K03'; runSpecimenVerification('K03');">
          Switch to Clean Specimen (K03)
        </button>
      </div>
    `}
  `;
}

async function executeGstinLookup() {
  const gstin = document.getElementById('inputGstinLookup').value.trim();
  const resDiv = document.getElementById('lookupResults');
  resDiv.innerHTML = 'Verifying with mock GST registry...';

  const res = await fetch('/api/kyc/lookup-gstin', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ gstin: gstin })
  });
  const data = await res.json();
  if (data.found) {
    resDiv.innerHTML = `
      <div style="background:var(--success-bg); border:1px solid var(--success); padding:14px; border-radius:8px; margin-top:12px;">
        <strong style="color:var(--success);">GSTIN Found: ${data.legal_name}</strong>
        <p style="font-size:12px; margin-top:4px;">Status: <strong>${data.status}</strong> | Trade Name: ${data.trade_name} | State: ${data.state}</p>
        <small class="text-muted">Principal Place: ${data.address}</small>
      </div>
    `;
  } else {
    resDiv.innerHTML = `<div style="color:var(--danger); padding:12px;">${data.message}</div>`;
  }
}

async function executeUdyamLookup() {
  const udyam = document.getElementById('inputUdyamLookup').value.trim();
  const resDiv = document.getElementById('lookupResults');
  resDiv.innerHTML = 'Verifying with mock Udyam registry...';

  const res = await fetch('/api/kyc/lookup-udyam', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ udyam: udyam })
  });
  const data = await res.json();
  if (data.found) {
    resDiv.innerHTML = `
      <div style="background:var(--success-bg); border:1px solid var(--success); padding:14px; border-radius:8px; margin-top:12px;">
        <strong style="color:var(--success);">Udyam Found: ${data.enterprise_name}</strong>
        <p style="font-size:12px; margin-top:4px;">Type: <strong>${data.enterprise_type}</strong> | City: ${data.city}, ${data.state}</p>
        <small class="text-muted">Activity: ${data.nic_description}</small>
      </div>
    `;
  } else {
    resDiv.innerHTML = `<div style="color:var(--danger); padding:12px;">${data.message}</div>`;
  }
}

function handleFileUpload(e) {
  const files = e.target.files;
  const feedback = document.getElementById('uploadFeedback');
  feedback.innerHTML = `
    <div style="background:var(--success-bg); padding:14px; border-radius:8px; margin-top:14px; color:var(--success);">
      <strong>✓ Uploaded ${files.length} documents successfully.</strong>
      <p style="font-size:12px; color:var(--text-dark); margin-top:4px;">DPDP Act Notice: Ephemeral cache verified. Automated purge scheduled in 30 days.</p>
    </div>
  `;
}

// ==========================================
// ORDER CONFIRMATION & LIVE TRACKER
// ==========================================
async function confirmOrder(businessName) {
  try {
    const res = await fetch('/api/orders/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        business_name: businessName || 'Ganesh Woodcraft',
        city: 'Nagpur',
        bundle_title: currentRecommendation ? currentRecommendation.bundle_title : 'Udyam Digital Starter',
        total_monthly_with_gst: 3184,
        setup_fee_inr: 0,
        estimated_install_days: 2
      })
    });
    const order = await res.json();
    renderOrderTracker(order);
    window.location.hash = '#tracker';
  } catch (err) {
    console.error('Error creating order:', err);
  }
}

function renderOrderTracker(order) {
  document.getElementById('trackOrderId').innerText = `ORDER: ${order.order_id}`;
  document.getElementById('trackBusinessName').innerText = `${order.business_name}, ${order.city}`;
  document.getElementById('trackStatusText').innerText = order.status;
  document.getElementById('trackActivationDate').innerText = `${order.estimated_activation_date} (Guaranteed)`;
  document.getElementById('trackTypicalDays').innerText = `${order.install_days} Days`;

  const milestonesContainer = document.getElementById('milestonesContainer');
  milestonesContainer.innerHTML = order.milestones.map(m => {
    let circleClass = 'pending';
    let icon = m.step;
    if (m.status === 'Completed') {
      circleClass = 'completed';
      icon = '✓';
    } else if (m.status === 'In Progress') {
      circleClass = 'in-progress';
    }

    return `
      <div class="milestone-row">
        <div class="milestone-circle ${circleClass}">${icon}</div>
        <div class="milestone-info">
          <strong>${m.title} <small class="text-muted">(${m.time})</small></strong>
          <small>${m.detail}</small>
        </div>
      </div>
    `;
  }).join('');

  const waFeed = document.getElementById('whatsappFeed');
  waFeed.innerHTML = order.notifications.map(n => `
    <div class="wa-message">
      <p>${n.message}</p>
      <span class="wa-time">${n.time} · Delivered</span>
    </div>
  `).join('');
}

// ==========================================
// PARTNER CRM & LEADS TABLE
// ==========================================
async function loadFunnelSummary() {
  try {
    const res = await fetch('/api/crm/funnel');
    const data = await res.json();
    const container = document.getElementById('crmFunnelSummary');

    container.innerHTML = `
      <div class="crm-card">
        <div class="stat-num">${data.total_leads.toLocaleString()}</div>
        <div class="stat-lbl">Total SMB Leads Evaluated</div>
      </div>
      <div class="crm-card">
        <div class="stat-num">${data.activated_count} <small style="font-size:14px;color:var(--text-muted);">(${data.activation_rate_pct}%)</small></div>
        <div class="stat-lbl">Legacy Activations (Benchmark)</div>
      </div>
      <div class="crm-card">
        <div class="stat-num">₹${data.blended_cac_inr.toLocaleString()}</div>
        <div class="stat-lbl">Legacy Blended CAC per Customer</div>
      </div>
      <div class="crm-card">
        <div class="stat-num">${data.avg_days_to_activate} Days</div>
        <div class="stat-lbl">Legacy Avg Days to Activate</div>
      </div>
    `;
  } catch (err) {
    console.error('Error loading funnel summary:', err);
  }
}

function debounceFetchLeads() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(fetchLeads, 300);
}

async function fetchLeads() {
  const stage = document.getElementById('filterStage').value;
  const segment = document.getElementById('filterSegment').value;
  const search = document.getElementById('searchLead').value.trim();

  const url = `/api/crm/leads?stage=${encodeURIComponent(stage)}&segment=${encodeURIComponent(segment)}&search=${encodeURIComponent(search)}&limit=25`;
  const tbody = document.getElementById('leadsTableBody');
  tbody.innerHTML = '<tr><td colspan="7" class="text-center p-3">Loading leads...</td></tr>';

  try {
    const res = await fetch(url);
    const leads = await res.json();

    if (leads.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="text-center p-3 text-muted">No matching leads found.</td></tr>';
      return;
    }

    tbody.innerHTML = leads.map(l => {
      let propClass = 'prop-low';
      if (l.propensity_level === 'High') propClass = 'prop-high';
      else if (l.propensity_level === 'Medium') propClass = 'prop-medium';

      return `
        <tr>
          <td><strong>${l.lead_id}</strong></td>
          <td>
            <strong>${l.business_name}</strong>
            <div style="font-size:11px;color:var(--text-muted);">${l.business_type}</div>
          </td>
          <td>${l.segment}<br><small class="text-muted">${l.city} (Tier ${l.city_tier})</small></td>
          <td><span class="badge-tag">${l.stage_reached}</span></td>
          <td><small class="text-danger">${l.drop_reason || '—'}</small></td>
          <td>
            <span class="propensity-badge ${propClass}">${l.propensity_level} (${l.propensity_score}%)</span>
          </td>
          <td style="max-width:280px;">
            <small><strong>Recommended Action:</strong> ${l.next_action}</small>
          </td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-danger p-3">Error fetching leads data.</td></tr>';
  }
}

// ==========================================
// MODALS
// ==========================================
function showModal(id) {
  document.getElementById(id).classList.add('active');
}

function hideModal(id) {
  document.getElementById(id).classList.remove('active');
}

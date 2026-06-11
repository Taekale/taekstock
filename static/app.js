// --- US/KR Stocks & ETFs Korean Name Mappings ---
const US_KOREAN_NAMES = {
    "AAPL": "애플", "MSFT": "마이크로소프트", "AMZN": "아마존", "NVDA": "엔비디아", "META": "메타",
    "GOOGL": "구글", "GOOG": "구글", "TSLA": "테슬라", "BRK-B": "버크셔 해서웨이", "LLY": "일라이 릴리",
    "AVGO": "브로드컴", "JPM": "JP모건 체이스", "UNH": "유나이티드헬스", "V": "비자", "MA": "마스터카드",
    "COST": "코스트코", "HD": "홈디포", "PG": "프록터 앤 갬블", "NFLX": "넷플릭스", "AMD": "AMD",
    "JNJ": "존슨앤존슨", "ABBV": "애브비", "MRK": "머크", "ORCL": "오라클", "WMT": "월마트",
    "BAC": "뱅크오브아메리카", "PEP": "펩시코", "CVX": "쉐브론", "KO": "코카콜라", "TMO": "써모 피셔",
    "CRM": "세일즈포스", "ADBE": "어도비", "ACN": "액센츄어", "QCOM": "퀄컴", "CSCO": "시스코 시스템즈",
    "MCD": "맥도날드", "ABT": "애보트 랩스", "INTC": "인텔", "TXN": "텍사스 인스트루먼트", "GE": "제너럴 일렉트릭",
    "AMGN": "암젠", "DIS": "디즈니", "ISRG": "인튜이티브 서지컬", "IBM": "IBM", "CAT": "캐터필러",
    "AXP": "아메리칸 익스프레스", "PFE": "화이자", "PM": "필립 모리스", "MS": "모건 스탠리", "NKE": "나이키",
    "GS": "골드만삭스", "HON": "하니웰", "CMCSA": "컴캐스트", "BKNG": "부킹홀딩스", "COP": "코노코필립스",
    "SPGI": "S&P 글로벌", "LOW": "로우스", "RTX": "레이시온", "AMAT": "어플라이드 머티어리얼즈", "TJX": "TJX 컴퍼니",
    "LRCX": "램 리서치", "UNP": "유니온 퍼시픽", "PLTR": "팔란티어", "PANW": "팔로알토 네트웍스", "FI": "피서브",
    "MU": "마이크론 테크놀로지", "REGN": "리제네론", "UBER": "우버", "ETN": "이튼", "MDT": "메드트로닉",
    "BMY": "브리스톨 마이어스 스퀴브", "DE": "디어앤컴퍼니", "SYK": "스트라이커", "SBUX": "스타벅스", "ADP": "ADP",
    "LMT": "록히드 마틴", "VRTX": "버텍스 파마슈티컬스", "ELV": "엘레반스 헬스", "CI": "시그나", "GILD": "길리어드 사이언스",
    "GEV": "GE 베르노바", "MDLZ": "몬델리즈", "CRWD": "크라우드스트라이크", "PGR": "프로그레시브", "ADI": "아날로그 디바이스",
    "MMC": "마쉬 앤 맥레넌", "BSX": "보스턴 사이언티픽", "MELI": "메르카도 리브레", "CB": "처브", "ANET": "아리스타 네트웍스",
    "SO": "서던 컴퍼니", "HCA": "HCA 헬스케어", "KLAC": "KLA", "WM": "웨이스트 매니지먼트", "DHR": "다나허", "ZTS": "조에티스",
    // US ETFs
    "SPY": "S&P 500 지수 ETF",
    "IVV": "iShares S&P 500 ETF",
    "VOO": "Vanguard S&P 500 ETF",
    "QQQ": "나스닥 100 ETF",
    "DIA": "다우 존스 ETF",
    "IWM": "러셀 2000 ETF",
    "SOXX": "필라델피아 반도체 ETF",
    "SMH": "반도체 25대 기업 ETF",
    "TQQQ": "나스닥 100 레버리지 3X ETF",
    "SQQQ": "나스닥 100 인버스 3X ETF",
    "JEPI": "JP모건 고배당 커버드콜 ETF",
    "SCHD": "미국 배당 다우존스 ETF (SCHD)",
    "TLT": "미국 20년 이상 국채 ETF",
    // KR ETFs
    "069500": "KODEX 200 (코스피 200 추종)",
    "122630": "KODEX 레버리지 (코스피 2X)",
    "252670": "KODEX 200선물인버스2X (곱버스)",
    "114800": "KODEX 인버스",
    "229200": "KODEX 코스닥150레버리지",
    "251340": "KODEX 코스닥150선물인버스",
    "379800": "KODEX 미국나스닥100레버리지(합성 H)",
    "453810": "PLUS 미국테크TOP10",
    "305720": "TIGER 2차전지테마"
};

// --- Application State ---
const state = {
    currentMarket: 'US', // 'US' or 'KR'
    isSyncing: false,
    dbStatus: null
};

// --- DOM Elements ---
const elements = {
    usCacheCount: document.getElementById('us-cache-count'),
    krCacheCount: document.getElementById('kr-cache-count'),
    etfUsCacheCount: document.getElementById('etf-us-cache-count'),
    etfKrCacheCount: document.getElementById('etf-kr-cache-count'),
    btnSyncData: document.getElementById('btn-sync-data'),
    searchInput: document.getElementById('search-input'),
    btnSearch: document.getElementById('btn-search'),
    marketTabBtns: document.querySelectorAll('.tab-btn'),
    lastCalcTime: document.getElementById('last-calc-time'),
    buyListContainer: document.getElementById('buy-list-container'),
    sellListContainer: document.getElementById('sell-list-container'),
    dashboardLoading: document.getElementById('dashboard-loading'),
    stockModal: document.getElementById('stock-modal'),
    btnCloseModal: document.getElementById('btn-close-modal'),
    toastContainer: document.getElementById('toast-container'),
    
    // Modal fields
    modalMarketTag: document.getElementById('modal-market-tag'),
    modalStockName: document.getElementById('modal-stock-name'),
    modalStockTicker: document.getElementById('modal-stock-ticker'),
    modalStockPrice: document.getElementById('modal-stock-price'),
    modalRecommendation: document.getElementById('modal-recommendation'),
    modalScoreText: document.getElementById('modal-score-text'),
    modalScoreFill: document.getElementById('modal-score-fill'),
    modalMetricPer: document.getElementById('modal-metric-per'),
    modalEvalPer: document.getElementById('modal-eval-per'),
    modalMetricPbr: document.getElementById('modal-metric-pbr'),
    modalEvalPbr: document.getElementById('modal-eval-pbr'),
    modalMetricPsr: document.getElementById('modal-metric-psr'),
    modalEvalPsr: document.getElementById('modal-eval-psr'),
    modalMetricRoe: document.getElementById('modal-metric-roe'),
    modalEvalRoe: document.getElementById('modal-eval-roe'),
    modalAnalysisText: document.getElementById('modal-analysis-text'),
    
    // Sync Progress Modal
    syncModal: document.getElementById('sync-modal'),
    syncProgressFill: document.getElementById('sync-progress-fill'),
    syncProgressMessage: document.getElementById('sync-progress-message'),
    syncProgressPercent: document.getElementById('sync-progress-percent'),
    
    // New Multi-Factor Modal Elements
    modalMetricVolume: document.getElementById('modal-metric-volume'),
    modalEvalVolume: document.getElementById('modal-eval-volume'),
    modalMetricTradingValue: document.getElementById('modal-metric-trading-value'),
    modalEvalTradingValue: document.getElementById('modal-eval-trading-value'),
    modalMetricSentiment: document.getElementById('modal-metric-sentiment'),
    modalEvalSentiment: document.getElementById('modal-eval-sentiment'),
    
    // Growth & Stability Elements
    modalCardPeg: document.getElementById('modal-card-peg'),
    modalMetricPeg: document.getElementById('modal-metric-peg'),
    modalEvalPeg: document.getElementById('modal-eval-peg'),
    modalCardRevenueGrowth: document.getElementById('modal-card-revenue-growth'),
    modalMetricRevenueGrowth: document.getElementById('modal-metric-revenue-growth'),
    modalEvalRevenueGrowth: document.getElementById('modal-eval-revenue-growth'),
    modalCardEarningsGrowth: document.getElementById('modal-card-earnings-growth'),
    modalMetricEarningsGrowth: document.getElementById('modal-metric-earnings-growth'),
    modalEvalEarningsGrowth: document.getElementById('modal-eval-earnings-growth'),
    modalCardDebtToEquity: document.getElementById('modal-card-debt-to-equity'),
    modalMetricDebtToEquity: document.getElementById('modal-metric-debt-to-equity'),
    modalEvalDebtToEquity: document.getElementById('modal-eval-debt-to-equity'),
    modalCardFreeCashFlow: document.getElementById('modal-card-free-cash-flow'),
    modalMetricFreeCashFlow: document.getElementById('modal-metric-free-cash-flow'),
    modalEvalFreeCashFlow: document.getElementById('modal-eval-free-cash-flow'),
    modalCardEps: document.getElementById('modal-card-eps'),
    modalMetricEps: document.getElementById('modal-metric-eps'),
    modalEvalEps: document.getElementById('modal-eval-eps')
};

// --- Helper Functions ---

// Formatting utilities
function formatPrice(price, market, ticker = '') {
    if (price === null || price === undefined) return '-';
    if (market === 'US' || market === 'ETF_US' || (market === 'ETF' && ticker && !ticker.endsWith('.KS') && !ticker.endsWith('.KQ'))) {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price);
    } else {
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(price);
    }
}

function formatMetric(val, suffix = '') {
    if (val === null || val === undefined || isNaN(val)) return '-';
    return Number(val).toFixed(2) + suffix;
}

function formatVolume(val) {
    if (val === null || val === undefined || isNaN(val) || val <= 0) return '-';
    return new Intl.NumberFormat('ko-KR').format(val) + ' 주';
}

function formatTradingValue(val, market) {
    if (val === null || val === undefined || isNaN(val) || val <= 0) return '-';
    if (market === 'US' || market === 'ETF_US') {
        const millions = val / 1000000;
        return `$${millions.toFixed(1)}M`;
    } else {
        const eok = val / 100000000;
        return `${eok.toFixed(1)}억 원`;
    }
}

function formatFCF(val, market) {
    if (val === null || val === undefined || isNaN(val)) return '-';
    const isNegative = val < 0;
    const absVal = Math.abs(val);
    let result = '';
    if (market === 'US' || market === 'ETF_US' || market === 'ETF') {
        const millions = absVal / 1000000;
        result = `$${millions.toFixed(1)}M`;
    } else {
        const eok = absVal / 100000000;
        result = `${eok.toFixed(1)}억 원`;
    }
    return isNegative ? `-${result}` : result;
}

function formatSentiment(val) {
    if (val === null || val === undefined || isNaN(val)) return '-';
    const pct = (val * 100).toFixed(1);
    return `${pct}%`;
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let iconClass = 'fa-circle-info';
    if (type === 'success') iconClass = 'fa-circle-check';
    if (type === 'error') iconClass = 'fa-triangle-exclamation';
    
    toast.innerHTML = `
        <i class="fa-solid ${iconClass}"></i>
        <span>${message}</span>
    `;
    
    elements.toastContainer.appendChild(toast);
    
    // Remove toast after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'toast-in 0.3s reverse forwards';
        toast.addEventListener('animationend', () => toast.remove());
    }, 4000);
}

// Map recommendations to badges
function getBadgeClass(rec) {
    switch (rec) {
        case '강력 매수': return 'badge-strong-buy';
        case '매수': return 'badge-buy';
        case '관망': return 'badge-neutral';
        case '매도': return 'badge-sell';
        case '강력 매도': return 'badge-strong-sell';
        default: return 'badge-neutral';
    }
}

function getBadgeModalClass(rec) {
    switch (rec) {
        case '강력 매수': return 'strong-buy';
        case '매수': return 'buy';
        case '관망': return 'neutral';
        case '매도': return 'sell';
        case '강력 매도': return 'strong-sell';
        default: return 'neutral';
    }
}

// Show/Hide Loading
function setDashboardLoading(isLoading) {
    if (isLoading) {
        elements.dashboardLoading.classList.add('active');
    } else {
        elements.dashboardLoading.classList.remove('active');
    }
}

// --- Data Fetching & Core Logic ---

// Fetch DB status & cached stocks count
async function fetchDbStatus() {
    try {
        const res = await fetch('/api/status');
        if (!res.ok) throw new Error('상태 정보를 가져오는데 실패했습니다.');
        
        state.dbStatus = await res.json();
        elements.usCacheCount.textContent = state.dbStatus.us_cached_stocks;
        elements.krCacheCount.textContent = state.dbStatus.kr_cached_stocks;
        if (elements.etfUsCacheCount && state.dbStatus.etf_us_cached_stocks !== undefined) {
            elements.etfUsCacheCount.textContent = state.dbStatus.etf_us_cached_stocks;
        }
        if (elements.etfKrCacheCount && state.dbStatus.etf_kr_cached_stocks !== undefined) {
            elements.etfKrCacheCount.textContent = state.dbStatus.etf_kr_cached_stocks;
        }
        
        // Update visitor stats
        const todayEl = document.getElementById('today-visitors');
        const totalEl = document.getElementById('total-visitors');
        if (todayEl && state.dbStatus.today_visitors !== undefined) {
            todayEl.textContent = state.dbStatus.today_visitors;
        }
        if (totalEl && state.dbStatus.total_visitors !== undefined) {
            totalEl.textContent = state.dbStatus.total_visitors;
        }
    } catch (err) {
        console.error(err);
    }
}

// Fetch and render Top 30 recommendations
async function loadTop30() {
    setDashboardLoading(true);
    try {
        const res = await fetch(`/api/top30?market=${state.currentMarket}`);
        if (!res.ok) throw new Error('Top 30 데이터를 가져오는데 실패했습니다.');
        
        const data = await res.json();
        renderList(data.buys, elements.buyListContainer, true);
        renderList(data.sells, elements.sellListContainer, false);
        
        // Update last calc time from the first available stock
        const allStocks = [...data.buys, ...data.sells];
        if (allStocks.length > 0 && allStocks[0].updated_at) {
            elements.lastCalcTime.textContent = allStocks[0].updated_at;
        } else {
            elements.lastCalcTime.textContent = '-';
        }
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        setDashboardLoading(false);
    }
}

// Render stock cards into lists
function renderList(stocks, container, isBuy) {
    container.innerHTML = '';
    
    if (!stocks || stocks.length === 0) {
        container.innerHTML = `<div class="empty-state">해당 시장에 저장된 평가 종목 데이터가 없습니다. 먼저 '업데이트' 버튼을 누르거나 검색해주세요.</div>`;
        return;
    }
    
    stocks.forEach((stock, index) => {
        const card = document.createElement('div');
        card.className = 'stock-card';
        
        const scorePercent = (stock.buy_score * 100).toFixed(1);
        const priceFormatted = formatPrice(stock.price, stock.market, stock.ticker);
        const badgeClass = getBadgeClass(stock.recommendation);
        
        // Apply US Korean names in parentheses or KR ETF overrides
        let nameToShow = stock.name;
        const cleanTicker = stock.ticker.split('.')[0].toUpperCase();
        const krName = US_KOREAN_NAMES[cleanTicker];
        if (stock.market === 'US' || stock.market === 'ETF' || stock.market === 'ETF_US' || stock.market === 'ETF_KR') {
            if (krName) {
                if (stock.ticker.endsWith('.KS') || stock.ticker.endsWith('.KQ')) {
                    nameToShow = krName;
                } else {
                    nameToShow = `${stock.name} (${krName})`;
                }
            }
        }
        
        card.innerHTML = `
            <span class="card-rank">${index + 1}</span>
            <div class="card-info">
                <span class="card-name" title="${nameToShow}">${nameToShow}</span>
                <span class="card-ticker">${stock.ticker}</span>
            </div>
            <div class="card-score-box">
                <div class="card-score-header">
                    <span>점수</span>
                    <strong>${scorePercent}%</strong>
                </div>
                <div class="card-score-bar-bg">
                    <div class="card-score-bar-fill" style="width: ${scorePercent}%"></div>
                </div>
            </div>
            <span class="card-badge ${badgeClass}">${stock.recommendation}</span>
            <span class="card-price">${priceFormatted}</span>
        `;
        
        card.addEventListener('click', () => openStockModal(stock));
        container.appendChild(card);
    });
}

// Open Detail Modal & Populate Data
function openStockModal(stock) {
    // Set tag based on market type
    if (stock.market === 'US') {
        elements.modalMarketTag.textContent = 'US MARKET';
    } else if (stock.market === 'KR') {
        elements.modalMarketTag.textContent = 'KR MARKET';
    } else if (stock.market === 'ETF_US') {
        elements.modalMarketTag.textContent = 'US ETF MARKET';
    } else if (stock.market === 'ETF_KR') {
        elements.modalMarketTag.textContent = 'KR ETF MARKET';
    } else {
        elements.modalMarketTag.textContent = 'ETF MARKET';
    }
    
    // Apply US Korean names in parentheses or KR ETF overrides
    let nameToShow = stock.name;
    const cleanTicker = stock.ticker.split('.')[0].toUpperCase();
    const krName = US_KOREAN_NAMES[cleanTicker];
    if (stock.market === 'US' || stock.market === 'ETF' || stock.market === 'ETF_US' || stock.market === 'ETF_KR') {
        if (krName) {
            if (stock.ticker.endsWith('.KS') || stock.ticker.endsWith('.KQ')) {
                nameToShow = krName;
            } else {
                nameToShow = `${stock.name} (${krName})`;
            }
        }
    }
    
    elements.modalStockName.textContent = nameToShow;
    elements.modalStockTicker.textContent = stock.ticker;
    elements.modalStockPrice.textContent = formatPrice(stock.price, stock.market, stock.ticker);
    
    // Set score bar
    const scorePercent = (stock.buy_score * 100).toFixed(1);
    elements.modalScoreText.textContent = `${scorePercent}%`;
    elements.modalScoreFill.style.width = `${scorePercent}%`;
    
    // Set recommendation badge
    elements.modalRecommendation.textContent = stock.recommendation;
    // Clear old recommendation classes
    elements.modalRecommendation.className = 'modal-recommend-badge';
    const recClass = getBadgeModalClass(stock.recommendation);
    elements.modalRecommendation.classList.add(recClass);
    
    // Render metrics with fallbacks
    elements.modalMetricVolume.textContent = formatVolume(stock.volume);
    elements.modalMetricTradingValue.textContent = formatTradingValue(stock.trading_value, stock.market);
    elements.modalMetricSentiment.textContent = formatSentiment(stock.sentiment_score);
    
    // Dynamic modal restructuring for ETFs
    const perCard = elements.modalMetricPer.closest('.metric-card');
    const pbrCard = elements.modalMetricPbr.closest('.metric-card');
    const psrCard = elements.modalMetricPsr.closest('.metric-card');
    const roeCard = elements.modalMetricRoe.closest('.metric-card');
    
    const perTitle = perCard.querySelector('.metric-title');
    const pbrTitle = pbrCard.querySelector('.metric-title');
    const psrTitle = psrCard.querySelector('.metric-title');
    
    if (stock.market === 'ETF' || stock.market === 'ETF_US' || stock.market === 'ETF_KR') {
        // 1. Rebrand PER card to 50-Day MA
        perTitle.innerHTML = '50일 이동평균 <small>(50 MA)</small>';
        elements.modalMetricPer.textContent = formatPrice(stock.fifty_day_avg, stock.market, stock.ticker);
        elements.modalEvalPer.textContent = '단기 추세 지표';
        elements.modalEvalPer.className = 'metric-evaluation text-neutral';
        
        // 2. Rebrand PBR card to 200-Day MA
        pbrTitle.innerHTML = '200일 이동평균 <small>(200 MA)</small>';
        elements.modalMetricPbr.textContent = formatPrice(stock.two_hundred_day_avg, stock.market, stock.ticker);
        elements.modalEvalPbr.textContent = '장기 추세 기준선';
        elements.modalEvalPbr.className = 'metric-evaluation text-neutral';
        
        // 3. Rebrand PSR card to Momentum ratio (50MA / 200MA)
        psrTitle.innerHTML = '모멘텀 비율 <small>(50MA/200MA)</small>';
        let ratio = null;
        if (stock.fifty_day_avg && stock.two_hundred_day_avg) {
            ratio = stock.fifty_day_avg / stock.two_hundred_day_avg;
        }
        elements.modalMetricPsr.textContent = formatMetric(ratio);
        
        const evalPsr = elements.modalEvalPsr;
        evalPsr.className = 'metric-evaluation';
        if (ratio === null || isNaN(ratio)) {
            evalPsr.textContent = '데이터 없음';
            evalPsr.classList.add('text-bad');
        } else if (ratio > 1.05) {
            evalPsr.textContent = '강한 상승국면 (골든크로스)';
            evalPsr.classList.add('text-good');
        } else if (ratio >= 0.98) {
            evalPsr.textContent = '보통/박스권 추세';
            evalPsr.classList.add('text-neutral');
        } else {
            evalPsr.textContent = '하락국면 (데드크로스 경계)';
            evalPsr.classList.add('text-bad');
        }
        
        // 4. Hide ROE card to form a clean 3x2 grid
        roeCard.style.display = 'none';
        
        // Hide growth metrics cards for ETFs
        elements.modalCardPeg.style.display = 'none';
        elements.modalCardRevenueGrowth.style.display = 'none';
        elements.modalCardEarningsGrowth.style.display = 'none';
        elements.modalCardDebtToEquity.style.display = 'none';
        elements.modalCardFreeCashFlow.style.display = 'none';
        elements.modalCardEps.style.display = 'none';
        
        // Generate ETF custom AI analysis explanation
        generateEtfExplanation(stock);
    } else {
        // Restore standard titles and visibility for stocks
        perTitle.innerHTML = 'PER <small>(주가수익비율)</small>';
        pbrTitle.innerHTML = 'PBR <small>(주가순자산비율)</small>';
        psrTitle.innerHTML = 'PSR <small>(주가매출비율)</small>';
        roeCard.style.display = 'flex';
        
        // Show growth metrics cards for stocks
        elements.modalCardPeg.style.display = 'flex';
        elements.modalCardRevenueGrowth.style.display = 'flex';
        elements.modalCardEarningsGrowth.style.display = 'flex';
        elements.modalCardDebtToEquity.style.display = 'flex';
        elements.modalCardFreeCashFlow.style.display = 'flex';
        elements.modalCardEps.style.display = 'flex';
        
        // Render standard metrics
        elements.modalMetricPer.textContent = formatMetric(stock.per);
        elements.modalMetricPbr.textContent = formatMetric(stock.pbr);
        elements.modalMetricPsr.textContent = formatMetric(stock.psr);
        elements.modalMetricRoe.textContent = formatMetric(stock.roe, '%');
        
        // Run standard evaluations and AI explanation
        evaluateMetrics(stock);
    }
    
    // Open Modal
    elements.stockModal.classList.add('active');
}

// Evaluate metric bounds and display labels in modal
function evaluateMetrics(stock) {
    // 1. PER evaluation
    const per = stock.per;
    const evalPer = elements.modalEvalPer;
    evalPer.className = 'metric-evaluation';
    if (per === null || per === undefined || per <= 0) {
        evalPer.textContent = '적자 혹은 데이터 없음';
        evalPer.classList.add('text-bad');
    } else if (per < 15) {
        evalPer.textContent = '저평가 (매우 양호)';
        evalPer.classList.add('text-good');
    } else if (per > 35) {
        evalPer.textContent = '고평가 경계';
        evalPer.classList.add('text-bad');
    } else {
        evalPer.textContent = '적정 수준';
        evalPer.classList.add('text-neutral');
    }
    
    // 2. PBR evaluation
    const pbr = stock.pbr;
    const evalPbr = elements.modalEvalPbr;
    evalPbr.className = 'metric-evaluation';
    if (pbr === null || pbr === undefined || pbr <= 0) {
        evalPbr.textContent = '자산 정보 부족';
        evalPbr.classList.add('text-bad');
    } else if (pbr < 1.2) {
        evalPbr.textContent = '장부가치 이하 혹은 인접 (매우 저렴)';
        evalPbr.classList.add('text-good');
    } else if (pbr > 5) {
        evalPbr.textContent = '순자산 대비 비쌈';
        evalPbr.classList.add('text-bad');
    } else {
        evalPbr.textContent = '보통 수준';
        evalPbr.classList.add('text-neutral');
    }
    
    // 3. PSR evaluation
    const psr = stock.psr;
    const evalPsr = elements.modalEvalPsr;
    evalPsr.className = 'metric-evaluation';
    if (psr === null || psr === undefined || psr <= 0) {
        evalPsr.textContent = '매출 정보 부족';
        evalPsr.classList.add('text-bad');
    } else if (psr < 1.5) {
        evalPsr.textContent = '매출액 대비 저평가';
        evalPsr.classList.add('text-good');
    } else if (psr > 8) {
        evalPsr.textContent = '매출 대비 상당한 고평가';
        evalPsr.classList.add('text-bad');
    } else {
        evalPsr.textContent = '적정 수준';
        evalPsr.classList.add('text-neutral');
    }
    
    // 4. ROE evaluation
    const roe = stock.roe;
    const evalRoe = elements.modalEvalRoe;
    evalRoe.className = 'metric-evaluation';
    if (roe === null || roe === undefined || roe <= 0) {
        evalRoe.textContent = '이익 창출 실패 혹은 정보 부족';
        evalRoe.classList.add('text-bad');
    } else if (roe >= 15) {
        evalRoe.textContent = '매우 높은 자본 효율성 (우수)';
        evalRoe.classList.add('text-good');
    } else if (roe < 6) {
        evalRoe.textContent = '자본 회수 효율성 저조';
        evalRoe.classList.add('text-bad');
    } else {
        evalRoe.textContent = '준수한 효율성';
        evalRoe.classList.add('text-neutral');
    }
    
    // 5. Volume evaluation
    const evalVolume = elements.modalEvalVolume;
    evalVolume.className = 'metric-evaluation';
    if (stock.volume === null || stock.volume === undefined || stock.volume <= 0) {
        evalVolume.textContent = '거래량 정보 부족';
        evalVolume.classList.add('text-bad');
    } else {
        evalVolume.textContent = '정상 거래 중';
        evalVolume.classList.add('text-good');
    }
    
    // 6. Trading Value evaluation
    const evalTradingValue = elements.modalEvalTradingValue;
    evalTradingValue.className = 'metric-evaluation';
    if (stock.trading_value === null || stock.trading_value === undefined || stock.trading_value <= 0) {
        evalTradingValue.textContent = '거래대금 정보 부족';
        evalTradingValue.classList.add('text-bad');
    } else if (stock.market === 'KR' && stock.trading_value > 5000000000) {
        evalTradingValue.textContent = '풍부한 유동성 (50억 초과)';
        evalTradingValue.classList.add('text-good');
    } else if (stock.market === 'US' && stock.trading_value > 10000000) {
        evalTradingValue.textContent = '풍부한 유동성 ($10M 초과)';
        evalTradingValue.classList.add('text-good');
    } else {
        evalTradingValue.textContent = '보통 수준의 유동성';
        evalTradingValue.classList.add('text-neutral');
    }
    
    // 7. Sentiment evaluation
    const evalSentiment = elements.modalEvalSentiment;
    evalSentiment.className = 'metric-evaluation';
    if (stock.sentiment_score === null || stock.sentiment_score === undefined) {
        evalSentiment.textContent = '뉴스 정보 없음';
        evalSentiment.classList.add('text-neutral');
    } else if (stock.sentiment_score >= 0.75) {
        evalSentiment.textContent = '강한 호재 감지 (매우 긍정)';
        evalSentiment.classList.add('text-good');
    } else if (stock.sentiment_score >= 0.55) {
        evalSentiment.textContent = '긍정적 뉴스 분위기';
        evalSentiment.classList.add('text-good');
    } else if (stock.sentiment_score <= 0.25) {
        evalSentiment.textContent = '우려/악재 경계 필요';
        evalSentiment.classList.add('text-bad');
    } else if (stock.sentiment_score <= 0.45) {
        evalSentiment.textContent = '약간 부정적인 뉴스가 지배적';
        evalSentiment.classList.add('text-bad');
    } else {
        evalSentiment.textContent = '중립적인 분위기';
        evalSentiment.classList.add('text-neutral');
    }
    
    // 8. PEG evaluation
    const peg = stock.peg_ratio;
    const evalPeg = elements.modalEvalPeg;
    evalPeg.className = 'metric-evaluation';
    elements.modalMetricPeg.textContent = formatMetric(peg);
    if (peg === null || peg === undefined || isNaN(peg)) {
        evalPeg.textContent = '데이터 없음';
        evalPeg.classList.add('text-neutral');
    } else if (peg < 0) {
        evalPeg.textContent = '성장률 음수 / 적자';
        evalPeg.classList.add('text-bad');
    } else if (peg < 1.0) {
        evalPeg.textContent = '저평가 고성장주 (우량)';
        evalPeg.classList.add('text-good');
    } else if (peg >= 1.5) {
        evalPeg.textContent = '고평가 경계';
        evalPeg.classList.add('text-bad');
    } else {
        evalPeg.textContent = '적정 수준';
        evalPeg.classList.add('text-neutral');
    }
    
    // 9. Revenue Growth evaluation
    const revG = stock.revenue_growth;
    const evalRevG = elements.modalEvalRevenueGrowth;
    evalRevG.className = 'metric-evaluation';
    elements.modalMetricRevenueGrowth.textContent = formatMetric(revG !== null ? revG * 100 : null, '%');
    if (revG === null || revG === undefined || isNaN(revG)) {
        evalRevG.textContent = '데이터 없음';
        evalRevG.classList.add('text-neutral');
    } else if (revG > 0.20) {
        evalRevG.textContent = '초고속 성장 (20% 초과)';
        evalRevG.classList.add('text-good');
    } else if (revG > 0.10) {
        evalRevG.textContent = '견조한 성장 (10% 초과)';
        evalRevG.classList.add('text-good');
    } else if (revG < 0) {
        evalRevG.textContent = '역성장 경계 필요';
        evalRevG.classList.add('text-bad');
    } else {
        evalRevG.textContent = '보통 수준의 성장';
        evalRevG.classList.add('text-neutral');
    }
    
    // 10. Earnings Growth evaluation
    const earnG = stock.earnings_growth;
    const evalEarnG = elements.modalEvalEarningsGrowth;
    evalEarnG.className = 'metric-evaluation';
    elements.modalMetricEarningsGrowth.textContent = formatMetric(earnG !== null ? earnG * 100 : null, '%');
    if (earnG === null || earnG === undefined || isNaN(earnG)) {
        evalEarnG.textContent = '데이터 없음';
        evalEarnG.classList.add('text-neutral');
    } else if (earnG > 0.25) {
        evalEarnG.textContent = '폭발적인 이익 성장 (25% 초과)';
        evalEarnG.classList.add('text-good');
    } else if (earnG > 0.10) {
        evalEarnG.textContent = '안정적 성장 (10% 초과)';
        evalEarnG.classList.add('text-good');
    } else if (earnG < 0) {
        evalEarnG.textContent = '이익 역성장 경계 필요';
        evalEarnG.classList.add('text-bad');
    } else {
        evalEarnG.textContent = '보통 수준의 성장';
        evalEarnG.classList.add('text-neutral');
    }
    
    // 11. Debt to Equity evaluation
    const debt = stock.debt_to_equity;
    const evalDebt = elements.modalEvalDebtToEquity;
    evalDebt.className = 'metric-evaluation';
    elements.modalMetricDebtToEquity.textContent = formatMetric(debt, '%');
    if (debt === null || debt === undefined || isNaN(debt)) {
        evalDebt.textContent = '데이터 없음';
        evalDebt.classList.add('text-neutral');
    } else if (debt < 100.0) {
        evalDebt.textContent = '재무 매우 건전 (100% 미만)';
        evalDebt.classList.add('text-good');
    } else if (debt > 200.0) {
        evalDebt.textContent = '부채 과다 경계 (200% 초과)';
        evalDebt.classList.add('text-bad');
    } else {
        evalDebt.textContent = '적정 수준';
        evalDebt.classList.add('text-neutral');
    }
    
    // 12. Free Cash Flow evaluation
    const fcf = stock.free_cash_flow;
    const evalFCF = elements.modalEvalFreeCashFlow;
    evalFCF.className = 'metric-evaluation';
    elements.modalMetricFreeCashFlow.textContent = formatFCF(fcf, stock.market);
    if (fcf === null || fcf === undefined || isNaN(fcf)) {
        evalFCF.textContent = '데이터 없음';
        evalFCF.classList.add('text-neutral');
    } else if (fcf > 0) {
        evalFCF.textContent = '현금 흐름 건전 (흑자)';
        evalFCF.classList.add('text-good');
    } else {
        evalFCF.textContent = '현금 흐름 잠식 경계 (적자)';
        evalFCF.classList.add('text-bad');
    }
    
    // 13. EPS evaluation
    const eps = stock.eps;
    const evalEps = elements.modalEvalEps;
    evalEps.className = 'metric-evaluation';
    elements.modalMetricEps.textContent = formatPrice(eps, stock.market, stock.ticker);
    if (eps === null || eps === undefined || isNaN(eps)) {
        evalEps.textContent = '데이터 없음';
        evalEps.classList.add('text-neutral');
    } else if (eps > 0) {
        evalEps.textContent = '주당순이익 흑자';
        evalEps.classList.add('text-good');
    } else {
        evalEps.textContent = '주당순이익 적자 경계';
        evalEps.classList.add('text-bad');
    }
    
    // AI investment explanation writeup
    generateExplanation(stock);
}

// Generate human-friendly Korean evaluation explanation
function generateExplanation(stock) {
    const scorePct = (stock.buy_score * 100).toFixed(0);
    let html = `<strong>${stock.name}</strong>은(는) 동종 시장(상대평가 그룹) 내에서 종합 백분위 <strong>상위 ${scorePct}%</strong>의 매력도를 기록하여 최종 <strong>[${stock.recommendation}]</strong> 판정을 받았습니다.<br><br>`;
    
    let bulletPoints = [];
    
    // Assessment logic
    if (stock.per && stock.per > 0 && stock.per < 15) {
        bulletPoints.push("이익 가치 측면(PER)에서 시장 대비 상대적으로 큰 저평가 메리트가 존재합니다.");
    } else if (stock.per && stock.per > 35) {
        bulletPoints.push("PER이 다소 높아 미래 성장에 대한 기대감이 크게 반영되어 있으며, 주가 조정 부담이 있을 수 있습니다.");
    }
    
    if (stock.pbr && stock.pbr > 0 && stock.pbr < 1.2) {
        bulletPoints.push("장부가치 자산 평가(PBR) 수준이 매우 낮아 주가 하방 경직성을 확보하고 있어 안정적입니다.");
    } else if (stock.pbr && stock.pbr > 5) {
        bulletPoints.push("순자산 대비 높은 PBR을 형성하고 있어 프리미엄이 많이 끼어 있습니다.");
    }
    
    if (stock.roe && stock.roe >= 15) {
        bulletPoints.push("주주의 투자 원금 대비 매년 15% 이상의 순이익을 창출해 내는 높은 사업 효율(ROE)을 보여줍니다.");
    } else if (stock.roe && stock.roe < 6) {
        bulletPoints.push("자기자본이익률(ROE)이 다소 저조하여 자본 효율 개선이 시급한 상황입니다.");
    }
    
    if (stock.psr && stock.psr > 0 && stock.psr < 1.5) {
        bulletPoints.push("매출 규모(PSR) 대비 주가가 매우 저렴하게 거래되고 있어 숨은 매출 성장 여력이 우수합니다.");
    }
    
    // 5. Sentiment & Trading Value evaluation in AI description
    if (stock.sentiment_score && stock.sentiment_score >= 0.65) {
        bulletPoints.push("최근 관련 뉴스 분석 결과 호재성 기사 비율이 높아 시장의 긍정적인 기대 심리가 잘 반영되어 있습니다.");
    } else if (stock.sentiment_score && stock.sentiment_score <= 0.35) {
        bulletPoints.push("최근 관련 뉴스 분석 결과 부정적인 기사가 주를 이루고 있어, 단기 투자 시 비중 관리에 신중해야 합니다.");
    }
    
    if (stock.trading_value && stock.market === 'KR' && stock.trading_value > 5000000000) {
        bulletPoints.push("일일 거래대금이 50억 원을 상회하여 유동성이 매우 풍부하고 시장의 높은 인기를 얻고 있습니다.");
    } else if (stock.trading_value && stock.market === 'US' && stock.trading_value > 10000000) {
        bulletPoints.push("일일 거래대금이 $10M을 상회하여 매수/매도 스프레드가 좁고 거래 편의성이 높습니다.");
    }
    
    if (stock.per === null || stock.per <= 0 || stock.roe === null || stock.roe <= 0) {
        bulletPoints.push("현재 적자 상태이거나 재무 지표가 불투명하므로 투자 시 리스크 관리에 신중해야 합니다.");
    }
    
    // Wrap up opinions
    if (stock.buy_score >= 0.8) {
        html += `<span class="text-good">★ 강력 매수 의견:</span> 4대 밸류 지표(PER, ROE, PBR, PSR) 균형이 매우 우수한 A급 종목입니다. 시장 평균 대비 현저히 싼 가격에 높은 효율을 내고 있어 중장기 투자가 매우 유망합니다.`;
    } else if (stock.buy_score >= 0.65) {
        html += `<span class="text-good">★ 매수 의견:</span> 전반적인 밸류 지표가 긍정적입니다. 상대적으로 낮은 밸류에이션 부담과 안정적인 재무 성과가 뒷받침되고 있습니다.`;
    } else if (stock.buy_score >= 0.35) {
        html += `<span class="text-neutral">★ 관망 의견:</span> 주가 밸류에이션과 기업 성장성이 균형을 이루고 있거나, 일부 재무 지표가 아쉽습니다. 분할 매수나 추가 실적 확인 후 진입이 권장됩니다.`;
    } else if (stock.buy_score >= 0.2) {
        html += `<span class="text-bad">★ 매도 의견:</span> 현재 주가가 내재 가치(이익, 매출, 순자산 등) 대비 고평가 영역에 속해 있어 차익 실현을 고려하는 것이 유리합니다.`;
    } else {
        html += `<span class="text-bad">★ 강력 매도 의견:</span> 기업 이익이 적자이거나 매출/자산 대비 주가 고평가 수준이 극심합니다. 하방 리스크가 크므로 신규 진입을 피하고 비중 축소를 권장합니다.`;
    }
    
    if (bulletPoints.length > 0) {
        html += "<br><br><strong>핵심 지표 분석 요약:</strong><ul>" + bulletPoints.map(pt => `<li>${pt}</li>`).join('') + "</ul>";
    }
    
    elements.modalAnalysisText.innerHTML = html;
}

function generateEtfExplanation(stock) {
    const scorePct = (stock.buy_score * 100).toFixed(0);
    let html = `<strong>${stock.name}</strong>은(는) ETF 상대평가 그룹 내에서 종합 모멘텀 백분위 <strong>상위 ${scorePct}%</strong>를 기록하여 최종 <strong>[${stock.recommendation}]</strong> 판정을 받았습니다.<br><br>`;
    
    let bulletPoints = [];
    let ratio = null;
    if (stock.fifty_day_avg && stock.two_hundred_day_avg) {
        ratio = stock.fifty_day_avg / stock.two_hundred_day_avg;
    }
    
    if (ratio) {
        if (ratio > 1.05) {
            bulletPoints.push("단기 50일 이동평균선이 장기 200일 선을 크게 상회하는 강한 골든크로스 상승 추세를 나타내고 있습니다.");
        } else if (ratio >= 0.98) {
            bulletPoints.push("50일 선과 200일 선이 인접해 있어 박스권 횡보 추세이거나 방향성 탐색 구간입니다.");
        } else {
            bulletPoints.push("단기 이평선이 장기 이평선 아래에 머무는 데드크로스 국면으로 단기적인 하락 압력이 우세합니다.");
        }
    }
    
    if (stock.volume && stock.volume > 10000) {
        bulletPoints.push("풍부한 거래량과 우수한 유동성을 확보하고 있어 괴리율 및 슬리피지 리스크가 최소화된 우량 ETF 상품입니다.");
    }
    
    if (stock.sentiment_score && stock.sentiment_score >= 0.65) {
        bulletPoints.push("최근 관련 뉴스 기사의 심리 분석 지표가 매우 긍정적으로 형성되어 시장의 우호적인 수급 유입이 기대됩니다.");
    } else if (stock.sentiment_score && stock.sentiment_score <= 0.35) {
        bulletPoints.push("최근 악재성 보도 비율이 다소 높아 보수적인 접근 또는 비중 관리가 권장됩니다.");
    }
    
    if (stock.buy_score >= 0.8) {
        html += `<span class="text-good">★ 강력 추천 매수 의견:</span> 장단기 모멘텀 정배열 흐름이 압도적이며 거래 유동성 또한 최상위권인 핵심 지수/섹터 ETF입니다. 적립식 및 추세 추종 매수 진입에 매우 유망합니다.`;
    } else if (stock.buy_score >= 0.65) {
        html += `<span class="text-good">★ 매수 의견:</span> 모멘텀 흐름이 견조하며 단기 이평선 지지력이 탄탄합니다. 안정적인 비중 확대를 권장합니다.`;
    } else if (stock.buy_score >= 0.35) {
        html += `<span class="text-neutral">★ 관망 의견:</span> 단기 추세가 보합권에 있어 섣부른 진입보다는 지지선 확인 후 매수 시점을 잡는 것이 좋습니다.`;
    } else if (stock.buy_score >= 0.2) {
        html += `<span class="text-bad">★ 매도 의견:</span> 장기 역배열 진행 중이며 매도세가 지배적입니다. 리스크 예방을 위해 비중을 축소하거나 현금 비중을 늘리는 것이 현명합니다.`;
    } else {
        html += `<span class="text-bad">★ 강력 매도 의견:</span> 추세 붕괴 및 하락 모멘텀이 극대화된 상태입니다. 신규 매수를 피하고 반등 시 비중을 과감히 축소하는 리스크 관리가 필요합니다.`;
    }
    
    if (bulletPoints.length > 0) {
        html += "<br><br><strong>ETF 모멘텀 요약 분석:</strong><ul>" + bulletPoints.map(pt => `<li>${pt}</li>`).join('') + "</ul>";
    }
    
    elements.modalAnalysisText.innerHTML = html;
}

// Execute stock search
async function executeSearch() {
    const query = elements.searchInput.value.trim();
    if (!query) {
        showToast('검색어를 입력해 주세요.', 'info');
        return;
    }
    
    setDashboardLoading(true);
    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.detail || '검색에 실패했습니다.');
        }
        
        const data = await res.json();
        const stock = data.stock;
        
        // Match current dashboard market with searched stock market to refresh lists
        state.currentMarket = stock.market;
        updateTabActiveState();
        
        // Open details
        openStockModal(stock);
        
        // Reload dashboard lists and stats (since dynamic search might add new ranking member)
        await fetchDbStatus();
        await loadTop30();
        
        showToast(`'${stock.name}' (${stock.ticker}) 검색 완료!`, 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        setDashboardLoading(false);
    }
}

// Synchronize database data
async function triggerSync() {
    if (state.isSyncing) return;
    
    state.isSyncing = true;
    if (elements.btnSyncData) {
        elements.btnSyncData.disabled = true;
        const syncIcon = elements.btnSyncData.querySelector('.sync-icon');
        if (syncIcon) syncIcon.classList.add('loading');
    }
    
    // Reset progress modal elements
    elements.syncProgressFill.style.width = '0%';
    elements.syncProgressPercent.textContent = '0%';
    elements.syncProgressMessage.textContent = '동기화 시작 준비 중...';
    
    // Show progress modal
    elements.syncModal.classList.add('active');
    
    try {
        const res = await fetch('/api/sync', { method: 'POST' });
        if (!res.ok) throw new Error('동기화 명령 전송에 실패했습니다.');
        
        // Polling interval
        const interval = setInterval(async () => {
            try {
                const progressRes = await fetch('/api/sync-progress');
                if (!progressRes.ok) throw new Error('진행 상태 조회 실패');
                
                const progressData = await progressRes.json();
                const pct = progressData.percent || 0;
                const msg = progressData.message || '진행 중...';
                
                // Update UI
                elements.syncProgressFill.style.width = `${pct}%`;
                elements.syncProgressPercent.textContent = `${pct}%`;
                elements.syncProgressMessage.textContent = msg;
                
                // Finish conditions
                if (progressData.status === 'idle' && pct >= 100) {
                    clearInterval(interval);
                    
                    // Reload top 30 lists and DB cache count
                    await fetchDbStatus();
                    await loadTop30();
                    
                    // Dismiss modal after a short delay for user satisfaction
                    setTimeout(() => {
                        elements.syncModal.classList.remove('active');
                        state.isSyncing = false;
                        if (elements.btnSyncData) {
                            elements.btnSyncData.disabled = false;
                            const syncIcon = elements.btnSyncData.querySelector('.sync-icon');
                            if (syncIcon) syncIcon.classList.remove('loading');
                        }
                        showToast('주식 데이터 동기화 및 가치 가중 평가가 성공적으로 완료되었습니다!', 'success');
                    }, 800);
                }
            } catch (pollErr) {
                console.error('진행 상태 폴링 에러:', pollErr);
            }
        }, 800);
        
    } catch (err) {
        showToast(err.message, 'error');
        elements.syncModal.classList.remove('active');
        state.isSyncing = false;
        if (elements.btnSyncData) {
            elements.btnSyncData.disabled = false;
            const syncIcon = elements.btnSyncData.querySelector('.sync-icon');
            if (syncIcon) syncIcon.classList.remove('loading');
        }
    }
}

function updateTabActiveState() {
    elements.marketTabBtns.forEach(btn => {
        if (btn.getAttribute('data-market') === state.currentMarket) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// --- Event Listeners Setup ---

function setupEventListeners() {
    // Market tab switching
    elements.marketTabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const market = btn.getAttribute('data-market');
            if (state.currentMarket !== market) {
                state.currentMarket = market;
                updateTabActiveState();
                loadTop30();
            }
        });
    });
    
    // Search Actions
    elements.btnSearch.addEventListener('click', executeSearch);
    elements.searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            executeSearch();
        }
    });
    
    // Sync Action
    if (elements.btnSyncData) {
        elements.btnSyncData.addEventListener('click', triggerSync);
    }
    
    // Modal Close
    elements.btnCloseModal.addEventListener('click', () => {
        elements.stockModal.classList.remove('active');
    });
    
    // Click outside modal container to close
    elements.stockModal.addEventListener('click', (e) => {
        if (e.target === elements.stockModal) {
            elements.stockModal.classList.remove('active');
        }
    });
}

// --- App Initialization ---
async function init() {
    setupEventListeners();
    await fetchDbStatus();
    await loadTop30();
    
    // If DB is empty, automatically trigger sync on startup
    const usCount = parseInt(elements.usCacheCount.textContent) || 0;
    const krCount = parseInt(elements.krCacheCount.textContent) || 0;
    const etfUsCount = elements.etfUsCacheCount ? (parseInt(elements.etfUsCacheCount.textContent) || 0) : 0;
    const etfKrCount = elements.etfKrCacheCount ? (parseInt(elements.etfKrCacheCount.textContent) || 0) : 0;
    
    if (usCount === 0 || krCount === 0 || etfUsCount === 0 || etfKrCount === 0) {
        showToast("데이터베이스 캐시가 비어 있거나 누락된 데이터가 있습니다. 최신 주식 평가 모델 동기화를 시작합니다!", "info");
        triggerSync();
    }
    
    // Set 5-second periodic auto-refresh for top 30 rankings
    setInterval(async () => {
        if (!state.isSyncing) {
            console.log("자동 실시간 갱신 실행 중...");
            await fetchDbStatus();
            await loadTop30();
        }
    }, 5000);
}

document.addEventListener('DOMContentLoaded', init);

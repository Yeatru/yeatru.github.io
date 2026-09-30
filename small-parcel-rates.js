/*!
 * Yeatru Sourcing — Small-Parcel Rates & Cost Model
 * ------------------------------------------------------------------
 * Source: 全球小包.xlsx (Yeatru Sourcing logistics desk, 2026-09).
 * Currency conversion: CNY → USD at fixed rate 6.6 (per business spec).
 *
 * Pricing rules (per the spreadsheet footnote):
 *   - Minimum chargeable weight per parcel: 0.5 kg
 *   - Weight is rounded UP to the next 0.5 kg increment ("0.5进位计费")
 *   - Volumetric weight = L × W × H / 6000 (cm); billable = max(actual, vol).
 *     We do NOT have per-SKU dimensions, so the model uses actual weight only.
 *     The volumetric rule is documented here so a future enhancement can
 *     pass {length, width, height} and the same calc() will pick the larger.
 *   - Per-destination max parcel weight (限重) varies (2–30 kg).
 *     A consignment heavier than the limit is split into N parcels.
 *   - Total CNY = Σ(parcel_billable_kg × rate_per_kg_cny) + N × per_package_cny
 *   - Total USD = Total CNY / 6.6
 *
 * Exposed API (window.YEATRU_SP):
 *   .CNY_RATE              — 6.6
 *   .RATES_BY_COUNTRY      — ISO-2 → rate row (USD values pre-computed)
 *   .COUNTRY_LIST          — ordered [{code, name_cn, continent, ...}]
 *   .CATEGORY_WEIGHTS      — mainCategory → estimated kg/unit
 *   .estimateUnitWeight(sku, mainCategory) → kg
 *   .calc({sku, mainCategory, qty, countryCode, dims?}) → breakdown
 *   .formatUsd(n)          — "$12.34"
 */
(function (global) {
  'use strict';

  var CNY_RATE = 6.6; // CNY → USD per 2026-09 spec

  // 90 destination zones. USD values are CNY / 6.6 (4 dp).
  // Source: 全球小包.xlsx Sheet1 rows 2-91.
  var RATES_BY_COUNTRY = {
    "US": { code:"US", name_cn:"美国",          continent:"北美洲",   min_kg:0.5, max_kg:5,  rate_per_kg_usd:26.5152, per_package_usd:6.8182,  eta:"8-12工作日",  notes:"DDP包税，岛屿地址单询" },
    "PR": { code:"PR", name_cn:"波多黎各",      continent:"北美洲",   min_kg:0.5, max_kg:30, rate_per_kg_usd:32.5758, per_package_usd:9.8485,  eta:"12-18工作日", notes:"收件人自税" },
    "CA": { code:"CA", name_cn:"加拿大",        continent:"北美洲",   min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:7.2727,  eta:"8-12工作日",  notes:"偏远付附加费13/23/43/78/件不等，14美元内免税" },
    "CR": { code:"CR", name_cn:"哥斯达黎加",    continent:"北美洲",   min_kg:0.5, max_kg:20, rate_per_kg_usd:30.3030, per_package_usd:7.4242,  eta:"15-25工作日", notes:"收件人自税" },
    "MX": { code:"MX", name_cn:"墨西哥",        continent:"北美洲",   min_kg:0.5, max_kg:30, rate_per_kg_usd:29.5455, per_package_usd:8.3333,  eta:"9-15工作日",  notes:"DDP包税" },
    "GB": { code:"GB", name_cn:"英国",          continent:"欧洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:21.9697, per_package_usd:5.9091,  eta:"8-12工作日",  notes:"100美元免税" },
    "AT": { code:"AT", name_cn:"奥地利",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:8.0303,  eta:"8-12工作日",  notes:"附加费14元/票+3欧元/申报项，100美元免税" },
    "BE": { code:"BE", name_cn:"比利时",        continent:"欧洲",     min_kg:0.5, max_kg:5,  rate_per_kg_usd:22.7273, per_package_usd:7.8788,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "BG": { code:"BG", name_cn:"保加利亚",      continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:6.6667,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "HR": { code:"HR", name_cn:"克罗地亚",      continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:6.5152,  eta:"8-12工作日",  notes:"14/票附加费+3欧元/申报项，100美元免税" },
    "CY": { code:"CY", name_cn:"塞浦路斯",      continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:28.0303, per_package_usd:6.6667,  eta:"8-15工作日",  notes:"3欧元/申报项，100美元免税" },
    "CZ": { code:"CZ", name_cn:"捷克",          continent:"欧洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:23.4848, per_package_usd:6.0606,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "DK": { code:"DK", name_cn:"丹麦",          continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:24.2424, per_package_usd:7.7273,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "EE": { code:"EE", name_cn:"爱沙尼亚",      continent:"欧洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:23.4848, per_package_usd:5.6061,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "FI": { code:"FI", name_cn:"芬兰",          continent:"欧洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:24.2424, per_package_usd:7.2727,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "FR": { code:"FR", name_cn:"法国",          continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:21.9697, per_package_usd:6.6667,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "DE": { code:"DE", name_cn:"德国",          continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:21.2121, per_package_usd:7.2727,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "GR": { code:"GR", name_cn:"希腊",          continent:"欧洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:23.4848, per_package_usd:6.2121,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "HU": { code:"HU", name_cn:"匈牙利",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:22.7273, per_package_usd:6.5152,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "IE": { code:"IE", name_cn:"爱尔兰",        continent:"欧洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:23.4848, per_package_usd:7.4242,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "IT": { code:"IT", name_cn:"意大利",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:21.2121, per_package_usd:7.7273,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "LV": { code:"LV", name_cn:"拉脱维亚",      continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:5.6061,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "LT": { code:"LT", name_cn:"立陶宛",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:5.6061,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "LU": { code:"LU", name_cn:"卢森堡",        continent:"欧洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:25.7576, per_package_usd:7.8788,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "MT": { code:"MT", name_cn:"马耳他",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:28.7879, per_package_usd:8.7879,  eta:"10-15工作日", notes:"3欧元/申报项，100美元免税" },
    "NL": { code:"NL", name_cn:"荷兰",          continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:22.7273, per_package_usd:7.5758,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "PL": { code:"PL", name_cn:"波兰",          continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:6.3636,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "PT": { code:"PT", name_cn:"葡萄牙",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:24.2424, per_package_usd:7.1212,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "RO": { code:"RO", name_cn:"罗马尼亚",      continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:9.6970,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "SK": { code:"SK", name_cn:"斯洛伐克",      continent:"欧洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:24.2424, per_package_usd:7.2727,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "SI": { code:"SI", name_cn:"斯洛文尼亚",    continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:6.5152,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "ES": { code:"ES", name_cn:"西班牙",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:21.2121, per_package_usd:6.5152,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "CH": { code:"CH", name_cn:"瑞士",          continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:8.7879,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "SE": { code:"SE", name_cn:"瑞典",          continent:"欧洲",     min_kg:0.5, max_kg:5,  rate_per_kg_usd:25.0000, per_package_usd:6.3636,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "NO": { code:"NO", name_cn:"挪威",          continent:"欧洲",     min_kg:0.5, max_kg:5,  rate_per_kg_usd:22.7273, per_package_usd:8.0303,  eta:"8-15工作日",  notes:"3欧元/申报项，100美元免税" },
    "RS": { code:"RS", name_cn:"塞尔维亚",      continent:"欧洲",     min_kg:0.5, max_kg:5,  rate_per_kg_usd:25.0000, per_package_usd:7.2727,  eta:"8-12工作日",  notes:"3欧元/申报项，100美元免税" },
    "UA": { code:"UA", name_cn:"乌克兰",        continent:"欧洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:26.5152, per_package_usd:5.4545,  eta:"10-15工作日", notes:"50美元免税" },
    "GG": { code:"GG", name_cn:"根西岛",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:25.0000, per_package_usd:8.7879,  eta:"15-25工作日", notes:"收件人自税" },
    "IM": { code:"IM", name_cn:"马恩岛",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:25.0000, per_package_usd:8.7879,  eta:"15-25工作日", notes:"收件人自税" },
    "JE": { code:"JE", name_cn:"泽西岛",        continent:"欧洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:25.0000, per_package_usd:8.7879,  eta:"15-25工作日", notes:"收件人自税" },
    "AR": { code:"AR", name_cn:"阿根廷",        continent:"南美洲",   min_kg:0.5, max_kg:2,  rate_per_kg_usd:43.9394, per_package_usd:7.2727,  eta:"15-25工作日", notes:"收件人自税" },
    "BR": { code:"BR", name_cn:"巴西",          continent:"南美洲",   min_kg:0.5, max_kg:5,  rate_per_kg_usd:28.0303, per_package_usd:12.2727, eta:"15-25工作日", notes:"税号必填，收件人支付税金，清关失败无赔付不退运费" },
    "CL": { code:"CL", name_cn:"智利",          continent:"南美洲",   min_kg:0.5, max_kg:10, rate_per_kg_usd:28.0303, per_package_usd:9.8485,  eta:"15-25工作日", notes:"发货人支付税金，申报货值的19%，代缴关税" },
    "CO": { code:"CO", name_cn:"哥伦比亚",      continent:"南美洲",   min_kg:0.5, max_kg:20, rate_per_kg_usd:31.8182, per_package_usd:9.0909,  eta:"15-25工作日", notes:"100美元免税，3公斤以上每增加0.5公斤+15元派送费" },
    "PE": { code:"PE", name_cn:"秘鲁",          continent:"南美洲",   min_kg:0.5, max_kg:5,  rate_per_kg_usd:31.8182, per_package_usd:9.8485,  eta:"15-25工作日", notes:"100美元免税，2KG以上每增加0.5公斤+5元派送费" },
    "AU": { code:"AU", name_cn:"澳大利亚",      continent:"大洋洲",   min_kg:0.5, max_kg:20, rate_per_kg_usd:22.8788, per_package_usd:6.8182,  eta:"8-12工作日",  notes:"偏远费用在偏远分区查看" },
    "NZ": { code:"NZ", name_cn:"新西兰",        continent:"大洋洲",   min_kg:0.5, max_kg:20, rate_per_kg_usd:22.7273, per_package_usd:7.8788,  eta:"8-12工作日",  notes:"偏远25/票" },
    "AZ": { code:"AZ", name_cn:"阿塞拜疆",      continent:"亚洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:28.7879, per_package_usd:7.1212,  eta:"8-12工作日",  notes:"税号必填" },
    "BN": { code:"BN", name_cn:"文莱",          continent:"亚洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:21.9697, per_package_usd:6.0606,  eta:"8-12工作日",  notes:"收件人自税" },
    "JP": { code:"JP", name_cn:"日本",          continent:"亚洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:18.1818, per_package_usd:7.5758,  eta:"8-12工作日",  notes:"50美元免税" },
    "MY": { code:"MY", name_cn:"马来西亚",      continent:"亚洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:19.6970, per_package_usd:5.3030,  eta:"8-12工作日",  notes:"15美元免税" },
    "MV": { code:"MV", name_cn:"马尔代夫",      continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:21.2121, per_package_usd:6.8182,  eta:"8-12工作日",  notes:"15美元免税" },
    "MN": { code:"MN", name_cn:"蒙古",          continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:16.6667, per_package_usd:6.8182,  eta:"15-25工作日", notes:"15美元免税" },
    "PK": { code:"PK", name_cn:"巴基斯坦",      continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:25.7576, per_package_usd:5.3030,  eta:"15-25工作日", notes:"收件人自税" },
    "PH": { code:"PH", name_cn:"菲律宾",        continent:"亚洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:23.4848, per_package_usd:5.3030,  eta:"8-12工作日",  notes:"10人民币免税" },
    "KR": { code:"KR", name_cn:"韩国",          continent:"亚洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:20.4545, per_package_usd:6.8182,  eta:"8-12工作日",  notes:"需要收货人的税号清关" },
    "SG": { code:"SG", name_cn:"新加坡",        continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:19.6970, per_package_usd:5.7576,  eta:"8-12工作日",  notes:"100美元免税" },
    "KH": { code:"KH", name_cn:"柬埔寨",        continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:18.1818, per_package_usd:5.3030,  eta:"8-12工作日",  notes:"50人民币免税，不查验无税" },
    "HK": { code:"HK", name_cn:"中国香港",      continent:"亚洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:17.4242, per_package_usd:6.0606,  eta:"8-12工作日",  notes:"50人民币免税，不查验无税" },
    "KZ": { code:"KZ", name_cn:"哈萨克斯坦",    continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:22.7273, per_package_usd:5.3030,  eta:"15-25工作日", notes:"50人民币免税，不查验无税" },
    "LA": { code:"LA", name_cn:"老挝",          continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:28.7879, per_package_usd:5.7576,  eta:"15-25工作日", notes:"50人民币免税，不查验无税" },
    "MM": { code:"MM", name_cn:"缅甸",          continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:25.7576, per_package_usd:5.3030,  eta:"15-25工作日", notes:"50人民币免税，不查验无税" },
    "LK": { code:"LK", name_cn:"斯里兰卡",      continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:27.2727, per_package_usd:6.8182,  eta:"15-25工作日", notes:"收件人自税" },
    "TW": { code:"TW", name_cn:"中国台湾",      continent:"亚洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:21.2121, per_package_usd:6.8182,  eta:"8-12工作日",  notes:"50人民币免税，不查验无税" },
    "TH": { code:"TH", name_cn:"泰国",          continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:18.9394, per_package_usd:5.4545,  eta:"8-12工作日",  notes:"50人民币免税，不查验无税" },
    "UZ": { code:"UZ", name_cn:"乌兹别克斯坦",  continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:33.3333, per_package_usd:6.2121,  eta:"15-25工作日", notes:"收件人自税" },
    "VN": { code:"VN", name_cn:"越南",          continent:"亚洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:16.6667, per_package_usd:5.0000,  eta:"8-12工作日",  notes:"50人民币免税，不查验无税" },
    "AE": { code:"AE", name_cn:"阿联酋",        continent:"亚洲（中东）", min_kg:0.5, max_kg:30, rate_per_kg_usd:24.2424, per_package_usd:6.5152,  eta:"8-12工作日",  notes:"100美元免税" },
    "BH": { code:"BH", name_cn:"巴林",          continent:"亚洲（中东）", min_kg:0.5, max_kg:5,  rate_per_kg_usd:33.3333, per_package_usd:8.0303,  eta:"8-12工作日",  notes:"200美元内免税，超过10%" },
    "IL": { code:"IL", name_cn:"以色列",        continent:"亚洲（中东）", min_kg:0.5, max_kg:5,  rate_per_kg_usd:25.7576, per_package_usd:6.3636,  eta:"8-12工作日",  notes:"自提，单边尺寸限制40CM" },
    "JO": { code:"JO", name_cn:"约旦",          continent:"亚洲（中东）", min_kg:0.5, max_kg:2,  rate_per_kg_usd:30.3030, per_package_usd:8.7879,  eta:"8-12工作日",  notes:"收件人自税" },
    "KW": { code:"KW", name_cn:"科威特",        continent:"亚洲（中东）", min_kg:0.5, max_kg:2,  rate_per_kg_usd:25.7576, per_package_usd:14.3939, eta:"8-12工作日",  notes:"申报价值的5%" },
    "OM": { code:"OM", name_cn:"阿曼",          continent:"亚洲（中东）", min_kg:0.5, max_kg:2,  rate_per_kg_usd:27.2727, per_package_usd:12.1212, eta:"8-12工作日",  notes:"24美元内免关税，超过10%" },
    "QA": { code:"QA", name_cn:"卡塔尔",        continent:"亚洲（中东）", min_kg:0.5, max_kg:2,  rate_per_kg_usd:30.3030, per_package_usd:18.9394, eta:"8-12工作日",  notes:"200美元内免税" },
    "SA": { code:"SA", name_cn:"沙特阿拉伯",    continent:"亚洲（中东）", min_kg:0.5, max_kg:10, rate_per_kg_usd:27.2727, per_package_usd:14.0909, eta:"8-12工作日",  notes:"税金申报货值的15%，运费包税" },
    "AO": { code:"AO", name_cn:"安哥拉",        continent:"非洲",     min_kg:0.5, max_kg:10, rate_per_kg_usd:34.8485, per_package_usd:6.8182,  eta:"10-18工作日", notes:"收件人自税" },
    "GH": { code:"GH", name_cn:"加纳",          continent:"非洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:37.8788, per_package_usd:6.8182,  eta:"15-25工作日", notes:"收件人自税" },
    "KE": { code:"KE", name_cn:"肯尼亚",        continent:"非洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:33.3333, per_package_usd:6.8182,  eta:"15-25工作日", notes:"收件人自税" },
    "MA": { code:"MA", name_cn:"摩洛哥",        continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:31.8182, per_package_usd:15.1515, eta:"15-25工作日", notes:"收件人自税" },
    "MG": { code:"MG", name_cn:"马达加斯加",    continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:29.5455, per_package_usd:15.1515, eta:"15-25工作日", notes:"收件人自税" },
    "MU": { code:"MU", name_cn:"毛里求斯",      continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:28.7879, per_package_usd:6.8182,  eta:"8-12工作日",  notes:"收件人自税" },
    "NG": { code:"NG", name_cn:"尼日利亚",      continent:"非洲",     min_kg:0.5, max_kg:20, rate_per_kg_usd:31.0606, per_package_usd:7.2727,  eta:"8-12工作日",  notes:"收件人自税" },
    "RW": { code:"RW", name_cn:"卢旺达",        continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:31.8182, per_package_usd:6.2121,  eta:"15-25工作日", notes:"收件人自税" },
    "SN": { code:"SN", name_cn:"塞内加尔",      continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:31.8182, per_package_usd:18.9394, eta:"8-12工作日",  notes:"收件人自税" },
    "SC": { code:"SC", name_cn:"塞舌尔",        continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:30.3030, per_package_usd:7.5758,  eta:"10-18工作日", notes:"收件人自税" },
    "TZ": { code:"TZ", name_cn:"坦桑尼亚",      continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:32.5758, per_package_usd:6.5152,  eta:"15-25工作日", notes:"收件人自税" },
    "UG": { code:"UG", name_cn:"乌干达",        continent:"非洲",     min_kg:0.5, max_kg:5,  rate_per_kg_usd:35.6061, per_package_usd:6.8182,  eta:"15-25工作日", notes:"收件人自税" },
    "RE": { code:"RE", name_cn:"留尼汪岛",      continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:30.3030, per_package_usd:14.3939, eta:"15-25工作日", notes:"收件人自税" },
    "ZA": { code:"ZA", name_cn:"南非",          continent:"非洲",     min_kg:0.5, max_kg:15, rate_per_kg_usd:37.8788, per_package_usd:9.0909,  eta:"15-25工作日", notes:"收件人自税" },
    "ZM": { code:"ZM", name_cn:"赞比亚",        continent:"非洲",     min_kg:0.5, max_kg:2,  rate_per_kg_usd:30.3030, per_package_usd:10.1515, eta:"15-25工作日", notes:"收件人自税" }
  };

  // Ordered country list grouped by continent for the dropdown UI.
  var CONTINENT_ORDER = ["北美洲","欧洲","南美洲","大洋洲","亚洲","亚洲（中东）","非洲"];
  var COUNTRY_LIST = (function () {
    var out = [];
    var byCont = {};
    Object.keys(RATES_BY_COUNTRY).forEach(function (code) {
      var r = RATES_BY_COUNTRY[code];
      (byCont[r.continent] = byCont[r.continent] || []).push(r);
    });
    CONTINENT_ORDER.forEach(function (c) {
      if (!byCont[c]) return;
      byCont[c].sort(function (a, b) {
        return a.name_cn.localeCompare(b.name_cn, "zh-Hans-CN");
      });
      byCont[c].forEach(function (r) { out.push(r); });
    });
    return out;
  })();

  // Estimated per-unit shipping weight (kg) — refined to the 50 sub-categories
  // actually used in site-data.json's `category` field. Site-data has no
  // per-SKU weights, so these are typical single-unit parcel weights derived
  // from the product profile of each sub-category. Override per-SKU by
  // setting window.YEATRU_SP_WEIGHTS[sku] = 0.123 (kg).
  var SUBCATEGORY_WEIGHTS = {
    "Toys":                 0.30, // plushies, figures, small toys
    "Storage & Organization": 0.60, // bins, organizers, boxes
    "Clothing":             0.25, // shirts, dresses, single garment
    "Shoes":                0.80, // a pair of shoes
    "Household":            1.50, // small appliances (kettles, irons)
    "Kitchen Storage":      0.40, // canisters, racks
    "Home & Garden":        0.50, // decor, planters, garden tools
    "Bags":                 0.40, // handbags, totes, purses
    "Cleaning":             0.35, // brushes, mops, sponges
    "Cups & Drinkware":     0.30, // bottles, tumblers, mugs
    "Kids":                 0.30, // kids' items
    "Kitchen Tools":        0.30, // peelers, graters, utensils
    "Lighting":             0.40, // lamps, bulbs, fixtures
    "Microphones/Audio":    0.50, // mics, small audio gear
    "Other":                0.50, // default bucket
    "Dog Supplies":         0.50, // pet toys, leashes, bowls
    "Audio/Electronics":    0.40, // speakers, cables, dongles
    "Fitness":              1.00, // dumbbells, resistance gear
    "Smart Electronics":    0.35, // smart plugs, trackers
    "Personal Care":        0.20, // shavers, trimmers, care devices
    "Machinery":            2.00, // small machines
    "Baby Care":            0.30, // bottles, soothers, baby gear
    "Stationery":           0.15, // pens, notebooks
    "Skin Care":            0.15, // creams, serums, jars
    "Auto Repair Tools":    0.80, // wrenches, jacks, sockets
    "Backpacks":            0.60, // student/travel backpacks
    "Hardware":             0.50, // fittings, brackets, fasteners
    "Hair Accessories":     0.05, // scrunchies, clips, pins
    "Photography":          0.80, // tripods, lights, accessories
    "Auto Accessories":     0.60, // mats, covers, trim
    "Swimwear":             0.20, // swimsuits
    "Audio/Video":          0.50, // adapters, small AV gear
    "Beauty":              0.15, // makeup, palettes
    "Locks":               0.40, // padlocks, smart locks
    "Accessories":          0.10, // misc small accessories
    "Fans":                1.20, // desk/stand fans
    "Kitchen/Bath":         0.40, // faucets, fixtures
    "Mobile Accessories":   0.10, // chargers, holders, cables
    "Footwear":             0.80, // shoes (generic)
    "KAP":                 1.00, // material (Kapton etc.)
    "Screen Protectors":   0.05, // films, glass
    "Musical Instruments": 1.50, // small instruments
    "OFC":                 1.00, // material (OFC wire/cable)
    "Outdoor":             0.80, // camping, hiking gear
    "Socks":               0.05, // socks (pair)
    "Kitchen Appliances":  2.00, // blenders, ovens, cookers
    "Tablets":             0.50, // tablets
    "Dry Goods":           1.00, // bulk material
    "MSF":                 1.00, // material
    "PET":                 1.00  // material
  };

  // Coarse fallback: 17 mainCategory-level weights (used only when the
  // sub-category isn't in SUBCATEGORY_WEIGHTS — shouldn't happen for any
  // catalogued SKU, but kept for safety / future categories).
  var CATEGORY_WEIGHTS = {
    "Apparel & Footwear":   0.30,
    "Auto Parts & Tools":   1.20,
    "Baby & Toys":          0.40,
    "Bags & Luggage":       0.50,
    "Beauty & Personal Care": 0.20,
    "Digital Electronics":  0.35,
    "Hardware & Home":      0.80,
    "Home & Daily Living":  0.50,
    "Home Appliances":      2.50,
    "Kitchen Supplies":     0.45,
    "Material":             1.00,
    "Musical Instruments":  1.50,
    "Others":               0.50,
    "Pet Supplies":         0.50,
    "Phone Accessories":    0.10,
    "Sports & Outdoor":     0.70,
    "Stationery & Office":  0.25
  };
  var DEFAULT_UNIT_KG = 0.50;

  /**
   * Estimate per-unit shipping weight in kg.
   * Priority: window.YEATRU_SP_WEIGHTS[sku] (real weighed data)
   *         > SUBCATEGORY_WEIGHTS[subcategory] (50 sub-cats)
   *         > CATEGORY_WEIGHTS[mainCategory] (17 main cats, fallback)
   *         > DEFAULT_UNIT_KG
   */
  function estimateUnitWeight(sku, subcategory, mainCategory) {
    if (sku && global.YEATRU_SP_WEIGHTS && global.YEATRU_SP_WEIGHTS[sku]) {
      return parseFloat(global.YEATRU_SP_WEIGHTS[sku]) || DEFAULT_UNIT_KG;
    }
    if (subcategory && SUBCATEGORY_WEIGHTS[subcategory]) {
      return SUBCATEGORY_WEIGHTS[subcategory];
    }
    if (mainCategory && CATEGORY_WEIGHTS[mainCategory]) {
      return CATEGORY_WEIGHTS[mainCategory];
    }
    return DEFAULT_UNIT_KG;
  }

  /** Whether the weight used is a real weighed value (vs category estimate). */
  function isRealWeight(sku) {
    return !!(sku && global.YEATRU_SP_WEIGHTS && global.YEATRU_SP_WEIGHTS[sku]);
  }

  // Round up to next 0.5 kg, with 0.5 kg minimum (per spreadsheet rule).
  function roundUpHalfKg(x) {
    if (!isFinite(x) || x <= 0) return 0.5;
    return Math.max(0.5, Math.ceil(x * 2) / 2);
  }

  /**
   * Full small-parcel cost breakdown.
   * @param {Object} args
   *   sku, subcategory, mainCategory, qty, countryCode, dims {l,w,h} (optional, cm)
   * @returns {Object|null} breakdown or null if country unknown
   */
  function calc(args) {
    args = args || {};
    var sku = args.sku || '';
    var subcategory = args.subcategory || '';
    var mainCategory = args.mainCategory || '';
    var qty = Math.max(1, parseInt(args.qty, 10) || 1);
    var countryCode = (args.countryCode || 'US').toUpperCase();
    var dims = args.dims; // optional {l,w,h} in cm

    var rate = RATES_BY_COUNTRY[countryCode];
    if (!rate) return null;

    var unitKg = estimateUnitWeight(sku, subcategory, mainCategory);
    var weightIsReal = isRealWeight(sku);
    var actualKg = unitKg * qty;

    // Volumetric weight: optional, only if all three dims supplied
    var volKg = 0;
    if (dims && dims.l && dims.w && dims.h) {
      // Per unit volumetric, multiplied by qty
      volKg = (dims.l * dims.w * dims.h / 6000) * qty;
    }
    var chargeKgRaw = Math.max(actualKg, volKg);

    // Per-parcel weight limit (country-specific); split into N parcels
    var maxPerPkg = rate.max_kg || 30;
    var numPackages = Math.max(1, Math.ceil(chargeKgRaw / maxPerPkg));
    var perPkgRaw = chargeKgRaw / numPackages;
    var perPkgBillable = roundUpHalfKg(perPkgRaw);
    var totalBillableKg = perPkgBillable * numPackages;

    var freight = totalBillableKg * rate.rate_per_kg_usd;
    var perPackageFee = numPackages * rate.per_package_usd;
    var total = freight + perPackageFee;

    return {
      countryCode: countryCode,
      countryCn:  rate.name_cn,
      continent:  rate.continent,
      sku: sku,
      subcategory: subcategory,
      mainCategory: mainCategory,
      qty: qty,
      unitKg: unitKg,
      weightIsReal: weightIsReal,
      actualKg: actualKg,
      volumetricKg: volKg,
      chargeKgRaw: chargeKgRaw,
      maxPerPkg: maxPerPkg,
      numPackages: numPackages,
      perPkgBillable: perPkgBillable,
      totalBillableKg: totalBillableKg,
      freightUsd: freight,
      perPackageFeeUsd: perPackageFee,
      totalUsd: total,
      eta: rate.eta,
      notes: rate.notes
    };
  }

  function formatUsd(n) {
    if (!isFinite(n)) return '—';
    return '$' + n.toFixed(2);
  }

  global.YEATRU_SP = {
    CNY_RATE: CNY_RATE,
    RATES_BY_COUNTRY: RATES_BY_COUNTRY,
    COUNTRY_LIST: COUNTRY_LIST,
    CONTINENT_ORDER: CONTINENT_ORDER,
    SUBCATEGORY_WEIGHTS: SUBCATEGORY_WEIGHTS,
    CATEGORY_WEIGHTS: CATEGORY_WEIGHTS,
    DEFAULT_UNIT_KG: DEFAULT_UNIT_KG,
    estimateUnitWeight: estimateUnitWeight,
    isRealWeight: isRealWeight,
    roundUpHalfKg: roundUpHalfKg,
    calc: calc,
    formatUsd: formatUsd
  };
})(typeof window !== 'undefined' ? window : this);

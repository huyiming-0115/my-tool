/**
 * 旅行地图工具
 * 从 Markdown 中提取地点信息，配合腾讯位置服务进行地理编码
 */

/**
 * 从 Markdown 文本中提取地点标记
 * 支持格式：
 *   - 📍 地点名
 *   - @地点名
 *   - 【地点名】
 *   - "游览/参观/打卡/前往 + 地点名"
 */
export function extractLocations(markdown) {
  if (!markdown) return []
  
  const locations = []
  const seen = new Set()
  
  // 匹配 📍 或 @ 开头的地点
  const markerPattern = /(?:📍|@)\s*([^，,。！!？?\n]+)/g
  let match
  while ((match = markerPattern.exec(markdown)) !== null) {
    const name = match[1].trim()
    if (name && !seen.has(name)) {
      seen.add(name)
      locations.push({ name, address: '', latitude: 0, longitude: 0 })
    }
  }
  
  // 匹配 "游览/参观/打卡/前往/抵达 + 地点"
  const verbPattern = /(?:游览|参观|打卡|前往|抵达|到达|入住|游玩|逛|游)\s*([^，,。！!？?\n【】]{2,20})/g
  while ((match = verbPattern.exec(markdown)) !== null) {
    const name = match[1].trim().replace(/[馆景区寺庙寺院园宫殿塔楼门城墙滩古镇邨]$/, '')
    if (name && !seen.has(name) && name.length >= 2) {
      seen.add(name)
      locations.push({ name, address: '', latitude: 0, longitude: 0 })
    }
  }
  
  // 匹配【】中的内容
  const bracketPattern = /【([^】]+)】/g
  while ((match = bracketPattern.exec(markdown)) !== null) {
    const name = match[1].trim()
    if (name && !seen.has(name) && name.length >= 2 && name.length <= 15) {
      seen.add(name)
      locations.push({ name, address: '', latitude: 0, longitude: 0 })
    }
  }
  
  return locations
}

/**
 * 预置的热门地点坐标库（离线可用）
 */
export const KNOWN_PLACES = {
  // 北京
  '天安门': { latitude: 39.9087, longitude: 116.3975, address: '北京市东城区' },
  '天安门广场': { latitude: 39.9087, longitude: 116.3975, address: '北京市东城区' },
  '故宫': { latitude: 39.9163, longitude: 116.3972, address: '北京市东城区景山前街4号' },
  '故宫博物院': { latitude: 39.9163, longitude: 116.3972, address: '北京市东城区景山前街4号' },
  '颐和园': { latitude: 39.9999, longitude: 116.2755, address: '北京市海淀区新建宫门路19号' },
  '长城': { latitude: 40.4319, longitude: 116.5704, address: '北京市延庆区G6京藏高速58号出口' },
  '八达岭长城': { latitude: 40.3598, longitude: 116.0156, address: '北京市延庆区八达岭特区' },
  '天坛': { latitude: 39.8822, longitude: 116.4066, address: '北京市东城区天坛东里甲1号' },
  '南锣鼓巷': { latitude: 39.9372, longitude: 116.4031, address: '北京市东城区南锣鼓巷' },
  '什刹海': { latitude: 39.9383, longitude: 116.3848, address: '北京市西城区什刹海' },
  '鸟巢': { latitude: 39.9929, longitude: 116.3965, address: '北京市朝阳区国家体育场南路1号' },
  '水立方': { latitude: 39.9913, longitude: 116.3844, address: '北京市朝阳区天辰东路11号' },
  
  // 上海
  '外滩': { latitude: 31.2397, longitude: 121.4900, address: '上海市黄浦区中山东一路' },
  '东方明珠': { latitude: 31.2397, longitude: 121.4998, address: '上海市浦东新区陆家嘴世纪大道1号' },
  '南京路': { latitude: 31.2359, longitude: 121.4737, address: '上海市黄浦区南京东路' },
  '豫园': { latitude: 31.2271, longitude: 121.4920, address: '上海市黄浦区安仁街137号' },
  '迪士尼': { latitude: 31.1440, longitude: 121.6576, address: '上海市浦东新区川沙新镇' },
  '田子坊': { latitude: 31.2107, longitude: 121.4698, address: '上海市黄浦区泰康路210号' },
  
  // 云南
  '大理': { latitude: 25.6069, longitude: 100.2675, address: '云南省大理白族自治州大理市' },
  '洱海': { latitude: 25.7908, longitude: 100.1788, address: '云南省大理白族自治州' },
  '大理古城': { latitude: 25.6944, longitude: 100.1611, address: '云南省大理市古城区' },
  '丽江': { latitude: 26.8721, longitude: 100.2322, address: '云南省丽江市' },
  '丽江古城': { latitude: 26.8721, longitude: 100.2322, address: '云南省丽江市古城区' },
  '玉龙雪山': { latitude: 27.0982, longitude: 100.1780, address: '云南省丽江市玉龙纳西族自治县' },
  '蓝月谷': { latitude: 27.0850, longitude: 100.1850, address: '云南省丽江市玉龙雪山景区' },
  '香格里拉': { latitude: 27.8533, longitude: 99.7008, address: '云南省迪庆藏族自治州香格里拉市' },
  '普达措': { latitude: 27.8600, longitude: 99.9800, address: '云南省迪庆州普达措国家公园' },
  '虎跳峡': { latitude: 27.1850, longitude: 100.0500, address: '云南省丽江市虎跳峡镇' },
  
  // 成都
  '成都': { latitude: 30.5728, longitude: 104.0668, address: '四川省成都市' },
  '宽窄巷子': { latitude: 30.6722, longitude: 104.0554, address: '四川省成都市青羊区金河路口' },
  '春熙路': { latitude: 30.6595, longitude: 104.0757, address: '四川省成都市锦江区春熙路' },
  '大熊猫基地': { latitude: 30.7344, longitude: 104.1466, address: '四川省成都市成华区熊猫大道1375号' },
  '熊猫基地': { latitude: 30.7344, longitude: 104.1466, address: '四川省成都市成华区熊猫大道1375号' },
  '锦里': { latitude: 30.6464, longitude: 104.0525, address: '四川省成都市武侯区武侯祠大街231号' },
  '武侯祠': { latitude: 30.6464, longitude: 104.0525, address: '四川省成都市武侯区武侯祠大街231号' },
  '杜甫草堂': { latitude: 30.6605, longitude: 104.0253, address: '四川省成都市青羊区青华路37号' },
  '九眼桥': { latitude: 30.6380, longitude: 104.0820, address: '四川省成都市锦江区' },
  
  // 天津
  '天津': { latitude: 39.3434, longitude: 117.3616, address: '天津市' },
  '五大道': { latitude: 39.1065, longitude: 117.2009, address: '天津市和平区五大道' },
  '意式风情街': { latitude: 39.1020, longitude: 117.2000, address: '天津市河北区自由道' },
  '古文化街': { latitude: 39.1378, longitude: 117.1854, address: '天津市南开区古文化街' },
  '天津之眼': { latitude: 39.1563, longitude: 117.1814, address: '天津市红桥区三岔河口' },
  '瓷房子': { latitude: 39.1155, longitude: 117.1950, address: '天津市和平区赤峰道72号' },
  '滨海': { latitude: 39.0000, longitude: 117.7000, address: '天津市滨海新区' },
  '滨海新区': { latitude: 39.0000, longitude: 117.7000, address: '天津市滨海新区' },
  
  // 日本
  '东京': { latitude: 35.6762, longitude: 139.6503, address: '日本东京都' },
  '浅草寺': { latitude: 35.7148, longitude: 139.7967, address: '东京都台东区浅草2-3-1' },
  '富士山': { latitude: 35.3606, longitude: 138.7274, address: '静冈县与山梨县交界处' },
  '京都': { latitude: 35.0116, longitude: 135.7681, address: '日本京都府' },
  '大阪': { latitude: 34.6937, longitude: 135.5023, address: '日本大阪府' },
  '环球影城': { latitude: 34.6654, longitude: 135.4323, address: '大阪市此花区樱岛2-1-33' },
}

/**
 * 为提取的地点匹配坐标
 */
export function matchLocationsWithCoords(locations) {
  return locations.map(loc => {
    // 精确匹配
    if (KNOWN_PLACES[loc.name]) {
      return { ...loc, ...KNOWN_PLACES[loc.name] }
    }
    // 模糊匹配
    for (const [key, coords] of Object.entries(KNOWN_PLACES)) {
      if (loc.name.includes(key) || key.includes(loc.name)) {
        return { ...loc, ...coords }
      }
    }
    return loc
  })
}

export default { extractLocations, matchLocationsWithCoords, KNOWN_PLACES }


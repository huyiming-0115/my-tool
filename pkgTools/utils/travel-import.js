/**
 * 旅行计划导入工具
 * 从粘贴的文本/链接中智能提取行程结构，生成 Markdown
 */

/**
 * 从纯文本中提取行程信息
 * 支持格式：
 *   - "Day 1 / 第一天 / D1" 等日期标记
 *   - 地点名称（含📍、@、地点等前缀）
 *   - 时间标记（如 08:00、14:30）
 */
export function parseTextToMarkdown(text, title = '我的旅行计划') {
  if (!text || !text.trim()) return ''
  
  const lines = text.split('\n').map(l => l.trim()).filter(l => l)
  if (lines.length === 0) return ''
  
  const sections = []
  let currentSection = null
  let currentItems = []
  
  // 日期/天次匹配模式
  const dayPatterns = [
    /^第?([一二三四五六七八九十\d]+)\s*[天日]/i,
    /^Day\s*(\d+)/i,
    /^D(\d+)/i,
    /^(\d{1,2})[月\/](\d{1,2})[日\/]?/,
  ]
  
  // 时间匹配
  const timePattern = /(\d{1,2}):(\d{2})/
  
  // 地点标记
  const locationPattern = /(?:📍|@|地点[：:]?\s*|打卡[：:]?\s*|前往|到达|游览|参观)/i
  
  function flushSection() {
    if (currentSection && currentItems.length > 0) {
      sections.push({ title: currentSection, items: [...currentItems] })
      currentItems = []
    }
  }
  
  for (const line of lines) {
    // 检查是否是日期/天次标题
    let isDay = false
    for (const pattern of dayPatterns) {
      if (pattern.test(line)) {
        flushSection()
        currentSection = line
        isDay = true
        break
      }
    }
    if (isDay) continue
    
    // 检查是否是时间开头的行程项
    if (timePattern.test(line) || locationPattern.test(line) || /^[-•·]/.test(line)) {
      currentItems.push(line.replace(/^[-•·]\s*/, ''))
    } else if (line.length > 2) {
      // 普通描述，作为列表项
      currentItems.push(line)
    }
  }
  flushSection()
  
  // 如果没有识别到结构化内容，直接作为引用块返回
  if (sections.length === 0) {
    return `# ${title}\n\n${text.split('\n').map(l => l.trim()).filter(l => l).map(l => `- ${l}`).join('\n')}\n\n> 💡 导入的原始内容，可继续编辑`
  }
  
  // 生成 Markdown
  let md = `# ${title}\n\n`
  for (const section of sections) {
    md += `## ${section.title}\n\n`
    for (const item of section.items) {
      md += `- ${item}\n`
    }
    md += '\n'
  }
  
  return md.trim()
}

/**
 * 从 URL 中提取内容（仅支持已知平台）
 * 注意：小程序中跨域请求受限，建议用户直接粘贴内容
 */
export function parseUrlToMarkdown(url, title = '我的旅行计划') {
  // 小红书链接
  if (url.includes('xiaohongshu.com') || url.includes('xhslink.com')) {
    return `# ${title}\n\n> 🔗 来源：小红书链接\n> ${url}\n\n## Day 1\n\n- 请手动补充行程内容\n\n> 💡 小红书链接需要登录才能访问，建议直接复制粘贴笔记内容`
  }
  
  // 大众点评
  if (url.includes('dianping.com')) {
    return `# ${title}\n\n> 🔗 来源：大众点评\n> ${url}\n\n## 行程安排\n\n- 请手动补充行程内容\n\n> 💡 建议直接复制粘贴点评内容`
  }
  
  // 通用链接
  return `# ${title}\n\n> 🔗 来源：${url}\n\n## Day 1\n\n- 请手动补充行程内容\n\n> 💡 建议直接复制粘贴内容以获取更好的解析效果`
}

/**
 * 智能导入：自动判断输入类型并解析
 */
export function smartImport(input, title = '我的旅行计划') {
  if (!input || !input.trim()) return ''
  
  const trimmed = input.trim()
  
  // 判断是否是 URL
  if (/^https?:\/\//i.test(trimmed)) {
    return parseUrlToMarkdown(trimmed, title)
  }
  
  // 判断是否是 Markdown（已有结构）
  if (/^#+\s/.test(trimmed) || /^[-*]\s/.test(trimmed)) {
    return trimmed
  }
  
  // 纯文本解析
  return parseTextToMarkdown(trimmed, title)
}

export default { parseTextToMarkdown, parseUrlToMarkdown, smartImport }

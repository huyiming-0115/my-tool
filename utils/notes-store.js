/**
 * 笔记本地存储工具
 * 数据结构：{ id, title, content, tags[], pinned, createdAt, updatedAt, excerpt }
 */

const STORAGE_KEY = "myNotes"
const SAMPLE_NOTES = [
  {
    id: "note-welcome",
    title: "欢迎来到笔记工具箱",
    content: `# 🎉 欢迎使用笔记工具箱

> 用 Markdown 记录你的灵感与思考，一处编写，随时预览。

---

## 快速上手

1. 点击底部 **+** 新建笔记
2. 左侧输入 Markdown 源码
3. 右侧 / 下方即时预览渲染结果
4. 通过 **标签** 和 **置顶** 管理笔记

## 支持的语法

- **标题**：\`# H1\` ~ \`### H3\`
- **加粗**：\`**文字**\`
- **斜体\`：\`*文字*\`
- **列表**：\`- item\` / \`1. item\`
- **引用**：\`> 引用内容\`
- **代码**：\` \`code\` \`
- **代码块**：三反引号
- **分隔线**：\`---\`
- **链接**：\`[文字](url)\`

---

> 💡 **提示：** 长呼笔记卡片可置顶或删除。

*开始记录你的第一篇笔记吧！*`,
    tags: ["欢迎", "教程"],
    pinned: true,
  },
  {
    id: "note-weekly",
    title: "本周工作计划",
    content: `# 本周工作计划
> 2026-07-15 ~ 2026-07-19

---

## 周一

- [x] 完成旅行计划小程序的**登录页**
- [x] 支持 Markdown 文档渲染
- [ ] 新建计划时支持导入 md 文件

## 周二

- [ ] 新增笔记功能
  - [ ] 列表页
  - [ ] 详情编辑页
  - [ ] 标签管理
- [ ] 修复 travel 页导航栏

## 周三

- [ ] 性能优化
- [ ] 代码清理

---

## 本周目标

1. 笔记功能 100% 完成
2. 游记模板沉淀
3. 完成首页工具箱焕新

> ⚡ 冲就完了！`,
    tags: ["工作", "计划"],
    pinned: false,
  },
  {
    id: "note-reading",
    title: "阅读清单",
    content: `# 📚 2026 年阅读清单

> 每本书都是一次新的旅行。

---

## 正在读

| 书名 | 作者 | 进度 | 评分 |
|------|------|------|------|
| 《人类简史》 | 尤瓦尔·赫拉利 | 60% | ⭐⭐⭐⭐⭐ |
| 《设计心理学》 | 唐纳德·诺曼 | 30% | ⭐⭐⭐⭐ |

## 想读

- [ ] 《代码整洁之道》
- [ ] 《重构》
- [ ] 《算法导论》
- [ ] 《百年孤独》

## 已读摘录

> "在漫长的岁月中，人类只是地球上一群不起眼的动物。短短几万年，我们却成了世界的主宰。"
> —— 《人类简史》

> "好的设计是显而易见的，但伟大的设计是透明的。"
> —— 《设计心理学》

---

*持续更新中...*`,
    tags: ["读书", "清单"],
    pinned: false,
  },
]

export function loadNotes() {
  try {
    const raw = uni.getStorageSync(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed) && parsed.length > 0) return parsed
    }
  } catch (e) { /* empty */ }
  // 首次启动塞进示例笔记
  const notes = SAMPLE_NOTES.map((n) => ({
    ...n,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * (24 - SAMPLE_NOTES.indexOf(n))).toISOString(),
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * (24 - SAMPLE_NOTES.indexOf(n))).toISOString(),
    excerpt: makeExcerpt(n.content),
  }))
  saveNotes(notes)
  return notes
}

export function saveNotes(notes) {
  uni.setStorageSync(STORAGE_KEY, JSON.stringify(notes))
}

export function getNote(notes, id) {
  return notes.find((n) => n.id === id) || null
}

export function makeExcerpt(markdown, maxLen = 80) {
  if (!markdown) return ""
  const clean = markdown
    .replace(/^#+\s+/gm, "")
    .replace(/^\>\s?/gm, "")
    .replace(/([\*\_\`\[\]\(\)])/g, "")
    .replace(/\n+/g, " ")
    .trim()
  return clean.length > maxLen ? clean.slice(0, maxLen) + "..." : clean
}

export function formatDate(iso) {
  if (!iso) return ""
  const d = new Date(iso)
  const now = new Date()
  const diffH = (now - d) / (1000 * 60 * 60)
  if (diffH < 1) return "刚刚"
  if (diffH < 24) return Math.floor(diffH) + " 小时前"
  if (diffH < 48) return "昨天"
  const sameY = d.getFullYear() === now.getFullYear()
  if (sameY) return `${d.getMonth() + 1}月${d.getDate()}日`
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`
}

export function getTags(notes) {
  const set = new Set()
  notes.forEach((n) => (n.tags || []).forEach((t) => set.add(t)))
  return Array.from(set).sort()
}

export function createEmptyNote() {
  const id = "note-" + Date.now()
  return {
    id,
    title: "",
    content: "# 新笔记\n\n开始编写...",
    tags: [],
    pinned: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    excerpt: "",
  }
}

export function upsertNote(notes, note) {
  const idx = notes.findIndex((n) => n.id === note.id)
  const updated = {
    ...note,
    excerpt: makeExcerpt(note.content),
    updatedAt: new Date().toISOString(),
  }
  if (idx >= 0) {
    notes[idx] = updated
  } else {
    notes.unshift(updated)
  }
  return notes
}

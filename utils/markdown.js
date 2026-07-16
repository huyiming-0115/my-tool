/**
 * 简易 Markdown 解析器 → 小程序 rich-text 节点数组
 * 支持：h1/h2/h3、列表、加粗、斜体、引用块、分隔线、表格、代码块、链接、图片、段落
 */

function parseInline(text) {
  const children = [];
  const regex = /(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`|\[([^\]]+)\]\((.+?)\))/g;
  let lastIndex = 0;
  let match;
  const seen = new Set();

  while ((match = regex.exec(text)) !== null) {
    // 防重复（处理转义等情况）
    if (seen.has(match.index)) { continue; }
    seen.add(match.index);
    if (match.index > lastIndex) {
      children.push({ type: "text", text: text.slice(lastIndex, match.index) });
    }
    if (match[2]) {
      children.push({ name: "strong", attrs: { style: "font-weight:700;" }, children: [{ type: "text", text: match[2] }] });
    } else if (match[3]) {
      children.push({ name: "em", attrs: { style: "font-style:italic;" }, children: [{ type: "text", text: match[3] }] });
    } else if (match[4]) {
      children.push({
        name: "code",
        attrs: { style: "background:#f5f5f5;border-radius:4rpx;padding:2rpx 8rpx;font-family:monospace;font-size:26rpx;color:#e74c3c;" },
        children: [{ type: "text", text: match[4] }],
      });
    } else if (match[5] && match[6]) {
      children.push({
        name: "a",
        attrs: { style: "color:#4a6cf7;text-decoration:underline;" },
        children: [{ type: "text", text: match[5] }],
      });
    }
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    children.push({ type: "text", text: text.slice(lastIndex) });
  }
  return children.length > 0 ? children : [{ type: "text", text: text }];
}

function escapeMd(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/**
 * 解析 Markdown → rich-text nodes
 */
export function parseMarkdown(text) {
  const lines = text.split("\n");
  const nodes = [];
  let i = 0;

  while (i < lines.length) {
    let line = lines[i];

    // 空行
    if (line.trim() === "") { i++; continue; }

    // 代码块 ``` ``` ```
    if (/^```/.test(line.trim())) {
      const codeLines = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i].trim())) {
        codeLines.push(lines[i]);
        i++;
      }
      i++; // skip closing ```
      nodes.push({
        name: "pre",
        attrs: { style: "background:#f5f5f5;border-radius:12rpx;padding:20rpx;margin:16rpx 0;overflow-x:auto;" },
        children: [{
          name: "code",
          attrs: { style: "font-family:monospace;font-size:24rpx;color:#333;white-space:pre-wrap;line-height:1.6;" },
          children: [{ type: "text", text: codeLines.join("\n") }],
        }],
      });
      continue;
    }

    // 表格 | ... | ... |
    if (/^\|.+\|$/.test(line.trim()) && i + 1 < lines.length && /^\|[\s\-:|]+\|$/.test(lines[i + 1].trim())) {
      // 解析表头
      const headerCells = line.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim());
      i += 2; // skip header + separator
      const bodyRows = [];
      while (i < lines.length && /^\|.+\|$/.test(lines[i].trim())) {
        const row = lines[i].trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim());
        bodyRows.push(row);
        i++;
      }
      // 转成 rich-text view 列表
      const tableStyle = "display:flex;flex-direction:column;border:2rpx solid #e0e0e0;border-radius:12rpx;margin:20rpx 0;overflow:hidden;";
      const rowStyle = "display:flex;border-bottom:2rpx solid #e0e0e0;";
      const lastRowStyle = "display:flex;";
      const cellStyle = "flex:1;padding:12rpx 16rpx;font-size:26rpx;line-height:1.6;";
      const headerCellStyle = cellStyle + "background:#4a6cf7;color:#fff;font-weight:600;";

      const tableChildren = [];
      // header row
      tableChildren.push({
        name: "view",
        attrs: { style: rowStyle },
        children: headerCells.map(c => ({
          name: "view",
          attrs: { style: headerCellStyle },
          children: parseInline(c),
        })),
      });
      // body rows
      bodyRows.forEach((row, idx) => {
        const rStyle = idx === bodyRows.length - 1 ? lastRowStyle : rowStyle;
        tableChildren.push({
          name: "view",
          attrs: { style: rStyle + (idx % 2 === 1 ? "background:#f8f9ff;" : "") },
          children: row.map(c => ({
            name: "view",
            attrs: { style: cellStyle },
            children: parseInline(c),
          })),
        });
      });
      nodes.push({ name: "view", attrs: { style: tableStyle }, children: tableChildren });
      continue;
    }

    // 分隔线
    if (/^---+$/.test(line.trim())) {
      nodes.push({ name: "view", attrs: { style: "height:2rpx;background:#e0e0e0;margin:30rpx 0;" }, children: [] });
      i++; continue;
    }

    // h1 - h6
    const h1m = line.match(/^#\s+(.*)/);
    if (h1m) {
      nodes.push({ name: "h1", attrs: { style: "font-size:44rpx;font-weight:700;color:#333;margin:30rpx 0 16rpx;line-height:1.4;" }, children: parseInline(h1m[1]) });
      i++; continue;
    }
    const h2m = line.match(/^##\s+(.*)/);
    if (h2m) {
      nodes.push({ name: "h2", attrs: { style: "font-size:36rpx;font-weight:700;color:#333;margin:24rpx 0 12rpx;line-height:1.4;" }, children: parseInline(h2m[1]) });
      i++; continue;
    }
    const h3m = line.match(/^###\s+(.*)/);
    if (h3m) {
      nodes.push({ name: "h3", attrs: { style: "font-size:30rpx;font-weight:600;color:#555;margin:20rpx 0 10rpx;line-height:1.4;" }, children: parseInline(h3m[1]) });
      i++; continue;
    }

    // 引用块（可能多行）
    if (/^>\s?/.test(line)) {
      const quoteLines = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        quoteLines.push(lines[i].replace(/^>\s?/, ""));
        i++;
      }
      nodes.push({
        name: "blockquote",
        attrs: { style: "border-left:6rpx solid #7c3aed;padding:16rpx 24rpx;margin:16rpx 0;background:#f3f0ff;border-radius:0 8rpx 8rpx 0;" },
        children: quoteLines.map((l, idx) => ({
          name: "p",
          attrs: { style: "font-size:28rpx;color:#555;line-height:1.8;" + (idx > 0 ? "margin-top:8rpx;" : "") },
          children: parseInline(l),
        })),
      });
      continue;
    }

    // 无序列表
    if (/^(\-|\*)\s+/.test(line)) {
      const listItems = [];
      while (i < lines.length && /^(\-|\*)\s+/.test(lines[i])) {
        const content = lines[i].replace(/^(\-|\*)\s+/, "");
        listItems.push(content);
        i++;
      }
      nodes.push({
        name: "ul",
        attrs: { style: "margin:12rpx 0;" },
        children: listItems.map(c => ({
          name: "li",
          attrs: { style: "font-size:28rpx;color:#333;padding:8rpx 0 8rpx 32rpx;line-height:1.8;position:relative;" },
          children: [
            { name: "span", attrs: { style: "color:#7c3aed;font-weight:700;margin-right:12rpx;" }, children: [{ type: "text", text: "•" }] },
            ...parseInline(c),
          ],
        })),
      });
      continue;
    }

    // 有序列表
    if (/^\d+\.\s+/.test(line)) {
      const listItems = [];
      while (i < lines.length && /^\d+\.\s+/.test(lines[i])) {
        const m = lines[i].match(/^(\d+)\.\s+(.*)$/);
        listItems.push({ num: m[1], content: m[2] });
        i++;
      }
      nodes.push({
        name: "ol",
        attrs: { style: "margin:12rpx 0;" },
        children: listItems.map(it => ({
          name: "li",
          attrs: { style: "font-size:28rpx;color:#333;padding:8rpx 0 8rpx 32rpx;line-height:1.8;" },
          children: [
            { name: "span", attrs: { style: "color:#4a6cf7;font-weight:700;margin-right:12rpx;" }, children: [{ type: "text", text: it.num + "." }] },
            ...parseInline(it.content),
          ],
        })),
      });
      continue;
    }

    // 段落
    nodes.push({
      name: "p",
      attrs: { style: "font-size:28rpx;color:#333;line-height:1.8;margin:12rpx 0;" },
      children: parseInline(line),
    });
    i++;
  }

  return { nodes };
}

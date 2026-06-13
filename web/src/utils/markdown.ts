const HEADING_RE = /^(#{1,6})\s+(.*)$/gm;

export function downloadMarkdown(filename: string, content: string) {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename.endsWith('.md') ? filename : `${filename}.md`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function demoteHeadings(content: string): string {
  return content.replace(HEADING_RE, '#$1 $2');
}

export function buildMarkdownPreview(pairs: { role: string; content: string }[]): string {
  const lines: string[] = [];
  for (const pair of pairs) {
    const header = pair.role === 'user' ? '# 用户' : pair.role === 'assistant' ? '# 模型' : `# ${pair.role}`;
    lines.push(header, '', demoteHeadings(pair.content), '');
  }
  return lines.join('\n');
}

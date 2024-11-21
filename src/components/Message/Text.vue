<script lang="ts" setup>
import { computed, onMounted, onUnmounted, onUpdated, ref } from 'vue'
import MarkdownIt from 'markdown-it'
import MdKatex from '@vscode/markdown-it-katex'
import MdLinkAttributes from 'markdown-it-link-attributes'
import MdMermaid from 'mermaid-it-markdown'
import hljs from 'highlight.js'
//import { useBasicLayout } from '@/hooks/useBasicLayout'
import { copyToClip } from '@/utils/copy'
import { ElNotification } from 'element-plus'
// 高亮样式
import 'highlight.js/styles/atom-one-dark.css'
import 'github-markdown-css';

interface Props {
  text?: string
  loading?: boolean
}

const props = defineProps<Props>()

//const { isMobile } = useBasicLayout()

const textRef = ref<HTMLElement>()

const mdi = new MarkdownIt({
  html: false,
  linkify: true,
  highlight(code, language) {
    const validLang = !!(language && hljs.getLanguage(language))
    if (validLang) {
      const lang = language ?? ''
      return highlightBlock(hljs.highlight(code, { language: lang }).value, lang)
    }
    return highlightBlock(hljs.highlightAuto(code).value, '')
  },
})

mdi.use(MdLinkAttributes, { attrs: { target: '_blank', rel: 'noopener' } }).use(MdKatex).use(MdMermaid)



const text = computed(() => {
  const value = props.text ?? ''
  // 对数学公式进行处理，自动添加 $$ 符号
  const escapedText = escapeBrackets(escapeDollarNumber(value))
    return mdi.render(escapedText)
  return value
})

function highlightBlock(str: string, lang?: string) {
  // return `<pre class="code-block-wrapper"><div class="code-block-header"><span class="code-block-header__lang">${lang}</span><span class="code-block-header__copy">复制代码</span></div><code class="hljs code-block-body ${lang}">${str}</code></pre>`
  return `<pre><div class="tongyi-design-highlighter global-dark-theme"><span class="tongyi-design-highlighter-header"><span class="tongyi-design-highlighter-lang">${lang}</span><div class="tongyi-design-highlighter-right-actions"><svg t="1731486131256" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1155" xmlns:xlink="http://www.w3.org/1999/xlink" width="12" height="12" class="cursor-pointer flex items-center tongyi-design-highlighter-copy-btn"><path d="M751.365 153.361l254.25 237.45 0.448 633.189H253.018V907.986H86.048c-37.618 0-68.115-30.499-68.115-68.124V68.129C17.933 30.509 48.43 0.005 86.048 0.005h611.875c37.612 0 68.11 30.503 68.11 68.124v68.124l-77.962-0.07v-38.27c0-12.591-10.22-22.732-22.735-22.732l-552.458 0.072c-12.592 0-22.73 10.215-22.73 22.73V805.55c0 12.586 10.138 22.734 22.73 22.734h140.14V657.273h0.46l-0.46-504.247 498.347 0.335z m-27.694 45.504v229.204h235.327L723.671 198.865zM300.086 657.273V978.16h658.912V473.912H676.607V198.865h-376.52v458.408z m569.678-32.854h-473.24v-47.286h473.24v47.286z m0 94.6h-473.24v-47.295h473.24v47.296z m0 94.574h-473.24v-47.287h473.24v47.287z" p-id="1156"></path></svg></div></span><div><pre style="display: block; overflow-x: auto; background: #2c2c36; color: rgb(248, 248, 242); padding: 16px 8px; margin: 0px; font-size: 13px;border-radius:0px"><code class="hljs code-block-body ${lang}">${str}</code></pre></div></div></pre>`
}

function addCopyEvents() {
  if (textRef.value) {
    const initialSvg = `M751.365 153.361l254.25 237.45 0.448 633.189H253.018V907.986H86.048c-37.618 0-68.115-30.499-68.115-68.124V68.129C17.933 30.509 48.43 0.005 86.048 0.005h611.875c37.612 0 68.11 30.503 68.11 68.124v68.124l-77.962-0.07v-38.27c0-12.591-10.22-22.732-22.735-22.732l-552.458 0.072c-12.592 0-22.73 10.215-22.73 22.73V805.55c0 12.586 10.138 22.734 22.73 22.734h140.14V657.273h0.46l-0.46-504.247 498.347 0.335z m-27.694 45.504v229.204h235.327L723.671 198.865zM300.086 657.273V978.16h658.912V473.912H676.607V198.865h-376.52v458.408z m569.678-32.854h-473.24v-47.286h473.24v47.286z m0 94.6h-473.24v-47.295h473.24v47.296z m0 94.574h-473.24v-47.287h473.24v47.287z`
    const copiedPath = `M892.064 261.888a31.936 31.936 0 0 0-45.216 1.472L421.664 717.248l-220.448-185.216a32 32 0 1 0-41.152 48.992l243.648 204.704a31.872 31.872 0 0 0 20.576 7.488 31.808 31.808 0 0 0 23.36-10.112L893.536 307.136a32 32 0 0 0-1.472-45.248z`
    const copyBtn = textRef.value.querySelectorAll('.tongyi-design-highlighter-copy-btn')
    copyBtn.forEach((btn) => {
      btn.addEventListener('click', () => {
        const code = btn.parentElement?.parentElement?.nextElementSibling?.textContent
        if (code) {
          copyToClip(code).then(() => {
          btn.querySelector('path')?.setAttribute('d', copiedPath);
          ElNotification({
            title: '成功',
            message: '复制成功',
            type: 'success'
          })
            setTimeout(() => {
              btn.querySelector('path')?.setAttribute('d', initialSvg);
            }, 1000)
          })
        }
      })
    })
  }
}

function removeCopyEvents() {
  if (textRef.value) {
    const copyBtn = textRef.value.querySelectorAll('.tongyi-design-highlighter-copy-btn')
    copyBtn.forEach((btn) => {
      btn.removeEventListener('click', () => { })
    })
  }
}

function escapeDollarNumber(text: string) {
  let escapedText = ''

  for (let i = 0; i < text.length; i += 1) {
    let char = text[i]
    const nextChar = text[i + 1] || ' '

    if (char === '$' && nextChar >= '0' && nextChar <= '9')
      char = '\\$'

    escapedText += char
  }

  return escapedText
}

function escapeBrackets(text: string) {
  const pattern = /(```[\s\S]*?```|`.*?`)|\\\[([\s\S]*?[^\\])\\\]|\\\((.*?)\\\)/g
  return text.replace(pattern, (match, codeBlock, squareBracket, roundBracket) => {
    if (codeBlock)
      return codeBlock
    else if (squareBracket)
      return `$$${squareBracket}$$`
    else if (roundBracket)
      return `$${roundBracket}$`
    return match
  })
}

onMounted(() => {
  addCopyEvents()
})

onUpdated(() => {
  addCopyEvents()
})

onUnmounted(() => {
  removeCopyEvents()
})
</script>

<template>
  <div class="text-black">
    <div ref="textRef" class="leading-relaxed break-words">
      <div>
        <div v-if="!props.loading"  class="markdown-body"  v-html="text" />
        <div v-else class="loading-container">
          <div class="moving-div">
            <svg-icon className="load-icon" icon="icon-loading"></svg-icon>
          </div>
        </div>
        <div v-show="!text && !props.loading">
            <el-empty description="数据为空" />
        </div>  
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.markdown-body {
  background-color: transparent;
  font-size: 14px;
}  
pre {
    padding: 0px !important;
}

:deep .tongyi-design-highlighter-header {
    align-items: center;
    background-color: #585a73;
    color: #fafafc;
    display: flex;
    font-size: 14px;
    height: 32px;
    padding: 0 14px
}

:deep .tongyi-design-highlighter {
  border-radius: 4px
}

:deep .tongyi-design-highlighter-right-actions {
    align-items: center;
    display: flex
}

:deep .tongyi-design-highlighter-lang {
    color: #fafafa;
    font-weight: 500;
    margin-right: auto
}

:deep .tongyi-design-highlighter-lang:first-letter {
    text-transform: uppercase
}

:deep .tongyi-design-highlighter-copy-btn {
    fill: #fafafa;
}

:deep .tongyi-design-highlighter-header+div>pre {
    padding: 16px!important;
}

:deep .markdown-body  pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    color: #1f2328;
    font-size: 100%;
    line-height: 1.45;
    overflow: auto;
    word-wrap: normal;
    margin-bottom: 1em;
    margin-top: 1em;
    padding: 0px;
}

:deep .tongyi-design-highlighter-copy-btn {
    fill: #f2f3f7;
    cursor: pointer;
    display: flex;
    align-items: center;
}

:deep .load-icon {
  width: 100px !important;
  height: 60px !important;
}

.loading-container {
  position: relative;
  width: 100%;
  height: 40px;
}

.moving-div {
  position: absolute;
  width: 100px; /* 根据实际需求调整 */
  height: 60px; /* 根据实际需求调整 */
  animation: moveRight 5s linear infinite;
}

@keyframes moveRight {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(50vw);
  }
}
</style>
/* scroll-motion ショールームのUI制御。
   外部ライブラリを読み込まない（オフライン動作）。

   フック:
   - [data-code-tab="css|tailwind"]  : コード表示の切替（ライブデモは CSS 版のまま）
   - [data-action="copy"]            : 表示中コードのコピー
   - [data-action="rerun"]           : ライブデモ iframe の再読み込み
   - [data-detail-link]              : 選択中バリアントの詳細デモへ遷移
*/

(() => {
  'use strict';

  const LANG_LABELS = { css: 'CSS版', tailwind: 'Tailwind版' };
  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

  function applyMotionPreference() {
    document.documentElement.classList.toggle('reduce-motion', motionQuery.matches);
  }

  function setStatus(card, message) {
    const status = card.querySelector('[data-copy-status]');
    if (!status) {
      return;
    }
    status.textContent = message;
    if (status.dataset.timerId) {
      window.clearTimeout(Number(status.dataset.timerId));
    }
    const timerId = window.setTimeout(() => {
      status.textContent = '';
      delete status.dataset.timerId;
    }, 2600);
    status.dataset.timerId = String(timerId);
  }

  function panels(card) {
    return Array.from(card.querySelectorAll('[data-code-panel]'));
  }

  function activateTab(card, lang, moveFocus) {
    const normalized = lang === 'tailwind' ? 'tailwind' : 'css';
    card.querySelectorAll('[data-code-tab]').forEach((tab) => {
      const selected = tab.dataset.codeTab === normalized;
      tab.setAttribute('aria-selected', selected ? 'true' : 'false');
      tab.tabIndex = selected ? 0 : -1;
      if (selected && moveFocus) {
        tab.focus();
      }
    });
    panels(card).forEach((panel) => {
      panel.hidden = panel.dataset.codePanel !== normalized;
    });
    card.dataset.currentLang = normalized;
    const label = card.querySelector('[data-lang-label]');
    if (label) {
      label.textContent = LANG_LABELS[normalized];
    }
    const detailLink = card.querySelector('[data-detail-link]');
    if (detailLink) {
      const href = normalized === 'tailwind' ? card.dataset.detailTailwind : card.dataset.detailCss;
      if (href) {
        detailLink.setAttribute('href', href);
      }
      detailLink.textContent = normalized === 'tailwind' ? '詳細デモを開く（Tailwind版）' : '詳細デモを開く（CSS版）';
    }
  }

  function visibleCode(card) {
    const lang = card.dataset.currentLang === 'tailwind' ? 'tailwind' : 'css';
    const panel = card.querySelector(`[data-code-panel="${lang}"]`);
    return { lang: lang, code: panel ? panel.textContent : '' };
  }

  async function writeClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (error) {
        /* file:// などで拒否された場合は textarea 方式へフォールバックする */
      }
    }
    try {
      const area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', 'readonly');
      area.style.position = 'fixed';
      area.style.top = '-1000px';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      area.setSelectionRange(0, area.value.length);
      const ok = document.execCommand('copy');
      document.body.removeChild(area);
      return ok;
    } catch (error) {
      return false;
    }
  }

  async function copyCode(card) {
    const current = visibleCode(card);
    const ok = await writeClipboard(current.code);
    setStatus(
      card,
      ok
        ? `${LANG_LABELS[current.lang]}のコード（${current.code.split('\n').length} 行）をコピーしました`
        : 'コピーできませんでした。コードを選択して手動でコピーしてください'
    );
  }

  function rerunDemo(card) {
    const frame = card.querySelector('[data-demo-frame]');
    if (!frame) {
      return;
    }
    const src = card.dataset.demoSrc || frame.getAttribute('src');
    const fresh = frame.cloneNode(false);
    fresh.setAttribute('src', src);
    fresh.setAttribute('loading', 'lazy');
    frame.replaceWith(fresh);
    setStatus(card, 'ライブデモを再読み込みしました');
  }

  function cardOf(element) {
    return element.closest ? element.closest('.card[data-effect]') : null;
  }

  document.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) {
      return;
    }
    const card = cardOf(button);
    if (!card) {
      return;
    }
    if (button.dataset.action === 'copy') {
      copyCode(card);
      return;
    }
    if (button.dataset.action === 'rerun') {
      rerunDemo(card);
      return;
    }
    if (button.dataset.codeTab) {
      activateTab(card, button.dataset.codeTab, false);
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') {
      return;
    }
    const tab = event.target.closest('[data-code-tab]');
    if (!tab) {
      return;
    }
    const card = cardOf(tab);
    if (!card) {
      return;
    }
    const tabs = Array.from(card.querySelectorAll('[data-code-tab]'));
    const index = tabs.indexOf(tab);
    const next = event.key === 'ArrowRight' ? (index + 1) % tabs.length : (index - 1 + tabs.length) % tabs.length;
    event.preventDefault();
    activateTab(card, tabs[next].dataset.codeTab, true);
  });

  document.querySelectorAll('.card[data-effect]').forEach((card) => {
    activateTab(card, card.dataset.currentLang, false);
  });

  applyMotionPreference();
  if (typeof motionQuery.addEventListener === 'function') {
    motionQuery.addEventListener('change', applyMotionPreference);
  }
})();

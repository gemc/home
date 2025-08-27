// assets/js/doc-toc.js
document.addEventListener('DOMContentLoaded', () => {
  const toc = document.querySelector('.toc');
  if (!toc) return;

  // Change to 'global' if you want to close EVERYTHING except the branch you open.
  const ACCORDION_MODE = 'siblings'; // 'siblings' | 'global'

  // --- helpers ---------------------------------------------------------------
  const hasChildren = (li) => !!li.querySelector(':scope > ul');

  function setExpanded(li, expanded, { closeSiblings = false } = {}) {
    if (!hasChildren(li)) return;
    li.classList.toggle('is-collapsed', !expanded);
    li.setAttribute('aria-expanded', expanded ? 'true' : 'false');

    const btn = li.querySelector(':scope > .toc-toggle');
    if (btn) btn.textContent = expanded ? '▾' : '▸';

    if (closeSiblings) {
      collapseSiblings(li);
    }
    if (ACCORDION_MODE === 'global' && expanded) {
      collapseAllExcept(li);
    }
  }

  function collapseSiblings(li) {
    const parent = li.parentElement; // UL
    if (!parent) return;
    parent.querySelectorAll(':scope > li.has-children').forEach(sib => {
      if (sib !== li) setExpanded(sib, false);
    });
  }

  function collapseAllExcept(keepLi) {
    toc.querySelectorAll('li.has-children').forEach(li => {
      if (!li.contains(keepLi)) setExpanded(li, false);
    });
  }

  function expandToHash(hash) {
    if (!hash) return;
    const active = toc.querySelector(`a[href="${hash}"]`);
    if (!active) return;

    toc.querySelectorAll('a').forEach(a => a.classList.remove('is-active'));
    active.classList.add('is-active');

    // Walk up from the active link, expanding parents and collapsing siblings
    let node = active.parentElement;
    while (node && node !== toc) {
      if (node.tagName === 'LI' && node.classList.contains('has-children')) {
        setExpanded(node, true, { closeSiblings: true });
      }
      node = node.parentElement;
    }
  }

  // --- build toggles & initial state ----------------------------------------
  toc.querySelectorAll('li').forEach(li => {
    const sub = li.querySelector(':scope > ul');
    if (!sub) return;

    li.classList.add('has-children', 'is-collapsed');
    li.setAttribute('aria-expanded', 'false');

    const link = li.querySelector(':scope > a');
    const btn = document.createElement('button');
    btn.className = 'toc-toggle';
    btn.setAttribute('aria-label', 'Toggle section');
    btn.setAttribute('aria-controls', ''); // purely presentational here
    btn.textContent = '▸';
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const expanded = li.classList.contains('is-collapsed');
      setExpanded(li, expanded, { closeSiblings: true });
    });
    li.insertBefore(btn, link);

    // NEW: clicking the TEXT also toggles (and still navigates to the section)
    link.addEventListener('click', () => {
      // Don’t prevent default — we want the hash navigation.
      const willExpand = li.classList.contains('is-collapsed');
      setExpanded(li, willExpand, { closeSiblings: true });
      // Navigation occurs; expandToHash() will also run on hashchange.
    });
  });

  // initial highlight/expand (if landing with a hash)
  expandToHash(location.hash);
  window.addEventListener('hashchange', () => expandToHash(location.hash));
});

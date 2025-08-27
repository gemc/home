document.addEventListener('DOMContentLoaded', () => {
  const toc = document.querySelector('.toc');
  if (!toc) return;

  const sidebar = toc.closest('.doc__toc') || document.scrollingElement;
  const hasChildren = (li) => !!li.querySelector(':scope > ul');

  // Keep the clicked row's position stable inside the sidebar while DOM expands/collapses.
  function stabilize(rowEl, mutator) {
    if (!rowEl || !sidebar) { mutator(); return; }
    const before = rowEl.getBoundingClientRect().top - sidebar.getBoundingClientRect().top;
    mutator();
	
    // Let layout settle a tick (works across Safari/Chrome/Firefox)
    requestAnimationFrame(() => {
      const after = rowEl.getBoundingClientRect().top - sidebar.getBoundingClientRect().top;
      sidebar.scrollTop += (after - before);
    });
  }

  function setExpanded(li, expanded) {
    if (!hasChildren(li)) return;
    li.classList.toggle('is-collapsed', !expanded);
    li.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    const btn = li.querySelector(':scope > .toc-toggle');
    if (btn) btn.textContent = expanded ? '▾' : '▸';
  }

  function selectTopic(li) {
    // Only one selected at a time
    toc.querySelectorAll('li.is-selected').forEach(n => n.classList.remove('is-selected'));
    li.classList.add('is-selected');
  }

  function expandToHash(hash) {
    if (!hash) return;
    const active = toc.querySelector(`a[href="${hash}"]`);
    if (!active) return;

    toc.querySelectorAll('a').forEach(a => a.classList.remove('is-active'));
    active.classList.add('is-active');

    // Ensure ancestors are expanded so the active item is visible
    let node = active.parentElement;
    let selected = null;
    stabilize(active.closest('li'), () => {
      while (node && node !== toc) {
        if (node.tagName === 'LI' && node.classList.contains('has-children')) {
          setExpanded(node, true);
          selected = selected || node; // nearest parent topic
        }
        node = node.parentElement;
      }
    });
    if (selected) selectTopic(selected);
  }

  // Build toggles & initial state
  toc.querySelectorAll('li').forEach(li => {
    const sub = li.querySelector(':scope > ul');
    if (!sub) return;

    li.classList.add('has-children', 'is-collapsed');
    li.setAttribute('aria-expanded', 'false');

    const link = li.querySelector(':scope > a');
    const btn = document.createElement('button');
    btn.className = 'toc-toggle';
    btn.setAttribute('aria-label', 'Toggle section');
    btn.textContent = '▸';

    // Prevent focus-on-mousedown from nudging sidebar in Safari
    if (link) link.addEventListener('mousedown', (e) => e.preventDefault());

    // Clicking the caret toggles ONLY this item, and keeps the row stationary
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      stabilize(li, () => {
        const willExpand = li.classList.contains('is-collapsed');
        setExpanded(li, willExpand);
        selectTopic(li);
      });
    });

    // Clicking the text navigates, toggles ONLY this item, and keeps the row stationary
    if (link) {
      link.addEventListener('click', () => {
        stabilize(li, () => {
          const willExpand = li.classList.contains('is-collapsed');
          setExpanded(li, willExpand);
          selectTopic(li);
        });
        // Let the browser handle hash navigation normally.
      });
    }

    li.insertBefore(btn, link);
  });

  // Initial highlight/expand (if landing with a hash)
  expandToHash(location.hash);
  window.addEventListener('hashchange', () => expandToHash(location.hash));
});

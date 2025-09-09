document.addEventListener('DOMContentLoaded', () => {
	const doc = document.querySelector('.doc');
	const toc = document.querySelector('.toc');
	// Never let link clicks bubble up and trigger any accidental toggles
	toc.addEventListener('click', (e) => {
		if (e.target.closest('a')) {
			e.stopPropagation();
		}
	}, true); // capture

	if (!doc || !toc) return;

	const activeTopicId = doc.getAttribute('data-active-topic');
	if (activeTopicId) {
		const grp = toc.querySelector(`.toc-group[data-topic="${activeTopicId}"]`);
		if (grp) grp.classList.add('is-selected');
	}

	const norm = s => (s || '').trim().replace(/\s+/g, ' ').toLowerCase();

// -------- Build nested H1/H2 list from fetched page --------
function buildTocList(docEl, baseHref, topicTitle) {
  const topicNorm = norm(topicTitle);
  const article = docEl.querySelector('article.doc__content') || docEl;
  // use H1/H2 instead of H2/H3
  const heads = Array.from(article.querySelectorAll('h1, h2'));
  if (!heads.length) return null;

  const ul = document.createElement('ul');
  let currentH1Li = null;
  let subUl = null;
  let sawTopH1 = false;

  heads.forEach(h => {
    const level = h.tagName === 'H1' ? 1 : 2;
    const text = (h.textContent || '').trim();
    const textNorm = norm(text);

    // Skip duplicate topic-title H1
    if (level === 1 && !sawTopH1) {
      sawTopH1 = true;
      if (topicNorm && textNorm === topicNorm) return;
    }

    let id = h.id;
    if (!id) id = text.toLowerCase().replace(/[^\w\- ]+/g, '').replace(/\s+/g, '-');

    const li = document.createElement('li');
    const a = document.createElement('a');
    a.textContent = text;
    a.href = `${baseHref}#${id}`;
    a.classList.add(`toc-h${level}`);
    li.appendChild(a);

    if (level === 1) {
      ul.appendChild(li);
      currentH1Li = li;
      subUl = null;
    } else {
      if (!currentH1Li) {
        ul.appendChild(li);
      } else {
        if (!subUl) {
          subUl = document.createElement('ul');
          currentH1Li.appendChild(subUl);
        }
        subUl.appendChild(li);
      }
    }
  });

  return ul.childElementCount ? ul : null;
}


	// -------- Enhance a built tree (caret-only collapse, with state memory) --------
	function enhanceTocTree(tree) {
		// Tracks which li are expanded (remembered across hash changes)
		const expandedSet = new WeakSet();

		// Initialize items; start collapsed
		tree.querySelectorAll('li').forEach(li => {
			const sub = li.querySelector(':scope > ul');
			const link = li.querySelector(':scope > a');
			if (sub) {
				li.classList.add('has-children', 'is-collapsed');
				li.setAttribute('aria-expanded', 'false');

				const btn = document.createElement('button');
				btn.className = 'toc-toggle';
				btn.setAttribute('aria-label', 'Toggle section');
				btn.textContent = '▸';
				li.insertBefore(btn, link);
			}
		});

		// Helper to set expanded state and remember it
		function setExpanded(li, expanded) {
			if (!li || !li.classList.contains('has-children')) return;
			li.classList.toggle('is-collapsed', !expanded);
			li.setAttribute('aria-expanded', expanded ? 'true' : 'false');
			const caret = li.querySelector(':scope > .toc-toggle');
			if (caret) caret.textContent = expanded ? '▾' : '▸';
			if (expanded) expandedSet.add(li); else expandedSet.delete(li);
		}

		// Event delegation: ONLY caret toggles expansion
		tree.addEventListener('click', (e) => {
			const caret = e.target.closest('.toc-toggle');
			if (!caret) return;
			e.preventDefault();
			e.stopPropagation();
			const li = caret.closest('li.has-children');
			if (!li) return;
			const willExpand = li.classList.contains('is-collapsed');
			setExpanded(li, willExpand);
		});

		// Capture-phase suppression for link clicks so nothing upstream toggles
		tree.addEventListener('click', (e) => {
			const link = e.target.closest('a');
			if (!link) return;

			// Never let link clicks toggle collapse
			e.stopPropagation(); // capture handler prevents bubbling toggles

			const href = link.getAttribute('href') || '';
			const here = location.pathname.replace(/\/+$/, '');
			let url = null;
			try {
				url = new URL(href, location.origin);
			} catch {
			}

			const there = url ? url.pathname.replace(/\/+$/, '') : here;
			const hasHash = url ? !!url.hash : href.startsWith('#');
			const isSame = (there === here);

			if (isSame && !hasHash) {
				// Topic link without hash -> go to top; do not change collapse state
				e.preventDefault();
				history.replaceState(null, '', here);
				window.scrollTo({top: 0, behavior: 'auto'});
				const title = document.querySelector('.doc__content .page-title');
				if (title) {
					title.classList.remove('is-hidden-title');
					title.removeAttribute('aria-hidden');
				}
			}
			// Same-page with hash: let default proceed (right content scrolls).
			// Cross-topic: allow navigation.
		}, true);

		// Expand ancestors of active link and then re-apply remembered expansions
		function markActiveFromHash() {
			const currentPath = location.pathname.replace(/\/+$/, '');
			const hash = location.hash;

			tree.querySelectorAll('a.is-active').forEach(a => a.classList.remove('is-active'));

			let active = null;
			if (hash) {
				active = tree.querySelector(`a[href="${currentPath}${hash}"]`) ||
					tree.querySelector(`a[href$="${hash}"]`);
			}
			if (active) {
				active.classList.add('is-active');

				// Ensure the active item is visible: expand ancestors ONLY
				let node = active.parentElement;
				while (node && node !== tree) {
					if (node.matches('li.has-children.is-collapsed')) {
						setExpanded(node, true); // also records in expandedSet
					}
					node = node.parentElement;
				}
			}

			// Re-apply any remembered expanded nodes that might have been altered
			tree.querySelectorAll('li.has-children').forEach(li => {
				if (expandedSet.has(li)) setExpanded(li, true);
			});
		}

		markActiveFromHash();
		window.addEventListener('hashchange', markActiveFromHash);
		// Safari sometimes paints before classes apply—nudge once more on the next frame
		window.addEventListener('hashchange', () => requestAnimationFrame(markActiveFromHash));

	}

	// -------- Build each topic group --------
	toc.querySelectorAll('.toc-group').forEach(async (group) => {
		const base = group.getAttribute('data-base') || '';
		const title = group.getAttribute('data-title') || '';
		const tree = group.querySelector('.toc-tree');
		if (!base || !tree) return;

		try {
			const res = await fetch(base, {credentials: 'same-origin'});
			if (!res.ok) throw new Error(`HTTP ${res.status}`);
			const html = await res.text();

			const parser = new DOMParser();
			const docEl = parser.parseFromString(html, 'text/html');

			const ul = buildTocList(docEl, base, title);
			tree.innerHTML = '';
			if (ul) {
				tree.appendChild(ul);
				enhanceTocTree(tree);
			}
		} catch (e) {
			tree.innerHTML = '';
		}
	});
});

// ---- Hide page title when on a section (hash present) ----
function togglePageTitle() {
	const title = document.querySelector('.doc__content .page-title');
	if (!title) return;
	if (location.hash) {
		title.classList.add('is-hidden-title');
		title.setAttribute('aria-hidden', 'true');
	} else {
		title.classList.remove('is-hidden-title');
		title.removeAttribute('aria-hidden');
	}
}

document.addEventListener('DOMContentLoaded', togglePageTitle);
window.addEventListener('hashchange', togglePageTitle);

// ---- Card click → open TOC group (no navigation) ----
(function enableTopicOpeners() {
	const toc = document.querySelector('.toc');
	if (!toc) return;

	function expandGroupById(id) {
		const group = toc.querySelector(`.toc-group[data-topic="${id}"]`);
		if (!group) return;

		toc.querySelectorAll('.toc-group.is-selected').forEach(g => g.classList.remove('is-selected'));
		group.classList.add('is-selected');

		group.querySelectorAll('.toc-tree li.has-children').forEach(li => {
			li.classList.remove('is-collapsed');
			li.setAttribute('aria-expanded', 'true');
			const caret = li.querySelector(':scope > .toc-toggle');
			if (caret) caret.textContent = '▾';
		});

		const aside = document.querySelector('.doc__toc');
		if (aside) aside.scrollTo({top: group.offsetTop - 8, behavior: 'smooth'});
	}

	document.addEventListener('click', (e) => {
		const a = e.target.closest('a.js-open-topic[data-open-topic]');
		if (!a) return;
		const id = a.getAttribute('data-open-topic');
		if (!id) return;

		e.preventDefault();
		const basePath = location.pathname.replace(/\/+$/, '');
		history.replaceState(null, '', `${basePath}#topic=${encodeURIComponent(id)}`);
		expandGroupById(id);
	});

	if (location.hash.startsWith('#topic=')) {
		const id = decodeURIComponent(location.hash.slice(7));
		window.requestAnimationFrame(() => expandGroupById(id));
	}
})();

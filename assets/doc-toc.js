document.addEventListener('DOMContentLoaded', () => {
	const doc = document.querySelector('.doc');
	const toc = document.querySelector('.toc');
	if (!doc || !toc) return;

	const activeTopicId = doc.getAttribute('data-active-topic');

	if (activeTopicId) {
		const grp = toc.querySelector(`.toc-group[data-topic="${activeTopicId}"]`);
		if (grp) grp.classList.add('is-selected');
	}

	const norm = s => (s || '').trim().replace(/\s+/g, ' ').toLowerCase();

	// Build a nested <ul> of H2/H3 from a fetched page Document
	function buildTocList(docEl, baseHref, topicTitle) {
		const topicNorm = norm(topicTitle);
		const article = docEl.querySelector('article.doc__content') || docEl;
		const heads = Array.from(article.querySelectorAll('h2, h3'));
		if (!heads.length) return null;

		const ul = document.createElement('ul');
		let currentH2Li = null;
		let subUl = null;
		let sawTopH2 = false;

		heads.forEach(h => {
			const level = h.tagName === 'H2' ? 2 : 3;
			const text = (h.textContent || '').trim();
			const textNorm = norm(text);

			// Skip the topic-title H2 (duplicates the group name)
			if (level === 2 && !sawTopH2) {
				sawTopH2 = true;
				if (topicNorm && textNorm === topicNorm) return; // ← skip
			}

			let id = h.id;
			if (!id) {
				id = text.toLowerCase().replace(/[^\w\- ]+/g, '').replace(/\s+/g, '-');
			}

			const li = document.createElement('li');
			const a = document.createElement('a');
			a.textContent = text;
			a.href = `${baseHref}#${id}`;
			a.classList.add(`toc-h${level}`);
			li.appendChild(a);

			if (level === 2) {
				ul.appendChild(li);
				currentH2Li = li;
				subUl = null;
			} else {
				if (!currentH2Li) {
					ul.appendChild(li);
				} else {
					if (!subUl) {
						subUl = document.createElement('ul');
						currentH2Li.appendChild(subUl);
					}
					subUl.appendChild(li);
				}
			}
		});

		return ul.childElementCount ? ul : null;
	}

	function enhanceTocTree(tree) {
		tree.querySelectorAll('li').forEach(li => {
			const sub = li.querySelector(':scope > ul');
			if (!sub) return;

			li.classList.add('has-children', 'is-collapsed');
			li.setAttribute('aria-expanded', 'false');

			const link = li.querySelector(':scope > a');
			const btn = document.createElement('button');
			btn.className = 'toc-toggle';
			btn.setAttribute('aria-label', 'Toggle section');
			btn.textContent = '▸';

			function setExpanded(expanded) {
				li.classList.toggle('is-collapsed', !expanded);
				li.setAttribute('aria-expanded', expanded ? 'true' : 'false');
				btn.textContent = expanded ? '▾' : '▸';
			}

			btn.addEventListener('click', (e) => {
				e.preventDefault();
				setExpanded(li.classList.contains('is-collapsed'));
			});

			if (link) {
				const href = link.getAttribute('href') || '';
				const here = location.pathname.replace(/\/+$/, '');
				let url = null;
				try {
					url = new URL(href, location.origin);
				} catch {
				}

				const there = url ? url.pathname.replace(/\/+$/, '') : here;
				const hasHash = url ? !!url.hash : href.startsWith('#');
				const isSamePage = (there === here);

				if (isSamePage && hasHash) {
					// Same page + hash → let the browser scroll the RIGHT content normally.
					// (Optionally auto-expand this branch)
					link.addEventListener('click', () => {
						if (li.classList.contains('has-children')) setExpanded(true);
						// No preventDefault: allow natural scroll to the heading.
						// Your CSS (scroll-margin-top) should keep it below the fixed header.
						// Active highlight will update on hashchange.
					});
				} else if (isSamePage && !hasHash) {
					// Same page, NO hash (clicking the main topic) → scroll to top.
					link.addEventListener('click', (e) => {
						e.preventDefault();
						history.replaceState(null, '', here); // clear hash
						window.scrollTo({top: 0, behavior: 'auto'});
						// Re-show page title if you hide it when a hash exists:
						const title = document.querySelector('.doc__content .page-title');
						if (title) {
							title.classList.remove('is-hidden-title');
							title.removeAttribute('aria-hidden');
						}
						// Clear any active link state in this tree:
						tree.querySelectorAll('a.is-active').forEach(a => a.classList.remove('is-active'));
					});
				} else {
					// Cross-topic → normal navigation
					// (leave it alone so the browser loads the other topic page)
				}
			}


			li.insertBefore(btn, link);
		});

		function markActiveFromHash() {
			const currentPath = location.pathname.replace(/\/+$/, '');
			const hash = location.hash;

			tree.querySelectorAll('a.is-active').forEach(a => a.classList.remove('is-active'));

			let active = null;
			if (hash) {
				active = tree.querySelector(`a[href="${currentPath}${hash}"]`) ||
					tree.querySelector(`a[href$="${hash}"]`);
			}
			if (!active) return;

			active.classList.add('is-active');

			let node = active.parentElement;
			while (node && node !== tree) {
				if (node.matches('li.has-children.is-collapsed')) {
					node.classList.remove('is-collapsed');
					node.setAttribute('aria-expanded', 'true');
					const b = node.querySelector(':scope > .toc-toggle');
					if (b) b.textContent = '▾';
				}
				node = node.parentElement;
			}
		}

		markActiveFromHash();
		window.addEventListener('hashchange', markActiveFromHash);
	}

	// Build each topic group’s tree
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
			// console.warn('TOC fetch failed for', base, e);
		}
	});
});

// Hide the big page title when viewing a section (hash present)
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

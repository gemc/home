#### Link checker:

https://validator.w3.org/checklink/

https://www.deadlinkchecker.com/



# Tabs in markdown.

- the plugin read_file is installed in _plugins
- the file tabs.html is in _includes

This will produce tabs, however not if gh-pages is used.

```
{% capture tab1 %}
  {{ "_documentation/databases/fields.md" | read_file }}
{% endcapture %}

{% capture tab2 %}
  {{ "_documentation/databases/fields.md" | read_file }}
{% endcapture %}

{% include tabs.html 
   tab1_title="Tab 1" tab1_content=tab1
   tab2_title="Tab 2" tab2_content=tab2
%}

```

### Run Periodically:

(put all these in a single script please)

```
./scripts/periodic.sh
```


---

- [ICONS](https://feathericons.com)

---

## Gist:

https://gist.github.com



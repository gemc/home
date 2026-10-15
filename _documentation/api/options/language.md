---
layout: default
title: 'GEMC option: language'
---

# `language`

Type: `option`

Description: language for GEMC logging messages, startup banner, and GUI text

Generated from:

```sh
gemc help language
```

```text
-language=<value> ..........: language for GEMC logging messages, startup banner, and GUI text


   Supported values:
   auto: detect your language automatically (default).
   en: English (original English messages).
   it: italiano (Italian).
   ja: 日本語 (Japanese).
   fr: français (French).
   zh: 中文 (Chinese).
   Automatic selection checks GEMC_LANGUAGE, LC_ALL, LC_MESSAGES, LANG, then system settings.
   Use -language=<code> or YAML language: <code> to override automatic selection.
   Regional tags such as it_IT.UTF-8 are accepted; missing regional entries use the base language.
   Missing languages or messages fall back to English. C and POSIX locales select English.
   Numeric formatting is unchanged.
```

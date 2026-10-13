---
layout: default
title: C++ Logging
category: api
permalink: /documentation/api/logging/
---

# C++ Logging

`GLogger` provides consistent messages for GEMC components and plugins, with subsystem headers,
verbosity/debug filtering, colors, and fatal exit codes. Components using `GBase` access it through
their %%log%% member. See the [Doxygen API](https://gemc.github.io/src/glogging/) for class details.

## Complete Message Templates

**Upcoming with the next release.**

Use a complete sentence with numbered placeholders and pass the values separately:

```cpp
log->info(
    0, "Using %1 threads out of %2 available cores.", useThreads, ncores);
```

The output for four threads and eight cores is:

```text
Using 4 threads out of 8 available cores.
```

The logger adds its usual subsystem, counter, and info-level header. The normal method names accept
complete templates. The transitional `*Template()` names remain forwarding aliases with the same behavior.

### Logging Categories

| Method | Behavior |
| --- | --- |
| `info(level, message, args...)` | Uses info verbosity levels 0, 1, or 2. |
| `info(message, args...)` | Defaults to info level 0. |
| `debug(type, message, args...)` | Emits only when debug is enabled. |
| `warning(message, args...)` | Always emits a warning. |
| `critical(message, args...)` | Always emits an emphasized message. |
| `error(exitCode, message, args...)` | Emits the error and exit-code line, then terminates. |

For example, inside a component with an initialized %%log%% member:

```cpp
log->info("Starting run %1.", runNumber);
log->warning("File %1 was not found; using %2.", filename, fallback);
log->debug(NORMAL, "Loaded %1 entries from %2.", count, filename);
log->critical("Starting detector %1.", detectorName);
log->error(EXIT_FAILURE, "Cannot read file %1.", filename);
```

Debug accepts %%NORMAL%%, %%CONSTRUCTOR%%, and %%DESTRUCTOR%%, preserving the existing lifecycle markers.
The last example terminates the process with %%EXIT_FAILURE%% after writing to Geant4's error stream.

### Placeholders and Values

Placeholders `%1` through `%99` refer to the one-based argument positions. They may be reordered
or repeated, and each supplied argument must appear at least once:

```cpp
log->info("%2 then %1 then %2", "first", "second");
// Message: second then first then second

log->info("%1%% complete", 50);
// Message: 50% complete
```

Two percent signs emit one literal percent sign. Other percent signs remain literal. To print text
that looks like a placeholder, escape its percent sign: `"%%1"` produces `"%1"`.

Values may be strings, numbers, or custom types with a stream insertion operator. Each value is converted
once using its own `std::ostringstream`, even when its placeholder is repeated. Inserted values are never
interpreted as templates, so percent signs in filenames or other values are preserved. Stream manipulators
do not carry over between parameters; prepare a formatted string when a value needs special formatting.

### Filtering and Invalid Templates

Info level 0 always emits. Level 1 requires verbosity greater than 0, and level 2 requires verbosity
greater than 1. Debug messages require a nonzero debug setting. Configure these settings through
[GEMC options](/home/documentation/api/options/) and
[plugin verbosity domains](/home/documentation/sensitivity/gplugins/#verbosity).

Suppressed info/debug messages neither convert parameter values nor validate placeholders. C++ still
evaluates argument expressions before calling the logger, so avoid expensive expressions in hot loops.

An emitted template throws `std::invalid_argument` before writing any output if a placeholder is invalid
or missing a corresponding value, or if a supplied value is unused. For example:

```cpp
log->info("File %2", filename);       // Missing the second argument.
log->info("File %0", filename);       // Positions start at 1.
log->info("File %1", filename, size); // The second argument is unused.
```

Placeholders with leading zeroes or positions above 99 are invalid. At most 99 arguments are supported.
An invalid info level retains the existing fatal verbosity error and exit code. Valid error templates
retain the caller's requested exit code; a formatting exception prevents the error from being emitted.

### Migrating Existing Calls

Replace concatenated fragments with a complete template and numbered parameters:

```cpp
// Before: log->info(0, "Using ", useThreads, " threads.");
log->info(0, "Using %1 threads.", useThreads);
```

Pass dynamic or already-formatted diagnostics as values so their percent signs remain literal:

```cpp
log->warning("%1", diagnosticText);
```

External plugins must migrate concatenating calls and rebuild against matching GEMC headers. Calls using
the transitional `*Template()` methods continue to work; new code should use the normal method names.

### Generated English Catalogs

**Upcoming with the next release.**

English templates are collected in `translations/en.yaml` in the GEMC and CLAS12 repositories.
Identical templates share an entry, with source references recorded as comments. The English template is
the lookup key and, in the English catalog, also the value:

```yaml
schema: 1
language: en
messages:
  "Using %1 threads.": "Using %1 threads."
```

Edit the English sentence in C++, then regenerate its catalog. From the GEMC source repository:

```shell
build/subprojects/pygemc/python_env/bin/python ci/extract_messages.py extract
build/subprojects/pygemc/python_env/bin/python ci/extract_messages.py extract --check
```

Use `--root ../clas12-systems` for the separate plugin catalog. The source manifest is
`translations/catalog.yaml`; build copies, tests, and documentation examples are excluded. Messages
containing only dynamic data, such as `log->warning("%1", diagnosticText)`, do not need translations.

The extractor also validates translated YAML catalogs, rejecting duplicate or unknown keys, empty
translations, and changed placeholder positions. See the
[catalog guide](https://github.com/gemc/src/blob/main/translations/README.md) for the format and commands.

### Runtime Language Selection

**Upcoming with the next release.**

The default %%language%% setting is `auto`, so users do not need to select their own language. An explicit
command-line or YAML setting overrides automatic detection:

```shell
gemc run.yaml -language=it
gemc run.yaml -language=en
```

Automatic selection checks %%GEMC_LANGUAGE%% first, then the first nonempty locale variable among
%%LC_ALL%%, %%LC_MESSAGES%%, and %%LANG%%. When those are unset, macOS uses its preferred language,
Windows uses its user locale, and other systems fall back to English. `C`, `C.UTF-8`, and `POSIX` select
English. Locale tags such as `it_IT.UTF-8` normalize to `it-it`, with `it.yaml` used for messages absent
from the regional `it-it.yaml` catalog. Missing languages or messages fall back to English.

`GLogger` looks up the translated template before inserting parameters. Numeric formatting, dynamic values,
verbosity filtering, headers, colors, counters, and fatal exit codes retain their behavior. The language is
resolved when the logger is constructed; `get_language()` reports the normalized requested tag.

### Catalog Installation and Discovery

Meson installs framework catalogs under `<prefix>/share/gemc/translations/gemc` and CLAS12 catalogs under
`<prefix>/share/gemc/translations/clas12`. The installation follows the configured %%datadir%%; `share`
is the default. Recognized build trees use their owning source catalog directories.

Existing plugin search paths also expose catalogs in neighboring installation prefixes. For additional
locations, %%GEMC_TRANSLATION_PATH%% accepts colon-separated directories holding language YAML files
directly or inside named domain directories. Regional entries precede base-language entries; within each
variant, the first matching message in search-path order wins.

Matching configurations share an immutable cache, so message lookup performs no filesystem access. Invalid
catalogs are ignored with a diagnostic and retain English fallback. Restart GEMC after changing catalogs.
Plugins must rebuild against matching headers and the new `glogging` library.

### Translation Status

Runtime lookup, automatic language detection, and English fallback are available. Production catalogs
currently contain English; scheduled agent translations will provide Italian, Japanese, French, and Chinese.
Command-line help, Qt labels, and Geant4's own output have separate translation paths.

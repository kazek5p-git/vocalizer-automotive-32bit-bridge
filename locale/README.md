# Translation Workflow

The file `vocalizer_automotive_driver.pot` is the neutral translation
template for the add-on interface. It contains the current English source
messages and no translations.

To add a language:

1. Create `locale/<language>/manifest.ini`.
2. Copy the POT file to `locale/<language>/LC_MESSAGES/nvda.po`.
3. Fill in the PO header and translate every `msgstr`.
4. Compile the PO file to
   `locale/<language>/LC_MESSAGES/nvda.mo`.
5. Add a localized `doc/<language>/readme.html` file.

With GNU gettext, the compilation command is:

```text
msgfmt -o locale/pl/LC_MESSAGES/nvda.mo locale/pl/LC_MESSAGES/nvda.po
```

Replace `pl` with the target locale. Poedit can also compile the `.po` file
when saving it.

The language directory must use the locale identifier expected by NVDA, for
example `pl` for Polish or `sk` for Slovak.

Keep placeholders such as `{error}`, `{driverVersion}` and `{licenseInfo}`
unchanged in translated messages. Keep the `&` marker in menu labels when
the translated label should have a keyboard accelerator.

The additional legacy Vocalizer locales were synchronized against the current
bridge POT file. Messages that did not exist in the original translation use
the English source text as NVDA's fallback.

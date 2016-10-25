# gettext-extractor
Extract translation strings or keys from text-based files

## About
We use the extraxtor in wordpress projects where we work with [.twig](http://twig.sensiolabs.org/) template files (via [timber](https://github.com/timber/timber)). We had the following problem with the [timber extractor](https://github.com/timber/timber/wiki/Text-Cookbook#generating-po-files-using-poedit): http://stackoverflow.com/questions/33910482/xgettext-does-not-extract-string-in-html-attribute, so we created our own implementation based on Python.

## How-to
You need to install [Python 2.7](https://www.python.org/downloads/) to run the script.

Confgure a new extractor for [PoEdit](https://poedit.net/) in the following way (example is for twig, but could be anything):

- Create a new extractor under `Preferences / Extractors`
- Set language to `Twig`, file-extenstion to `*.twig`
- Set command to extract to `python /[absolute-path-to-this-project]/src/translation_extractor.py -o %o -%K --files %F`
- Set item in keyword list to `-k%k`
- Set item in input file list to `%f`
- Set source code charset to `--from-code=%c`

## Todo
- At the moment the following gettext keywords are hardcoded in the script: `__`,` _x`, `trans`, `transX`. Needs to be refactored to get the keyword defintions from the translation file configuration in Poedit.
- Convert to Python 3 (?)

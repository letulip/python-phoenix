# Заметки владельца по плейтестам

Сюда складываем замечания после сессий (дата, упражнение, что не так), а рядом – еженедельные выгрузки
`python-phoenix-progress-YYYY-MM-DD.json` из экрана «Прогресс».

## Волна 1

- (пусто – ждём первых трёх сессий)

## 2026-11-05 · round 1

1. Hidden test shows identical-looking `expected` and `got` (`'tea x 2 3.00'` both) – the one-space difference was invisible because inline `code` collapsed whitespace. Fixed in feat/wave-1: whitespace preserved, the differing characters are highlighted, spaces inside the highlight are drawn as dots, multi-line output is compared line by line and lists element by element; the note under the block gives lengths, index and type.


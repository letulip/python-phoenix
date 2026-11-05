# Заметки владельца по плейтестам

Сюда складываем замечания после сессий (дата, упражнение, что не так), а рядом – еженедельные выгрузки
`python-phoenix-progress-YYYY-MM-DD.json` из экрана «Прогресс».

## Волна 1

- (пусто – ждём первых трёх сессий)

## 2026-11-05 · round 1

1. Hidden test shows identical-looking `expected` and `got` (`'tea x 2 3.00'` both) – the one-space difference was invisible because inline `code` collapsed whitespace. Fixed in feat/wave-1: whitespace preserved, the differing characters are highlighted, spaces inside the highlight are drawn as dots, multi-line output is compared line by line and lists element by element; the note under the block gives lengths, index and type.

2. No way to look at the module card from inside an exercise: the card is a one-time session step, and the «card» link on the map would leave the task (which records the attempt as `left`). Fixed in feat/wave-1: a «Карточка» button in the task header opens the current module's card in an overlay over the exercise (✕, Esc or a click outside closes it); the editor, timer and results stay as they were. Hidden in the placement test, like hints. Every opening is logged (event `cardPeek`, counter `cardPeeks` on the attempt).

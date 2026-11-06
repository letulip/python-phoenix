# Заметки владельца по плейтестам

Сюда складываем замечания после сессий (дата, упражнение, что не так), а рядом – еженедельные выгрузки
`python-phoenix-progress-YYYY-MM-DD.json` из экрана «Прогресс».

## Волна 1

- (пусто – ждём первых трёх сессий)

## 2026-11-05 · round 1

1. Hidden test shows identical-looking `expected` and `got` (`'tea x 2 3.00'` both) – the one-space difference was invisible because inline `code` collapsed whitespace. Fixed in feat/wave-1: whitespace preserved, the differing characters are highlighted, spaces inside the highlight are drawn as dots, multi-line output is compared line by line and lists element by element; the note under the block gives lengths, index and type.

2. No way to look at the module card from inside an exercise: the card is a one-time session step, and the «card» link on the map would leave the task (which records the attempt as `left`). Fixed in feat/wave-1: a «Карточка» button in the task header opens the current module's card in an overlay over the exercise (✕, Esc or a click outside closes it); the editor, timer and results stay as they were. Hidden in the placement test, like hints. Every opening is logged (event `cardPeek`, counter `cardPeeks` on the attempt).
3. The owner was told at an interview that he codes at middle level and asked, per task, how a middle and how a senior would solve it, with reasoning, plus 3–4 tasks per module. Done in feat/wave-1: every task and refactor (30 now) carries LEVELS, a middle and a senior solution with a note in both languages, both gated against the hidden tests and the examples; the outcome block shows them after the explanation (the plain solution is hidden when it equals one of the levels). Every module now has 4 tasks + 1 refactor: 15 new exercises, L0 is 259 minutes. Drills carry no levels. The old solution_alt of four exercises was folded into the levels.

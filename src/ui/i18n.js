/** UI strings. Task statements stay English; explanations and chrome follow the language setting. */

export const STRINGS = {
  ru: {
    "nav.today": "Сегодня", "nav.map": "Карта", "nav.progress": "Прогресс", "nav.settings": "Настройки",
    "runtime.idle": "Python не запущен", "runtime.booting": "Python загружается…", "runtime.ready": "Python {python} готов",
    "runtime.busy": "Python выполняет…", "runtime.restarting": "Python перезапускается…", "runtime.error": "Python не загрузился: {message}",

    "home.tagline": "Руки вспоминают быстрее, чем кажется.",
    "home.placement.title": "Сначала диагностика?",
    "home.placement.text": "{n} коротких задач без подсказок, около 15 минут. По итогам стенд отметит модули, которые ты уже помнишь, и начнёт с нужного места.",
    "home.placement.start": "Пройти диагностику", "home.placement.skip": "Начать с нуля",
    "home.session.title": "Сессия дня",
    "home.session.new": "Сегодня: {module}. Карточка и упражнения примерно на {minutes} минут.",
    "home.session.progress": "Сделано {done} из {total} шагов.",
    "home.session.done": "Сессия на сегодня закрыта. Хочешь ещё – на карте всё открыто.",
    "home.session.start": "Начать сессию", "home.session.continue": "Продолжить", "home.session.open": "Открыть итоги",
    "home.allDone": "Все модули этой волны пройдены. Повторяй на карте, следующая волна уже в пути.",
    "home.streak": "Серия", "home.days": "дн.", "home.passed": "решено", "home.of": "из",
    "home.module.start": "Стартовый модуль: {module}", "home.map": "Открыть карту", "home.progress": "Открыть прогресс",

    "session.title": "Сессия дня", "session.date": "{date}", "session.begin": "Начать", "session.continue": "Продолжить",
    "session.role.warmup": "Разминка", "session.role.lesson": "Урок", "session.role.review": "Повтор", "session.role.card": "Карточка",
    "session.step.card": "Карточка модуля: {module}",
    "session.done.title": "Сессия закрыта",
    "session.done.text": "{items} шагов, {minutes} мин активной работы, решено {passed}.",
    "session.done.hints": "подсказок: {n}", "session.done.errors": "ошибок: {n}", "session.done.noErrors": "без ошибок выполнения",
    "session.home": "На главную", "session.empty": "Сегодня шагов нет: всё пройдено.",
    "session.status.done": "готово", "session.status.pending": "ждёт", "session.status.skipped": "пропущено",

    "card.title": "Карточка модуля", "card.gotchas": "Ловушки", "card.phrase": "Фраза для интервью",
    "card.done": "Прочитал, дальше", "card.close": "Закрыть",

    "task.statement": "Условие", "task.examples": "Примеры", "task.hints": "Подсказки", "task.talk": "Проговори", "task.model": "Образец",
    "task.run": "Запустить", "task.tests": "Скрытые тесты", "task.reset": "Сброс", "task.giveup": "Сдаюсь", "task.skip": "Пропустить",
    "task.next": "Далее", "task.toSession": "К сессии", "task.toMap": "К карте", "task.toDiagnostic": "Дальше по диагностике",
    "task.hint.show": "Показать подсказку {n} из {total}", "task.hint.none": "Подсказок больше нет.",
    "task.solution.show": "Показать решение", "task.solution": "Решение", "task.solutionAlt": "Ещё вариант",
    "task.explanation": "Разбор", "task.followups": "Вопросы интервьюера", "task.complexity": "Сложность",
    "task.output": "Вывод", "task.noOutput": "(ничего не напечатано)", "task.outputTruncated": "(вывод обрезан)",
    "task.examplesResult": "Примеры", "task.testsResult": "Тесты: {passed} из {total}",
    "task.errorAt": "{type} в строке {line}: {message}", "task.errorNoLine": "{type}: {message}",
    "task.timeout": "Код не ответил за {ms} мс – похоже на бесконечный цикл. Python перезапущен.",
    "task.pasteBlocked": "Здесь только руками: вставка отключена.", "task.pasteLogged": "Вставка записана в журнал попытки.",
    "task.passed": "Пройдено", "task.gaveUp": "Решение показано", "task.failed": "Не пройдено",
    "task.resetConfirm": "Вернуть стартовый код? Твои правки пропадут.",
    "task.giveupConfirm": "Показать решение и закрыть упражнение как несданное?",
    "task.notFound": "Такого упражнения нет.", "task.minutes": "{n} мин", "task.difficulty": "сложность {n} из 5",
    "task.type.retype": "Перепечатай", "task.type.cloze": "Дополни", "task.type.task": "Задача", "task.type.refactor": "Рефакторинг",
    "task.help.retype": "Перепечатай образец руками (вкладка «Образец»), затем запусти скрытые тесты. Любой рабочий вариант проходит.",
    "task.help.cloze": "Заполни пропуски ___ так, чтобы прошли тесты.",
    "task.help.task": "Напиши функцию по условию. «Запустить» проверяет примеры, «Скрытые тесты» решают.",
    "task.help.refactor": "Код работает, но некрасив. Перепиши, не меняя поведение: тесты проверяют и результат, и структуру.",
    "task.diff": "Разница с образцом", "task.diff.missing": "нет в твоём коде", "task.diff.extra": "лишняя строка",
    "task.runtimeNotReady": "Python ещё загружается, секунду.",
    "task.timer": "время", "task.runs": "запусков",
    "task.wasExpected": "ожидалось", "task.got": "получено",

    "map.title": "Карта", "map.card": "карточка", "map.status.done": "пройден", "map.status.known": "знаю",
    "map.status.active": "в работе", "map.status.new": "впереди", "map.exercise.passed": "пройдено", "map.exercise.tried": "пробовал",

    "progress.title": "Прогресс", "progress.export": "Скачать JSON", "progress.copy": "Скопировать JSON", "progress.import": "Импорт JSON",
    "progress.wipe": "Стереть всё", "progress.wipeConfirm": "Стереть все попытки и настройки на этом устройстве? Сначала скачай JSON.",
    "progress.copied": "JSON в буфере обмена.", "progress.imported": "Импортировано: {attempts} попыток.",
    "progress.importError": "Файл не похож на экспорт Python Phoenix: {message}",
    "progress.noData": "Попыток пока нет. Начни сессию дня.",
    "progress.summary": "{passed} из {total} упражнений, {attempts} попыток, {noHint}% решено без подсказок",
    "progress.modules": "Модули", "progress.concepts": "Концепты", "progress.errors": "Ошибки выполнения",
    "progress.sessions": "Сессии", "progress.types": "По типам",
    "progress.col.concept": "концепт", "progress.col.attempts": "попыток", "progress.col.pass": "пройдено", "progress.col.hints": "подсказок",
    "progress.col.median": "медиана", "progress.col.type": "тип", "progress.col.date": "дата", "progress.col.minutes": "мин", "progress.col.items": "шагов",
    "progress.noErrors": "Ни одной ошибки выполнения. Подозрительно хорошо.",

    "settings.title": "Настройки", "settings.lang": "Язык пояснений и интерфейса", "settings.sessionMinutes": "Длина сессии",
    "settings.paste": "Разрешать вставку в задачах урока (в дриллах и диагностике она всегда закрыта)",
    "settings.coderpad": "Режим CoderPad: без подсветки синтаксиса", "settings.closeBrackets": "Автозакрытие скобок и кавычек",
    "settings.theme": "Тема", "settings.theme.auto": "как в системе", "settings.theme.light": "светлая", "settings.theme.dark": "тёмная",
    "settings.saved": "Сохранено.", "settings.version": "Версия {version}",

    "diag.title": "Диагностика", "diag.intro": "{n} упражнений по одному из каждого модуля, без подсказок и без решений. Около 15 минут. Не получается – жми «Пропустить», это тоже ответ.",
    "diag.start": "Начать", "diag.progress": "Упражнение {i} из {n}",
    "diag.result.title": "Диагностика пройдена", "diag.result.known": "Уже помнишь: {modules}", "diag.result.none": "Начинаем с самого начала, и это нормально.",
    "diag.result.start": "Стартовый модуль: {module}", "diag.home": "На главную", "diag.restart": "Пройти ещё раз",

    "fun.pass": ["Феникс взлетел. 🔥", "Пиксель одобряет. Вкусняшка разблокирована.", "Чисто. Отправляем.", "Капитан Байт кивнул. На этом корабле это высшая похвала.", "Всё зелёное. Разомни лапы.", "Это в зал славы.", "Собирается, проходит, сверкает.", "Мышечная память +1."],
    "fun.fail": ["Ещё не то. Первый красный тест знает что-то, чего не знаешь ты.", "Пиксель смахнул кружку со стола. Прочитай подпись упавшего теста.", "Близко. Капитан Байт хочет видеть «ожидалось» и «получено» рядом.", "Тесты ворчат, но не врут. Проверь граничный случай.", "Ещё заход. Напечатай промежуточное значение и посмотри."],
    "fun.gaveUp": ["Посмотреть решение – тоже ход. Завтра эта задача вернётся вариантом.", "Разбор ниже. Прочитай вслух, как объяснил бы интервьюеру."],

    "common.yes": "Да", "common.no": "Нет", "common.min": "мин", "common.sec": "с", "common.back": "Назад",
    "common.loading": "Загрузка…", "common.today": "сегодня",
  },
  en: {
    "nav.today": "Today", "nav.map": "Map", "nav.progress": "Progress", "nav.settings": "Settings",
    "runtime.idle": "Python not started", "runtime.booting": "Loading Python…", "runtime.ready": "Python {python} ready",
    "runtime.busy": "Python running…", "runtime.restarting": "Restarting Python…", "runtime.error": "Python failed to load: {message}",

    "home.tagline": "Hands remember faster than you think.",
    "home.placement.title": "Placement test first?",
    "home.placement.text": "{n} short exercises without hints, about 15 minutes. The result marks the modules you still remember and starts you at the right place.",
    "home.placement.start": "Take the placement test", "home.placement.skip": "Start from scratch",
    "home.session.title": "Today's session",
    "home.session.new": "Today: {module}. Card and exercises for about {minutes} minutes.",
    "home.session.progress": "{done} of {total} steps done.",
    "home.session.done": "Today's session is closed. Want more? Everything is open on the map.",
    "home.session.start": "Start the session", "home.session.continue": "Continue", "home.session.open": "Open the summary",
    "home.allDone": "Every module of this wave is done. Review on the map; the next wave is coming.",
    "home.streak": "Streak", "home.days": "days", "home.passed": "solved", "home.of": "of",
    "home.module.start": "Starting module: {module}", "home.map": "Open the map", "home.progress": "Open progress",

    "session.title": "Today's session", "session.date": "{date}", "session.begin": "Begin", "session.continue": "Continue",
    "session.role.warmup": "Warm-up", "session.role.lesson": "Lesson", "session.role.review": "Review", "session.role.card": "Card",
    "session.step.card": "Module card: {module}",
    "session.done.title": "Session closed",
    "session.done.text": "{items} steps, {minutes} min of active work, {passed} solved.",
    "session.done.hints": "hints: {n}", "session.done.errors": "runtime errors: {n}", "session.done.noErrors": "no runtime errors",
    "session.home": "Home", "session.empty": "No steps today: everything is done.",
    "session.status.done": "done", "session.status.pending": "pending", "session.status.skipped": "skipped",

    "card.title": "Module card", "card.gotchas": "Gotchas", "card.phrase": "Interview phrase",
    "card.done": "Read it, next", "card.close": "Close",

    "task.statement": "Statement", "task.examples": "Examples", "task.hints": "Hints", "task.talk": "Talk track", "task.model": "Model",
    "task.run": "Run", "task.tests": "Hidden tests", "task.reset": "Reset", "task.giveup": "Give up", "task.skip": "Skip",
    "task.next": "Next", "task.toSession": "Back to session", "task.toMap": "Back to map", "task.toDiagnostic": "Continue placement",
    "task.hint.show": "Show hint {n} of {total}", "task.hint.none": "No more hints.",
    "task.solution.show": "Show the solution", "task.solution": "Solution", "task.solutionAlt": "Another way",
    "task.explanation": "Explanation", "task.followups": "Interviewer follow-ups", "task.complexity": "Complexity",
    "task.output": "Output", "task.noOutput": "(nothing printed)", "task.outputTruncated": "(output truncated)",
    "task.examplesResult": "Examples", "task.testsResult": "Tests: {passed} of {total}",
    "task.errorAt": "{type} at line {line}: {message}", "task.errorNoLine": "{type}: {message}",
    "task.timeout": "No answer within {ms} ms – looks like an infinite loop. Python was restarted.",
    "task.pasteBlocked": "Hands only here: pasting is off.", "task.pasteLogged": "Paste recorded in the attempt log.",
    "task.passed": "Passed", "task.gaveUp": "Solution shown", "task.failed": "Not passed",
    "task.resetConfirm": "Restore the starter code? Your edits will be lost.",
    "task.giveupConfirm": "Show the solution and close this exercise as not solved?",
    "task.notFound": "No such exercise.", "task.minutes": "{n} min", "task.difficulty": "difficulty {n} of 5",
    "task.type.retype": "Retype", "task.type.cloze": "Fill in", "task.type.task": "Task", "task.type.refactor": "Refactor",
    "task.help.retype": "Retype the model by hand (see the Model tab), then run the hidden tests. Any working variant passes.",
    "task.help.cloze": "Fill in the ___ blanks so the tests pass.",
    "task.help.task": "Write the function. Run checks the examples; Hidden tests decide.",
    "task.help.refactor": "The code works but is ugly. Rewrite it without changing behaviour: tests check the result and the structure.",
    "task.diff": "Difference from the model", "task.diff.missing": "missing in your code", "task.diff.extra": "extra line",
    "task.runtimeNotReady": "Python is still loading, one second.",
    "task.timer": "time", "task.runs": "runs",
    "task.wasExpected": "expected", "task.got": "got",

    "map.title": "Map", "map.card": "card", "map.status.done": "done", "map.status.known": "known",
    "map.status.active": "in progress", "map.status.new": "ahead", "map.exercise.passed": "passed", "map.exercise.tried": "tried",

    "progress.title": "Progress", "progress.export": "Download JSON", "progress.copy": "Copy JSON", "progress.import": "Import JSON",
    "progress.wipe": "Wipe everything", "progress.wipeConfirm": "Erase all attempts and settings on this device? Download the JSON first.",
    "progress.copied": "JSON copied to the clipboard.", "progress.imported": "Imported: {attempts} attempts.",
    "progress.importError": "This file does not look like a Python Phoenix export: {message}",
    "progress.noData": "No attempts yet. Start today's session.",
    "progress.summary": "{passed} of {total} exercises, {attempts} attempts, {noHint}% solved without hints",
    "progress.modules": "Modules", "progress.concepts": "Concepts", "progress.errors": "Runtime errors",
    "progress.sessions": "Sessions", "progress.types": "By type",
    "progress.col.concept": "concept", "progress.col.attempts": "attempts", "progress.col.pass": "passed", "progress.col.hints": "hints",
    "progress.col.median": "median", "progress.col.type": "type", "progress.col.date": "date", "progress.col.minutes": "min", "progress.col.items": "steps",
    "progress.noErrors": "Not a single runtime error. Suspiciously good.",

    "settings.title": "Settings", "settings.lang": "Language of explanations and UI", "settings.sessionMinutes": "Session length",
    "settings.paste": "Allow pasting in lesson tasks (drills and placement always block it)",
    "settings.coderpad": "CoderPad mode: no syntax highlighting", "settings.closeBrackets": "Auto-close brackets and quotes",
    "settings.theme": "Theme", "settings.theme.auto": "system", "settings.theme.light": "light", "settings.theme.dark": "dark",
    "settings.saved": "Saved.", "settings.version": "Version {version}",

    "diag.title": "Placement test", "diag.intro": "{n} exercises, one per module, no hints and no solutions. About 15 minutes. Stuck? Press Skip, that is an answer too.",
    "diag.start": "Start", "diag.progress": "Exercise {i} of {n}",
    "diag.result.title": "Placement done", "diag.result.known": "Still remembered: {modules}", "diag.result.none": "Starting from the very beginning, and that is fine.",
    "diag.result.start": "Starting module: {module}", "diag.home": "Home", "diag.restart": "Take it again",

    "fun.pass": ["Phoenix rises. 🔥", "Pixel approves. Treats unlocked.", "Clean. Ship it.", "Captain Byte nods. On this ship that is the highest praise.", "Green across the board. Stretch your paws.", "Straight into the hall of fame.", "Compiles, passes, sparkles.", "Muscle memory +1."],
    "fun.fail": ["Not yet. The first red test knows something you don't.", "Pixel knocked a mug off the desk. Read the failing label.", "Close. Captain Byte wants to see expected and actual side by side.", "The tests are grumpy, not wrong. Check the edge case.", "One more pass. Print an intermediate value and look."],
    "fun.gaveUp": ["Looking at the solution is a move too. This one comes back tomorrow as a variant.", "The explanation is below. Read it aloud, as you would to an interviewer."],

    "common.yes": "Yes", "common.no": "No", "common.min": "min", "common.sec": "s", "common.back": "Back",
    "common.loading": "Loading…", "common.today": "today",
  },
};

export function makeT(getLang) {
  return (key, vars = {}) => {
    const lang = getLang();
    let value = STRINGS[lang]?.[key] ?? STRINGS.en[key] ?? key;
    if (Array.isArray(value)) return value;
    for (const [k, v] of Object.entries(vars)) value = value.split(`{${k}}`).join(String(v));
    return value;
  };
}

export function makePick(getLang) {
  return (obj, field) => {
    if (!obj) return "";
    const lang = getLang();
    return obj[`${field}_${lang}`] ?? obj[`${field}_en`] ?? obj[field] ?? "";
  };
}

export function randomFrom(list, random = Math.random) {
  if (!Array.isArray(list) || list.length === 0) return "";
  return list[Math.floor(random() * list.length)];
}

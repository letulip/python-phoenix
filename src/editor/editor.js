/** CodeMirror 6 wrapper: Python, 4-space indent, no autocomplete, optional paste blocking, run shortcuts. */
import * as CM from "../../vendor/codemirror.js";

const baseTheme = CM.EditorView.theme({
  "&": { fontSize: "14px", height: "100%" },
  ".cm-scroller": { fontFamily: "ui-monospace, 'SF Mono', Menlo, Consolas, monospace", lineHeight: "1.55" },
  ".cm-content": { padding: "10px 0" },
  "&.cm-focused": { outline: "none" },
  ".cm-gutters": { border: "none" },
});

export function createEditor({
  parent, doc = "", dark = false, coderpad = false, closeBrackets = true, readOnly = false,
  onRun = () => {}, onTests = () => {}, onChange = () => {},
  pasteAllowed = () => true, onPaste = () => {}, onPasteBlocked = () => {},
}) {
  const themeComp = new CM.Compartment();
  const langComp = new CM.Compartment();
  const bracketsComp = new CM.Compartment();
  const readOnlyComp = new CM.Compartment();

  const themeExt = (isDark) => (isDark ? CM.oneDark : CM.syntaxHighlighting(CM.defaultHighlightStyle, { fallback: true }));
  const langExt = (plain) => (plain ? [] : CM.python());
  const bracketsExt = (on) => (on ? CM.closeBrackets() : []);

  const shortcuts = CM.Prec.highest(CM.keymap.of([
    { key: "Mod-Enter", run: () => { onRun(); return true; } },
    { key: "Shift-Mod-Enter", run: () => { onTests(); return true; } },
    CM.indentWithTab,
  ]));

  const pasteGuard = CM.EditorView.domEventHandlers({
    paste(event) {
      if (!pasteAllowed()) { event.preventDefault(); onPasteBlocked(); return true; }
      onPaste();
      return false;
    },
    drop(event) {
      if (!pasteAllowed()) { event.preventDefault(); onPasteBlocked(); return true; }
      onPaste();
      return false;
    },
  });

  const state = CM.EditorState.create({
    doc,
    extensions: [
      CM.lineNumbers(), CM.highlightActiveLineGutter(), CM.highlightSpecialChars(),
      CM.history(), CM.drawSelection(), CM.dropCursor(), CM.indentOnInput(), CM.bracketMatching(),
      CM.highlightActiveLine(),
      shortcuts,
      CM.keymap.of([...CM.closeBracketsKeymap, ...CM.defaultKeymap, ...CM.historyKeymap]),
      CM.indentUnit.of("    "), CM.EditorState.tabSize.of(4),
      langComp.of(langExt(coderpad)),
      bracketsComp.of(bracketsExt(closeBrackets)),
      themeComp.of(themeExt(dark)),
      readOnlyComp.of(CM.EditorState.readOnly.of(readOnly)),
      baseTheme, pasteGuard,
      CM.EditorView.updateListener.of((update) => { if (update.docChanged) onChange(update.state.doc.toString()); }),
    ],
  });
  const view = new CM.EditorView({ state, parent });

  return {
    view,
    getDoc: () => view.state.doc.toString(),
    setDoc(text) { view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } }); },
    focus: () => view.focus(),
    setDark(isDark) { view.dispatch({ effects: themeComp.reconfigure(themeExt(isDark)) }); },
    setCoderpad(plain) { view.dispatch({ effects: langComp.reconfigure(langExt(plain)) }); },
    setCloseBrackets(on) { view.dispatch({ effects: bracketsComp.reconfigure(bracketsExt(on)) }); },
    setReadOnly(flag) { view.dispatch({ effects: readOnlyComp.reconfigure(CM.EditorState.readOnly.of(flag)) }); },
    destroy: () => view.destroy(),
  };
}

// Single CodeMirror 6 bundle for the app (built once by `npm run build:vendor`, committed to vendor/).
// Keeping every module in one file avoids duplicate @codemirror/state instances from CDN loads.
export { EditorState, Compartment, Prec, EditorSelection } from "@codemirror/state";
export {
  EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter,
  drawSelection, dropCursor, highlightSpecialChars, placeholder,
} from "@codemirror/view";
export {
  defaultKeymap, history, historyKeymap, indentWithTab, indentMore, indentLess, insertNewlineAndIndent,
} from "@codemirror/commands";
export {
  bracketMatching, indentOnInput, indentUnit, syntaxHighlighting, defaultHighlightStyle,
} from "@codemirror/language";
export { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
export { python } from "@codemirror/lang-python";
export { oneDark } from "@codemirror/theme-one-dark";

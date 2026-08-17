// Forge landing page — single configuration point for the deployment domain.
const FORGE_DOMAIN = "hermes-agents-forge.vercel.app";
const ACTIVATION_COMMAND = `hermes skills install https://${FORGE_DOMAIN}/SKILL.md`;

(function () {
  "use strict";

  // Keep every rendered copy of the command in sync with FORGE_DOMAIN.
  document.querySelectorAll("[data-command]").forEach(function (el) {
    el.textContent = ACTIVATION_COMMAND;
  });

  const button = document.getElementById("copy-button");
  const status = document.getElementById("copy-status");
  const commandEl = document.getElementById("install-command");
  if (!button || !commandEl) return;

  const defaultLabel = button.textContent;
  let resetTimer = null;

  function announce(message) {
    if (status) status.textContent = message;
  }

  function showCopied() {
    button.textContent = "Copied";
    button.classList.add("copied");
    announce("Command copied to clipboard.");
    if (resetTimer) clearTimeout(resetTimer);
    resetTimer = setTimeout(function () {
      button.textContent = defaultLabel;
      button.classList.remove("copied");
    }, 2000);
  }

  function selectCommandText() {
    const range = document.createRange();
    range.selectNodeContents(commandEl);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  }

  function legacyCopy(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "absolute";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    let ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (err) {
      ok = false;
    }
    document.body.removeChild(textarea);
    return ok;
  }

  async function copyCommand() {
    const text = ACTIVATION_COMMAND;

    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        showCopied();
        return;
      } catch (err) {
        // Fall through to legacy path (e.g. permission denied).
      }
    }

    if (legacyCopy(text)) {
      showCopied();
      return;
    }

    // Last resort: select the command so the user can press Ctrl/Cmd+C.
    selectCommandText();
    announce("Clipboard unavailable. The command is selected — press Ctrl+C or Cmd+C to copy.");
    button.textContent = "Select + Ctrl+C";
    if (resetTimer) clearTimeout(resetTimer);
    resetTimer = setTimeout(function () {
      button.textContent = defaultLabel;
    }, 4000);
  }

  button.addEventListener("click", copyCommand);
})();

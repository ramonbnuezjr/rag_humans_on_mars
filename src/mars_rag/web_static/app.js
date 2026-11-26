"use strict";
const $ = (selector) => document.querySelector(selector);
const state = { busy: false, ready: false, controller: null, generation: 0, history: [] };
const question = $("#question");
const status = $("#status");

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function announce(text, error = false) {
  status.textContent = text;
  status.classList.toggle("error", error);
}
function setBusy(value) {
  state.busy = value;
  $("#submit").disabled = value || !state.ready;
  $("#submit").textContent = value ? "Searching…" : "Search";
  $("#thread").setAttribute("aria-busy", String(value));
  document.querySelectorAll("[data-question]").forEach((button) => { button.disabled = value || !state.ready; });
}
async function request(url, options = {}) {
  let response;
  try { response = await fetch(url, { cache: "no-store", ...options }); }
  catch (error) { error.category = "network"; throw error; }
  let data;
  try { data = await response.json(); } catch {
    throw Object.assign(new Error("The local server returned an unreadable response."), { category: "unreadable_response" });
  }
  if (!response.ok) throw Object.assign(new Error(data.error || "The local server could not complete this search."),
    { category: "http_error", error_id: data.error_id, logged: data.logged });
  return data;
}
async function errorReference(error, operation) {
  let receipt = error;
  if (!error.error_id) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2000);
    try {
      const response = await fetch("/api/ui-errors", { method: "POST", cache: "no-store",
        headers: { "Content-Type": "application/json" }, signal: controller.signal,
        body: JSON.stringify({ operation, category: error.category || "javascript" }) });
      receipt = response.ok ? await response.json() : {};
    } catch { receipt = {}; }
    finally { clearTimeout(timeout); }
  }
  return receipt.logged && receipt.error_id ? `Saved to the local error log. Reference: ${receipt.error_id}.` :
    "The local error log could not be saved. Please copy this error here to report it.";
}
async function showUnexpectedError() {
  announce("An unexpected browser error occurred.", true);
  const reference = await errorReference({}, "browser");
  announce(`An unexpected browser error occurred. ${reference}`, true);
}
window.addEventListener("error", () => { void showUnexpectedError(); });
window.addEventListener("unhandledrejection", (event) => {
  if (event.reason?.name !== "AbortError") void showUnexpectedError();
});
function addHistory(text) {
  state.history = [text, ...state.history.filter((item) => item !== text)].slice(0, 8);
  $("#empty-history").hidden = true;
  $("#history").replaceChildren();
  for (const item of state.history) {
    const button = element("button", item);
    button.type = "button";
    button.title = item;
    button.addEventListener("click", () => { question.value = item; question.focus(); });
    $("#history").append(button);
  }
}
function resultCard(result) {
  const fragment = $("#result-template").content.cloneNode(true);
  fragment.querySelector(".source-tag").textContent = result.source_id;
  fragment.querySelector(".page-label").textContent = `PDF page ${result.pdf_page}`;
  fragment.querySelector(".source-title").textContent = result.title;
  fragment.querySelector(".edition").textContent = result.edition || "Edition not established";
  fragment.querySelector(".passage").textContent = result.passage;
  fragment.querySelector(".pdf-link").href = result.pdf_url;
  fragment.querySelector(".printed-label").textContent = result.printed_page ? `Printed page ${result.printed_page}` : "Printed page label not reviewed";
  const context = fragment.querySelector(".page-context");
  context.hidden = !result.page_context;
  context.querySelector("pre").textContent = result.page_context || "";
  const notes = fragment.querySelector(".notes-content");
  notes.append(element("p", result.mission_context || "Mission context has not been reviewed."));
  notes.append(element("p", `Evidence: ${(result.evidence_type || "not classified").replaceAll("_", " ")}. Source review: ${(result.metadata_status || "pending").replaceAll("_", " ")}.`));
  if (result.limitations.length) {
    const list = element("ul");
    result.limitations.forEach((text) => list.append(element("li", text)));
    notes.append(list);
  }
  notes.append(element("p", `File: ${result.filename}`));
  const provenance = element("details");
  provenance.append(element("summary", "Evidence identifiers"));
  for (const [key, value] of Object.entries(result.provenance)) {
    if (value !== null) provenance.append(element("p", `${key}: ${value}`, "provenance"));
  }
  notes.append(provenance);
  return fragment;
}
const ratingLabels = { fully: "Fully", partially: "Partially", not_at_all: "Not at all", unsure: "Unsure" };
async function refreshReviews() {
  const container = $("#review-summary");
  try {
    const data = await request("/api/feedback/summary");
    container.replaceChildren(element("p", `${data.total} reviewed ${data.total === 1 ? "search" : "searches"}`));
    for (const [rating, label] of Object.entries(ratingLabels)) container.append(element("p", `${label}: ${data.counts[rating]}`));
    for (const item of data.recent) {
      const entry = element("details");
      entry.append(element("summary", `${ratingLabels[item.rating]} · ${item.question}`));
      entry.append(element("p", new Date(item.recorded_at).toLocaleString()));
      if (item.note) entry.append(element("p", item.note));
      container.append(entry);
    }
  } catch {
    container.replaceChildren(element("p", "Saved reviews unavailable. Reload to retry.", "error-panel"));
  }
}
function reviewForm(data) {
  const form = element("form", undefined, "review-form");
  form.setAttribute("aria-label", "Review evidence coverage");
  form.append(element("h3", "Does this evidence answer your question?"));
  form.append(element("p", "How well did the evidence above answer your question?", "muted"));
  if (!data.review_receipt) {
    form.append(element("p", "Review storage is unavailable. Search again after local storage is restored.", "error-panel"));
    return form;
  }
  const label = element("label", "Evidence coverage");
  const select = element("select"); select.required = true;
  const placeholder = element("option", "Choose an assessment…"); placeholder.value = ""; select.append(placeholder);
  for (const [rating, text] of Object.entries(ratingLabels)) {
    const option = element("option", text); option.value = rating; select.append(option);
  }
  label.append(select); form.append(label);
  const noteDetails = element("details"); noteDetails.append(element("summary", "Add a note (optional)"));
  const noteLabel = element("label", "What is missing or useful?");
  const note = element("textarea"); note.rows = 2; note.maxLength = 2000; noteLabel.append(note); noteDetails.append(noteLabel); form.append(noteDetails);
  form.append(element("p", "Saves your question, assessment, note and source references locally, outside GitHub. No PDF text is copied.", "muted"));
  const save = element("button", "Save review"); save.type = "submit";
  const message = element("p"); message.setAttribute("role", "status"); message.setAttribute("aria-live", "polite");
  form.append(save, message);
  form.addEventListener("input", () => { message.textContent = "Changes not saved."; });
  form.addEventListener("submit", async (event) => {
    event.preventDefault(); if (save.disabled) return;
    save.disabled = true; select.disabled = true; note.disabled = true; message.textContent = "Saving review…";
    message.classList.remove("error-panel");
    try {
      const receipt = await request("/api/feedback", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ receipt: data.review_receipt, rating: select.value, note: note.value }) });
      if (!receipt.saved) throw new Error("The review was not saved.");
      message.textContent = `Saved locally: ${ratingLabels[select.value]}. You can change and save this review again.`;
      await refreshReviews();
    } catch (error) {
      message.classList.add("error-panel");
      message.textContent = `Review not saved. ${error.message} Your choices are still here; retry.`;
      const reference = await errorReference(error, "feedback");
      message.append(document.createTextNode(` ${reference}`));
    } finally { save.disabled = false; select.disabled = false; note.disabled = false; }
  });
  return form;
}
async function runSearch() {
  const text = question.value.trim();
  if (!text || state.busy || !state.ready) return;
  const generation = state.generation;
  state.controller = new AbortController();
  const source = $("#source").value;
  const ranking = $("#ranking").value;
  const sourceLabel = $("#source").selectedOptions[0].textContent;
  $("#welcome").hidden = true;
  const turn = element("section", undefined, "turn");
  turn.append(element("p", text, "user-question"));
  const response = element("div");
  response.append(element("p", "Searching your collection…", "response-label"));
  turn.append(response);
  $("#thread").append(turn);
  addHistory(text);
  question.value = "";
  setBusy(true);
  announce("Searching the selected local PDFs…");
  turn.scrollIntoView({ behavior: "smooth", block: "start" });
  try {
    const data = await request("/api/search", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: text, source_id: source, ranking }), signal: state.controller.signal });
    if (generation !== state.generation) return;
    response.replaceChildren(element("p", "FROM YOUR COLLECTION", "response-label"));
    response.append(element("h2", `${data.results.length} matching ${data.results.length === 1 ? "passage" : "passages"}`, "response-heading"));
    response.append(element("p", `${sourceLabel} · ${ranking === "context" ? "Experimental ranking" : ranking === "baseline" ? "Original short passages" : "Standard search"}`, "response-notice"));
    response.append(element("p", data.notice, data.results.length ? "response-notice" : "empty-result"));
    data.results.forEach((result) => response.append(resultCard(result)));
    response.append(reviewForm(data));
    announce(data.results.length ? "Search complete. Check the source assumptions and surrounding page before drawing conclusions." : "No keyword matches. Try different wording or another source.");
  } catch (error) {
    if (generation !== state.generation || error.name === "AbortError") return;
    const panel = element("p", `${error.message} Your question is back in the search box so you can retry.`, "error-panel");
    response.replaceChildren(panel);
    question.value = text;
    announce("Search failed. Check that the local server is running, then retry.", true);
    const reference = await errorReference(error, "search");
    if (generation === state.generation) panel.append(document.createTextNode(` ${reference}`));
  } finally {
    if (generation === state.generation) { setBusy(false); state.controller = null; question.focus({ preventScroll: true }); }
  }
}
$("#search-form").addEventListener("submit", (event) => { event.preventDefault(); runSearch(); });
question.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) { event.preventDefault(); runSearch(); }
});
document.querySelectorAll("[data-question]").forEach((button) => button.addEventListener("click", () => {
  question.value = button.dataset.question; runSearch();
}));
$("#new-search").addEventListener("click", () => {
  state.generation += 1;
  if (state.controller) state.controller.abort();
  state.controller = null;
  $("#thread").replaceChildren();
  $("#welcome").hidden = false;
  question.value = "";
  setBusy(false);
  announce(state.ready ? "Ready to search your local collection." : "Collection unavailable. Restart the server and reload this page.");
  question.focus();
  $("#conversation").scrollTo({ top: 0, behavior: "smooth" });
});
async function initialize() {
  setBusy(false);
  try {
    const data = await request("/api/collection");
    $("#collection-count").textContent = `${data.indexed} indexed documents`;
    $("#collection-detail").textContent = `${data.pages} pages · ${data.passages} passages · ${data.registered} PDFs registered`;
    for (const source of data.sources) {
      const option = element("option", source.title); option.value = source.source_id; $("#source").append(option);
      $("#document-list").append(element("li", source.title));
    }
    state.ready = true; question.disabled = false; setBusy(false);
    announce("Ready to search your local collection.");
  } catch (error) {
    $("#collection-count").textContent = "Collection unavailable";
    const reference = await errorReference(error, "collection");
    announce(`${error.message} Restart the server and reload to try again. ${reference}`, true);
  }
}
initialize();
refreshReviews();

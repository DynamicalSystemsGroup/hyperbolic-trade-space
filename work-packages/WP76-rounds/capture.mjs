// Capture the rendered Kitchenham-CSC page at two widths in both colour schemes (WP76 R-11).
//
//   node work-packages/WP76-rounds/capture.mjs BASE_URL OUT_DIR
//
// Drives Google Chrome headless over its debugging protocol (Node's built-in WebSocket and
// fetch; nothing installed): for each (width, scheme) it emulates the viewport and
// prefers-color-scheme, loads the page, records the console errors and whether the page scrolls
// sideways, and writes a full-page PNG. Chrome follows the system scheme by default, so the
// scheme is set explicitly for every capture.
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const [base, out] = process.argv.slice(2);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333;
const PAGES = [["kitchenham", "examples/kitchenham/"], ["examples", "examples/"]];
const WIDTHS = [1280, 375];
const SCHEMES = ["light", "dark"];
mkdirSync(out, { recursive: true });

const chrome = spawn(CHROME, [
  "--headless=new", "--disable-gpu", `--remote-debugging-port=${PORT}`,
  "--no-first-run", "--user-data-dir=/tmp/wp76-chrome-profile", "about:blank",
], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let version;
for (let i = 0; i < 50 && !version; i++) {
  try { version = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); } catch { await sleep(200); }
}
if (!version) { chrome.kill(); throw new Error("chrome did not answer"); }

const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const pending = new Map(); const events = [];
ws.onmessage = (m) => {
  const msg = JSON.parse(m.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  else if (msg.method) events.push(msg);
};
const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
  const n = ++id; pending.set(n, (msg) => (msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result)));
  ws.send(JSON.stringify({ id: n, method, params, sessionId }));
});

const rows = [];
for (const [name, path] of PAGES) for (const width of WIDTHS) for (const scheme of SCHEMES) {
  const { targetId } = await send("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await send("Target.attachToTarget", { targetId, flatten: true });
  const s = (m, p) => send(m, p, sessionId);
  await s("Page.enable"); await s("Runtime.enable"); await s("Log.enable");
  await s("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: scheme }] });
  await s("Emulation.setDeviceMetricsOverride", { width, height: 900, deviceScaleFactor: 1, mobile: width < 768 });
  events.length = 0;
  await s("Page.navigate", { url: base + path });
  await sleep(2500);
  const ev = async (expr) => (await s("Runtime.evaluate", { expression: expr, returnByValue: true })).result.value;
  const height = await ev("document.documentElement.scrollHeight");
  const sideways = await ev("document.documentElement.scrollWidth > document.documentElement.clientWidth");
  const matched = await ev(`window.matchMedia('(prefers-color-scheme: ${scheme})').matches`);
  const scheme_attr = await ev("document.body.getAttribute('data-md-color-scheme')");
  const figures = await ev("Array.from(document.images).filter(i => i.src.includes('kitchenham-')).map(i => [i.src.split('/').pop(), i.naturalWidth, getComputedStyle(i).display])");
  await s("Emulation.setDeviceMetricsOverride", { width, height: Math.min(height, 12000), deviceScaleFactor: 1, mobile: width < 768 });
  await sleep(300);
  const shot = await s("Page.captureScreenshot", { format: "png", captureBeyondViewport: true });
  const file = `${name}-${width}-${scheme}.png`;
  writeFileSync(join(out, file), Buffer.from(shot.data, "base64"));
  const errors = events.filter((e) => (e.method === "Log.entryAdded" && e.params.entry.level === "error") || e.method === "Runtime.exceptionThrown").map((e) => JSON.stringify(e.params).slice(0, 160));
  rows.push({ file, width, scheme, height, sideways, matched, scheme_attr, figures, errors });
  await send("Target.closeTarget", { targetId });
}
writeFileSync(join(out, "captures.json"), JSON.stringify(rows, null, 2));
for (const r of rows) console.log(r.file, "height", r.height, "sideways", r.sideways, "scheme", r.scheme_attr, "figures", JSON.stringify(r.figures), "errors", r.errors.length);
ws.close(); chrome.kill();

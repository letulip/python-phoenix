/**
 * Persistent storage. IndexedDB in the browser (attempts can hold code snapshots and
 * outgrow localStorage), with a memory backend for node tests and as a fallback when
 * IndexedDB is unavailable (the memory backend mirrors itself into localStorage if present).
 */

export const DB_NAME = "python-phoenix";
export const DB_VERSION = 1;
export const STORE_NAMES = ["attempts", "events", "kv"];
const KEY_PATHS = { attempts: "id", events: "id", kv: "key" };

function promisify(request) {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export class IDBBackend {
  constructor(db) { this.db = db; }

  static open(indexedDB = globalThis.indexedDB) {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        for (const name of STORE_NAMES) {
          if (!db.objectStoreNames.contains(name)) db.createObjectStore(name, { keyPath: KEY_PATHS[name] });
        }
      };
      req.onsuccess = () => resolve(new IDBBackend(req.result));
      req.onerror = () => reject(req.error);
      req.onblocked = () => reject(new Error("IndexedDB upgrade blocked by another tab"));
    });
  }

  tx(store, mode = "readonly") { return this.db.transaction(store, mode).objectStore(store); }
  get(store, key) { return promisify(this.tx(store).get(key)); }
  getAll(store) { return promisify(this.tx(store).getAll()); }
  put(store, value) { return promisify(this.tx(store, "readwrite").put(value)); }
  delete(store, key) { return promisify(this.tx(store, "readwrite").delete(key)); }
  clear(store) { return promisify(this.tx(store, "readwrite").clear()); }
  count(store) { return promisify(this.tx(store).count()); }
}

export class MemoryBackend {
  constructor({ storage = null, storageKey = "python-phoenix:db" } = {}) {
    this.storage = storage;
    this.storageKey = storageKey;
    this.data = Object.fromEntries(STORE_NAMES.map((n) => [n, new Map()]));
    this.load();
  }

  load() {
    if (!this.storage) return;
    try {
      const raw = this.storage.getItem(this.storageKey);
      if (!raw) return;
      const parsed = JSON.parse(raw);
      for (const name of STORE_NAMES) {
        for (const item of parsed[name] || []) this.data[name].set(item[KEY_PATHS[name]], item);
      }
    } catch { /* corrupted mirror: start empty */ }
  }

  persist() {
    if (!this.storage) return;
    try {
      const out = Object.fromEntries(STORE_NAMES.map((n) => [n, [...this.data[n].values()]]));
      this.storage.setItem(this.storageKey, JSON.stringify(out));
    } catch { /* quota exceeded: keep the in-memory copy */ }
  }

  async get(store, key) { return this.data[store].get(key); }
  async getAll(store) { return [...this.data[store].values()]; }
  async put(store, value) { this.data[store].set(value[KEY_PATHS[store]], value); this.persist(); return value[KEY_PATHS[store]]; }
  async delete(store, key) { this.data[store].delete(key); this.persist(); }
  async clear(store) { this.data[store].clear(); this.persist(); }
  async count(store) { return this.data[store].size; }
}

export class Store {
  constructor(backend) { this.backend = backend; }

  static async open() {
    if (globalThis.indexedDB) {
      try { return new Store(await IDBBackend.open()); } catch { /* fall through */ }
    }
    return new Store(new MemoryBackend({ storage: globalThis.localStorage || null }));
  }

  // key/value
  async kvGet(key, fallback = null) {
    const row = await this.backend.get("kv", key);
    return row === undefined || row === null ? fallback : row.value;
  }
  async kvSet(key, value) { await this.backend.put("kv", { key, value }); return value; }
  async kvDelete(key) { await this.backend.delete("kv", key); }
  async kvAll() {
    const rows = await this.backend.getAll("kv");
    return Object.fromEntries(rows.map((r) => [r.key, r.value]));
  }

  // attempts & events
  async putAttempt(attempt) { await this.backend.put("attempts", attempt); return attempt; }
  async getAttempt(id) { return this.backend.get("attempts", id); }
  async getAttempts() {
    const rows = await this.backend.getAll("attempts");
    return rows.sort((a, b) => String(a.startedAt).localeCompare(String(b.startedAt)));
  }
  async addEvent(event) { await this.backend.put("events", event); return event; }
  async getEvents() {
    const rows = await this.backend.getAll("events");
    return rows.sort((a, b) => String(a.t).localeCompare(String(b.t)));
  }
  async wipe() { for (const name of STORE_NAMES) await this.backend.clear(name); }
}

export function uuid() {
  if (globalThis.crypto && typeof globalThis.crypto.randomUUID === "function") return globalThis.crypto.randomUUID();
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

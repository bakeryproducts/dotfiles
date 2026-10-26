import { execFile, spawn } from "node:child_process"
import { mkdir, rm, writeFile } from "node:fs/promises"
import { homedir } from "node:os"
import { join } from "node:path"

const seen = new Set<string>()

async function sessionTitle(ctx: any, sessionID?: string): Promise<string> {
  if (!sessionID) return ""
  const info = await ctx.session.get({ sessionID }).catch(() => undefined)
  return String(info?.title ?? "")
}

function popup(color: string, text: string) {
  const msg = `fontsize:20 ${text}`
  spawn("hyprctl", ["notify", "-1", "6000", color, msg], { stdio: "ignore", detached: true }).unref()
}

function onEvent(event: any, title = "") {
  if (event.id) {
    if (seen.has(event.id)) return
    seen.add(event.id)
    if (seen.size > 500) seen.delete(seen.values().next().value!)
  }
  const label = title ? ` - ${title}` : ""
  if (event.type === "permission.asked") popup("rgb(fb4934)", `Permission needed${label}`)
  if (event.type === "session.idle" || event.type === "session.execution.succeeded") popup("rgb(d79921)", `Done${label}`)
}

const QUEUE = join(process.env.XDG_CACHE_HOME ?? join(homedir(), ".cache"), "oc-attention")
const ADD: Record<string, string> = {
  "permission.asked": "permission",
  "question.asked": "question",
  "session.execution.succeeded": "done",
}
const CLEAR = new Set(["permission.replied", "question.replied"])

function windowAddress(title: string): Promise<string | undefined> {
  return new Promise((resolve) => {
    execFile("hyprctl", ["clients", "-j"], (err, out) => {
      if (err) return resolve(undefined)
      try {
        resolve(JSON.parse(out).find((c: any) => c.title === `OC | ${title}`)?.address)
      } catch {
        resolve(undefined)
      }
    })
  })
}

async function track(event: any, title: string) {
  const sessionID = event.data?.sessionID
  if (!sessionID) return
  const file = join(QUEUE, String(sessionID))
  if (CLEAR.has(event.type)) return rm(file, { force: true })
  const address = await windowAddress(title)
  if (!address) return
  await mkdir(QUEUE, { recursive: true })
  await writeFile(file, JSON.stringify({ address, kind: ADD[event.type], title, ts: Date.now() }))
}

export default {
  id: "sound-notify",
  setup(ctx: any) {
    const controller = new AbortController()
    void (async () => {
      for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
        if (!(event.type in ADD) && !CLEAR.has(event.type)) continue
        const title = await sessionTitle(ctx, event.data?.sessionID)
        if (title.startsWith("ocq/")) continue
        await track(event, title).catch(() => {})
        if (event.type === "permission.asked" || event.type === "session.execution.succeeded") onEvent(event, title)
      }
    })().catch(() => {})
    return () => controller.abort()
  },
  async server() {
    return { event: async ({ event }: any) => onEvent(event) }
  },
}

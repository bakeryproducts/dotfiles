import { execFile, spawn } from "node:child_process"
import { mkdir, rm, writeFile } from "node:fs/promises"
import { homedir } from "node:os"
import { join } from "node:path"

const seen = new Set<string>()

const SOUNDS = join(homedir(), ".config/opencode/sounds")
const VOLUME = "0.6"
const SOUND: Record<string, string> = {
  question: "bip-bop-03.mp3",
  permission: "staplebops-06.mp3",
  error: "nope-03.mp3",
  done: "bip-bop-01.mp3",
  subagent_done: "yup-01.mp3",
}

function play(name: string) {
  spawn("pw-play", ["--volume", VOLUME, join(SOUNDS, SOUND[name])], { stdio: "ignore", detached: true }).unref()
}

function soundFor(event: any, info: any): string | undefined {
  if (event.type === "form.created") return "question"
  if (event.type === "permission.asked") return "permission"
  if (event.type === "session.execution.failed") return event.data?.error?.type === "provider.free-limit" ? undefined : "error"
  if (event.type === "session.execution.succeeded" || event.type === "session.execution.interrupted")
    return info?.parentID ? "subagent_done" : "done"
}

async function sessionInfo(ctx: any, sessionID?: string): Promise<any> {
  if (!sessionID) return undefined
  return ctx.session.get({ sessionID }).catch(() => undefined)
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
const SOUND_EVENTS = new Set([
  "form.created",
  "permission.asked",
  "session.execution.succeeded",
  "session.execution.interrupted",
  "session.execution.failed",
])

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
        const tracked = event.type in ADD || CLEAR.has(event.type)
        if (!tracked && !SOUND_EVENTS.has(event.type)) continue
        const info = await sessionInfo(ctx, event.data?.sessionID ?? event.data?.form?.sessionID)
        const title = String(info?.title ?? "")
        if (title.startsWith("ocq/")) continue
        const sound = soundFor(event, info)
        if (sound) play(sound)
        if (!tracked) continue
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

import { spawn } from "node:child_process"

const SOUNDS = "/home/gsm/Documents/gmcp/oc-bridge-plugin/data/sounds"
const PERMISSION_SOUND = `${SOUNDS}/question/painsharp04.mp3`
const IDLE_SOUND = `${SOUNDS}/message/gunslingerpunch03.mp3`

function play(file: string, volume: number) {
  spawn("paplay", [`--volume=${volume}`, file], { stdio: "ignore", detached: true }).unref()
}

const seen = new Set<string>()

const muted = new Map<string, boolean>()

async function isMuted(ctx: any, sessionID?: string) {
  if (!sessionID) return false
  if (!muted.has(sessionID)) {
    const info = await ctx.session.get({ sessionID }).catch(() => undefined)
    muted.set(sessionID, String(info?.title ?? "").startsWith("ocq/"))
    if (muted.size > 500) muted.delete(muted.keys().next().value!)
  }
  return muted.get(sessionID)!
}

function onEvent(event: any) {
  if (event.id) {
    if (seen.has(event.id)) return
    seen.add(event.id)
    if (seen.size > 500) seen.delete(seen.values().next().value!)
  }
  if (event.type === "permission.asked") play(PERMISSION_SOUND, 52429)
  if (event.type === "session.idle" || event.type === "session.execution.succeeded") play(IDLE_SOUND, 32768)
}

export default {
  id: "sound-notify",
  setup(ctx: any) {
    const controller = new AbortController()
    void (async () => {
      for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
        if (event.type !== "permission.asked" && event.type !== "session.execution.succeeded") continue
        if (await isMuted(ctx, event.data?.sessionID)) continue
        onEvent(event)
      }
    })().catch(() => {})
    return () => controller.abort()
  },
  async server() {
    return { event: async ({ event }: any) => onEvent(event) }
  },
}

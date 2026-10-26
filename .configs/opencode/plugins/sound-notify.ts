import { spawn } from "node:child_process"

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

export default {
  id: "sound-notify",
  setup(ctx: any) {
    const controller = new AbortController()
    void (async () => {
      for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
        if (event.type !== "permission.asked" && event.type !== "session.execution.succeeded") continue
        const title = await sessionTitle(ctx, event.data?.sessionID)
        if (title.startsWith("ocq/")) continue
        onEvent(event, title)
      }
    })().catch(() => {})
    return () => controller.abort()
  },
  async server() {
    return { event: async ({ event }: any) => onEvent(event) }
  },
}

import type { Plugin } from "@opencode-ai/plugin"
import { appendFileSync } from "node:fs"

const SOUNDS = "/home/gsm/Documents/gmcp/oc-bridge-plugin/data/sounds"
const PERMISSION_SOUND = `${SOUNDS}/question/painsharp04.mp3`
const IDLE_SOUND = `${SOUNDS}/message/gunslingerpunch03.mp3`
const DEBUG_LOG = "/tmp/opencode/plugin-debug.log"

function debug(msg: string) {
  try {
    appendFileSync(DEBUG_LOG, `${new Date().toISOString()} ${msg}\n`)
  } catch {}
}

export default (async ({ $ }) => {
  debug("plugin loaded")

  function play(file: string, volume: number) {
    debug(`play ${file}`)
    $`paplay --volume=${volume} ${file}`
      .quiet()
      .nothrow()
      .then((out) => {
        debug(`play exit=${out.exitCode} stderr=${out.stderr.toString().slice(0, 300)}`)
      })
      .catch((err) => {
        debug(`play error=${String(err)}`)
      })
  }

  return {
    event: async ({ event }) => {
      debug(`event ${event.type}`)
      if (event.type === "permission.asked") {
        play(PERMISSION_SOUND, 52429)
      }
      if (event.type === "session.idle") {
        play(IDLE_SOUND, 32768)
      }
    },
  }
}) satisfies Plugin

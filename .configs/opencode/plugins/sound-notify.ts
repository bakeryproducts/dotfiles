import type { Plugin } from "@opencode-ai/plugin"
import { spawn } from "node:child_process"

const SOUNDS = "/home/gsm/Documents/gmcp/oc-bridge-plugin/data/sounds"
const PERMISSION_SOUND = `${SOUNDS}/question/painsharp04.mp3`
const IDLE_SOUND = `${SOUNDS}/message/gunslingerpunch03.mp3`

function play(file: string, volume: number) {
  spawn("paplay", [`--volume=${volume}`, file], { stdio: "ignore", detached: true }).unref()
}

export default (async () => {
  return {
    event: async ({ event }) => {
      if (event.type === "permission.asked") {
        play(PERMISSION_SOUND, 52429)
      }
      if (event.type === "session.idle") {
        play(IDLE_SOUND, 32768)
      }
    },
  }
}) satisfies Plugin

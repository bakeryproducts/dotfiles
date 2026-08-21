import type { Plugin } from "@opencode-ai/plugin"

const SOUNDS = "/home/gsm/Documents/gmcp/oc-bridge-plugin/data/sounds"
const PERMISSION_SOUND = `${SOUNDS}/question/painsharp04.mp3`
const IDLE_SOUND = `${SOUNDS}/message/gunslingerpunch03.mp3`

export default (async ({ $ }) => {
  function play(file: string, volume: number) {
    $`paplay --volume=${volume} ${file}`.quiet().nothrow()
  }

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

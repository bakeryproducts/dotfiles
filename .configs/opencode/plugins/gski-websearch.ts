import { execFile } from "node:child_process"

const GSKI = "/home/gsm/miniconda3/bin/gski"

function run(query: string, signal: AbortSignal) {
  return new Promise<string>((resolve, reject) => {
    execFile(GSKI, ["websearch", query], { signal, maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
      if (err) return reject(new Error(stderr || err.message))
      resolve(stdout)
    })
  })
}

export default {
  id: "gski-websearch",
  async setup(ctx: any) {
    await ctx.websearch.transform((editor: any) => {
      editor.add({
        id: "gski",
        name: "gski websearch",
        execute: async ({ query }: { query: string }, { signal }: { signal: AbortSignal }) => {
          const content = await run(query, signal)
          return [{ url: "https://www.google.com/search?q=" + encodeURIComponent(query), title: query, content, time: {} }]
        },
      })
      editor.default.set("gski")
    })
  },
}

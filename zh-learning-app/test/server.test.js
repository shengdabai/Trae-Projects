import { test } from 'node:test'
import assert from 'node:assert/strict'
import { once } from 'node:events'
import { createApp, createPipelineLoader, startServer } from '../server.js'

test('default server listens exclusively on loopback', async t => {
  const server = startServer(0)
  t.after(() => new Promise(resolve => server.close(resolve)))
  await once(server, 'listening')
  assert.equal(server.address().address, '127.0.0.1')
})

test('concurrent callers share model initialization', async () => {
  const calls = []
  const load = createPipelineLoader(async (task, model) => {
    calls.push(model)
    await new Promise(resolve => setImmediate(resolve))
    return model
  })
  const first = load()
  assert.equal(load(), first)
  const [a, b] = await Promise.all([first, load()])
  assert.equal(a, b)
  assert.deepEqual(calls, ['Xenova/opus-mt-en-zh', 'Xenova/opus-mt-zh-en'])
  assert.equal(await load(), a)
})

test('model initialization can retry after failure', async () => {
  let attempts = 0
  const load = createPipelineLoader(async () => {
    if (++attempts === 1) throw new Error('download failed')
    return () => []
  })
  await assert.rejects(load(), /download failed/)
  assert.equal(typeof (await load()).zh2en, 'function')
  assert.equal(attempts, 3)
})

test('retry preserves the first model if the second model fails to initialize', async () => {
  const calls = []
  const load = createPipelineLoader(async (task, model) => {
    calls.push(model)
    if (calls.length === 2) throw new Error('second model failed')
    return () => []
  })
  await assert.rejects(load(), /second model failed/)
  await load()
  assert.deepEqual(calls, ['Xenova/opus-mt-en-zh', 'Xenova/opus-mt-zh-en', 'Xenova/opus-mt-zh-en'])
})

test('HTTP input boundaries reject invalid requests before loading models', async t => {
  let loads = 0
  const app = createApp(async () => {
    loads++
    return {
      en2zh: async () => [{ translation_text: '你好' }],
      zh2en: async () => [{ translation_text: 'hello' }]
    }
  })
  const server = app.listen(0, '127.0.0.1')
  t.after(() => new Promise(resolve => server.close(resolve)))
  await once(server, 'listening')
  const base = `http://127.0.0.1:${server.address().port}`
  const post = body => fetch(`${base}/api/translate`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body
  })
  assert.deepEqual(await (await fetch(`${base}/health`)).json(), { ok: true })
  for (const english of [null, 42, {}, ['hello'], '', 'x'.repeat(501)]) {
    const response = await post(JSON.stringify({ english }))
    assert.equal(response.status, 400)
    assert.ok((await response.json()).error)
  }
  for (const [body, status] of [['{', 400], ['"' + 'x'.repeat(1024 * 1024) + '"', 413]]) {
    const response = await post(body)
    assert.equal(response.status, status)
    assert.deepEqual(await response.json(), { error: status === 413 ? 'Input too large' : 'invalid request' })
  }
  assert.equal(loads, 0)
  const response = await post(JSON.stringify({ english: '  Hello   world  ', granularity: 'char' }))
  assert.equal(response.status, 200)
  const data = await response.json()
  assert.equal(data.chinese, '你好')
  assert.equal(data.notes.normalized_english, 'Hello world')
  assert.deepEqual(data.segments.map(s => s.zh), ['你', '好'])
  assert.ok(data.segments.every(s => s.en === 'hello' && s.py))
})

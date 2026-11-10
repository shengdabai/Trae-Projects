import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import vm from 'node:vm'

test('HTTP failures notify the user without replacing the last successful result', async () => {
  const nodes = new Map(['translate', 'input', 'granularity', 'result', 'zh', 'py', 'norm', 'segments']
    .map(id => [`#${id}`, { value: 'hello', style: {}, textContent: 'last result' }]))
  let click
  nodes.get('#translate').addEventListener = (event, listener) => { click = listener }
  const alerts = []
  vm.runInNewContext(await readFile(new URL('../public/app.js', import.meta.url), 'utf8'), {
    document: { querySelector: selector => nodes.get(selector) },
    fetch: async () => ({ ok: false, status: 429, json: async () => ({ error: 'Too many requests' }) }),
    alert: message => alerts.push(message),
    console: { error() {} }
  })
  await click()
  assert.equal(alerts.length, 1)
  assert.equal(nodes.get('#zh').textContent, 'last result')
  assert.equal(nodes.get('#result').style.display, undefined)
  assert.equal(nodes.get('#translate').disabled, false)
})

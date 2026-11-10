import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp, copyFile, writeFile, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import path from 'node:path'
import { execFileSync } from 'node:child_process'

test('Kimi wrapper preserves arguments without bypassing permission prompts', async t => {
  const dir = await mkdtemp(path.join(tmpdir(), 'kimi-wrapper-'))
  t.after(() => rm(dir, { recursive: true, force: true }))
  await copyFile(new URL('../../bin/kimi', import.meta.url), path.join(dir, 'kimi'))
  await writeFile(path.join(dir, 'claude'), '#!/bin/bash\nprintf "%s\\n" "$@"\n', { mode: 0o700 })
  const args = execFileSync('bash', [path.join(dir, 'kimi'), 'a question with spaces'], {
    env: { PATH: process.env.PATH, MOONSHOT_API_KEY: 'synthetic-test-value' }, encoding: 'utf8'
  }).trim().split('\n')
  assert.deepEqual(args, ['--model', 'moonshot-v1-8k', 'a question with spaces'])
})

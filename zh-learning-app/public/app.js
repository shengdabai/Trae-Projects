const $ = sel => document.querySelector(sel)

$('#translate').addEventListener('click', async () => {
  const english = $('#input').value.trim()
  const granularity = $('#granularity').value
  if (!english) return
  $('#translate').disabled = true
  try {
    const res = await fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ english, granularity })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`)
    $('#result').style.display = 'block'
    $('#zh').textContent = data.chinese || ''
    $('#py').textContent = data.pinyin || ''
    $('#norm').textContent = data.notes?.normalized_english || ''
    const tbody = $('#segments')
    tbody.innerHTML = ''
    for (const seg of data.segments || []) {
      const tr = document.createElement('tr')
      const tdZh = document.createElement('td')
      tdZh.textContent = seg.zh
      const tdPy = document.createElement('td')
      tdPy.className = 'mono'
      tdPy.textContent = seg.py || ''
      const tdEn = document.createElement('td')
      tdEn.textContent = seg.en || ''
      tr.append(tdZh, tdPy, tdEn)
      tbody.appendChild(tr)
    }
  } catch (e) {
    alert('请求失败，请重试')
    console.error(e)
  } finally {
    $('#translate').disabled = false
  }
})

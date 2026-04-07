import React, { useEffect, useState } from 'react'
import './App.css'

const launchSteps = [
  'Masuk ke folder react-vite-dev',
  'Jalankan npm install sekali saja',
  'Jalankan npm run dev',
  'Buka localhost:18089',
]

const features = [
  {
    title: 'Port Sudah Dikunci',
    text: 'Dev server selalu berjalan di port 18089 supaya tidak bentrok dengan contoh lain.',
  },
  {
    title: 'React JavaScript Biasa',
    text: 'File utama memakai .jsx tanpa TypeScript agar lebih sederhana untuk belajar dan testing.',
  },
  {
    title: 'Siap Edit Langsung',
    text: 'Ubah komponen, simpan file, lalu lihat HMR bekerja otomatis di browser.',
  },
]

function App() {
  const [status, setStatus] = useState('Mode default aktif')
  const [clock, setClock] = useState('')

  useEffect(() => {
    const updateClock = () => {
      setClock(
        new Intl.DateTimeFormat('id-ID', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
        }).format(new Date())
      )
    }

    updateClock()
    const timer = window.setInterval(updateClock, 1000)

    return () => window.clearInterval(timer)
  }, [])

  return React.createElement(
    'div',
    { className: 'page-shell' },
    React.createElement(
      'header',
      { className: 'hero-panel' },
      React.createElement('p', { className: 'eyebrow' }, 'React + Vite Dev Playground'),
      React.createElement(
        'div',
        { className: 'hero-copy' },
        React.createElement(
          'div',
          null,
          React.createElement('h1', null, 'React JS siap jalan dengan npm run dev.'),
          React.createElement(
            'p',
            { className: 'lead' },
            'Project ini dibuat untuk testing React JavaScript biasa, dengan dev server langsung di port 18089.'
          )
        ),
        React.createElement(
          'div',
          { className: 'status-card' },
          React.createElement('span', { className: 'status-label' }, 'Status'),
          React.createElement('strong', null, status),
          React.createElement('span', { className: 'clock' }, `Jam lokal: ${clock || '--:--:--'}`)
        )
      ),
      React.createElement(
        'div',
        { className: 'hero-actions' },
        React.createElement(
          'button',
          { type: 'button', onClick: () => setStatus('Hot reload siap dipakai') },
          'Tes Interaksi'
        ),
        React.createElement('code', null, 'http://localhost:18089')
      )
    ),
    React.createElement(
      'main',
      { className: 'content-grid' },
      React.createElement(
        'section',
        { className: 'steps-panel' },
        React.createElement(
          'div',
          { className: 'section-head' },
          React.createElement('p', { className: 'section-kicker' }, 'Quick Start'),
          React.createElement('h2', null, 'Langsung pakai')
        ),
        React.createElement(
          'ol',
          { className: 'steps-list' },
          launchSteps.map((step) => React.createElement('li', { key: step }, step))
        )
      ),
      React.createElement(
        'section',
        { className: 'features-panel' },
        React.createElement(
          'div',
          { className: 'section-head' },
          React.createElement('p', { className: 'section-kicker' }, 'Kenapa setup ini'),
          React.createElement('h2', null, 'Sederhana tapi enak dipakai')
        ),
        React.createElement(
          'div',
          { className: 'feature-list' },
          features.map((feature) =>
            React.createElement(
              'article',
              { key: feature.title, className: 'feature-card' },
              React.createElement('h3', null, feature.title),
              React.createElement('p', null, feature.text)
            )
          )
        )
      )
    )
  )
}

export default App
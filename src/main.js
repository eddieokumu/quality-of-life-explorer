import "./tailwind.css"
import './css/metadata.css'
import './css/table.css'
import './css/sw-dialog.css'
import './lib/registerServiceWorker'
import { selectedMetric } from './store/store'
import Tabs from './lib/Tabs.svelte'
import Meta from './lib/Meta.svelte'
import Map from './lib/Map.svelte'
import SubMap from './lib/SubMap.svelte'
import Charts from './lib/Charts.svelte'
import Search from './lib/Search.svelte'
import Embed from './lib/Embed.svelte'
import Contact from './lib/Contact.svelte'
import NavMenu from './lib/NavMenu.svelte'
import Help from './lib/Help.svelte'
import Welcome from './lib/Welcome.svelte'


// Bridge window.model.metricId setter → Svelte selectedMetric store
// This makes the related variable links in meta HTML files work
window.model = {}
Object.defineProperty(window.model, 'metricId', {
  set(value) {
    // Ensure the metric has the 'm' prefix
    const metric = value.startsWith('m') ? value : `m${value}`
    selectedMetric.set(metric)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})

new NavMenu({
  target: document.getElementById("navmenu")
})

new Welcome({
  target: document.getElementById("welcome")
})

new Tabs({
  target: document.getElementById("tabs")
})

new Meta({
  target: document.getElementById("meta")
})

new Map({
  target: document.getElementById("mapContainer")
})

new SubMap({
  target: document.getElementById("misccontrols")
})

new Charts({
  target: document.getElementById("charts")
})

new Search({
  target: document.getElementById("search")
})

new Help({
  target: document.getElementById("help")
})

new Embed({
  target: document.getElementById("embed")
})

new Contact({
  target: document.getElementById("contact")
})

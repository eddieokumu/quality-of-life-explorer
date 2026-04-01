<script>
  import { selectedNeighborhoods, mapZoom } from "../store/store"
  import groups from "../assets/neighborhod-groups.json"
  import wardNames from "../assets/ward-names.json"

  let searchString = ""
  let searchResults = []
  let inputFocused = false

  // Pre-build a flat list of all searchable items for fast lookup
  // Format: { cat, label, sublabel, ids: [] }
  const searchIndex = buildSearchIndex()

  function buildSearchIndex() {
    const index = []

    // Add individual wards (searchable by ID or name)
    for (const [id, name] of Object.entries(wardNames)) {
      // Find which constituency this ward belongs to
      let constituency = ""
      for (const [con, wards] of Object.entries(groups.Constituency)) {
        if (wards.includes(id)) { constituency = con; break }
      }
      index.push({
        cat: "Ward",
        label: name,
        sublabel: constituency ? `Ward ${id} · ${constituency}` : `Ward ${id}`,
        ids: [id],
        searchTerms: [name.toLowerCase(), id]
      })
    }

    // Add constituencies (selects all wards in that constituency)
    for (const [name, wards] of Object.entries(groups.Constituency)) {
      index.push({
        cat: "Constituency",
        label: name,
        sublabel: `${wards.length} wards`,
        ids: wards,
        searchTerms: [name.toLowerCase()]
      })
    }

    // Add municipalities
    for (const [name, wards] of Object.entries(groups.Municipality)) {
      index.push({
        cat: "Municipality",
        label: name,
        sublabel: `${wards.length} wards`,
        ids: wards,
        searchTerms: [name.toLowerCase()]
      })
    }

    return index
  }

  function search() {
    const str = searchString.trim().toLowerCase()

    if (str.length === 0) {
      searchResults = []
      return
    }

    searchResults = searchIndex.filter(item =>
      item.searchTerms.some(term => term.includes(str))
    ).slice(0, 10)
  }

  function selectResult(result) {
    $selectedNeighborhoods = result.ids
    $mapZoom = true
    searchResults = []
    searchString = ""
  }

  // Badge color by category
  const catColor = {
    Ward: "#e20025",
    Constituency: "#1a5276",
    Municipality: "#117a65"
  }
</script>

<div class="relative">
  <div class="mb-2">
    <input
      class="w-full border-b border-gray-300 py-1 text-base focus:border-b-2 focus:border-highlight focus:outline-none transition-all bg-transparent"
      bind:value={searchString}
      on:input={search}
      on:focus={() => { inputFocused = true; search() }}
      on:blur={() => setTimeout(() => { searchResults = []; inputFocused = false }, 200)}
      placeholder="Search ward or constituency…"
      autocomplete="off"
      spellcheck="false"
    />
  </div>

  {#if searchResults.length > 0}
    <div
      class="absolute w-full bg-white border border-gray-200 shadow-lg overflow-y-auto overflow-x-hidden z-50 rounded-sm"
      style="max-height: 260px;"
    >
      {#each searchResults as result}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <div
          role="button"
          tabindex="0"
          class="cursor-pointer text-sm px-3 py-2 hover:bg-gray-100 transition-colors flex items-center gap-2 border-b border-gray-100 last:border-0"
          on:click={() => selectResult(result)}
        >
          <span
            class="flex-shrink-0 text-white text-xs font-bold px-1.5 py-0.5 rounded"
            style="background: {catColor[result.cat] || '#555'}; min-width: 2.5rem; text-align: center;"
          >
            {result.cat.substring(0, 4).toUpperCase()}
          </span>
          <span class="flex-1 min-w-0">
            <span class="font-medium text-gray-900 block truncate">{result.label}</span>
            <span class="text-gray-400 text-xs">{result.sublabel}</span>
          </span>
        </div>
      {/each}
    </div>
  {/if}

  <p class="text-sm mt-3" style="color: #757575;">
    Search by
    <span
      class="cursor-help"
      style="border-bottom: 1px dashed;"
      title="Wards are the smallest geographic units used for data presentation in the Machakos County Quality of Life Explorer. Each ward falls within one of the eight constituencies."
    >ward name</span>,
    ID, or
    <span
      class="cursor-help"
      style="border-bottom: 1px dashed;"
      title="Machakos County has 8 constituencies: Kangundo, Kathiani, Machakos Town, Masinga, Matungulu, Mavoko, Mwala, and Yatta."
    >constituency</span>.
  </p>
</div>

<style>
  input:focus {
    outline: none;
  }
</style>

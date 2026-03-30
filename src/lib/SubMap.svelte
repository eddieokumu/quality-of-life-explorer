<script>
  import Time from "./Time.svelte"
  import Table from "./Table.svelte"
  import groups from "../assets/neighborhod-groups.json"
  import {
    selectedNeighborhoods,
    selectedMetric,
    selectedData,
    selectedConfig,
    mapZoom,
  } from "../store/store"
  import { sendDownload, formatNumber } from "./utils"

  let download
  let openGroup = null  // tracks which dropdown is open

  function toggleGroup(group) {
    openGroup = openGroup === group ? null : group
  }

  function closeAll() {
    openGroup = null
  }

  function doDownload() {
    const selectedFilter =
      download === "sgeojson" || download === "scsv" ? true : false

    if (download === "geojson" || download === "sgeojson") {
      const outJSON = {
        type: "FeatureCollection",
        features: [],
      }
      fetch("./data/geography/geography.geojson.json")
        .then((response) => {
          if (!response.ok) {
            throw new Error()
          }
          return response.json()
        })
        .then((json) => {
          json.features.forEach((elem, jsonidx) => {
            $selectedData.years.forEach((y, idx) => {
              elem.properties[y] = $selectedData.m[elem.properties.id][idx]
              if ($selectedConfig.raw_label) {
                elem.properties[`${y}-raw`] =
                  Math.round(
                    $selectedData.d[elem.properties.id][idx] *
                      $selectedData.m[elem.properties.id][idx] *
                      10
                  ) / 10
              }
            })
            if (
              !selectedFilter ||
              (selectedFilter &&
                $selectedNeighborhoods.indexOf(elem.properties.id) !== -1)
            ) {
              outJSON.features.push(elem)
            }
          })
          sendDownload(
            JSON.stringify(outJSON),
            "data:text/json;charset=utf-8;",
            `${$selectedConfig.title}.geojson`
          )
        })
        .catch((error) => {
          download = "default"
          console.error(
            "There has been a problem with your fetch operation:",
            error
          )
        })
    }
    if (download === "csv" || download === "scsv") {
      const header = []
      let body = ""

      header.push("NPA")
      header.push(...$selectedData.years)

      if ($selectedConfig.raw_label)
        header.push(...$selectedData.years.map((el) => `${el} Raw`))

      for (const key in $selectedData.m) {
        let row = [
          key,
          ...$selectedData.m[key].map((el) =>
            formatNumber(el, $selectedConfig.format || null)
          ),
        ]
        if ($selectedConfig.raw_label) {
          row.push(
            ...$selectedData.m[key].map(
              (el, idx) =>
                `"${formatNumber(el * $selectedData.d[key][idx], null)}"`
            )
          )
        }
        if (
          !selectedFilter ||
          (selectedFilter && $selectedNeighborhoods.indexOf(key) !== -1)
        ) {
          body += row.toString() + "\n"
        }
      }

      sendDownload(
        header.join(",") + "\n" + body,
        "data:text/csv;charset=utf-8;",
        `${$selectedConfig.title}.csv`
      )
    }
    if (download === "zip") {
      window.open("downloads/qol-data.zip")
    }
    if (download === "metadata") {
      window.open(`data/meta/${$selectedConfig.metric}.html`)
    }

    download = "default"
  }

  function selectItem(items) {
    $selectedNeighborhoods = items
    $mapZoom = true
    openGroup = null
  }

  function print() {
    window.open(
      `./report.html#${$selectedMetric.replace(
        "m",
        ""
      )}/${$selectedNeighborhoods.join(",")}`
    )
  }
</script>

<style>
  .approx-container {
    position: relative;
    display: inline-block;
  }
  .approx-link {
    color: #e20025;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.875rem;
    text-decoration: underline;
    margin-left: 8px;
    background: none;
    border: none;
    padding: 0;
    font-family: inherit;
  }
  .approx-link:hover {
    color: #9e0018;
  }
  .approx-dropdown {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    background: white;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    min-width: 180px;
    z-index: 999;
    padding: 4px 0;
  }
  .approx-dropdown-item {
    display: block;
    width: 100%;
    padding: 8px 16px;
    text-align: left;
    font-size: 0.875rem;
    color: #1b2631;
    background: none;
    border: none;
    cursor: pointer;
    font-family: Roboto, sans-serif;
  }
  .approx-dropdown-item:hover {
    background: #f5f5f5;
  }
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 998;
  }
</style>

<Time />

<div class="py-3 text-right flex justify-end items-center gap-2">
  <button class="bg-gray-200 text-black hover:bg-gray-300 px-4 py-2 font-bold text-sm uppercase" on:click={() => ($selectedNeighborhoods = [])}>Clear Selected</button>
  <button class="bg-highlight text-white hover:bg-red-800 px-4 py-2 font-bold text-sm uppercase" on:click={print}>Report</button>
  <button class="bg-highlight text-white hover:bg-red-800 px-4 py-2 font-bold text-sm uppercase" on:click={() => window.print()}>Print Map</button>
</div>

<div class="text-right text-sm text-gray-700 flex justify-end items-center flex-wrap gap-1 mb-2">
  <span class="mr-1">Approximate:</span>
  {#each Object.keys(groups) as group}
    <div class="approx-container">
      <button class="approx-link" on:click|stopPropagation={() => toggleGroup(group)}>
        {group}
      </button>
      {#if openGroup === group}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="overlay" on:click={closeAll}></div>
        <div class="approx-dropdown">
          {#each Object.keys(groups[group]) as item}
            <button class="approx-dropdown-item" on:click={() => selectItem(groups[group][item])}>
              {item}
            </button>
          {/each}
        </div>
      {/if}
    </div>
  {/each}
</div>

<Table />

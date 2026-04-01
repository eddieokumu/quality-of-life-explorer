<script>
  import {
    selectedData,
    selectedConfig,
    calcCounty,
    calcSelected,
    selectedNeighborhoods,
    yearIdx,
    breaks,
    colors
  } from "../store/store"
  import { formatNumber, isNumeric } from "./utils"
  import { equalIntervalBreaks } from 'simple-statistics'
  import { onMount, tick } from "svelte"

  let tchart
  let dchart
  let ApexCharts
  let mounted = false

  // SVG distribution chart state
  let distChartData = []
  let distMedian = '0'
  let distYear = ''
  let distSelected = []

  onMount(async () => {
    const { default: apexcharts } = await import("apexcharts")
    ApexCharts = apexcharts
    mounted = true
  })

  // trend chart
  $: {
    if (mounted && $selectedData && $selectedNeighborhoods) {
      handleTrendChart($selectedData.years && $selectedData.years.length > 1);
    }
  }

  async function handleTrendChart(shouldShow) {
    if (shouldShow) {
      await tick();
      trendChart();
    } else if (tchart) {
      tchart.destroy();
      tchart = null;
    }
  }

  // SVG Data Distribution chart — purely reactive
  $: if ($selectedData && $selectedNeighborhoods && $yearIdx >= 0 && $breaks) {
    updateDistChart()
  }

  function updateDistChart() {
    const rawData = []
    distYear = $selectedData.years[$yearIdx]

    for (const key in $selectedData.m) {
      const val = $selectedData.m[key][$yearIdx]
      if (isNumeric(val)) {
        rawData.push({ id: key, val })
      }
    }
    rawData.sort((a, b) => a.val - b.val)

    const n = rawData.length
    let medVal = 0
    if (n > 0) {
      medVal = n % 2 === 0
        ? (rawData[n/2 - 1].val + rawData[n/2].val) / 2
        : rawData[Math.floor(n/2)].val
    }
    distMedian = formatNumber(medVal, $selectedConfig.format || null)
    distSelected = $selectedNeighborhoods
    distChartData = rawData
  }

  // Determine which of the 5 break bands a value belongs to
  function getBandIndex(val, bks) {
    for (let i = 0; i < bks.length; i++) {
      if (val <= bks[i]) return i
    }
    return bks.length - 1
  }

  function trendChart() {
    const countySeries = []
    $calcCounty.forEach((el, idx) => {
      if (el !== null && el !== undefined) {
        countySeries.push({
          x: parseInt($selectedData.years[idx], 10),
          y: el,
        })
      }
    })

    let options = {
      chart: {
        type: "line",
        height: 200,
        zoom: { enabled: false },
        toolbar: { show: false },
        fontFamily: 'Roboto, sans-serif',
      },
      markers: {
        size: 4,
        strokeWidth: 0,
        hover: { sizeOffset: 2 }
      },
      series: [
        {
          name: "County",
          data: countySeries,
        },
      ],
      xaxis: {
        type: "numeric",
        tickAmount: $selectedData.years.length - 1 > 0 ? $selectedData.years.length - 1 : 1,
        tooltip: { enabled: false },
        labels: {
          style: { fontSize: '10px', colors: '#999' },
          formatter: function(val) {
            return Math.floor(val).toString();
          }
        },
        axisBorder: { show: false },
        axisTicks: { show: false },
      },
      stroke: {
        curve: "smooth",
        width: 2,
      },
      colors: ["#FFBF00", "#2A9D8F"],
      yaxis: {
        min: 0,
        labels: {
          style: { fontSize: '10px', colors: '#999' },
          formatter: (value) =>
            formatNumber(value, $selectedConfig.format || null),
        },
      },
      grid: {
        borderColor: '#e5e7eb',
        strokeDashArray: 4,
        xaxis: { lines: { show: false } },
        yaxis: { lines: { show: true } },
      },
      tooltip: {
        x: { format: "yyyy" },
      },
    }

    if ($selectedNeighborhoods.length > 0) {
      const selectSeries = []
      $calcSelected.forEach((el, idx) => {
        if (el !== null && el !== undefined) {
          selectSeries.push({
            x: parseInt($selectedData.years[idx], 10),
            y: el,
          })
        }
      })
      options.series.push({
        name: "Selected",
        data: selectSeries,
      })
    }

    if ($selectedConfig.format && $selectedConfig.format === "percent") {
      options.yaxis.min = 0
      options.yaxis.max = 100
    }

    if (!tchart) {
      tchart = new ApexCharts(document.querySelector("#tchart"), options)
      tchart.render()
    } else {
      tchart.updateOptions(options)
    }
  }


</script>

<style>
  .chart-card {
    background: white;
    border: 1px solid #e0e0e0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    padding: 20px 15px 15px 15px;
    border-radius: 4px;
  }
  .dist-title {
    text-align: center;
    font-size: 1rem;
    font-weight: 500;
    color: #444;
    margin: 0 0 4px;
    font-family: Roboto, sans-serif;
  }
  .dist-legend {
    text-align: center;
    font-size: 0.78em;
    color: #757575;
    margin: 2px 0 4px;
    font-family: Roboto, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }

</style>

<div class="flex flex-col gap-3">
  <!-- Card 1: SVG Data Distribution Chart -->
  <div class="chart-card">
    <h1 class="dist-title">Data Distribution, {distYear}</h1>
    <div class="dist-legend">
      {#if distSelected.length > 0}
        <span><svg class="inline align-middle" style="width: 1.25em; height: 1.25em; fill: #2A9D8F; margin-right: 2px;" viewBox="0 0 32 32"><path d="M16 2.688c7.375 0 13.313 5.938 13.313 13.313s-5.938 13.313-13.313 13.313-13.313-5.938-13.313-13.313 5.938-13.313 13.313-13.313z"></path></svg> Selected</span>
      {/if}
      <span><svg class="inline align-middle" style="width: 1.25em; height: 1.25em; fill: #757575; margin-right: 2px;" viewBox="0 0 32 32"><path d="M16 13.313c1.438 0 2.688 1.25 2.688 2.688s-1.25 2.688-2.688 2.688-2.688-1.25-2.688-2.688 1.25-2.688 2.688-2.688zM24 13.313c1.438 0 2.688 1.25 2.688 2.688s-1.25 2.688-2.688 2.688-2.688-1.25-2.688-2.688 1.25-2.688 2.688-2.688zM8 13.313c1.438 0 2.688 1.25 2.688 2.688s-1.25 2.688-2.688 2.688-2.688-1.25-2.688-2.688 1.25-2.688 2.688-2.688z"></path></svg> Median {distMedian}</span>
    </div>
    {#if distChartData.length > 1 && $breaks}
      {@const W = 340}
      {@const H = 140}
      {@const PAD_L = 26}
      {@const PAD_R = 6}
      {@const PAD_B = 4}
      {@const PAD_T = 4}
      {@const n = distChartData.length}
      {@const minVal = distChartData[0].val}
      {@const maxVal = distChartData[n-1].val}
      {@const valRange = maxVal - minVal || 1}
      {@const chartW = W - PAD_L - PAD_R}
      {@const chartH = H - PAD_B - PAD_T}
      {@const bandColors = ['rgb(242,232,207)','rgb(168,213,186)','rgb(96,165,142)','rgb(42,157,143)','rgb(38,70,83)']}
      {@const getX = (i) => PAD_L + (i / (n - 1)) * chartW}
      {@const getY = (v) => PAD_T + chartH - ((v - minVal) / valRange) * chartH}

      <svg viewBox="0 0 {W} {H}" width="100%" style="display:block;" xmlns="http://www.w3.org/2000/svg">
        <!-- Y axis grid lines -->
        {#each [0, 0.25, 0.5, 0.75, 1] as t}
          {@const ty = PAD_T + chartH * (1 - t)}
          <line x1={PAD_L} y1={ty} x2={W - PAD_R} y2={ty} stroke="#e5e7eb" stroke-width="1" stroke-dasharray="3,2"/>
          <text x={PAD_L - 4} y={ty + 4} text-anchor="end" fill="#bbb" font-size="7.5">{formatNumber(minVal + t * valRange)}</text>
        {/each}
        <!-- Y axis line -->
        <line x1={PAD_L} y1={PAD_T} x2={PAD_L} y2={PAD_T + chartH} stroke="#ddd" stroke-width="1"/>

        <!--
          No-gap area fill: for each consecutive pair of points we draw a
          filled trapezoid. Color is determined by the band of the LEFT point.
          This guarantees zero gaps between segments.
        -->
        {#each distChartData as d, i}
          {#if i < n - 1}
            {@const d2 = distChartData[i+1]}
            {@const x1 = getX(i)}
            {@const y1 = getY(d.val)}
            {@const x2 = getX(i+1)}
            {@const y2 = getY(d2.val)}
            {@const baseline = PAD_T + chartH}
            {@const bi = getBandIndex(d.val, $breaks)}
            <polygon
              points="{x1},{baseline} {x1},{y1} {x2},{y2} {x2},{baseline}"
              fill={bandColors[bi]}
            />
          {/if}
        {/each}
        <!-- Last bar (single point at the far right) -->
        {#if n > 0}
          {@const d = distChartData[n-1]}
          {@const x1 = getX(n-2 >= 0 ? n-1 : 0)}
          {@const y1 = getY(d.val)}
          {@const baseline = PAD_T + chartH}
          {@const bi = getBandIndex(d.val, $breaks)}
          <!-- already covered by trapezoid loop above -->
        {/if}

        <!-- Outline polyline on top for clean edge -->
        <polyline
          points={distChartData.map((d, i) => `${getX(i)},${getY(d.val)}`).join(' ')}
          fill="none"
          stroke="rgba(0,0,0,0.06)"
          stroke-width="1"
        />

        <!-- Dashed median line at actual median value -->
        {#if distChartData.length > 0}
          {@const medIdx = Math.floor(n / 2)}
          {@const medRawVal = n % 2 === 0 ? (distChartData[n/2-1].val + distChartData[n/2].val)/2 : distChartData[medIdx].val}
          {@const medY = getY(medRawVal)}
          <line
            x1={PAD_L}
            y1={medY}
            x2={W - PAD_R}
            y2={medY}
            stroke="#757575"
            stroke-width="1.5"
            stroke-dasharray="5,2"
          />
        {/if}

        <!-- Selected neighborhood dots -->
        {#each distChartData as d, i}
          {#if distSelected.includes(d.id)}
            <circle cx={getX(i)} cy={getY(d.val)} r="4" fill="#2A9D8F"/>
          {/if}
        {/each}
      </svg>
    {/if}
  </div>

  <!-- Card 2: Trend chart -->
  {#if $selectedData && $selectedData.years.length > 1}
    <div class="chart-card">
      {#if $selectedConfig}
        <h1 class="dist-title">{$selectedConfig.title}</h1>
        <div class="dist-legend pb-2">
          <span style="color: #FFBF00;"><svg class="inline align-middle" style="width: 1.5em; height: 1.5em; margin-right: 2px; margin-bottom: 2px;" viewBox="0 0 32 32"><path fill="currentColor" d="M21.313 8h8v8l-3.063-3.063-8.375 8.375-5.313-5.313-8 8-1.875-1.875 9.875-9.875 5.313 5.313 6.5-6.5z"></path></svg> County</span>
          {#if $selectedNeighborhoods.length > 0}
            <span style="color: #2A9D8F; margin-left: 8px;"><svg class="inline align-middle" style="width: 1.5em; height: 1.5em; margin-right: 2px; margin-bottom: 2px;" viewBox="0 0 32 32"><path fill="currentColor" d="M21.313 8h8v8l-3.063-3.063-8.375 8.375-5.313-5.313-8 8-1.875-1.875 9.875-9.875 5.313 5.313 6.5-6.5z"></path></svg> Selected</span>
          {/if}
        </div>
      {/if}
      <div id="tchart" />
    </div>
  {/if}
</div>

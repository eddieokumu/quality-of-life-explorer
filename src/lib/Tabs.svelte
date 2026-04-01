<script>
  import { selectedConfig, selectedMetric, dataConfig, dataCategories, whatsnew } from '../store/store'

  const categories = $dataCategories

  let activeCategory
  $: {
    activeCategory = $selectedConfig.category
  }
</script>

<style>
  /* Tab bar - matches County Explorer MDL tab styling */
  .tab-bar {
    display: flex;
    align-items: center;
    border-bottom: 1px solid #e0e0e0;
    background: white;
    overflow-x: auto;
    justify-content: flex-start;
  }

  .tab-btn {
    position: relative;
    padding: 0 14px;
    height: 48px;
    display: inline-flex;
    align-items: center;
    font-family: Roboto, sans-serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #666;
    background: none;
    border: none;
    cursor: pointer;
    white-space: nowrap;
    border-bottom: 4px solid transparent;
    transition: color 0.18s, border-color 0.18s;
  }

  .tab-btn:hover {
    color: #264653;
  }

  .tab-btn.is-active {
    color: #264653;
    font-weight: 700;
    border-bottom: 4px solid #2A9D8F;
  }

  /* Metric pill panel */
  .metric-panel {
    padding: 8px 10px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    background: white;
    min-height: 46px;
  }

  /* MDL chip style — same padding always, consistent height */
  .metric-chip {
    display: inline-flex;
    align-items: center;
    height: 32px;
    margin: 3px;
    border-radius: 16px;
    background: #f0f0f0;
    color: #555;
    font-family: Roboto, sans-serif;
    font-size: 13px;
    border: none;
    cursor: pointer;
    transition: background 0.15s, color 0.15s, box-shadow 0.15s;
    white-space: nowrap;
  }

  .metric-chip:hover {
    background: #e0e0e0;
    color: #264653;
  }

  .metric-chip.is-active {
    background: #2A9D8F;
    color: white;
    box-shadow: 0 2px 2px 0 rgba(0,0,0,.14), 0 3px 1px -2px rgba(0,0,0,.2), 0 1px 5px 0 rgba(0,0,0,.12);
  }

  .chip-text {
    padding: 0 12px;
    line-height: 32px;
  }

  .new-badge {
    display: inline-block;
    margin-left: -6px;
    margin-right: 4px;
    background: #757575;
    color: white;
    padding: 0 6px;
    border-radius: 16px;
    font-size: 11px;
    line-height: 20px;
    height: 20px;
    align-self: center;
  }

  .metric-chip.is-active .new-badge {
    background: rgba(255,255,255,0.3);
  }

  /* Mobile select */
  .mobile-select {
    display: none;
  }

  @media (max-width: 768px) {
    .tab-bar,
    .metric-panel {
      display: none;
    }
    .mobile-select {
      display: block;
    }
  }
</style>

<!-- Mobile fallback -->
<div class="mobile-select">
  <select bind:value={$selectedMetric} class="w-full py-3 px-1 rounded cursor-pointer text-xl font-bold bg-white">
    {#each categories as cat}
    <optgroup label={cat}>
      {#each $dataConfig.filter(el => el.category === cat) as metric}
        <option value={metric.metric}>{metric.title}</option>
      {/each}
    </optgroup>
    {/each}
  </select>
</div>

<!-- Desktop tabs -->
<div class="bg-white shadow-sm">
  <!-- Category tab bar -->
  <div class="tab-bar" role="tablist">
    {#each categories as cat}
      <button
        class="tab-btn"
        class:is-active={activeCategory === cat}
        role="tab"
        aria-selected={activeCategory === cat}
        on:click={() => activeCategory = cat}
      >
        {cat}
      </button>
    {/each}
  </div>

  <!-- Metric chips — only the active category's panel is shown -->
  {#each categories as cat}
    {#if cat === activeCategory}
      <div class="metric-panel" role="tabpanel">
        {#each $dataConfig.filter(el => el.category === cat) as metric}
          <button
            class="metric-chip"
            class:is-active={$selectedMetric === metric.metric}
            on:click={() => $selectedMetric = metric.metric}
          >
            <span class="chip-text">{metric.title}</span>
            {#if $whatsnew.indexOf(metric.metric) !== -1}
              <span class="new-badge">new</span>
            {/if}
          </button>
        {/each}
      </div>
    {/if}
  {/each}
</div>

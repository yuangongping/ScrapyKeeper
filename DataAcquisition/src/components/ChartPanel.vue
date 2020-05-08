<template>
  <div class="chart-panel">
    <slot></slot>
  </div>
</template>

<style>
  .chart-panel {
    width: 100%;
    height: 100%;
    position: relative;
    background-size: 100% 100%;
  }
</style>

<script>
  export default {
    name: 'ChartPanel'
  }
</script>
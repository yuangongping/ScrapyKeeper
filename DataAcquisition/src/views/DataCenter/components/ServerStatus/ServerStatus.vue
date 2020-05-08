<template>
    <div class="server-status">
        <div class="cpu">
            <chart-panel id="cpu-chart" ></chart-panel>
        </div>

        <div class="RAM">
            <chart-panel id="RAM-chart"></chart-panel>
        </div>

        <div class="project-running">
            <chart-panel id="project-running-chart"></chart-panel>
        </div>

        <div class="project-running-status">
            <chart-panel id="project-running-status-chart"></chart-panel>
        </div>
        
    </div>
</template>>
<script>
import ChartPanel from '@/components/ChartPanel'
import draw from './draw.js'

  
export default {
    props: [
        'data'
    ], 
    components: {
        ChartPanel
    },
    mounted() {
        this.doDraw()
    },
    methods: {
        doDraw() {
            for (var i=0; i < this.data.length ; i++) {
                draw(this.data[i]);
            }
        },
    }
}
</script>
<style lang="scss" scoped>
.server-status{
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 30px 20px 0px 50px;
  .cpu, .RAM, .project-running, .project-running-status{
    width: 20%;
    height: 350px;
  }

}
</style>
<template>
    <div class="projectDataContainer">
        <chart-panel id="projectData"></chart-panel>
    </div>
</template>>
<script>
import ChartPanel from '@/components/ChartPanel'
import draw from './draw.js'
  
export default {
    props: [ 'data', 'timeline', 'xAxislLabel'],
    components: {
        ChartPanel
    },
    mounted() {
        this.doDraw();
    },
    methods: {
        doDraw(){
            var params = new Object();
            // 绑定dom的id
            params.id = "projectData"
            params.options = this.data
            params.timeline = this.timeline
            params.xAxislLabel = this.xAxislLabel
            // 绘图函数
            draw(params)
        }
    }
}
</script>
<style lang="scss" scoped>
.projectDataContainer{
    width: 100%;
    height: 600px;
}
</style>
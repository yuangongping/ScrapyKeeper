<template>
  <div class="dataCenter" v-if="flag">
    <!-- 服务器状态饼图组件 -->
    <ServerStatus :data='pieChartList'/>

    <!-- 数据概览组件 -->
    <DataOverview  :num='num' :totalSize='totalSize' :fileSize='fileSize' />

    <!-- 一周内数据采集总量 -->
    <AllData />

    <!-- 近一周采集量组件 -->
    <ProjectData :data="weekData" :timeline="timeline" :xAxislLabel="xAxislLabel" />
  </div>
  
</template>

<style lang="scss" >
</style>

<script>
import ServerStatus from './components/ServerStatus/ServerStatus'
import DataOverview from './components/DataOverview/DataOverview'
import ProjectData from './components/ProjectData/ProjectData'
import AllData from './components/AllData/AllData'

import { apiGetStatus, apiGetProjectWeekData } from "@/api/dataCentral"

export default {
  components: {
    ServerStatus,
    DataOverview,
    ProjectData,
    AllData

  },
  data() {
    return {
      num: 0,
      totalSize: 45511,
      fileSize: 31552,
      pieChartList: [
        {
          domId: "cpu-chart",
          title: "CPU使用量",
          legendData: ["已使用", "未使用"],
          seriesData: [ 
              {value: 0, name: '已使用'},
              {value: 0, name: '未使用'}
          ]
        },
        {
          domId: "RAM-chart",
          title: "内存使用量",
          legendData: ["已使用", "未使用"],
          seriesData: [ 
              {value: 0, name: '已使用'},
              {value: 0, name: '未使用'}
          ]
        },
        {
          domId: "project-running-chart",
          title: "运行率",
          legendData: ["正在运行", "等待"],
          seriesData: [ 
              {value: 0, name: '正在运行'},
              {value: 0, name: '等待'}
          ]
        },
        {
          domId: "project-running-status-chart",
          title: "错误率",
          legendData: ["正常", "错误"],
          seriesData: [ 
              {value: 0, name: '错误'},
              {value: 0, name: '正常'}
          ]
        },
      ],
      weekData: {},
      timeline: [],
      xAxislLabel: [],
      flag: false
    }
  },
  mounted() {
    this.getStatus();
    this.getProjectWeekData()
  },
  methods: {
    async getStatus() {
      const res = await apiGetStatus()
      this.flag = true
      this.pieChartList[0].seriesData[0].value = parseInt(res.cupStatus.used)
      this.pieChartList[0].seriesData[1].value = parseInt(res.cupStatus.Unused)
      this.pieChartList[1].seriesData[0].value = parseInt(res.memorystate.used)
      this.pieChartList[1].seriesData[1].value = parseInt(res.memorystate.Unused)
      this.pieChartList[2].seriesData[0].value = parseInt(res.project_running_status.running)
      this.pieChartList[2].seriesData[1].value = parseInt(res.project_running_status.waitting)
      this.pieChartList[3].seriesData[0].value = parseInt(res.project_error_rate_status.error)
      this.pieChartList[3].seriesData[1].value = parseInt(res.project_error_rate_status.normal)
      this.num = res.dataCount
    },
    async getProjectWeekData() {
      var res = await apiGetProjectWeekData()
      var options = []
      for(var j = 0, len=res.xAxis.length; j < len; j++) {
        var temp = {
          title: {text: res.xAxis[j] + '数据入库量'},
          series: [{ data:  res.yAxis[ res.xAxis[j]] }]
        }
        options.push(temp)
      }
      this.weekData = options
      this.timeline = res.xAxis
      this.xAxislLabel = res.label_data
    }
  }
}
</script>

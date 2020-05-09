<template>
  <div class="allDataPicture">
    <div class="title">一周数据入库总量概览</div>
    <div class="box">
      <ve-line
        :data="chartData"
        :settings="chartSettings"
        :width="lineWidth"
        :height="lineHeight"
        :legend-visible="false"
        :tooltip-visible="false"
      ></ve-line>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    this.chartSettings = {
      stack: {
        用户: ["数据入库量"]
      },
      yAxisName: ["数据入库量/条"],
      xAxisName: ["日期"],
      area: true, //是否显示为面积图
      itemStyle: {
        //面积图颜色设置
        color: {
          type: "linear",
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 0,
              color: "#7bc0ff" // 0% 处的颜色
            },
            {
              offset: 1,
              color: "#edf4ff" // 100% 处的颜色
            }
          ],
          globalCoord: true // 缺省为 false
        }
      }
    };
    return {
      lineWidth: "95%", //宽度
      lineHeight: "600px", //高度
      chartData: {
        //数据
        columns: ["日期", "入库量"],
        rows: [
          {
            日期: "1",
            入库量: 1000
          },
          {
            日期: "2",
            入库量: 2007
          },
          {
            日期: "3",
            入库量: 3800
          },
          {
            日期: "4",
            入库量: 5200
          },
          {
            日期: "5",
            入库量: 6400
          },
          {
            日期: "6",
            入库量: 9300
          },
          {
            日期: "7",
            入库量: 11100
          }
        ]
      }
    };
  }
};
</script>

<style lang="scss" scoped>
.allDataPicture {
  .title {
      font-weight: bold;
      color: #333;
      font-size: 17px;
      margin-left: 5px;
  }
  .box {
    padding-left: 7.5%;
  }
}
</style>
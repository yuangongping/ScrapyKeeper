var echarts = require('echarts')
var option = {
    baseOption: {
        timeline: {
            axisType: 'category',
            autoPlay: true,
            playInterval: 1000,
            data: [],
            label: {formatter : function(s) {return s;}}
        },
        tooltip: {
        },
        calculable : true,
        grid: {
            top: 80,
            bottom: 100,
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow',
                    label: {
                        show: true,
                        formatter: function (params) {
                            return params.value.replace('\n', '');
                        }
                    }
                }
            }
        },
        xAxis: [
            {
                'type':'category',
                'name': "工程",
                'axisLabel':{'interval':0},
                'data':[],
                splitLine: {show: false}
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '数据量（条）'
            }
        ],
        series: [
            {
                name: '数据量', 
                type: 'bar',
                itemStyle : {
                    normal : {
                      color: function(params) {
                          // build a color map as your need.
                          let colorList = [
                            '#ff0000', '#239676', '#eb4310', '#f6941d', '#fbb417', '#c23531', '#2f4554', '#61a0a8', '#24998d', '#1f9baa', 
                            '#d48265', '#91c7ae', '#749f83', '#ca8622', '#cdd541', '#99cc33', '#3f9337', '#219167', '#0080ff', '#3366cc', 
                            '#333399', '#003366', '#800080', '#a1488e', '#c71585', '#bd2158'                      
                          ];
                          return colorList[params.dataIndex]
                      },
                      label: {
                        show: true,
                        position: 'top',                              
                        // padding: [0,0,10,0],                  
                      }
                    },
                },
                barMaxWidth: '20',
            },
        ]
    }
};

const draw = (params) => {
    var crawl_hot_chart = echarts.init(document.getElementById(params.id));
    option.options = params.options
    option.baseOption.timeline.data = params.timeline
    option.baseOption.xAxis[0].data = params.xAxislLabel
    crawl_hot_chart.setOption(option);
    crawl_hot_chart.resize();
}
export default draw;
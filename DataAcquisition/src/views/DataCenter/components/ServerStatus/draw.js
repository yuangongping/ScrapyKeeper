var echarts = require('echarts');

var option = {
    title: {
        text: 'CPU使用量',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        top: 30,
        data: []
    },
    color : [ 'red', '#009ACD'],
    series: [
        {
            name: '姓名',
            type: 'pie',
            // 设置图的整体大小
            radius: '45%',
            center: ['40%', '50%'],
            data: [],
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

const draw = (params) => {
    var crawl_hot_chart = echarts.init(document.getElementById(params.domId));
    // var crawl_hot_chart = echarts.init(params.domId);
    // 设置表标题
    option.title.text = params.title;
    option.legend.data = params.legendData;
    option.series[0].data = params.seriesData;
    option.series[0].name = params.title;
    crawl_hot_chart.setOption(option);
    crawl_hot_chart.resize();
}


export default draw;
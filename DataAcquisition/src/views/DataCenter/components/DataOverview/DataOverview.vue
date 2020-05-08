<template>
  <div class="DataOverviewContainer">
    <div class="item">
      <label>数据总量</label>
      <div class="body">
        <div class="card_text">
          <b>{{ num | fileterNum}}</b>
          <span>条</span>
        </div>
      </div>
    </div>
    <div class="item">
      <label>数据规模</label>
      <div class="body">
        <div class="card_text">
          <b>{{ totalSize | fileterSize}}</b>
          <span>B</span>
        </div>
      </div>
    </div>
    <div class="item">
      <label>文件</label>
      <div class="body">
        <div class="card_text">
          <b>{{ fileSize | fileterSize }}</b>
          <span>B</span>
        </div>
      </div>
    </div>
  </div>
</template>>


<script>
export default {
  props: [
    'num', 'totalSize', 'fileSize'
  ],
  filters: {
    fileterNum: function(value) {
      if(value < 10000){
        return value.toString()
      }else if(value >= 10000 && value < 10000000) {
        return (value/10000).toFixed(2).toString() +'万'
      } else {
        return (value/100000000).toFixed(2).toString() +'亿'
      }
    },
    fileterSize: function(value) {
      if(value < 10000){
        return (value/1024).toFixed(2).toString() +'M'
      }else if( value >= 10000 && value < 100000000) {
        return (value/1024/1024).toFixed(2).toString() +'G'
      } else {
        return (value/1024/1024/1024).toFixed(2).toString() +'T'
      }
    },
  }
}
</script>

<style lang="scss">
.DataOverviewContainer{
    display: flex;
    flex-flow: wrap;
    justify-content: space-between;
    padding: 10px 5%;
    margin-bottom: 40px;
    .item{
        display: flex;
        flex-direction: column;
        width: 14%;
        border: 1px solid rgb(231, 227, 227);
        border-radius: 2px;
        height: 150px;
        margin-right: 20px;
        padding: 16px;
        label{
            font-size: 14px;
            color: #666;
            font-weight: 700;
        }
        .body {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100%;
          .card_text{
            width: 100%;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            b {
                font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                font-size: 2.333em;
                line-height: 1.7;
                color: #333;
            }
            span {
              font-size: .5em;
              margin-left: 10px;
              color: black;
            }
          }
        }
    }
}
</style>
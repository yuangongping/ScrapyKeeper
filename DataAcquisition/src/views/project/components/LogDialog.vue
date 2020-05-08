<template>
  <div class="log-view">
    <el-dialog :visible.sync="visible" :show-close="false" :close-on-click-modal="false">
      <div class="title">日志详情</div>
      <div class="content">
        <p class="dispalyLog" v-for="log_line in logList" :key="log_line">{{log_line}}</p>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="cancle">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  props: ["visible", "logList"],
  data() {
    return {};
  },
  computed: {},
  methods: {
    cancle() {
      this.$emit("logViewCancle");
    }
  }
};
</script>

<style lang="scss" scoped>
.title {
  text-align: center;
  margin-bottom: 20px;
  margin-top: -30px;
  font-weight: bolder;
  font-size: 18px;
}
.content {
  height: 500px;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  p {
    padding: 0 5px 0 5px;
  }
}
.dispalyLog {
  word-wrap: break-word;
  word-break: break-all;
  overflow: hidden;
}
</style>>
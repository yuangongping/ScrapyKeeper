<template>
  <div class="scheduler">
    <el-dialog :title="form.project_alias+'-调度任务'" :visible.sync="visible" :show-close="false" :close-on-click-modal="false">
      <div class="tip">时间参数</div>
      <div class="sub">
        <el-tabs type="border-card">
          <el-tab-pane label="月份选择">
              <el-checkbox-group v-model="schedulerForm.cron_month">
                  <el-checkbox v-for="month in 12" :label="month" :key="month">{{ month >= 10 ? month:'0'+String(month)  }}</el-checkbox>
              </el-checkbox-group>
          </el-tab-pane>
          <el-tab-pane label="天选择">
              <el-checkbox-group v-model="schedulerForm.cron_day_of_month">
                  <el-checkbox v-for="day in 31" :label="day" :key="day">{{  day >= 10 ? day:'0'+String(day)   }}</el-checkbox>
              </el-checkbox-group>
          </el-tab-pane>
          <el-tab-pane label="小时选择">
              <el-checkbox-group v-model="schedulerForm.cron_hour">
                  <el-checkbox v-for="hour in 24" :label="hour-1" :key="hour-1">{{ hour-1 >= 10 ? hour-1:'0'+String(hour-1) }}</el-checkbox>
              </el-checkbox-group>
          </el-tab-pane>
          <el-tab-pane label="分钟选择">
              <el-checkbox-group v-model="schedulerForm.cron_minutes">
                  <el-checkbox v-for="minute in 60" :label="minute-1" :key="minute-1">{{ minute-1 >= 10 ? minute-1:'0'+String(minute-1)  }}</el-checkbox>
              </el-checkbox-group>
          </el-tab-pane>
        </el-tabs>     
      </div>
      <div class="tip">描述</div>
      <div class="sub">
        <el-input type="text" v-model="desc" maxlength="30" show-word-limit="true" placeholder="请输入简短的调度描述，如，每天12点" />
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="cancle">取 消</el-button>
        <el-button size="small" type="primary" @click="submit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    props: [
      'visible', 'form'
    ],
    data() {
      return {
        desc: '每天中午12点',
        schedulerForm: {
          cron_month: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          cron_day_of_month: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
          cron_hour: [0],
          cron_minutes: [0]
        }
      }
    },
    computed: {
    },
    methods: {
      submit() {
        this.schedulerForm['project_id'] = this.form.id
        this.schedulerForm['desc'] = this.desc
        this.$emit('addScheduler', this.schedulerForm)
      },
      cancle() {
        this.$emit('schedulerClickCancle')
      }
    }
  }
</script>

<style lang="scss" scoped>
  .sub{
    margin: 10px 0px 25px 20px; 
  }
  .tip{
    font-size: 16px;
    padding-left: 10px;
    border-left: 2px solid steelblue;
    margin: 10px 0px 0px 0px;
  }
  .el-checkbox:nth-child(1){
    margin-left: 30px;
  }
</style>>
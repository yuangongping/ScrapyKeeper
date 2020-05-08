<template>
<div class="base-info">
  <el-dialog title="添加工程" :visible.sync="visible" :show-close="false" :close-on-click-modal="false">
    <el-form :model="editeForm">
      <el-form-item label="项目名称" :label-width="formLabelWidth" prop="project_alias">
        <el-input v-model="editeForm.project_alias" auto-complete="off"></el-input>
      </el-form-item>

      <el-form-item label="首页URL" :label-width="formLabelWidth" prop="url">
        <el-input v-model="editeForm.url" auto-complete="off" ></el-input>
      </el-form-item>

      <el-form-item label="模板" :label-width="formLabelWidth" prop="category">
        <el-select v-model="editeForm.category" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="cancle" size="small">取 消</el-button>
      <el-button type="primary" @click="submit" size="small">确 定</el-button>
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
      options: [
        {
          value: 'news',
          label: '通用型新闻网页'
        },
        {
          value: 'weibo',
          label: '新浪微博'
        },
        {
          value: 'gongzhonghao',
          label: '微信公众号'
        }
      ],
      formLabelWidth: '200'
    }
  },
  computed: {
    editeForm: function() {
      return this.form
    }
  },
  methods: {
    submit() {
      this.$emit('addProjectSubmit', this.editeForm)
    },
    cancle() {
      this.$emit('addProjectCancle')
    }
  }
}
</script>
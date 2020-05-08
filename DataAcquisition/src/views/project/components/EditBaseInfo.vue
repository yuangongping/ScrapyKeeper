<template>
<div class="base-info">
  <el-dialog title="编辑项目" :visible.sync="visible" :show-close="false" :close-on-click-modal="false">
    <el-form :model="editeForm">
      <el-form-item label="名称" :label-width="formLabelWidth" prop="project_alias">
        <el-input v-model="editeForm.project_alias" auto-complete="off"></el-input>
      </el-form-item>

      <el-form-item label="分类" :label-width="formLabelWidth" prop="category">
        <el-input v-model="editeForm.category" auto-complete="off" ></el-input>
      </el-form-item>

      <el-form-item label="类型" :label-width="formLabelWidth" prop="is_msd">
        <el-input v-model="editeForm.is_msd" auto-complete="off"></el-input>
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
      this.$emit('editInfo', this.editeForm)
    },
    cancle() {
      this.$emit('cancle')
    }
  }
}
</script>
<template>
  <div class="base-info">
    <el-dialog
      title="添加模板"
      :visible.sync="visible"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <el-form :model="Form">
        <el-form-item label="网页名称" :label-width="formLabelWidth" prop="project_alias">
          <el-input v-model="Form.crawl_name" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="网页地址 / 微信公众号" :label-width="formLabelWidth" prop="url">
          <el-input v-model="Form.crawl_url" auto-complete="off"></el-input>
        </el-form-item>

        <el-form-item label="模板选择" :label-width="formLabelWidth" prop="category">
          <el-select v-model="Form.name" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
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
  props: ["visible"],
  data() {
    return {
      Form: {},
      options: [
        {
          value: "news",
          label: "通用型新闻网页"
        },
        {
          value: "weibo",
          label: "新浪微博"
        },
        {
          value: "gongzhonghao",
          label: "微信公众号"
        }
      ],
      formLabelWidth: "200"
    };
  },
  methods: {
    submit() {
      if (!this.Form.crawl_name || !this.Form.crawl_url) {
        this.$message({
          type: "error",
          message: "所填字段不能为空!"
        });
      } else {
        this.$emit("addProjectSubmit", this.Form);
      }
    },
    cancle() {
      this.$emit("addProjectCancle");
    }
  }
};
</script>
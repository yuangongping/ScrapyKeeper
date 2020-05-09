<template>
  <div class="base-info">
    <el-dialog title="编辑项目" :visible.sync="visible" :show-close="false" :close-on-click-modal="false">
      <el-form :model="editeForm" label-width="80px">
        <el-form-item label="名称:" prop="crawl_name">
          <el-input v-model="editeForm.crawl_name"></el-input>
        </el-form-item>

        <el-form-item label="类型:" prop="name">
          <el-select v-model="editeForm.name" placeholder="请选择">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="地址:" prop="crawl_url">
          <el-input v-model="editeForm.crawl_url"></el-input>
        </el-form-item>

        <el-form-item label="状态:" prop="status">
          <el-input v-model="editeForm.status"></el-input>
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
  props: ["visible", "form"],
  data() {
    return {
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
      ]
    };
  },
  computed: {
    editeForm() {
      return this.form;
    },
  },
  methods: {
    submit() {
      this.$emit("editInfo", this.editeForm);
    },
    cancle() {
      this.$emit("cancle");
    }
  }
};
</script>
<template>
  <div class="base-info">
    <el-dialog
      title="添加工程"
      :visible.sync="visible"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <el-form :model="editeForm" label-width="100px" label-position="right">
        <el-form-item label="项目名称" prop="project_alias">
          <el-input v-model="editeForm.project_alias" auto-complete="off" style="width: 320px;"></el-input>
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="editeForm.category" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="候选模板" prop="startUrls">
          <el-transfer
            filterable
            :titles="['候选模板', '已选模板']"
            :filter-method="filterMethod"
            filter-placeholder="请输关键字"
            v-model="value"
            :data="data"
          ></el-transfer>
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
import { apiStartUrl } from "@/api/starturl";
export default {
  props: ["visible", "form"],
  data() {
    return {
      options: [
        {
          value: "news",
          label: "网页官网"
        },
        {
          value: "weibo",
          label: "微博"
        },
        {
          value: "gongzhonghao",
          label: "公众号"
        }
      ],
      value: [],
      data: [],
      startUrls: []
    };
  },
  computed: {
    editeForm: function() {
      return this.form;
    }
  },
  created() {
    this.getdata();
  },
  methods: {
    change() {
      this.getdata();
    },
    async getdata() {
      this.data = [];
      const res = await apiStartUrl({ name: this.editeForm.category });
      if (res.length > 0) {
        for (var i in res) {
          this.data.push({
            key: res[i].crawl_url,
            label: res[i].crawl_name
          });
        }
      }
    },
    filterMethod(query, item) {
      return item;
    },
    submit() {
      this.$emit("addProjectSubmit", this.editeForm);
    },
    cancle() {
      this.$emit("addProjectCancle");
    }
  }
};
</script>
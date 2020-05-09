<template>
  <div class="app-container">
    <Toolbar @Cate="Cate" @Search="Search" @addModel="addModel" />

    <el-table :data="list" v-loading.body="listLoading" element-loading-text="Loading" border style="width: 100%">
      <el-table-column label="序号" width="50" type="index" align="center"></el-table-column>
      <el-table-column label="名称" prop="crawl_name" show-overflow-tooltip></el-table-column>
      <el-table-column label="创建时间" prop="date_created"></el-table-column>
      <el-table-column label="类型" prop="name_zh"></el-table-column>
      <el-table-column label="地址" prop="crawl_url" show-overflow-tooltip></el-table-column>
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button type="text" @click="editeClick(scope.row)">编辑</el-button>
          <el-button type="text" style="color: red" @click="del_project(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        background
        @current-change="pageChange"
        layout="total, prev, pager, next, jumper"
        :page-size="pagination.pageSize"
        :total="pagination.total"
      ></el-pagination>
    </div>
    <!-- 编辑工程对话框 -->
    <EditBaseInfo
      :visible="editDialog"
      :form="editForm"
      v-on:cancle="cancle"
      v-on:editInfo="editInfoSubmit"
    />
    <!-- 添加模板对话框 -->
    <AddProjectDialog
      :visible="addProjectDialog"
      @addProjectCancle="addProjectCancle"
      @addProjectSubmit="addProjectSubmit"
    />

  </div>
</template>

<script>
import { getAllProject, apiEditProjectInfo, delProject, apiAddProject } from "@/api/project";
import { apiAddModel, apiGetModel, delModel, apiEditModel } from "@/api/templates"
import { apidRunImmediately, apidCancleRunning, apiAddScheduler, apiCancelScheduler } from "@/api/scheduler";
import { apiOriginalLog } from "@/api/originalLog";
import EditBaseInfo from "./components/EditBaseInfo";
import AddProjectDialog from "./components/AddProjectDialog";
import Toolbar from "./components/Toolbar"

export default {
  name: "templates",
  components: { EditBaseInfo, AddProjectDialog, Toolbar },
  data() {
    return {
      query: {
        name_zh: '',
        crawl_name: ''
      },
      pagination:{
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      modelMap: new Map([['news', '通用型新闻网页'], ['weibo', '新浪微博'], ['gongzhonghao', '微信公众号']]),
      list: null,
      listLoading: true,
      editDialog: false,
      editForm: {
        id: null,
        name_zh: null,
        status: null,
        name: null,
        crawl_name: null,
        crawl_url: null
      },
      addProjectDialog: false,
    };
  },
  created() {
    this.getModelList();
  },
  methods: {
    // 分类筛选
    Cate(value) {
      this.query.name_zh = this.modelMap.get(value)
      this.getModelList()
    },
    //搜索
    Search(name) {
      this.query.crawl_name = name
      this.getModelList()
    },
    // 翻页
    pageChange(page) {
      this.pagination.currentPage = page;
      this.getModelList()
    },
    // 点击编辑响应事件
    editeClick(form) {
      this.editForm.crawl_name = form.crawl_name;
      this.editForm.name = form.name;
      this.editForm.crawl_url = form.crawl_url;
      this.editForm.id = form.id;
      this.editForm.name_zh = form.name_zh;
      this.editForm.status = form.status;
      this.editDialog = true;
    },
    // 向后端提交编辑编辑事件
    async editInfoSubmit(form) {
      var params = form
      params.name_zh = this.modelMap.get(params.name)
      await apiEditModel(params);
      this.editDialog = false;
      this.$message.success("编辑成功！");
      this.getModelList();
    },
    // 取消编辑事件
    cancle() {
      this.editDialog = false;
    },
    // 获取模板列表
    async getModelList() {
      this.listLoading = true;
      var params = {
        'page_size': this.pagination.pageSize,
        'page_index': this.pagination.currentPage,
        'name_zh': this.query.name_zh,
        'crawl_name': this.query.crawl_name
      }
      const res = await apiGetModel(params)
      this.listLoading = false
      this.list = res.data
      this.pagination.total = res.total
    },
    // 删除
    async del_project(id) {
      await delModel(id);
      this.getModelList();
      this.$message.success("删除成功！");
    },
    // 点击添加模板按钮
    addModel(add) {
      this.addProjectDialog = add;
    },
    // 提交添加模板
    async addProjectSubmit(form) {
      this.addProjectDialog = false;
      form.name_zh = this.modelMap.get(form.name)
      const loading = this.$loading({
        lock: true,
        text: "正在添加, 请耐心等候！",
        spinner: "el-icon-loading"
      });
      const res = await apiAddModel(form);
      loading.close();
      if(res) {
        this.$message.success("添加成功！");
      }
      this.getModelList();
    },
    // 取消添加模板
    addProjectCancle() {
      this.addProjectDialog = false;
    }
  }
};
</script>


<style lang="scss" scoped>
.pagination {
  margin-top: 20px;
}
.el-button--text {
  padding: 0px 0px;
}
</style>

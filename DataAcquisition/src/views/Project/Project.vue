<template>
  <div class="app-container">
    <!-- 筛选、搜索、添加项目 -->
    <Toolbar @Cate="Cate" @State="State" @Search="Search" @addProject="addProject" />
    <!-- 表格 -->
    <el-table :data="list" v-loading.body="listLoading" element-loading-text="Loading" border style="width: 100%">
      <el-table-column label="序号" width="50" type="index" align="center"></el-table-column>
      <el-table-column label="名称" prop="project_alias"></el-table-column>
      <el-table-column label="分类" prop="category"></el-table-column>
      <el-table-column label="周期">
        <template >每天**点</template>
      </el-table-column>
      <el-table-column label="发布时间" prop="date_created"></el-table-column>
      <el-table-column align="center" width="100" label="状态">
        <template slot-scope="scope">{{ scope.row.status | statusMapping }}</template>
      </el-table-column>
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button type="text" @click="editeClick(scope.row)">调度</el-button>
          <el-button type="text" @click="editeClick(scope.row)">编辑</el-button>
          <el-button type="text" style="color: red" @click="del_project(scope.row)">删除</el-button>
        </template>
      </el-table-column>

      <!-- <el-table-column align="center" label="调度" >
        <template slot-scope="scope">
          <el-button type="text" @click="runImmediately(scope.row.id)">立即运行</el-button>
          <el-button type="text" @click="cancleRunning(scope.row.id)">取消运行</el-button>
          <el-button type="text" @click="schedulerClick(scope.row)">周期调度</el-button>
          <el-button type="text" @click="cancelScheduler(scope.row.id)">取消调度</el-button>
        </template>
      </el-table-column>-->
      <el-table-column align="center" label="待采队列">
        <template >
          <!-- <svg-icon icon-class="watch"></svg-icon> -->
          <el-button type="text">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column align="center" label="数据详情">
        <template >
          <!-- <svg-icon icon-class="watch"></svg-icon> -->
          <el-button type="text">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column align="center" label="数据趋势图">
        <template >
          <!-- <svg-icon icon-class="watch"></svg-icon> -->
          <el-button type="text">趋势图</el-button>
        </template>
      </el-table-column>
      <el-table-column align="center" label="日志">
        <template slot-scope="scope">
          <span class="error-info" v-if="scope.row.error > 0">{{ scope.row.error | ellipsis }}</span>
          <el-button type="text" @click="ViewLogClick(scope.row.id)">日志详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination">
      <el-pagination
        background
        @current-change="handleCurrentChange"
        layout="total, prev, pager, next, jumper"
        :page-size="pageSzie"
        :total="total_num"
      ></el-pagination>
    </div>
    <!-- 编辑工程对话框 -->
    <EditBaseInfo
      :visible="editDialog"
      :form="editForm"
      v-on:cancle="cancle"
      v-on:editInfo="editInfoSubmit"
    />
    <!-- 添加工程对话框 -->
    <AddProjectDialog
      :visible="addProjectDialog"
      :form="addProjectForm"
      v-on:addProjectCancle="addProjectCancle"
      v-on:addProjectSubmit="addProjectSubmit"
    />
    <!-- 添加调度对话框 -->
    <SchedulerDialog
      :visible="schedulerDialog"
      :form="schedulerForm"
      v-on:addScheduler="addScheduler"
      v-on:schedulerClickCancle="schedulerClickCancle"
    />
    <!-- 显示日志对话框 -->
    <LogDialog :visible="dialog" :logList="logList" v-on:logViewCancle="logViewCancle" />
  </div>
</template>

<script>
import { getAllProject, apiEditProjectInfo, delProject, apiAddProject } from "@/api/project";
import { apidRunImmediately, apidCancleRunning, apiAddScheduler, apiCancelScheduler } from "@/api/scheduler";
import { apiOriginalLog } from "@/api/originalLog";
import EditBaseInfo from "./components/EditBaseInfo";
import AddProjectDialog from "./components/AddProjectDialog";
import SchedulerDialog from "./components/SchedulerDialog";
import LogDialog from "./components/LogDialog";
import Toolbar from "./components/Toolbar"

export default {
  name: "project",
  components: {
    EditBaseInfo,
    AddProjectDialog,
    SchedulerDialog,
    LogDialog,
    Toolbar
  },
  data() {
    return {
      categoryMapping: {
        news: "网页官网"
      },
      list: null,
      listLoading: true,
      pageIndex: 1,
      pageSzie: 8,
      total_num: null,
      editDialog: false,
      editForm: {
        id: null,
        category: null,
        is_msd: null,
        project_alias: null
      },
      addProjectDialog: false,
      addProjectForm: {
        project_alias: null,
        url: null,
        category: "news"
      },
      schedulerDialog: false,
      schedulerForm: {},
      dialog: false,
      logList: []
    };
  },
  created() {
    this.fetchData();
  },
  filters: {
    statusMapping: function(value) {
      if (value === "running") {
        return "运行中";
      } else {
        return "休眠";
      }
    },
    ellipsis(value) {
      if (value > 100) {
        return "100+";
      } else {
        return value;
      }
    }
  },
  methods: {
    //根据分类进行筛选
    Cate(value) {
      console.log('aaaa')
      console.log(value,'分类筛选')
    },
    //根据状态筛选
    State(value) {
      console.log(value, '状态筛选')
    },
    //搜索项目
    Search(name) {
      console.log(name, '搜索')
    },
    // 翻页函数
    handleCurrentChange(val) {
      this.pageIndex = val;
      this.fetchData();
    },
    // 点击编辑响应事件
    editeClick(form) {
      this.editForm.id = form.id;
      this.editForm.category = form.category;
      this.editForm.is_msd = form.is_msd;
      this.editForm.project_alias = form.project_alias;
      this.editDialog = true;
    },
    // 向后端提交编辑编辑事件
    async editInfoSubmit(form) {
      await apiEditProjectInfo(form);
      this.editDialog = false;
      this.$message.success("信息更新成功！");
      this.fetchData();
    },
    // 取消编辑事件
    cancle() {
      this.editDialog = false;
    },
    // 分页获取所有工程数据事件
    fetchData() {
      this.listLoading = true;
      getAllProject(this.pageIndex, this.pageSzie).then(response => {
        this.total_num = response.data.total;
        this.list = response.data;
        this.listLoading = false;
      });
    },
    // 删除工程
    async del_project(form) {
      await delProject(form);
      this.fetchData();
      this.$message.success("删除成功！");
    },
    // 点击添加工程按钮
    addProject(add) {
      this.addProjectDialog = add;
    },
    // 提交添加工程
    async addProjectSubmit(form) {
      this.addProjectDialog = false;
      const loading = this.$loading({
        lock: true,
        text: "工程添加中, 该过程可能需要约30s, 请耐心等候！",
        spinner: "el-icon-loading"
      });
      const res = await apiAddProject(form);
      loading.close();
      if (res) {
        this.$message.success("添加成功！");
      }
      this.fetchData();
    },
    // 取消添加工程
    addProjectCancle() {
      this.addProjectDialog = false;
    },
    // 立即运行事件
    async runImmediately(id) {
      await apidRunImmediately(id);
      this.$message.success("调度成功！");
    },
    // 取消运行事件
    async cancleRunning(id) {
      await apidCancleRunning(id);
      this.$message.success("已经取消！");
    },
    // 点击周期调度按钮， 显示对话框
    schedulerClick(project) {
      this.schedulerForm = project;
      this.schedulerDialog = true;
    },
    // 关闭周期调度对话框
    schedulerClickCancle() {
      this.schedulerDialog = false;
    },
    // 提交添加调度事件
    async addScheduler(form) {
      form.cron_month = form.cron_month.join(",");
      form.cron_day_of_month = form.cron_day_of_month.join(",");
      form.cron_hour = form.cron_hour.join(",");
      form.cron_minutes = form.cron_minutes.join(",");
      await apiAddScheduler(form);
      this.$message.success("添加成功！");
      this.schedulerDialog = false;
    },
    async ViewLogClick(id) {
      this.dialog = true;
      const res = await apiOriginalLog(id);
      this.logList = res;
    },
    logViewCancle() {
      this.dialog = false;
    },
    async cancelScheduler(project_id) {
      await apiCancelScheduler(project_id);
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
.error-info{
  background-color: #f56c6c;
  border-radius: 10px;
  color: #fff; 
  display: inline-block;
  font-size: 12px;
  padding: 0 6px;
  text-align: center; 
  border: 1px solid #fff;
  height: 18px;
  line-height: 18px;
  cursor: pointer;
}
</style>

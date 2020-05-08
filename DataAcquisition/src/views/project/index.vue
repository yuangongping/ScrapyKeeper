<template>
  <div class="app-container">
    <div class="operate">
      <div class="select">
        <span>分类:</span>
        <el-select v-model="cate" size="mini" placeholder="请选择">
          <el-option label="全部" value="1"></el-option>
          <el-option label="网页官网" value="2"></el-option>
          <el-option label="媒体" value="3"></el-option>
        </el-select>
      </div>
      <div class="select">
        <span>状态:</span>
        <el-select v-model="state" size="mini" placeholder="请选择">
          <el-option label="全部" value="1"></el-option>
          <el-option label="休眠" value="2"></el-option>
          <el-option label="运行中" value="3"></el-option>
        </el-select>
      </div>
      <div class="search">
        <el-input size="mini" v-model="name" placeholder="请输入项目名称">
          <el-button size="mini" slot="append" type="primary">搜索</el-button>
        </el-input>
      </div>
      <div class="add-project">
        <el-button
          round
          icon="el-icon-plus"
          size="small"
          type="primary"
          @click="addProjectClick"
        >添加工程</el-button>
      </div>
    </div>

    <el-table
      :data="list"
      v-loading.body="listLoading"
      element-loading-text="Loading"
      border
      style="width: 100%"
    >
      <el-table-column label="序号" width="50" type="index" align="center"></el-table-column>

      <el-table-column label="名称">
        <template slot-scope="scope">{{scope.row.project_alias}}</template>
      </el-table-column>

      <el-table-column label="分类">
        <template slot-scope="scope">{{ categoryMapping[scope.row.category] }}</template>
      </el-table-column>

      <el-table-column label="周期">
        <template >每天**点</template>
      </el-table-column>

      <el-table-column label="发布时间">
        <template slot-scope="scope">{{scope.row.date_created}}</template>
      </el-table-column>
      <el-table-column align="center" width="100" label="状态">
        <template slot-scope="scope">{{ scope.row.status | statusMapping }}</template>
      </el-table-column>
      <el-table-column align="center" label="操作">
        <template>
          <!-- <svg-icon icon-class="dispatch"></svg-icon>
          <svg-icon icon-class="edit"></svg-icon>
          <svg-icon icon-class="del"></svg-icon> -->
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
          <span
            v-if="scope.row.error > 0"
            style="background-color: #f56c6c;border-radius: 10px;color: #fff; 
            display: inline-block;font-size: 12px;padding: 0 6px;
            text-align: center; border: 1px solid #fff;height: 18px;line-height: 18px;cursor: pointer"
          >{{ scope.row.error | ellipsis }}</span>
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

export default {
  name: "project",
  components: {
    EditBaseInfo,
    AddProjectDialog,
    SchedulerDialog,
    LogDialog
  },
  data() {
    return {
      query: {
        page: 1,
        size: 1,
        name: '',
        category: '',
        status: 1,
      },
      cate: "1",
      state: "1",
      time: "1",
      name: '',
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
    addProjectClick(form) {
      this.addProjectDialog = true;
    },
    // 提交添加工程
    async addProjectSubmit(form) {
      this.addProjectDialog = false;
      const loading = this.$loading({
        lock: true,
        text: "工程添加中, 该过程可能需要约30s, 请耐心等候！",
        spinner: "el-icon-loading"
      });
      await apiAddProject(form);
      loading.close();
      this.$message.success("添加成功！");
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
.svg-icon{
  font-size: 28px;
}
.operate {
  padding-bottom: 10px;
  display: flex;
  flex-direction: row;
  background-color: white;
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #ebeef5;
  .select {
    font-size: 14px;
    color: gray;
    padding-right: 25px;
  }
  .search {
    padding-left: 26px;
    font-size: 13px;
  }
  .add-project {
    margin-left: auto;
  }
}
.pagination {
  margin-top: 20px;
}
.el-button--text {
  padding: 0px 0px;
}
</style>

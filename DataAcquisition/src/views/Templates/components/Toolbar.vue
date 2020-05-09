<template>
  <div class="operate">
    <div class="select">
      <span>分类:</span>
      <el-select v-model="cate" size="mini" placeholder="请选择" @change="Cate">
        <el-option label="全部" value=""></el-option>
        <el-option label="通用型新闻网页" value="news"></el-option>
        <el-option label="新浪微博" value="weibo"></el-option>
        <el-option label="微信公众号" value="gongzhonghao"></el-option>
      </el-select>
    </div>
    <div class="search">
      <el-input size="mini" v-model="name" placeholder="请输入项目名称">
        <el-button size="mini" slot="append" @click="Search">搜索</el-button>
      </el-input>
    </div>
    <div class="add-project">
      <el-button round icon="el-icon-plus" size="small" type="primary" @click="addModel">添加模板</el-button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cate: "",
      state: "",
      name: "",
      add: true
    };
  },
  methods: {
      Cate(value) {
          this.$emit("Cate", value)
      },
      Search() {
          this.$emit("Search", this.name)
      },
      addModel() {
          this.$emit("addModel", this.add)
      }
  }
};
</script>

<style lang="scss" scoped>
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
    span {
      padding-right: 3px;
    }
  }
  .search {
    padding-left: 26px;
    font-size: 13px;
  }
  .add-project {
    margin-left: auto;
  }
}
</style>